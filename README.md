# Physics-Guided Battery Health Estimation

This project is planned as a physics-guided machine learning project for battery health and remaining useful life estimation.

The goal is to start with a real public battery aging dataset, build clear visual analysis, train baseline models, and then test whether physics-guided constraints can make the predictions more reliable.

This is not a finished battery management system yet. The first version will focus on data loading, visualization, baseline modeling, and honest evaluation.

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

Project roadmap created.

Next step:

- add dataset notes and the first data-loading script
