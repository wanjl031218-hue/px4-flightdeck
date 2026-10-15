# PX4 FlightDeck

**Learn, build, and debug PX4 with an AI assistant that checks the evidence.**

[English](README.md) · [简体中文](README.zh-CN.md) · [Skill](skills/px4-flightdeck/SKILL.md) · [Technical guides](skills/px4-flightdeck/references/sources.md) · [Validation](evals/results.md) · [License notices](THIRD_PARTY_NOTICES.md)

The default branch, `codex/en`, opens this English homepage. For a Chinese homepage,
select `codex/zh-CN` in GitHub's branch selector. Both branches include the bilingual
skill and the same tools; see [language branches](docs/LANGUAGES.md).

Turn “generate some code” into a project you can run, explain, and evaluate.
PX4 FlightDeck is a bilingual agent skill for PX4 learners and developers: teaching,
C++/CMake/WorkQueue development, ROS 2 + Gazebo integration, diagnosis, and bounded
parameter experiments. It reads your actual version and project context rather than
assuming every tutorial matches your installation.

**Three explanation styles. One standard of evidence.**

| Style | Ask for | What you receive |
| --- | --- | --- |
| Plain | “Explain simply” / “通俗教学” | Concrete behavior, defined terms, critical code path, something to observe |
| Engineering | “Engineering style” / “工程实战” | Diagnosis or change, exact execution context, expected output, verification and rollback |
| Academic | “Academic style” / “学术研究” | Assumptions, mechanisms, metric definitions, evidence, uncertainty and limitations |

Use English or Chinese, and switch styles naturally at any time. Answers are in the
requested language; code identifiers and diagnostic messages remain exact.

## What makes it useful

- **Teach while delivering:** connect inputs, logic, outputs, and completion criteria
  to the code you're actually using.
- **Check the artifact you're running:** distinguish source, compiled target,
  installed executable, and process identity.
- **Explain the stack:** separate mission logic, DDS transport, PX4 control,
  simulator physics, and ground-station commands.
- **Investigate before tuning:** distinguish control behavior from stale code,
  clock problems, estimator resets, communication, and mode/ownership problems.
- **Make experiments traceable:** deterministic metrics, declared windows, retained
  failures, parameter snapshots, regression tasks, and held-out validation.

This packages instructions, technical references, read-only examples and analysis helpers. It does not
fine-tune a model, replace PX4, or execute flights by installation. Your agent client
provides the model and tools; no extra API key, cloud service, or PX4 installation is
required merely to load the skill. Actual builds and simulations need their own environment.

## What's included

| Resource | Start here |
| --- | --- |
| Task → interface → controller → feedback | [Architecture guide](skills/px4-flightdeck/references/architecture.md) |
| C++ / CMake / Kconfig / WorkQueue | [Module guide](skills/px4-flightdeck/references/modules-build.md) and [complete example](skills/px4-flightdeck/assets/examples/px4-module/README.md) |
| ROS 2 / DDS / Offboard / frames / clocks | [Interface guide](skills/px4-flightdeck/references/ros2-offboard.md) and [read-only subscriber](skills/px4-flightdeck/assets/examples/ros2-observer/README.md) |
| Parameter definitions → consuming controller | [Controller guide](skills/px4-flightdeck/references/controllers-parameters.md) |
| Log alignment, RMSE, overshoot, settling | [Metric definitions and runnable scorer](skills/px4-flightdeck/references/logs-metrics.md) |

Technical source anchors use PX4 **v1.17.0** at a pinned commit, with a recorded
`px4_msgs` snapshot and source hashes. This is a reference for adaptation, not a
tested compatibility promise. Guides use English with Chinese explanations of key
pitfalls; the assistant teaches in the language you request. Read-only PX4/ROS
examples include build/run/acceptance procedures but have **not** passed PX4/ROS
compilation or SITL acceptance in this release.

## Install in a minute

On GitHub, clone this repository or use **Code → Download ZIP** and extract it.
For a tagged release, choose the full source ZIP, enter its `px4-flightdeck` folder,
and run the command below. Loading the skill alone needs no ROS/PX4 installation.

From a cloned or downloaded copy of this repository, with Python 3.9 or newer:

```bash
python3 scripts/install.py
```

