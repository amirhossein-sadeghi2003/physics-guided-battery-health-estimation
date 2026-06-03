# Dataset Selection Notes

## Selected First Dataset

The first dataset planned for this project is the NASA Li-ion Battery Aging Dataset.

This dataset is a good first choice because it is connected to battery degradation and prognostics, and it contains real battery test data rather than only synthetic examples.

## Why This Dataset Fits the Project

This project is focused on physics-guided battery health estimation.

The NASA battery dataset fits because it can support:

- capacity fade visualization
- cycle-based degradation analysis
- voltage and current curve inspection
- temperature-aware analysis
- baseline capacity or state-of-health prediction
- later physics-guided constraints such as monotonic degradation behavior

The first goal is not to build a full battery management system. The first goal is to understand the dataset, create reliable visualizations, and build a simple baseline before adding physics-guided modeling.

## Expected Data Types

The dataset is expected to include battery operation records such as:

- charge cycles
- discharge cycles
- impedance measurements
- measured voltage
- measured current
- measured temperature
- time-series values within cycles
- capacity values for discharge cycles

The exact structure should be verified after downloading and inspecting the files.

## First Analysis Questions

The first milestone should answer these questions:

1. Which battery cells are available?
2. How many cycles does each battery have?
3. Which cycles include capacity values?
4. Does capacity generally decrease over cycle number?
5. What do voltage curves look like during discharge?
6. Are there missing or irregular records?
7. Which target should be modeled first: capacity, state of health, or remaining useful life?

## First Visualizations

The first useful plots should be:

- capacity vs cycle number
- discharge voltage vs time for selected cycles
- temperature vs time for selected cycles
- current vs time for selected cycles
- battery-to-battery capacity fade comparison

## Modeling Plan

The modeling should start simple:

1. Build a clean cycle-level table.
2. Use cycle number and simple discharge features as inputs.
3. Predict capacity or state of health.
4. Compare baseline models.
5. Add physics-guided constraints only after the baseline is working.

## Physics-Guided Direction

The first physics-guided idea should be conservative and defensible.

Possible constraints:

- capacity should generally not increase over long-term aging
- predicted state of health should stay within a realistic range
- model behavior should be checked against cycle progression
- noisy local capacity recovery should not be over-interpreted as real long-term improvement

This should be called physics-guided modeling unless a real differential-equation residual is implemented later.

## Hardware Extension Later

A later hardware version could collect simple battery discharge logs using:

- ESP32
- INA219 or INA226 voltage/current sensor
- temperature sensor
- Li-ion battery
- simple discharge load

That hardware extension should come after the dataset-based workflow is working.
