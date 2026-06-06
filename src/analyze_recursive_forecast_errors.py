from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main():
    predictions_path = Path("results/recursive_soh_forecast_predictions.csv")
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(predictions_path)

    required_columns = {
        "battery_id",
        "discharge_index",
        "soh",
        "naive_predicted_soh",
        "one_step_predicted_soh",
        "recursive_predicted_soh",
    }
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.sort_values(["battery_id", "discharge_index"]).copy()

    df["naive_abs_error"] = (df["soh"] - df["naive_predicted_soh"]).abs()
    df["one_step_abs_error"] = (df["soh"] - df["one_step_predicted_soh"]).abs()
    df["recursive_abs_error"] = (df["soh"] - df["recursive_predicted_soh"]).abs()

    summary_rows = []

    for battery_id, group in df.groupby("battery_id"):
        group = group.sort_values("discharge_index")

        worst_row = group.loc[group["recursive_abs_error"].idxmax()]
        final_row = group.iloc[-1]

        summary_rows.append(
            {
                "battery_id": battery_id,
                "test_cycles": len(group),
                "recursive_mean_abs_error": group["recursive_abs_error"].mean(),
                "recursive_max_abs_error": group["recursive_abs_error"].max(),
                "worst_cycle": int(worst_row["discharge_index"]),
                "final_cycle": int(final_row["discharge_index"]),
                "final_recursive_abs_error": final_row["recursive_abs_error"],
                "final_actual_soh": final_row["soh"],
                "final_recursive_soh": final_row["recursive_predicted_soh"],
            }
        )

    summary = pd.DataFrame(summary_rows)

    summary_path = results_dir / "recursive_forecast_error_analysis.txt"
    summary_csv_path = results_dir / "recursive_forecast_error_analysis.csv"
    plot_path = results_dir / "recursive_forecast_error_by_battery.png"

    summary.to_csv(summary_csv_path, index=False)

    with summary_path.open("w") as f:
        f.write("Recursive forecast error analysis\n")
        f.write("=================================\n\n")
        f.write("This analysis checks where the recursive SOH forecast drifts during the test window.\n")
        f.write("The recursive model feeds its own predictions back as future lag values, so error can accumulate over time.\n\n")

        for _, row in summary.iterrows():
            f.write(
                f"{row['battery_id']}: "
                f"test cycles = {int(row['test_cycles'])}, "
                f"mean recursive abs error = {row['recursive_mean_abs_error']:.4f}, "
                f"max recursive abs error = {row['recursive_max_abs_error']:.4f} "
                f"at cycle {int(row['worst_cycle'])}, "
                f"final abs error = {row['final_recursive_abs_error']:.4f} "
                f"at cycle {int(row['final_cycle'])}\n"
            )

        worst_battery = summary.sort_values("recursive_mean_abs_error", ascending=False).iloc[0]
        f.write("\nLargest average recursive drift:\n")
        f.write(
            f"{worst_battery['battery_id']} with mean absolute error "
            f"{worst_battery['recursive_mean_abs_error']:.4f}\n"
        )

    plt.figure(figsize=(8, 5))
    plt.bar(summary["battery_id"], summary["recursive_mean_abs_error"])
    plt.ylabel("Mean absolute SOH error")
    plt.xlabel("Battery")
    plt.title("Recursive Forecast Error by Battery")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=200)
    plt.close()

    print(f"Saved text summary to {summary_path}")
    print(f"Saved CSV summary to {summary_csv_path}")
    print(f"Saved plot to {plot_path}")


if __name__ == "__main__":
    main()
