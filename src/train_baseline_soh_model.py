from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def mean_absolute_error(y_true, y_pred):
    return float(np.mean(np.abs(y_true - y_pred)))


def root_mean_squared_error(y_true, y_pred):
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def add_metric_row(rows, battery_id, model_name, train_size, test_size, y_true, y_pred):
    rows.append(
        {
            "battery_id": battery_id,
            "model": model_name,
            "train_cycles": train_size,
            "test_cycles": test_size,
            "test_mae": mean_absolute_error(y_true, y_pred),
            "test_rmse": root_mean_squared_error(y_true, y_pred),
        }
    )


def main():
    data_path = Path("data/processed/discharge_capacity.csv")
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)

    required_columns = {"battery_id", "discharge_index", "capacity_ah"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.sort_values(["battery_id", "discharge_index"]).copy()

    initial_capacity = df.groupby("battery_id")["capacity_ah"].transform("first")
    df["soh"] = df["capacity_ah"] / initial_capacity

    all_predictions = []
    metric_rows = []

    plt.figure(figsize=(10, 6))

    for battery_id, group in df.groupby("battery_id"):
        group = group.sort_values("discharge_index").copy()

        split_index = int(len(group) * 0.7)
        train = group.iloc[:split_index]
        test = group.iloc[split_index:]

        x_train = train["discharge_index"].to_numpy(dtype=float)
        y_train = train["soh"].to_numpy(dtype=float)

        x_test = test["discharge_index"].to_numpy(dtype=float)
        y_test = test["soh"].to_numpy(dtype=float)

        last_observed_soh = y_train[-1]
        y_pred_naive = np.full_like(y_test, fill_value=last_observed_soh, dtype=float)

        coefficients = np.polyfit(x_train, y_train, deg=2)
        model = np.poly1d(coefficients)
        y_pred_poly = model(x_test)

        add_metric_row(
            metric_rows,
            battery_id,
            "naive_last_observed",
            len(train),
            len(test),
            y_test,
            y_pred_naive,
        )
        add_metric_row(
            metric_rows,
            battery_id,
            "quadratic_polynomial",
            len(train),
            len(test),
            y_test,
            y_pred_poly,
        )

        prediction_frame = test[["battery_id", "discharge_index", "soh"]].copy()
        prediction_frame["naive_predicted_soh"] = y_pred_naive
        prediction_frame["quadratic_predicted_soh"] = y_pred_poly
        all_predictions.append(prediction_frame)

        plt.plot(
            group["discharge_index"],
            group["soh"],
            linewidth=1.5,
            label=f"{battery_id} actual",
        )

        plt.plot(
            test["discharge_index"],
            y_pred_poly,
            linestyle="--",
            linewidth=1.5,
            label=f"{battery_id} quadratic",
        )

    predictions = pd.concat(all_predictions, ignore_index=True)
    metrics = pd.DataFrame(metric_rows)

    predictions_path = results_dir / "baseline_soh_predictions.csv"
    metrics_path = results_dir / "baseline_soh_metrics.txt"
    plot_path = results_dir / "baseline_soh_prediction.png"
    metric_plot_path = results_dir / "baseline_soh_metric_comparison.png"

    predictions.to_csv(predictions_path, index=False)

    average_metrics = (
        metrics.groupby("model")[["test_mae", "test_rmse"]]
        .mean()
        .reset_index()
        .sort_values("test_mae")
    )

    with metrics_path.open("w") as f:
        f.write("Baseline SOH prediction metrics\n")
        f.write("===============================\n\n")
        f.write("Task: predict later-cycle normalized SOH from earlier cycles of the same battery\n")
        f.write("Target: normalized SOH\n")
        f.write("Train/test split: first 70% cycles train, last 30% cycles test\n\n")
        f.write("Models:\n")
        f.write("- naive_last_observed: repeats the last SOH value seen in the training split\n")
        f.write("- quadratic_polynomial: degree-2 polynomial fitted to discharge_index vs SOH\n\n")

        for battery_id, battery_metrics in metrics.groupby("battery_id"):
            f.write(f"{battery_id}:\n")
            for _, row in battery_metrics.iterrows():
                f.write(
                    f"  {row['model']}: "
                    f"train cycles = {int(row['train_cycles'])}, "
                    f"test cycles = {int(row['test_cycles'])}, "
                    f"MAE = {row['test_mae']:.4f}, "
                    f"RMSE = {row['test_rmse']:.4f}\n"
                )
            f.write("\n")

        f.write("Average metrics:\n")
        for _, row in average_metrics.iterrows():
            f.write(
                f"{row['model']}: "
                f"MAE = {row['test_mae']:.4f}, "
                f"RMSE = {row['test_rmse']:.4f}\n"
            )

    plt.title("Baseline SOH Prediction")
    plt.xlabel("Discharge cycle index")
    plt.ylabel("State of Health")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    x = np.arange(len(average_metrics))
    width = 0.35

    plt.bar(
        x - width / 2,
        average_metrics["test_mae"],
        width,
        label="MAE",
    )
    plt.bar(
        x + width / 2,
        average_metrics["test_rmse"],
        width,
        label="RMSE",
    )

    plt.xticks(x, average_metrics["model"], rotation=15, ha="right")
    plt.ylabel("SOH error")
    plt.title("Average Baseline SOH Prediction Error")
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(metric_plot_path, dpi=200)
    plt.close()

    print(f"Saved predictions to {predictions_path}")
    print(f"Saved metrics to {metrics_path}")
    print(f"Saved plot to {plot_path}")
    print(f"Saved metric comparison plot to {metric_plot_path}")


if __name__ == "__main__":
    main()
