# Project Plan

## Project Idea

Build a battery health estimation project that starts from real battery aging data and later can be extended toward simple embedded data logging.

The project should not be a generic neural network demo. It should compare ordinary data-driven prediction with physics-guided modeling ideas.

## Phase 1: Dataset and Visualization

Tasks:

- choose the first dataset
- document dataset source and structure
- write a data inspection script
- create capacity degradation plots
- create voltage/current/temperature plots if available

Expected output:

- dataset notes
- exploratory plots
- first README update with real dataset details

## Phase 2: Baseline Prediction

Tasks:

- build a clean processed dataset
- train baseline models
- evaluate capacity or state-of-health prediction
- plot true vs predicted values
- report error metrics

Possible models:

- linear regression baseline
- random forest regressor
- small neural network baseline

## Phase 3: Physics-Guided Modeling

Tasks:

- add monotonic degradation constraint or penalty
- compare constrained and unconstrained predictions
- check whether the physics-guided version behaves better under sparse or noisy data

Important note:

This should be called physics-guided unless a real PINN-style differential-equation residual is implemented.

## Phase 4: Visual Dashboard

Tasks:

- combine key plots into a dashboard figure
- show capacity fade, prediction performance, and error behavior
- keep the visual design clean and technical

## Phase 5: Optional Hardware Version

Possible hardware:

- ESP32
- INA219 or INA226 current/voltage sensor
- Li-ion battery
- discharge load
- temperature sensor

Goal:

Collect simple battery discharge logs and compare them with the dataset-based workflow.

This phase should only be started after the dataset-based model is working.
