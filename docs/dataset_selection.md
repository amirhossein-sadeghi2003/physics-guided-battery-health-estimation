# Dataset Selection

## Selected Dataset

This project uses the NASA Prognostics Center of Excellence Battery Data Set:

- [official repository and citation](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)
- [complete dataset download](https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip)

The selected cells are `B0005`, `B0006`, `B0007`, and `B0018`.

## Why It Fits

The dataset contains repeated charge, discharge, and impedance operations from real Li-ion aging experiments. It supports:

- capacity-fade analysis;
- normalized SOH calculation;
- within-cycle voltage inspection;
- chronological later-cycle forecasting;
- analysis of forecast drift and local capacity recovery.

## Current Public Representation

The raw MATLAB files remain outside Git. The tracked cycle-level table stores:

- battery identifier;
- original cycle index;
- discharge-cycle index;
- ambient temperature;
- measured discharge capacity;
- number of within-cycle samples.

The current table has 636 rows with no missing values or duplicate battery/discharge-index pairs.

## Implemented Modeling Scope

The repository currently evaluates:

1. a last-observed SOH baseline;
2. quadratic extrapolation from cycle index;
3. one-step linear prediction from two observed SOH lags;
4. recursive forecasting using the model's own prior predictions;
5. recursive error growth across the test horizon.

The evaluation is chronological but remains within each battery. It does not test whether a model trained on some cells generalizes to a different cell.

## Physics-Guided Direction

No physics-guided constraint is implemented in the current version. A future extension should only use that label after adding and evaluating a concrete mechanism, such as:

- a defensible monotonic or bounded formulation;
- physically meaningful voltage, current, temperature, or impedance features;
- an electrochemical or equivalent-circuit relationship;
- an explicit comparison with the unconstrained baseline.

Remaining useful life is also outside the current implementation.
