# Teaching and development

## Make the system legible

For learning tasks, begin with the smallest explanation that supports the current
decision. Connect a concept to an observable signal or a short relevant code path.
If the user wants complete files, supply coordinated files plus build, run, and
acceptance instructions; explain the important decisions alongside the deliverable.

In a typical ROS 2 + PX4 + Gazebo setup, distinguish:

| Component | Responsibility | Evidence to inspect |
| --- | --- | --- |
| Mission node | Targets, task state machine, completion and timeout logic | Node code, parameters, state transitions |
| Micro XRCE-DDS Agent and PX4 client | ROS 2 / PX4 message transport | Client status, topics/types, QoS, traffic |
| PX4 | Estimation, mode management, controllers, actuator commands | Versioned source, status, setpoints, ULog |
| Gazebo | Simulated dynamics, sensors, optionally simulation clock | World/model, sensor timestamps, real-time factor |
| QGroundControl | Monitoring and another potential command source | Mode/arming state, joystick activity, MAVLink |

This is one architecture, not a prerequisite for all PX4 projects. Distinguish
MAVLink, DDS/uXRCE-DDS, uORB, and the simulator bridge. The DDS Agent is not a
planner; a ROS node publishing a PX4 setpoint is not directly moving Gazebo.

## Build and deploy an internally consistent change

1. Inspect a nearby implementation in the same checkout. Locate the actual target,
   module/package registration, dependencies, source files, and startup mechanism.
2. Explain the change through its input, output, scheduling, state, and stop behavior.
3. Modify the minimum coordinated set of files, preserving established working code.
4. Build the relevant target/package. Resolve the first current compiler error before
   diagnosing cascaded errors. Scope cache cleaning to an evidenced stale artifact.
5. Identify the installed executable and launch path. Compare available build identity
   with source and runtime startup output. Reloading `setup.bash` does not compile C++.
6. Verify behavior using logs/state/measurements at the requested level, then report
   what was actually tested and what remains untested.

For a PX4 module, inspect `CMakeLists.txt` registration and its `MAIN` entry,
`Kconfig`, target/board enablement, declarations, definitions, and module lifecycle.
A declared Kconfig option is not an enabled build option. Derive the actual module
command from the current checkout rather than an old tutorial's name.

For `ScheduledWorkItem`, follow the branch's lifecycle and cleanup pattern. Scheduled
callbacks share queue execution; use bounded work and return instead of blocking a
queue with an unbounded loop. Verify subscription validity/update handling and stop
cleanup. A read-only first module is useful when the user's goal is lifecycle learning;
it is not a universal prerequisite for an experienced developer.

For ROS 2 packages, align `package.xml`, CMake target/install rules, executable name,
configuration installation, and underlay/overlay order. Use the installed package share
directory for packaged configs. A source-relative path may work locally but fail after
distribution. Check actual workspace selection before deleting or rebuilding artifacts.

## Commands a learner can execute

Label blocks by location, for example:

- Ubuntu VM / regular shell / PX4 checkout: build and run simulator.
- Ubuntu VM / regular shell / ROS workspace: build and source an overlay.
- PX4 shell (`pxh>`): PX4 module/status commands; omit the prompt in copied text.
- Host: edit, package, inspect exported experiment files.

For a multi-process tutorial, give a short terminal map with each process's purpose,
readiness signal, shutdown effect, and whether it sends commands. One vehicle should
have one intended active command owner; multi-vehicle projects need explicit namespaces
and ownership per vehicle, not a global ban on multiple processes.

Mark launch commands that immediately begin an autonomous task. If preparing a runbook,
explain their effects before the command. During an active run, use the agreed control
handover rather than recommending arbitrary `Ctrl+C` or broad process-kill commands.

## Teach feedback rather than appearances

For a mission, show states, transition guards, commands and acknowledgments, fresh
state feedback, acceptance dwell time, abort/release paths, and final idle behavior.
Waiting five seconds before printing `GO_TO_B` proves a timer/state sequence; it does
not prove arrival at A, stable hover, or movement to B.

Record coordinate frame, units, origin, and time domain. In a PX4 local-NED interface,
positive z is down; a height above a captured reference is a negative z offset.
Check the actual message definition before applying this convention to another
interface. ROS conventions alone do not transform the payload. A captured `home`
offset does not reset the estimator origin; `z == 0` need not mean ground.

Distinguish armed vs airborne, requested mode vs accepted mode, Land mode vs detected
landing, commanded motion vs measured motion, and task IDLE vs a spatial destination.
Treat estimator resets as possible reference discontinuities, not ordinary tracking
error; determine how the task and evaluator handle the reset.

Use one task-linked understanding check when helpful: “Which signal proves arrival?”
or “If the simulator pauses, which timer should stop?” Explain the observation after
the user predicts it. Respect a request for a concise fix or deeper source walkthrough.

## Portable delivery

Include complete changed files or an unambiguous patch, exact destinations, dependencies,
build/run instructions, configuration, acceptance and rollback. Archive relative to a
known top-level directory and inspect its contents; avoid duplicated nested package
directories and compiled files from another architecture. Preserve artifact identity
across source → archive → installed binary → startup output. Run external commands
only where the assistant actually has access; provide instructions otherwise.
