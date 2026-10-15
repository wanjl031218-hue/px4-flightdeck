# Controllers and parameters / 控制链与参数追踪

Use when explaining parameter mechanisms or evaluating bounded tuning proposals.
Reference: PX4 v1.17.0 `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`.
These are source-backed search anchors, not a parameter allowlist or recommended values.

## Read the consuming code / 读参数实际用在哪里

In the reference `PositionControl.cpp`, `_positionControl()` forms a velocity
contribution from position error and position P gains, adds available velocity
feedforward, then constrains velocity. `_velocityControl(dt)` uses velocity error,
an integral term and a measured-velocity derivative term to form acceleration, adds
acceleration feedforward and handles thrust limits/anti-windup.

中文：位置误差大，可能来自目标生成、速度限制、估计误差，也可能来自控制增益。
“回调慢”是一种现象；先定义扰动结束时刻、误差容差与保持时间，才能比较恢复速度。

| Parameter/search family | Source-backed mechanism | What to examine before attributing performance |
| --- | --- | --- |
| `MPC_XY_P`, `MPC_Z_P` | Position-error to velocity contribution | Position/velocity targets, measured response, limits and valid state |
| `MPC_XY_VEL_P_ACC`, `MPC_Z_VEL_P_ACC` and I/D counterparts | Velocity-loop acceleration gains | Velocity error, acceleration/thrust response, noise and saturation |
| `MPC_XY_VEL_MAX`, `MPC_Z_VEL_MAX_UP/DN` | Limits used in position control | Whether limits are reached; direction and flight mode |
| `MPC_XY_CRUISE`, `MPC_JERK_AUTO` | Read by trajectory/goto generation paths | Whether that generator is active for this task; externally generated targets can differ |
| `MPC_THR_HOVER`, `MPC_USE_HTE` | Hover-thrust initialization/estimation selection | Actual estimator use, current values, thrust constraints |

The wiring is visible in `MulticopterPositionControl::parameters_update` and its
calls to `setPositionGains`, `setVelocityGains` and `_goto_control` setters.
Some parameters can also be constrained or derived by higher-level settings; inspect
the whole update function and runtime readback after applying a candidate.

## Reproduce a parameter trace

PX4 checkout / regular OS shell:

```bash
rg -n 'MPC_XY_P|MPC_XY_VEL_P_ACC|MPC_XY_VEL_MAX|MPC_USE_HTE' src/modules/mc_pos_control
rg -n 'setPositionGains|setVelocityGains|parameters_update|_param_mpc_xy_p|_param_mpc_use_hte' src/modules/mc_pos_control
rg -n '_positionControl|_velocityControl|_lim_vel_horizontal|_hover_thrust' src/modules/mc_pos_control/PositionControl
```

Find definition, metadata (unit/range), binding, consuming function and any dependent
overrides. In the actual PX4 shell, read current values, for example:

```text
param show MPC_XY_P
param show MPC_XY_VEL_P_ACC
param show MPC_USE_HTE
```

These are reads, not writes. Preserve an actual parameter snapshot before proposing
numeric current → candidate → rollback values. Defaults in source do not establish
the current vehicle configuration.

## Select by scenario evidence

- Hover disturbance recovery: evaluate declared recovery time plus peak deviation,
  residual error and oscillation; inspect velocity/thrust response before choosing gains.
- Waypoint tracking: separate target-generation limits from tracking error; improving
  flight time by changing the mission is a different intervention from tuning PX4.
- Altitude changes: use the NED direction correctly and distinguish ascent/descent
  limits, landing behavior and estimator resets.

These are example analyses. Use the user's actual three tasks and metric definitions.
Position logs alone cannot prove which inner-loop mechanism caused an improvement.
For experimental controls, failures, change budgets and held-out retests, read
[experiments](experiments.md); for executable metric definitions read
[logs and metrics](logs-metrics.md).

## Source anchors

- [Parameter-to-controller wiring and constraints](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/mc_pos_control/MulticopterPositionControl.cpp)
- [Position and velocity controller](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/mc_pos_control/PositionControl/PositionControl.cpp)
- [Hover-thrust parameter definitions](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/mc_pos_control/multicopter_position_control_params.c)
