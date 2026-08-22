# Data Loading Notes

## Source

The project uses the Battery Data Set from the NASA Prognostics Center of Excellence:

- [NASA PCoE Data Set Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)
- [Battery Data Set download](https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip)

Dataset citation:

> B. Saha and K. Goebel (2007). “Battery Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, CA.

## Raw Files

Raw MATLAB files are intentionally not tracked. Extract the NASA archive and place the required `B*.mat` files anywhere under:

```text
data/raw/
```

Inspect their structure with:

```bash
python src/inspect_raw_battery_data.py
```

The script reports top-level MATLAB keys, array shapes, and data types.

## Capacity Extraction

Build the tracked cycle-level table with:

```bash
python src/extract_discharge_capacity.py
```

The extractor recursively finds `B*.mat` files under `data/raw/` and writes:

```text
data/processed/discharge_capacity.csv
```

The current public table contains 636 discharge cycles from `B0005`, `B0006`, `B0007`, and `B0018`.

## Voltage-Curve Input

`src/plot_discharge_voltage_curves.py` uses one fixed raw-data path:

```text
data/raw/nasa_battery/arc_fy08q4/B0005.mat
```

Place `B0005.mat` there before regenerating the discharge-voltage figure.
