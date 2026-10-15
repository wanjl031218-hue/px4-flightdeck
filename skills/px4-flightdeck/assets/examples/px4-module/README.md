# Read-only WorkQueue module / 只读 PX4 模块

Reference: PX4 v1.17.0 `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`.
Checked against the upstream WorkItemExample APIs and local-position schema.
**Not PX4-compiled or SITL-tested in this release.** Do not describe the example as
build-verified until the following steps pass in an actual PX4 environment.

中文：这个例子每秒读取一次本地位置；不发目标、不写参数、不控制飞机。它展示“源码 →
构建启用 → 命令 → 定时执行 → 退出”。原始 PX4 生命周期代码的 BSD 许可随包保留。

## Copy and build

Linux PX4 development machine / regular shell, with a provisioned checkout.
Replace paths; do not use a macOS host path inside an unrelated VM.

```bash
export FLIGHTDECK_REPO=/path/to/px4-flightdeck
export FLIGHTDECK_PX4=/path/to/PX4-Autopilot
test ! -e "$FLIGHTDECK_PX4/src/examples/flightdeck_observer" && \
  cp -R "$FLIGHTDECK_REPO/skills/px4-flightdeck/assets/examples/px4-module" \
    "$FLIGHTDECK_PX4/src/examples/flightdeck_observer"
cd "$FLIGHTDECK_PX4"
git describe --tags --always --dirty
```

Review `boards/px4/sitl/default.px4board` and add this line once for the default SITL
target (preserve other options):

```text
CONFIG_EXAMPLES_FLIGHTDECK_OBSERVER=y
```

Then in the regular OS shell, PX4 root:

```bash
make px4_sitl_default
```

Launch the project's established SITL setup; if its configured model is Gazebo X500,
the usual target is `make px4_sitl gz_x500`. Check prerequisites/version first.
The added module is not automatically started and no flight is needed for observation.

## Run and accept

In that SITL instance's PX4 shell (`pxh>`), copy commands without the prompt:

```text
flightdeck_observer start
flightdeck_observer status
```

Expected: running status and approximately one local-position line each second when
new estimator samples are available. The reported age is based on PX4's own clock.
An invalid position remains invalid even when the module prints it successfully.
No new samples should produce an explicit message rather than a fabricated position.

```text
flightdeck_observer stop
flightdeck_observer status
```

Expected: module stops, status reports not running and recurring output ceases.
Start it once more to check restart behavior, then stop. Preserve actual build output,
revision, PX4 version and observed behavior as the acceptance record. If the command
is unknown, follow [build diagnosis](../../../references/modules-build.md).

To undo: stop the observer, remove only its enablement line and copied source
directory, then rebuild the same target. No flight parameters were changed.