This copies the skill and license into `~/.agents/skills/px4-flightdeck`, a user-level
Codex discovery location documented by [OpenAI](https://developers.openai.com/codex/skills/).
For a client configured to use another skill directory, select it explicitly:

```bash
python3 scripts/install.py --skills-dir ~/.codex/skills
```

For authoring, add `--link` to keep edits in this checkout immediately available.
The installer uses local files only and refuses to overwrite by default. To install
an updated checkout into the **same discovery directory**, use:

```bash
python3 scripts/install.py --update
```

This preserves the previous folder or symlink in `flightdeck-backups` beside the
discovery directory, prints its path, then installs the new version. A failed copy
restores the old installation. If you installed with `--skills-dir`, pass that same
option on update. A `--link` installation follows edits in its checkout automatically.

Alternatively, extract the release's **standalone skill ZIP** into your configured
skill directory. The resulting layout must be `skills/px4-flightdeck/SKILL.md`, not
an extra nested `px4-flightdeck/px4-flightdeck` directory. Both archives retain licenses.
If the skill does not appear, restart the client. Other agent clients may accept the
same `SKILL.md` folder; follow their discovery rules. Their behavior has not been tested.

## Try it

```text
Use $px4-flightdeck in plain style. Help me understand how my ROS 2 mission
node sends a target to PX4 and knows the vehicle has arrived. Start from my files.
```

```text
Use $px4-flightdeck in engineering style. My source says build r8, but the
running node prints r5. Inspect the build/deployment chain before changing mission logic.
```

```text
Use $px4-flightdeck in academic style. Review my baseline and propose a
PX4-parameter-only comparison. Separate data-quality limits from control hypotheses.
```

Give it your actual task and relevant files. It should reuse known context and ask for
facts only when they affect the task. For a recurring project, copy the optional
[project context template](skills/px4-flightdeck/assets/project-context.template.md)
into that project. Your learning notes stay with your project, outside the reusable skill.

The optional inspector runs where the source files live:

```bash
python3 skills/px4-flightdeck/scripts/inspect_workspace.py \
  --px4 /path/to/PX4-Autopilot \
  --ros-workspace /path/to/ros_workspace
```

Replace paths with real ones; either argument can be used alone. Output is JSON to
stdout and may contain local paths. It reads source metadata, not running PX4 or an
installed node. It does not build, launch, connect to a vehicle, or upload anything.

## Scope and validation

Version `0.2.0` adds source-backed technical guides, examples and reproducible packaging.
The workflows were motivated
by learning/development records involving PX4, ROS 2, and Gazebo. They intentionally
avoid treating one user's release, vehicle, command rate, or tuning policy as universal.

Local package/helper checks and manual or independent-agent behavioral review are
different from simulator acceptance. See [evaluation instructions and results](evals/README.md).
No PX4/ROS 2 build, simulator or hardware acceptance, quantified productivity improvement,
or cross-client compatibility is claimed for this release.

Vehicle-affecting operations require the user's authorization for the actual target.
Simulation evidence supports only its tested conditions. This is an independent community
project, not an official PX4 or Dronecode product.

## Contribute

Bring a reproducible case: task, relevant versions, sanitized input/log excerpt, actual
answer, expected observable behavior, and verification result. Try the same case with
and without the skill, keeping the model, tools, budget, and input fixed. Useful changes
improve decisions or evidence; adding more “expert” adjectives does not establish quality.

Remove credentials, personal paths, vehicle identifiers, and location data before sharing
artifacts. Link to upstream PX4 sources rather than copying manuals into this repository.
Keep both READMEs aligned when changing user-facing behavior. Original contributions
use MIT; the adapted PX4 module example retains BSD-3-Clause. See
[contribution guidance](CONTRIBUTING.md) and [third-party notices](THIRD_PARTY_NOTICES.md).

## Build a release

Python 3.9+, standard library only:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py
```

Outputs: full source ZIP, standalone skill ZIP and `SHA256SUMS.txt` under `dist/`.
Archives use deterministic file ordering/timestamps and exclude Git internals,
caches and flight-record extensions. GitHub package checks run on pushes/PRs;
the tag workflow builds and publishes release assets. See
[publishing instructions](docs/PUBLISHING.md) and [changes](CHANGELOG.md).
