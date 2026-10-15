# Read-only ROS 2 observer / 只读订阅示例

Complete `ament_python` package; requires ROS 2, `rclpy`, a built/sourced `px4_msgs`
and an existing PX4 DDS connection. Python syntax checked locally; ROS build and
runtime acceptance have **not** run. Reference schemas are linked in
[the interface guide](../../../references/ros2-offboard.md).

中文：先验证状态消息真的收到，再考虑主动任务。本包不创建 publisher，不解锁、不切模式、
不写参数。它报告主机收包间隔和 PX4 时间戳，两者的差值不代表延迟。

## Install and observe

Use the Linux VM where ROS 2 and PX4 DDS run. Replace the first two paths with real
locations. Copy this entire directory to the chosen workspace's `src` directory.
Do not overwrite an existing package without reviewing it.

```bash
export FLIGHTDECK_REPO=/path/to/px4-flightdeck
export FLIGHTDECK_ROS_WS=/path/to/ros_workspace
test ! -e "$FLIGHTDECK_ROS_WS/src/flightdeck_ros_observer" && \
  cp -R "$FLIGHTDECK_REPO/skills/px4-flightdeck/assets/examples/ros2-observer" \
    "$FLIGHTDECK_ROS_WS/src/flightdeck_ros_observer"
cd "$FLIGHTDECK_ROS_WS"
# Source your actual ROS underlay and the overlay providing px4_msgs first.
colcon build --packages-select flightdeck_ros_observer
source install/setup.bash
ros2 pkg prefix flightdeck_ros_observer
ros2 topic list -t
```

Select the exact `px4_msgs/msg/VehicleLocalPosition` topic shown in the list, then:

```bash
export FLIGHTDECK_POSITION_TOPIC=/fmu/out/vehicle_local_position_v1
ros2 topic info -v "$FLIGHTDECK_POSITION_TOPIC"
ros2 run flightdeck_ros_observer observe_position \
  --topic "$FLIGHTDECK_POSITION_TOPIC" --duration 15
```

The `_v1` topic is an **example** for message version 1, not a universal name. If your
runtime lists another name/namespace, use that instead. The package does not auto-
launch PX4 or a DDS Agent; use the actual project's established launch procedure.

## Acceptance and cleanup / 验收与清理

Expect increasing `samples` and `advances`, zero timestamp regressions, recent receipt,
valid position samples, and displayed NED coordinates/reset counters. Exit 0 means
those limited delivery checks passed; exit 2 means they did not; interrupt is 130.
It does not prove that every sample was valid, that resets never occurred, that a
vehicle is safe to fly, or that data was newly acquired at the sensor.

If no samples arrive, preserve `topic info -v`, schema and selected package prefix.
Check matching publisher, message version/translation, reliability and DDS domain.
Do not change control parameters to fix a missing subscription.

The process ends after the stated host duration, including while simulation time is
paused. Stopping this read-only observer does not withdraw a flight-control publisher.
Keep build and runtime evidence with the tested revision. To undo the source addition,
remove only this copied package after stopping the observer; do not delete the whole
workspace or shared install tree.
