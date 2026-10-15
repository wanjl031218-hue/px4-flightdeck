# PX4 architecture / 架构与数据流

Use for tracing a target to feedback or deciding which component to change.
Reference: PX4 v1.17.0, commit `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`.
Source-inspected on 2026-10-15; no simulator acceptance is implied.

## Follow one signal / 沿一个信号追踪

For a ROS 2 position task using the standard uXRCE-DDS integration:

```text
mission node: target + completion logic
  → ROS 2 TrajectorySetpoint / OffboardControlMode
  → DDS Agent ↔ PX4 uXRCE-DDS client
  → uORB setpoints + mode/validity checks
  → multicopter position/velocity control
  → attitude/rate control → control allocation → actuator output
  → simulator dynamics/sensors → estimator → vehicle_local_position
  → DDS → mission node: fresh feedback + arrival guard
```

This is a conceptual path, not a promise that every mode traverses every stage.
Offboard position, velocity, attitude, and actuator interfaces enter at different
levels. Locate the active path from the selected message fields and control flags.

中文：任务节点决定“去哪、何时算完成”，控制器根据状态误差决定“怎样跟踪”。
修改任务轨迹、修改 PX4 参数、修改仿真模型是三种不同的实验干预。

## Find the actual implementation

Run in the PX4 checkout, regular OS shell:

```bash
git describe --tags --always --dirty
git rev-parse HEAD
rg --files msg src/modules | rg 'TrajectorySetpoint|OffboardControlMode|VehicleLocalPosition|mc_pos_control|uxrce_dds'
rg -n 'trajectory_setpoint|offboard_control_mode|vehicle_local_position' src/modules/uxrce_dds_client/dds_topics.yaml
rg -n 'setInputSetpoint|setPositionGains|setVelocityGains|_positionControl|_velocityControl' src/modules/mc_pos_control
```

Expected evidence: a revision, actual message files, exported DDS directions, and
symbols linking setpoints to the controller. Search results identify places to read;
read the surrounding function and conditions before explaining behavior.

At the reference commit, two schemas are under `msg/versioned/`, while
`OffboardControlMode.msg` remains under `msg/`. A remembered flat `msg/` path can fail.
`dds_topics.yaml` lists base names; inspect versioned runtime topic names separately.

## Distinguish the buses / 区分通信层

| Interface | Role | Evidence |
| --- | --- | --- |
| uORB | PX4 internal publish/subscribe | `.msg`, subscriptions/publications, `listener` |
| uXRCE-DDS / ROS 2 | Export/import configured messages | DDS map, agent/client status, endpoint QoS, received samples |
| MAVLink | Telemetry, commands, supported setpoint interfaces | Stream/command code, acknowledgments, vehicle state |
| Simulator bridge | Dynamics/sensors and simulated vehicle outputs | Actual simulator setup, timestamps, sensor and actuator traffic |

QGroundControl and a ROS task can both influence mode/commands. Draw the current
command owner and handover explicitly. Seeing a target in ROS proves publication;
it does not prove PX4 accepted it or that the vehicle reached it.

## Source anchors

- [DDS export/import map](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/uxrce_dds_client/dds_topics.yaml)
- [MulticopterPositionControl.cpp](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/mc_pos_control/MulticopterPositionControl.cpp)
- [PositionControl.cpp](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/mc_pos_control/PositionControl/PositionControl.cpp)

See [ROS 2 interfaces](ros2-offboard.md) for topic/type/frame checks and
[controller tracing](controllers-parameters.md) for parameter hypotheses.
