# Modules, CMake and WorkQueue / 模块与构建

Use when adding a C++ module, diagnosing a missing command, or teaching scheduling.
Reference: PX4 v1.17.0 at `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`.
The bundled example was checked against source APIs; it has not been compiled with PX4.

## Four connected identities / 四个必须对应的名称

| Place | Bundled example | What it controls |
| --- | --- | --- |
| Directory | `src/examples/flightdeck_observer` | Source location and Kconfig discovery |
| Kconfig | `EXAMPLES_FLIGHTDECK_OBSERVER` | Selectable build option |
| Board configuration | `CONFIG_EXAMPLES_FLIGHTDECK_OBSERVER=y` | Enablement in the chosen build |
| CMake `MAIN` and exported function | `flightdeck_observer`, `flightdeck_observer_main` | PX4 shell command |

Kconfig declaration alone does not enable compilation. Compiling a command does not
start it. Add startup configuration only when automatic startup is actually requested.
Use the supplied [read-only example and runbook](../assets/examples/px4-module/README.md)
to see the complete files and acceptance steps.

## Lifecycle and scheduling

The example uses `ModuleBase<T>` for start/stop/status and `ScheduledWorkItem` for a
1 Hz polling callback on `px4::wq_configurations::test1`. The upstream work-item
example also demonstrates callback-driven scheduling. Select based on the workload.

`task_spawn` creates the instance, stores module identity, marks it as a work-queue
task, then schedules work. `Run()` checks `should_exit()`, clears scheduling and calls
`exit_and_cleanup()` before returning. Ordinary iterations read at most the latest
sample and return. A stop must be serviced even when no new uORB samples arrive.

中文：WorkQueue 是共享执行资源。把无限循环或长时间等待写进 `Run()`，会拖住同队列
其他工作。这个例子采用定时调度，因此无数据时仍能检查退出请求。

For a callback-based module, inspect registration failure, callback unregistration,
schedule cleanup and races using the branch's nearby implementation. A polling module
does not need callback cleanup it never registered.

## Observe the build chain

In an already provisioned Linux PX4 development environment, regular shell:

```bash
rg -n 'FLIGHTDECK_OBSERVER' src/examples/flightdeck_observer boards/px4/sitl/default.px4board
make px4_sitl_default
```

Expected: the target builds and includes the module. In a running SITL `pxh>` shell,
the example's start/status/stop commands should exist. An unknown command suggests a
different target/binary, missing enablement, or missing build; it is not an estimator bug.
Use the runbook for actual command blocks and expected observations.

If compilation fails, preserve the first diagnostic and file/line. Distinguish missing
header/API, registration/linker failure, unsupported toolchain and stale configuration.
Before clearing a build directory, identify which directory and target are implicated.

## Source anchors

- [WorkItemExample.hpp](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/examples/work_item/WorkItemExample.hpp)
- [WorkItemExample.cpp](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/examples/work_item/WorkItemExample.cpp)
- [Work-item CMake](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/examples/work_item/CMakeLists.txt)
- [Work-item Kconfig](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/examples/work_item/Kconfig)
- [SITL board configuration](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/boards/px4/sitl/default.px4board)
