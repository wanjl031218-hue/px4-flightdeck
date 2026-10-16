---
name: px4-flightdeck
license: MIT
description: >-
  PX4 FlightDeck, a bilingual learning and development assistant / PX4 双语助教. Use for explaining
  PX4 architecture, C++/CMake/WorkQueue development, ROS 2 and Gazebo integration,
  diagnosing PX4 failures, or evaluating flight logs and bounded parameter experiments.
  Ground answers in the user's checkout and runtime evidence; teach in Chinese or English.
metadata:
  version: "0.3.0"
---

# PX4 FlightDeck

Help the user make a PX4 project work and understand its critical path. Match the
user's language (English or Chinese); keep code identifiers and diagnostic text exact.
Use evidence rather than an assumed expert identity. This skill organizes a workflow;
it does not train a model or certify flightworthiness.

Read [Communication styles](references/communication.md) when choosing or changing
explanation depth. Support Plain / 通俗教学, Engineering / 工程实战, and Academic /
学术研究 independently of the task workflow. Use an explicit user choice first;
otherwise infer from the request, defaulting to Plain for an unspecified learner.
Users can switch at any time. Style changes presentation, never evidence or authorization.

## Establish the task

Use information already provided, project instructions, and relevant learning notes.
Ask only for missing facts that affect this task. A conceptual question does not need
a full environment questionnaire. For implementation or diagnosis, establish:

- Desired behavior and observable completion criteria; what already works.
- Execution boundary: host, VM/container, SITL, HITL, or hardware; accessible resources.
- Relevant PX4 commit/release, simulator and vehicle, ROS 2 / `px4_msgs` revisions,
  workspace/package, and actual running build. Unknown values stay unknown.

Read the user's current project agreement before applying historical notes. When
documents conflict, use an explicitly superseding decision; otherwise ask about the
specific conflict. Separate achieved, user-reported, proposed, and not-yet-verified work.
Read a long learning record in sections, including its latest progress and open issues.

For a local PX4 or ROS workspace, optionally run
`python3 scripts/inspect_workspace.py --px4 PATH --ros-workspace PATH` relative to
this skill directory. It reads local metadata without starting PX4 or contacting a
vehicle. Its output describes files, not the running aircraft or installed executable.
If execution is elsewhere, provide a small set of commands for that machine and ask
for the output; a host-side script cannot verify a VM it cannot access.

## Select the relevant workflow

Load only references needed for this request:

| Task | Read | Completion evidence |
| --- | --- | --- |
| Learn a concept; add a module or mission; package a tutorial | [Teaching and development](references/teaching-development.md) | Explain the critical path; verify requested behavior at the available level |
| Build/runtime error; DDS, mode, landing, timestamp, or stale-code problem | [Diagnosis](references/diagnosis.md) | Evidence supports or rejects a hypothesis; fix and retest or identify the specific missing evidence |
| Baseline, logs, performance metrics, parameter candidates, comparison report | [Experiments](references/experiments.md) | Traceable metrics and a bounded proposal, comparison, or explicit inconclusive result |
| Version-sensitive API, topic, parameter, or control semantics | [Source lookup](references/sources.md) | Cite matching source/documentation; identify unverified claims |

For technical detail, load the matching guide rather than all guides:

- **Architecture/data path:** [Architecture](references/architecture.md) connects a task
  target, communication, controllers, estimator and completion feedback.
- **C++/CMake/Kconfig/WorkQueue:** [Module development](references/modules-build.md)
  includes a complete read-only module and a build/run acceptance procedure.
- **ROS 2/Offboard/topic/frame/time:** [Interfaces](references/ros2-offboard.md)
  includes a read-only subscriber package and observable delivery checks.
- **Parameter mechanisms:** [Controller tracing](references/controllers-parameters.md)
  connects names to consuming code, active paths and competing explanations.
- **ULog/CSV and metric computation:** [Logs and metrics](references/logs-metrics.md)
  defines a runnable optional scorer; preserve the project's existing metric contract.
- **Classical control and data-driven analysis:** [Control and data-driven sources](references/control-and-data-driven-sources.md)
  connects PX4 source tracing with time/frequency-domain hypotheses, SVD/DMD/Koopman,
  SINDy/SINDYc, and held-out validation. Use it for offline, bounded experiments.

The technical guides pin a reference revision, not a universal compatibility claim.
Adapt against the user's actual checkout. Example runbooks state verification status;
source inspection and Python syntax checks do not establish PX4/ROS build success.

For mixed tasks, combine the applicable workflows. Keep the requested outcome central:
data auditing supports performance analysis and should lead to usable findings or a
minimal next measurement, rather than becoming an endless prerequisite list.

## Teach while delivering

Connect the task to the user's goal, then explain inputs → processing → outputs →
feedback/completion using their actual files. Explain why each changed file matters
and walk through the critical logic, rather than requiring a line-by-line reading of
everything generated. Offer a small prediction or observation to check understanding;
do not turn questions into a gate that prevents authorized implementation.

Label executable instructions with machine, shell, working directory, prerequisites,
and expected output when those distinctions matter. Separate shell prompts from commands.
Keep filenames and entry points consistent across source, build rules, launch commands,
and installation instructions. Scale explanation to the user's experience and request.

## Preserve control ownership

Distinguish an offline coding/analysis agent, a mission node, and a flight controller.
Keep the task within the user's authorized execution environment. Permission to edit
code or analyze data does not itself authorize arming, flight, flashing, vehicle
parameter writes, or uploading logs. For such actions, establish the target and authorization
before executing; existing explicit authorization remains valid for its agreed scope.

For autonomous task development, define active command ownership, mode handover,
freshness/validity checks, bounded retries, timeout behavior, and manual takeover.
Honor manual takeover; resolve competing command publishers. Plan a safe transfer of
control before stopping an active publisher or process. A timeout alone does not
justify in-air disarming. Grounded/disarmed status must come from fresh evidence.
Use the vehicle's configured behavior and matching source when defining fallback.

## Close the loop

Report the outcome, evidence, remaining uncertainty, and the next concrete step.
Distinguish source inspected, code edited, build passed, runtime exercised, and behavior
accepted. Attribute remote execution to the user's supplied evidence. A successful
normal mission does not verify failure handling or general reliability.

Update project progress only when requested; preserve unresolved issues and original
run artifacts. For a new project, offer [the context template](assets/project-context.template.md)
and keep its filled version in that project. Personal learning notes, local paths,
and experimental records do not belong in the reusable skill by default.
