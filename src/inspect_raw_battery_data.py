from pathlib import Path

from scipy.io import loadmat


RAW_DIR = Path("data/raw")


def describe_value(value, indent=0):
    prefix = " " * indent

    if hasattr(value, "shape"):
        print(f"{prefix}- type: {type(value).__name__}, shape: {value.shape}, dtype: {getattr(value, 'dtype', 'n/a')}")
    else:
        print(f"{prefix}- type: {type(value).__name__}")


def inspect_mat_file(path):
    print("=" * 80)
    print(f"File: {path}")
    print("=" * 80)

    data = loadmat(path, squeeze_me=True, struct_as_record=False)

    keys = [key for key in data.keys() if not key.startswith("__")]

    print("Top-level keys:")
    for key in keys:
        print(f"- {key}")
        describe_value(data[key], indent=2)

    print()


def main():
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Missing raw data directory: {RAW_DIR}")

    mat_files = sorted(RAW_DIR.rglob("*.mat"))

    if not mat_files:
        print("No .mat files found under data/raw/")
        print("Download or extract the NASA battery .mat files under data/raw/.")
        return

    print(f"Found {len(mat_files)} .mat files")

    for path in mat_files:
        inspect_mat_file(path)


if __name__ == "__main__":
    main()
