from pathlib import Path

import pandas as pd
from scipy.io import loadmat


RAW_DIR = Path("data/raw")
OUTPUT_PATH = Path("data/processed/discharge_capacity.csv")


def load_battery_mat(path):
    data = loadmat(path, squeeze_me=True, struct_as_record=False)
    battery_id = path.stem

    if battery_id not in data:
        raise KeyError(f"Expected key {battery_id} in {path}")

    return battery_id, data[battery_id]


def extract_discharge_cycles(path):
    battery_id, battery = load_battery_mat(path)
    rows = []

    discharge_index = 0

    for cycle_index, cycle in enumerate(battery.cycle):
        if cycle.type != "discharge":
            continue

        discharge_index += 1
        cycle_data = cycle.data

        if not hasattr(cycle_data, "Capacity"):
            continue

        rows.append(
            {
                "battery_id": battery_id,
                "cycle_index": cycle_index,
                "discharge_index": discharge_index,
                "ambient_temperature": cycle.ambient_temperature,
                "capacity_ah": float(cycle_data.Capacity),
                "num_samples": len(cycle_data.Time),
            }
        )

    return rows


def main():
    mat_files = sorted(RAW_DIR.rglob("B*.mat"))

    if not mat_files:
        print("No battery .mat files found under data/raw/")
        return

    rows = []

    for path in mat_files:
        print(f"Extracting discharge cycles from: {path}")
        rows.extend(extract_discharge_cycles(path))

    df = pd.DataFrame(rows)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print()
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print()
    print("Battery summary:")
    print(
        df.groupby("battery_id")
        .agg(
            discharge_cycles=("discharge_index", "count"),
            first_capacity_ah=("capacity_ah", "first"),
            last_capacity_ah=("capacity_ah", "last"),
            min_capacity_ah=("capacity_ah", "min"),
            max_capacity_ah=("capacity_ah", "max"),
        )
        .round(4)
    )


if __name__ == "__main__":
    main()
