from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def mean_absolute_error(y_true, y_pred):
    return float(np.mean(np.abs(y_true - y_pred)))


def root_mean_squared_error(y_true, y_pred):
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def fit_linear_regression(X, y):
    X_with_bias = np.column_stack([np.ones(len(X)), X])
    coefficients, *_ = np.linalg.lstsq(X_with_bias, y, rcond=None)
    return coefficients


def predict_linear_regression(X, coefficients):
    X_with_bias = np.column_stack([np.ones(len(X)), X])
    return X_with_bias @ coefficients


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


def build_features(df):
    frames = []

    for battery_id, group in df.groupby("battery_id"):
        group = group.sort_values("discharge_index").copy()
        group["soh_lag_1"] = group["soh"].shift(1)
        group["soh_lag_2"] = group["soh"].shift(2)
        group["capacity_lag_1"] = group["capacity_ah"].shift(1)
        frames.append(group)

    features = pd.concat(frames, ignore_index=True)
    features = features.dropna(
        subset=["soh_lag_1", "soh_lag_2", "capacity_lag_1"]
    ).copy()

    return features


def recursive_forecast(test_index_values, coefficients, last_soh_1, last_soh_2, initial_capacity):
    predictions = []

    previous_soh_1 = float(last_soh_1)
    previous_soh_2 = float(last_soh_2)
    previous_capacity = previous_soh_1 * initial_capacity

    for discharge_index in test_index_values:
        X_next = np.array(
            [[
                float(discharge_index),
                previous_soh_1,
                previous_soh_2,
                previous_capacity,
            ]]
        )

        predicted_soh = float(predict_linear_regression(X_next, coefficients)[0])
        predictions.append(predicted_soh)

        previous_soh_2 = previous_soh_1
        previous_soh_1 = predicted_soh
        previous_capacity = predicted_soh * initial_capacity

    return np.array(predictions, dtype=float)


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

    df_features = build_features(df)

    feature_columns = [
        "discharge_index",
        "soh_lag_1",
        "soh_lag_2",
        "capacity_lag_1",
    ]

    all_predictions = []
    metric_rows = []

    plt.figure(figsize=(10, 6))

    for battery_id, group in df_features.groupby("battery_id"):
        group = group.sort_values("discharge_index").copy()

        split_index = int(len(group) * 0.7)
        train = group.iloc[:split_index]
        test = group.iloc[split_index:]

        X_train = train[feature_columns].to_numpy(dtype=float)
        y_train = train["soh"].to_numpy(dtype=float)

        X_test = test[feature_columns].to_numpy(dtype=float)
        y_test = test["soh"].to_numpy(dtype=float)

        coefficients = fit_linear_regression(X_train, y_train)

        y_pred_one_step = predict_linear_regression(X_test, coefficients)

        last_observed_soh = y_train[-1]
        y_pred_naive = np.full_like(y_test, fill_value=last_observed_soh, dtype=float)

        last_train_soh_1 = train["soh"].iloc[-1]
        last_train_soh_2 = train["soh"].iloc[-2]
        first_capacity = df.loc[df["battery_id"] == battery_id, "capacity_ah"].iloc[0]

        y_pred_recursive = recursive_forecast(
            test_index_values=test["discharge_index"].to_numpy(dtype=float),
            coefficients=coefficients,
            last_soh_1=last_train_soh_1,
            last_soh_2=last_train_soh_2,
            initial_capacity=float(first_capacity),
        )

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
            "lag_one_step_linear",
            len(train),
            len(test),
            y_test,
            y_pred_one_step,
        )
        add_metric_row(
            metric_rows,
            battery_id,
            "recursive_lag_linear",
            len(train),
            len(test),
            y_test,
            y_pred_recursive,
        )

        prediction_frame = test[
            ["battery_id", "discharge_index", "soh", *feature_columns]
        ].copy()
        prediction_frame["naive_predicted_soh"] = y_pred_naive
        prediction_frame["one_step_predicted_soh"] = y_pred_one_step
        prediction_frame["recursive_predicted_soh"] = y_pred_recursive
        all_predictions.append(prediction_frame)

        plt.plot(
            group["discharge_index"],
            group["soh"],
            linewidth=1.5,
            label=f"{battery_id} actual",
        )
        plt.plot(
            test["discharge_index"],
            y_pred_recursive,
            linestyle="--",
            linewidth=1.5,
            label=f"{battery_id} recursive",
        )

    predictions = pd.concat(all_predictions, ignore_index=True)
    metrics = pd.DataFrame(metric_rows)

    predictions_path = results_dir / "recursive_soh_forecast_predictions.csv"
    metrics_path = results_dir / "recursive_soh_forecast_metrics.txt"
    plot_path = results_dir / "recursive_soh_forecast.png"
    metric_plot_path = results_dir / "recursive_soh_forecast_metric_comparison.png"

    predictions.to_csv(predictions_path, index=False)

    average_metrics = (
        metrics.groupby("model")[["test_mae", "test_rmse"]]
        .mean()
        .reset_index()
        .sort_values("test_mae")
    )

    with metrics_path.open("w") as f:
        f.write("Recursive SOH forecast metrics\n")
        f.write("==============================\n\n")
        f.write("Task: later-cycle SOH forecasting using a lag-based linear model\n")
        f.write("Target: normalized SOH\n")
        f.write("Train/test split: first 70% cycles train, last 30% cycles test\n\n")
        f.write("Models:\n")
        f.write("- naive_last_observed: repeats the last SOH value seen in training\n")
        f.write("- lag_one_step_linear: uses observed lag features in the test window\n")
        f.write("- recursive_lag_linear: feeds its own predictions back as future lag values\n\n")
        f.write("Important note: recursive_lag_linear is stricter than the one-step lag test.\n")
        f.write("It does not use observed future SOH values as lag inputs after forecasting starts.\n\n")

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

    plt.title("Recursive SOH Forecast")
    plt.xlabel("Discharge cycle index")
    plt.ylabel("State of Health")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=200)
    plt.close()

    plt.figure(figsize=(9, 5))
    x = np.arange(len(average_metrics))
    width = 0.35

    plt.bar(x - width / 2, average_metrics["test_mae"], width, label="MAE")
    plt.bar(x + width / 2, average_metrics["test_rmse"], width, label="RMSE")

    plt.xticks(x, average_metrics["model"], rotation=15, ha="right")
    plt.ylabel("SOH error")
    plt.title("Average Recursive SOH Forecast Error")
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
