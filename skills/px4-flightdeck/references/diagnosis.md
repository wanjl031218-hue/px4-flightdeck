# Diagnosis

## Follow the evidence

Capture the exact symptom, current run/build, expected behavior, and relevant interval.
Read supplied logs first. Separate observations, hypotheses, and discriminating tests.
Choose a small test that distinguishes likely causes before changing code or parameters.
When a fix is justified, make a bounded change and repeat the failing path. If execution
is unavailable, state the missing measurement rather than claim a reproduced fix.

Prefer a specific chain, such as “the installed binary predates this source change,”
over “PX4 is unstable.” Independent symptoms may have independent causes.

## Source, build, installed artifact, running process

When edits appear ineffective or a command is missing, compare:

1. Intended source and commit/dirty state.
2. Selected build target/package, actual compiler output, and build timestamps.
3. Installed path or ROS package prefix, overlay order, and build identity/hash.
4. Process launched from that artifact and its startup/version output.

`Summary: finished` is not evidence that C++ was recompiled. Sourcing an overlay loads
environment variables; it does not install new code. Old terminal output is not evidence
from the latest run. `strings` may reveal an existing build marker but is not a general
proof of binary provenance; use the project's actual version mechanism where available.

For `Clock skew detected`, distinguish filesystem modification times and VM/host clock
from PX4 boot time, ROS time, and sensor timestamps. A scoped clean rebuild can replace
a stale binary without fixing the cause of a clock discrepancy. Diagnose both separately.
For C++ syntax errors, inspect matching declarations/definitions and accidental pasted
Markdown fences before rewriting the module. Verify Kconfig/board inclusion and the
current CMake `MAIN` command for `Invalid command`.

## ROS 2 and transport

Discover actual topics/types and package revisions before constructing subscriptions.
Check PX4 DDS export configuration, `px4_msgs` schemas, message versions/translation,
namespace/vehicle instance, QoS compatibility, and competing workspace overlays.
A suffix such as `_v1` is interface/version dependent, not a universal topic name.

Publisher/subscriber counts prove discovery of endpoints, not current message delivery.
Check bounded message-rate and sample reads; include compatible QoS when required by
the actual publisher. Then check payload validity, timestamp units, freshness, and
estimator reset counters. A fresh receipt of a repeated stale payload may still be stale.
Attribute a payload timestamp to its known clock; do not subtract incomparable clocks.

For an inaccessible VM, give commands for that VM. The absence of `ros2` on the host
does not mean ROS 2 is missing from the VM.

## Control ownership, landing, and manual takeover

Align mode, command acknowledgments, outgoing targets, velocity/thrust, land detection,
and arming state from the same run and nearby timestamps. Trace who is publishing each
target and when. A position target continuing during automatic landing is a hypothesis
about command ownership to inspect against source and mode behavior, not a diagnosis
inferred from an unrelated old case.

Define a deliberate transition to the landing controller and which streams should
continue or stop. Verify mode acceptance and fresh feedback. Stopping an Offboard
heartbeat can trigger a configured failsafe: choose a handover using matching source
and configuration rather than treating “stop all publishing” as universally safe.

When evidence shows pilot takeover, release autonomous command ownership and report the
reason; do not repeatedly request Offboard to defeat it. Keep takeover intervals out of
claims about autonomous control performance, while retaining them as experiment outcomes.

Land mode is not `landed`; near-zero local z is not landing proof. Inspect actual landing
signals and their validity before normal disarm behavior. Preserve the distinction
between setpoint descent and measured descent when explaining a land detector condition.

## Sensor and timing anomalies

For acceleration/gyro timeouts or estimator resets, inspect sensor instances, selected
sensor, publication rate, timestamp monotonicity, simulation real-time factor, resource
pressure, and clock synchronization as relevant. Separate a startup transient from an
event in the evaluation window. An anomaly-free video does not establish healthy data;
a warning by itself does not establish the cause of a control failure.

Resist hiding a sensor, arming, or time problem with unrelated controller gains or
relaxed failsafe thresholds. Explain which evidence would support each competing cause
and what remains unresolved after a workaround.
