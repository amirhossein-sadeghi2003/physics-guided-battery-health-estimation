from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


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

    plt.figure(figsize=(10, 6))

    for battery_id, group in df.groupby("battery_id"):
        plt.plot(
            group["discharge_index"],
            group["soh"],
            marker="o",
            markersize=2,
            linewidth=1.5,
            label=battery_id,
        )

    plt.axhline(0.8, linestyle="--", linewidth=1, label="80% SOH reference")

    plt.title("Normalized Battery State of Health")
    plt.xlabel("Discharge cycle index")
    plt.ylabel("State of Health (capacity / initial capacity)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_path = results_dir / "normalized_soh.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    summary_rows = []
    for battery_id, group in df.groupby("battery_id"):
        start_soh = group["soh"].iloc[0]
        final_soh = group["soh"].iloc[-1]
        summary_rows.append(
            {
                "battery_id": battery_id,
                "cycles": int(group["discharge_index"].max()),
                "start_soh": start_soh,
                "final_soh": final_soh,
                "soh_drop_percent": (start_soh - final_soh) * 100,
            }
        )

    summary = pd.DataFrame(summary_rows)
    summary_path = results_dir / "normalized_soh_summary.txt"

    with summary_path.open("w") as f:
        f.write("Normalized SOH summary\n")
        f.write("======================\n\n")
        for _, row in summary.iterrows():
            f.write(
                f"{row['battery_id']}: "
                f"{int(row['cycles'])} discharge cycles, "
                f"final SOH = {row['final_soh']:.4f}, "
                f"SOH drop = {row['soh_drop_percent']:.2f}%\n"
            )

    print(f"Saved plot to {output_path}")
    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()
