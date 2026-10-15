"""Observe only: no publishers, commands, arming, mode changes or parameter writes."""

import argparse
import math
import time

import rclpy
from rclpy.clock import Clock, ClockType
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from px4_msgs.msg import VehicleLocalPosition


class PositionObserver(Node):
    def __init__(self, topic, stale_after):
        super().__init__("flightdeck_position_observer")
        self.samples = 0
        self.valid_samples = 0
        self.timestamp_advances = 0
        self.timestamp_regressions = 0
        self.last_received = None
        self.last = None
        self.stale_after = stale_after
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         durability=DurabilityPolicy.VOLATILE,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.subscription = self.create_subscription(VehicleLocalPosition, topic, self.receive, qos)
        self.timer = self.create_timer(1.0, self.report, clock=Clock(clock_type=ClockType.STEADY_TIME))
        self.get_logger().info("Read-only; topic=" + topic + "; type=px4_msgs/msg/VehicleLocalPosition")

    def receive(self, message):
        if self.last is not None:
            self.timestamp_advances += int(message.timestamp > self.last.timestamp)
            self.timestamp_regressions += int(message.timestamp < self.last.timestamp)
        self.samples += 1
        self.valid_samples += int(message.xy_valid and message.z_valid
                                  and all(math.isfinite(v) for v in (message.x, message.y, message.z)))
        self.last_received = time.monotonic()
        self.last = message

    def report(self):
        if self.last is None:
            self.get_logger().warning("samples=0; inspect exact topic/type, QoS and DDS endpoints")
            return
        m = self.last
        age = time.monotonic() - self.last_received
        self.get_logger().info(
            f"samples={self.samples} rx_age_s={age:.3f} rx_recent={age <= self.stale_after} "
            f"px4_timestamp_us={m.timestamp} advances={self.timestamp_advances} "
            f"regressions={self.timestamp_regressions} xy_valid={m.xy_valid} z_valid={m.z_valid} "
            f"NED_m=({m.x:.3f},{m.y:.3f},{m.z:.3f}) "
            f"reset_xy={m.xy_reset_counter} reset_z={m.z_reset_counter}")

    def delivery_observed(self):
        return (self.timestamp_advances > 0 and self.timestamp_regressions == 0
                and self.valid_samples > 0 and self.last_received is not None
                and time.monotonic() - self.last_received <= self.stale_after)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Exact discovered VehicleLocalPosition topic")
    parser.add_argument("--duration", type=float, default=15.0, help="Host steady-clock seconds")
    parser.add_argument("--stale-after", type=float, default=1.0, help="Receipt-age threshold, not a flight limit")
    args, ros_args = parser.parse_known_args(argv)
    if (not math.isfinite(args.duration) or args.duration <= 0
            or not math.isfinite(args.stale_after) or args.stale_after <= 0):
        parser.error("duration and stale-after must be finite and > 0")
    rclpy.init(args=ros_args)
    node = None
    result = 2
    try:
        node = PositionObserver(args.topic, args.stale_after)
        deadline = time.monotonic() + args.duration
        while rclpy.ok() and time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.2)
        node.report()
        result = 0 if node.delivery_observed() else 2
    except KeyboardInterrupt:
        result = 130
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    return result
