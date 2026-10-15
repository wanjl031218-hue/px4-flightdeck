# Logs and deterministic metrics / 日志与指标

Use when converting measured tracking into reproducible numbers. Read the actual
project scorer first; the bundled scorer is an optional explicit CSV convention,
not a replacement for an agreed evaluation protocol or a ULog parser.

## From logs to one aligned table

Inventory the ULog/CSV schemas and distinguish commanded target from measured state.
Record run ID, frame/origin, units, event times, estimator resets, mode, parameter
snapshot and artifact identity. ULog can contain multi-rate instances: choose the
correct topic instance and align target and measurement with a declared method.
Do not independently interpolate across resets, stale targets or unobserved gaps.

For the pinned PX4 schema, `vehicle_local_position` includes validity flags and
reset counters. A converter should turn those and task-specific checks into a
window decision; merely setting every `valid` to 1 does not establish data quality.
Inspect logged `vehicle_local_position_setpoint` versus externally sent trajectory
targets when distinguishing internal limits from external intent.

中文：先决定“这段数据能否支持这个指标”，再算数。一次估计器重置不一定让整次试验
作废，但不能把坐标跳变直接算成普通跟踪误差。失败和被排除窗口都需要保留。

## Bundled scorer contract

`scripts/score_tracking.py` accepts these columns, with seconds/meters:

```text
t_s,target_x_m,target_y_m,target_z_m,x_m,y_m,z_m,valid
```

- Target and measurement already share a frame and origin. `--frame NED|ENU` is
  the caller's declaration, not an automatic conversion or verification.
- Timestamps strictly increase. Selected window boundaries must be recorded sample
  times. At least two samples, finite selected values and `valid=1` are required.
- An interval longer than `--max-gap` causes rejection, not hidden interpolation.
- Axis RMSE uses trapezoidal integration of **sampled squared errors** divided by
  duration; vector RMSE is the square root of summed axis mean-square errors.
  This quadrature convention is not the exact integral of a linearly interpolated error.
- Optional step scoring treats `--start` as the step event; the selected axis target
  must be constant after it. The caller supplies the actual pre-step target.
- Directional overshoot is clamped at zero and normalized by absolute step amplitude.
  Settling is the first sampled entry that stays inside tolerance through the end,
  with at least the declared dwell remaining. No settling gives JSON `null` and
  `not_settled_within_horizon`, never a fabricated zero.

The script proves properties of the supplied sampled table. It cannot prove between-
sample behavior, sensor freshness, estimator health, actuator effort, causality or
that the event actually occurred. Use a suitable sample rate and external quality checks.

## Runnable synthetic example

From this skill's directory, on any Python 3.9+ host:

```bash
python3 scripts/score_tracking.py assets/examples/tracking-step.csv \
  --start 0 --end 4 --max-gap 1.1 --frame NED \
  --step-axis x --initial-target 0 --tolerance 0.05 --dwell 1
```

Expected: vector RMSE `sqrt(0.1375) ≈ 0.37081 m`, overshoot `0.1 m` / `10%`, settling
`3 s`. Hand calculation: squared errors are `[1, .04, .01, 0, 0]`; trapezoidal area
is `.52 + .025 + .005 + 0 = .55`, divided by duration 4. This is synthetic data,
not a PX4 flight result. The output records a SHA-256 identity and scorer version.

Retain each run's result and report spread/failures across trials. An improvement in
this metric is not enough if a required regression task or hard constraint worsens.
Use [experiments](experiments.md) for comparison design and proposal rules.

## Source anchors

- [ULog format](https://docs.px4.io/v1.17/en/dev_log/ulog_file_format.html)
- [Versioned local-position schema and reset fields](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/msg/versioned/VehicleLocalPosition.msg)
