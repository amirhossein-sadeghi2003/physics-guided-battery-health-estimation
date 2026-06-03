from pathlib import Path

import matplotlib.pyplot as plt
from scipy.io import loadmat


RAW_FILE = Path("data/raw/nasa_battery/arc_fy08q4/B0005.mat")
RESULTS_DIR = Path("results")
OUTPUT_PATH = RESULTS_DIR / "b0005_discharge_voltage_curves.png"


SELECTED_DISCHARGE_INDICES = [1, 40, 80, 120, 160]


def load_battery(path):
    data = loadmat(path, squeeze_me=True, struct_as_record=False)
    battery_id = path.stem

    if battery_id not in data:
        raise KeyError(f"Expected key {battery_id} in {path}")

    return battery_id, data[battery_id]


def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Missing raw battery file: {RAW_FILE}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    battery_id, battery = load_battery(RAW_FILE)

    discharge_cycles = [
        cycle for cycle in battery.cycle
        if cycle.type == "discharge"
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    for discharge_index in SELECTED_DISCHARGE_INDICES:
        if discharge_index > len(discharge_cycles):
            continue

        cycle = discharge_cycles[discharge_index - 1]
        data = cycle.data

        ax.plot(
            data.Time,
            data.Voltage_measured,
            linewidth=1.6,
            label=f"Cycle {discharge_index}",
        )

    ax.set_title(f"{battery_id} Discharge Voltage Curves")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Measured voltage (V)")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Discharge cycle")

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=150)
    plt.close()

    print(f"Saved plot: {OUTPUT_PATH}")
    print(f"Battery: {battery_id}")
    print(f"Discharge cycles available: {len(discharge_cycles)}")
    print(f"Selected cycles: {SELECTED_DISCHARGE_INDICES}")


if __name__ == "__main__":
    main()
