# Version-aware source lookup

Use the user's checked-out source and observed runtime for claims about that project.
For intended semantics, prefer official documentation matching that release. Resolve
disagreements among current code, runtime, and docs explicitly. `main` is a moving
reference, not an assertion about the user's stable release.

For version-sensitive claims, retain repository/release/commit, file and symbol or
documentation section. Public reports should use commit-pinned links when possible.
Local source citations should point to files and lines the assistant actually read.
If sources cannot be fetched, say which behavior remains unverified and request or
inspect matching local material; do not silently promote recalled details to facts.

## Bundled technical guides

The [reference snapshot](upstream-snapshot.json) records revisions, retrieval date and
SHA-256 hashes for inspected upstream files. Guides summarize mechanisms in our own
words and link to pinned source. They are not a vendored PX4 manual or a runtime
compatibility matrix. Full document snapshots remain outside the release package.

| Question | Read on demand |
| --- | --- |
| Task-to-controller signal path | [Architecture](architecture.md) |
| Module/build/lifecycle | [Modules and WorkQueue](modules-build.md) |
| Topics, QoS, frames, time, Offboard | [ROS 2 interfaces](ros2-offboard.md) |
| Controller gains/limits and parameter consumers | [Controller tracing](controllers-parameters.md) |
| Log windows and reproducible scoring | [Logs and metrics](logs-metrics.md) |

## Live lookup map

These are starting points, not a frozen compatibility matrix:

| Question | Authoritative entry point |
| --- | --- |
| Build targets and toolchain | [Building PX4](https://docs.px4.io/main/en/dev_setup/building_px4.html), local build configuration |
| Module structure and lifecycle | [Module template](https://docs.px4.io/main/en/modules/module_template.html), adjacent local examples |
| uORB schema and subscriptions | [uORB](https://docs.px4.io/main/en/middleware/uorb.html), local `msg/` and publisher/subscriber source |
| ROS 2 compatibility, frames, DDS, QoS | [ROS 2 user guide](https://docs.px4.io/main/en/ros2/user_guide.html), local `px4_msgs`, PX4 DDS configuration |
| Offboard liveness, modes, loss behavior | [Offboard mode](https://docs.px4.io/main/en/flight_modes/offboard.html), branch-specific mode/failsafe implementation |
| Parameter definitions and controller effects | [Parameter reference](https://docs.px4.io/main/en/advanced_config/parameter_reference.html), local definitions and their consumers |
| ULog format and available measurements | [ULog format](https://docs.px4.io/main/en/dev_log/ulog_file_format.html), actual logged message schemas |
| Exact PX4 code | [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) at the user's commit |
| ROS 2 message definitions | [px4_msgs](https://github.com/PX4/px4_msgs) at the installed revision |
| Skill structure and Codex discovery | [OpenAI skills documentation](https://developers.openai.com/codex/skills/) |

Select the correct release in the documentation site. Search the actual tree rather
than assuming an example is under `src/modules` or `src/examples`, a message uses a
particular suffix, or a controller lives at a remembered path. A source tree may include
different message generations or a translation mechanism; establish the interface in
use rather than requiring identical branch names by habit.

## Retrieved reference versus verified behavior

A fetched document establishes what it states. Inspecting source establishes what is
implemented at that revision. Compiling establishes build success. Only an appropriate
run with observable acceptance establishes the tested behavior in its stated conditions.
Preserve these distinctions in teaching, diagnosis, and reports.
