# ROS 2 and Offboard / 接口、坐标和控制权

Use for no-data subscriptions, setpoint interfaces, coordinate questions or handover.
Source reference: PX4 v1.17.0 `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`.
The inspected `px4_msgs` release/1.17 snapshot is
`86d8239e962f6939e05c3737784f60c02fa884db`; this is not a claim of full-stack compatibility.

## Establish the interface before writing code

1. Inspect PX4's DDS map and actual schema. Versioned messages may use `_vN` topics;
   discover the runtime name rather than appending a suffix to every message.
2. Inspect the ROS package actually selected by the sourced environment, its schema,
   and the endpoint type. Compatible branch names alone do not prove schema equality.
3. Check publisher and subscriber QoS. A reliable subscriber may not match a
   best-effort publisher. The bundled observer requests best-effort, volatile,
   keep-last depth 5, following the sensor-data subscription pattern. Read endpoint
   evidence before changing durability or blaming a network interface.
4. Prove callbacks receive changing samples; discovery alone is insufficient.

Ubuntu/ROS shell after sourcing the intended underlay and overlay:

```bash
ros2 pkg prefix px4_msgs
ros2 topic list -t
ros2 interface show px4_msgs/msg/VehicleLocalPosition
```

Then run `ros2 topic info -v` with the exact topic discovered above. Inspect count,
type, reliability and durability. If using a message translation node, identify both
sides and its matching configuration. Do not assume incompatible schemas can connect
without translation just because the ROS type names are the same.

Try the [read-only ROS observer](../assets/examples/ros2-observer/README.md) before
debugging an active mission when receiving state is the unresolved question.

## Coordinates / 坐标

At the pinned PX4 revision, `VehicleLocalPosition` describes local NED: x north,
y east, z down. For a reference captured at `z_ref = 0.2 m`, a target 2 m above it
is `z_target = 0.2 - 2 = -1.8 m`. That is relative to the captured reference;
ground clearance requires separate information.

For vectors, ENU → NED maps `(x, y, z)` to `(y, x, -z)`. Body FLU → FRD maps
`(x, y, z)` to `(x, -y, -z)`. Attitude/quaternion conversion must handle world and
body bases together using a tested transform; component negation copied from a
position-vector example is not an attitude conversion.

`TrajectorySetpoint` defines NaN as an uncontrolled state component. Zero is a
numeric target or feedforward value. Inspect valid combinations and the selected
control level; a zero-filled message is not a universal “hold” command.

## Clocks and validity / 时间与有效性

Keep three measurements separate: PX4 boot-relative message timestamp in microseconds,
ROS/simulation clock, and host steady-clock time since callback receipt. A host wall
timestamp minus a PX4 boot timestamp has no physical meaning without clock alignment.
Recent arrival alone does not prove recent sensor acquisition: replayed or stale
timestamped samples can still arrive. Check timestamp progression, validity flags,
reset counters and estimator state according to the task.

The bundled observer reports host receipt age and PX4 timestamp separately. It does
not label their difference as transport latency or prove synchronization.

## Offboard is a contract / 模式是持续满足的条件

For ROS 2, distinguish the `OffboardControlMode` liveness/control-level message from
the trajectory target. At the reference source, `OffboardChecks::checkAndReport`
checks freshness using `COM_OF_LOSS_T`, selected control flags and required estimator
validity. Read mode-entry requirements and configured loss actions as well; that one
function does not describe the entire mode/failsafe state machine.

For an active task, verify separately: command sent → acknowledgment/result → actual
mode/state → target tracking → completion. A command acknowledgment is not arrival.
Plan landing/mode handover using observed state and the configured controller behavior.
After manual takeover, the task must relinquish command ownership as agreed.

## Source anchors

- [ROS 2 guide snapshot: QoS, frames and message compatibility](https://github.com/PX4/PX4-user_guide/blob/2fa62338099f18fc3092197e856615eca94d2975/en/ros2/user_guide.md)
- [PX4 VehicleLocalPosition](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/msg/versioned/VehicleLocalPosition.msg)
- [ROS VehicleLocalPosition](https://github.com/PX4/px4_msgs/blob/86d8239e962f6939e05c3737784f60c02fa884db/msg/VehicleLocalPosition.msg)
- [TrajectorySetpoint](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/msg/versioned/TrajectorySetpoint.msg)
- [OffboardControlMode](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/msg/OffboardControlMode.msg)
- [Offboard availability checks](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/commander/HealthAndArmingChecks/checks/offboardCheck.cpp)
