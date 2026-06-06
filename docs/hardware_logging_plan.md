# Hardware Logging Plan

This document describes the planned hardware extension for this battery health estimation repository.

The current repository is based on the NASA battery aging dataset. The hardware extension is meant to add a small Arduino-based logging setup for simple voltage, current, and temperature measurements. It is not intended to replace the dataset-based analysis, and it is not a full battery management system.

## Goal

The goal is to collect small physical battery-load logs using simple hardware, then compare the measured behavior with the existing battery health workflow in this repository.

The hardware phase will focus on:

- measuring battery/load voltage
- measuring current through a known load
- measuring battery surface temperature
- saving serial logs as CSV files
- plotting voltage, current, power, and temperature over time

## Planned Hardware

The planned setup uses:

- Arduino UNO R3
- INA226 voltage/current monitor module
- DS18B20 waterproof temperature sensor
- TP4056/TC4056 lithium battery charger and protection module
- single 18650 battery holder
- QB 18650 Li-ion rechargeable cell, 3.7 V, 2000 mAh
- 27 ohm 10 W cement resistor as the first test load
- 10 ohm 10 W cement resistor as a heavier later test load
- 4.7 kOhm resistor for the DS18B20 data pull-up

## Planned Logged Signals

The expected CSV format is:

timestamp_s,bus_voltage_v,current_ma,power_mw,temperature_c,load_resistance_ohm,test_stage

The meaning of each column is:

- timestamp_s: elapsed time from the start of the test
- bus_voltage_v: measured voltage from the INA226 module
- current_ma: measured current through the load
- power_mw: estimated load power
- temperature_c: measured surface temperature near the battery
- load_resistance_ohm: resistor value used during the test
- test_stage: short label describing the current test stage

## Planned Test Order

The hardware should be tested in stages:

1. Arduino serial test only
2. DS18B20 temperature sensor test only
3. INA226 voltage/current monitor test only
4. TP4056/TC4056 battery charging and protection check
5. short load test with the 27 ohm resistor
6. later short load test with the 10 ohm resistor, only if earlier tests are stable

The 27 ohm resistor should be used first because it is the safer and lighter load. The 10 ohm resistor draws more current and can become hot during testing.

## Safety Notes

This setup must be tested conservatively.

- Do not connect the battery directly to the Arduino.
- Do not connect the battery directly to a load before the wiring is checked.
- Use the TP4056/TC4056 protection module between the battery and the output/load side.
- Start with the 27 ohm load.
- Keep the first tests short.
- Monitor temperature during load tests.
- Do not touch the cement resistor during or immediately after testing.
- Stop the test if the battery or resistor becomes unexpectedly hot.
- Avoid over-discharging the cell.

## What This Extension Does Not Claim

This extension is not:

- a production battery management system
- a controlled battery cycler
- an accurate SOH estimator from a few short tests
- a replacement for the NASA battery aging dataset
- a safety-certified lithium battery testing system

The purpose is to connect the dataset-based battery health workflow to a small physical logging experiment in a transparent and limited way.

## Connection to the Existing Repository

The existing repository already includes:

- NASA battery capacity extraction
- capacity fade visualization
- normalized SOH visualization
- baseline SOH prediction
- lag-based SOH prediction
- recursive SOH forecasting
- recursive forecast error analysis

The hardware logging extension will add a small real-measurement layer on top of this workflow. The first useful result will likely be a simple voltage/current/temperature curve from a short load test, not a full battery aging or SOH experiment.
