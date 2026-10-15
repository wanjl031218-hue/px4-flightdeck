# Experiments and parameter assistance

## Fix the question and boundaries

Identify the scenario, desired performance, hard constraints, baseline, candidate
variables, allowed changes, and evaluation rules. Preserve the user's chosen role:
an offline parameter-analysis agent is different from an online flight policy.
Read the current allowlist and change-budget agreement rather than inventing one.
Resolve conflicting local policies before making a proposal that depends on them.

Keep mission settings, PX4 parameters, simulator physics, and controller source as
distinct change types. A PX4-parameter-only experiment does not permit changing a
trajectory, tolerance, scorer, or model to manufacture better results.

## Establish what the data can support

Inventory each run's configuration/build identity, target and measured state, events,
coordinate frame/units, clock definitions, and any PX4 parameter snapshot or ULog.
Parse the actual schema; example filenames are not a guaranteed logging standard.
Keep raw artifacts immutable and retain unsuccessful/aborted runs with reasons.

Judge data per metric and time window. Useful working categories are:

- **Usable:** required fields and conditions support the specified metric/window.
- **Usable with caveats:** a bounded comparison is possible with explicit limitations.
- **Invalid for this metric:** missing/inconsistent inputs make that metric undefined.

Map the project's labels to these meanings; do not silently relabel its raw records.
A reset before a stable evaluation window need not invalidate every later metric;
a complete CSV does not prove estimator health. Check finite values, timestamp order,
gaps, message freshness, resets, mode changes, and recording completeness. Segment
windows using events and declared rules, retain exclusions, and report coverage.
Do not fill missing values with zero or treat an absent field as a successful check.

When failure handling is part of the claim, report all attempted runs and outcomes.
“Five successful runs” can establish a conditional performance reference; if failed
attempts were omitted, it cannot establish an overall task-success rate.

## Calculate, then interpret

For schema alignment and an optional executable CSV scorer, see
[logs and metrics](logs-metrics.md). For parameter-to-controller mechanisms, see
[controller tracing](controllers-parameters.md). Load these when the task needs them.

Use a deterministic analysis script appropriate to the available schema. Read an
existing scorer before replacing it. Record metric definitions, units, windows,
configuration, and scorer revision; use the same definitions for baseline/candidate.
Do not estimate precise metrics by visual inspection or fabricate results if execution
is unavailable. Write/run a minimal suitable analysis when authorized and feasible.

Specify conventions before calculating:

- Tracking RMSE: axis/vector definition, frame alignment, weighting. At uniform
  sampling, `sqrt(mean(error**2))`; at irregular sampling, use a declared time-weighted
  rule or justify resampling. Avoid weighting long gaps as observed healthy behavior.
- Overshoot: reference change, direction, peak definition, and normalization. A zero
  reference step cannot define percentage overshoot. Moving references need a different
  definition from a static step response.
- Settling/recovery time: event start, tolerance, required dwell, valid feedback, and
  observation horizon. If it never settles, report censored/not settled rather than zero.
- Steady-state error: signed/absolute definition and a declared terminal window.
- Oscillation/effort/saturation: use appropriate measured signals. Position and velocity
  alone cannot establish actuator saturation, thrust effort, or attitude-loop causality.

For each result cite run ID, artifact, fields, and interval (plus schema/scorer when
needed). Separate computed observation, plausible mechanism, and evidence needed for a
causal claim. A useful analysis offers a control hypothesis even with caveats, but marks
which conclusions require more data.

## Propose a bounded candidate

Check the actual PX4 branch's parameter definition and relevant controller use:
name, type, unit, range, coupled limits, and automatic estimation/adaptation.
Confirm current runtime values from a snapshot/readback; source defaults are not current
values. Missing current values prevent a grounded numeric change and rollback plan;
still give a mechanism hypothesis and targeted measurement request when useful.

For every candidate provide current → proposed → rollback values, affected control
stage, supporting data, expected benefit, side effects, confidence, and a discriminating
retest. Respect the project's allowlist and permitted number/group of changes. Avoid
using sensor, battery, communication, or safety settings to hide a tracking problem.
Separate proposing changes from authorization to apply them to a target.

Editing candidate files is ordinary authorized coding work; applying them to a vehicle
is a separate operation. For approved runtime application, identify the target/configuration and fresh ground/disarmed
state, save current values, apply only the agreed change, read it back, and preserve the
recovery method. Hardware validation requires its own appropriate agreed procedure;
SITL evidence does not authorize a real flight or prove real-flight behavior.

## Compare without moving the target

Pair baseline/candidate trials on the same conditions/seeds/disturbances where possible.
Freeze the mission, scorer, vehicle/model, and timing rules. Predetermine acceptance and
hard constraints. Report all attempted runs, individual and aggregate results, spread,
missingness, and failures, not only the best trial. A small batch supports a limited
proof of concept; avoid unsupported significance or broad reliability claims.

Reserve validation conditions not used to select parameters; distinguish matched-case
improvement from generalization. Regression tasks check whether a local improvement
harms other required behaviors. Report accept, reject/restore, or inconclusive with the
actual evidence. Preserve agent input/output, parameter snapshots, human decision,
retest results, and limitations so the report can be reproduced.
