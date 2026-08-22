# Project Status and Roadmap

## Current Scope

The repository is a reproducible battery-degradation and SOH-forecasting baseline built on four NASA aging trajectories.

## Completed

- inspect the nested NASA MATLAB structure;
- extract a public cycle-level capacity table;
- visualize capacity fade and normalized SOH;
- compare selected `B0005` discharge-voltage curves;
- evaluate last-observed and quadratic baselines;
- evaluate a one-step lag model;
- run a recursive multi-step forecast;
- quantify recursive drift by battery;
- document the difference between one-step and free-running evaluation.

## Current Result

The one-step lag model reaches an average MAE of `0.0078`, but it uses observed preceding-cycle SOH values in the test window. When the same model feeds its own predictions forward, average MAE rises to `0.0331`, close to the `0.0323` naive baseline.

This gap is the main result of the current repository.

## Not Implemented

- physics-guided constraints or losses;
- remaining-useful-life estimation;
- cross-battery generalization;
- uncertainty quantification;
- hardware data collection;
- a production battery-management system.

## Defensible Next Experiments

1. Evaluate leave-one-battery-out or another cross-cell split.
2. Add cycle-level health indicators from voltage, current, temperature, or impedance.
3. Measure error as a function of forecast horizon.
4. Compare an unconstrained model with a concrete monotonic or bounded formulation.
5. Keep the Arduino logger separate until real measurements exist.

The optional hardware concept remains documented in `docs/hardware_logging_plan.md`, but it is not part of the implemented results.
