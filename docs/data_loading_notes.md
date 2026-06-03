# Data Loading Notes

The first data-loading step is focused on understanding the raw NASA battery `.mat` files before building a processed dataset.

Raw data should be placed under:

    data/raw/

Raw data files are intentionally not tracked by Git.

## First Inspection Script

Script:

    src/inspect_raw_battery_data.py

Purpose:

- find `.mat` files in `data/raw/`
- print top-level MATLAB keys
- show array shapes and data types
- confirm the raw structure before writing a converter

Run:

    python src/inspect_raw_battery_data.py

Expected first result before downloading data:

    No .mat files found in data/raw/

Expected result after adding NASA battery files:

- list of battery files
- top-level keys
- MATLAB structure information

## Next Data Step

After the raw structure is confirmed, the next script should extract discharge cycles into a clean table with fields such as:

- battery_id
- cycle_index
- capacity
- voltage_measured
- current_measured
- temperature_measured
- time
