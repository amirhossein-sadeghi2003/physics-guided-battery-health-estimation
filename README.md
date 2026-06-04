# Physics-Guided Battery Health Estimation

This project is planned as a physics-guided machine learning project for battery health and remaining useful life estimation.

The goal is to start with a real public battery aging dataset, build clear visual analysis, train baseline models, and then test whether physics-guided constraints can make the predictions more reliable.

This is not a finished battery management system yet. The first version will focus on data loading, visualization, baseline modeling, and honest evaluation.


## First Results

The first processed dataset in this repository is built from the NASA battery aging files `B0005`, `B0006`, `B0007`, and `B0018`.

So far, the project extracts discharge-cycle capacity values and visualizes capacity fade across cycles.

Current processed table:

- `data/processed/discharge_capacity.csv`

Current result files:

- `results/capacity_fade.png`
- `results/capacity_fade_summary.txt`
- `results/normalized_soh.png`
- `results/normalized_soh_summary.txt`
- `results/b0005_discharge_voltage_curves.png`

### Capacity Fade Plot

![NASA Battery Capacity Fade](results/capacity_fade.png)


### Normalized State of Health Plot

The project also normalizes each cell's capacity by its first discharge capacity:

`SOH = capacity / initial capacity`

This makes the degradation trend easier to compare across cells, even when their absolute starting capacities are slightly different.

Result files:

- `results/normalized_soh.png`
- `results/normalized_soh_summary.txt`

![Normalized Battery State of Health](results/normalized_soh.png)

In the current subset, `B0006` falls the fastest and ends at about `0.5825` SOH after 168 discharge cycles.

### Discharge Voltage Curve Example

The repository also includes an example discharge-voltage visualization for `B0005`.

This plot compares several discharge cycles from early, middle, and later life:

- cycle 1
- cycle 40
- cycle 80
- cycle 120
- cycle 160

Result file:

- `results/b0005_discharge_voltage_curves.png`

![B0005 Discharge Voltage Curves](results/b0005_discharge_voltage_curves.png)

This figure makes the degradation behavior more concrete than a single capacity table. Later cycles show a shorter discharge trajectory and lower voltage sustain compared with earlier cycles.

### Capacity Fade Summary

From the first four batteries:

- `B0005`: capacity drop ≈ 28.62%
- `B0006`: capacity drop ≈ 41.75%
- `B0007`: capacity drop ≈ 24.25%
- `B0018`: capacity drop ≈ 27.71%

Among these four cells, `B0006` shows the largest relative capacity loss in the current subset.

This is still an early data-processing stage. The project has not yet built predictive models or physics-guided constraints.

## Planned Direction

The project will follow this path:

1. Load and inspect a real battery aging dataset
2. Visualize capacity fade over cycles
3. Plot voltage, current, and temperature behavior during charge/discharge
4. Build baseline ML models for capacity or health prediction
5. Add physics-guided constraints such as monotonic capacity degradation
6. Compare baseline ML against physics-guided modeling
7. Create visual result dashboards
8. Later, optionally connect the workflow to simple ESP32-based battery voltage/current logging

## Why This Project Fits My Portfolio

This project connects machine learning with a real physical degradation process.

It fits my broader direction in intelligent physical systems because it combines:

- time-series sensor data
- physical system behavior
- degradation modeling
- machine learning
- interpretable evaluation
- possible embedded data logging in a later version

## Planned Visual Results

The project should eventually include:

- capacity fade curves
- voltage-discharge curves
- true vs predicted capacity
- remaining useful life trend
- prediction error plots
- model comparison figures
- a battery health dashboard-style summary

## Planned Hardware Extension

A later hardware version may use:

- ESP32
- Li-ion battery
- INA219 or INA226 voltage/current sensor
- temperature sensor
- simple load for discharge testing
- optional OLED or SD-card logging

The hardware version is not part of the first milestone. It should only be added after the dataset-based modeling pipeline is working.

## Current Status

The first data-processing and visualization milestone is complete.

Implemented so far:

- NASA battery `.mat` file inspection
- discharge capacity extraction
- capacity fade visualization
- normalized SOH visualization
- example discharge-voltage curve comparison for `B0005`

Next step:

- build a simple baseline model for capacity or SOH prediction
