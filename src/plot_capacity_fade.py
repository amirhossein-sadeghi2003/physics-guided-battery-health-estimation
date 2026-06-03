from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = Path("data/processed/discharge_capacity.csv")
RESULTS_DIR = Path("results")
PLOT_PATH = RESULTS_DIR / "capacity_fade.png"
SUMMARY_PATH = RESULTS_DIR / "capacity_fade_summary.txt"


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing processed table: {INPUT_PATH}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    required_columns = {
        "battery_id",
        "discharge_index",
        "capacity_ah",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    fig, ax = plt.subplots(figsize=(10, 6))

    for battery_id, part in df.groupby("battery_id"):
        part = part.sort_values("discharge_index")
        ax.plot(
            part["discharge_index"],
            part["capacity_ah"],
            marker="o",
            markersize=2.5,
            linewidth=1.4,
            label=battery_id,
        )

    ax.set_title("NASA Battery Capacity Fade")
    ax.set_xlabel("Discharge cycle index")
    ax.set_ylabel("Capacity (Ah)")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Battery")

    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()

    summary = (
        df.groupby("battery_id")
        .agg(
            discharge_cycles=("discharge_index", "count"),
            first_capacity_ah=("capacity_ah", "first"),
            last_capacity_ah=("capacity_ah", "last"),
            min_capacity_ah=("capacity_ah", "min"),
            max_capacity_ah=("capacity_ah", "max"),
        )
        .reset_index()
    )

    summary["capacity_drop_ah"] = (
        summary["first_capacity_ah"] - summary["last_capacity_ah"]
    )

    summary["capacity_drop_percent"] = (
        summary["capacity_drop_ah"] / summary["first_capacity_ah"] * 100.0
    )

    summary = summary.round(4)

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("NASA battery capacity fade summary\n\n")
        f.write(summary.to_string(index=False))
        f.write("\n")

    print(f"Saved plot: {PLOT_PATH}")
    print(f"Saved summary: {SUMMARY_PATH}")
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
