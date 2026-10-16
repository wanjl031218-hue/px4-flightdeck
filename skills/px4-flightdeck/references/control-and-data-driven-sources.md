# Control and data-driven references / 控制与数据驱动参考

This note adds a source-grounded layer for PX4 parameter experiments. It combines
three complementary views: PX4's implemented signal path, classical feedback-control
analysis, and data-driven modeling. The references are used to teach a workflow; they
are not a claim that any author endorses PX4 FlightDeck, and they do not provide flight
certification or universal gain values.

这份参考把三种视角接起来：PX4 实际实现的信号路径、经典反馈控制分析、以及
数据驱动建模。内容服务于可复现实验，不代表相关作者为本项目背书，也不提供
适用于所有机型的增益数值或适航结论。

## Source register / 来源登记

The links below are primary or author-maintained sources. PX4 source links are pinned
to the same v1.17.0 snapshot used by the rest of this skill (`d6f12ad...`). The
authors' tutorials and repositories are moving resources, so record the retrieval date
and a commit when copying a concrete example into an experiment.

| Source | What it supports | Boundary |
| --- | --- | --- |
| [PX4 `MulticopterPositionControl.cpp` at `d6f12ad`](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/mc_pos_control/MulticopterPositionControl.cpp) and [`PositionControl.cpp` at the same commit](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/mc_pos_control/PositionControl/PositionControl.cpp) | Parameter-to-controller wiring, position/velocity error paths, limits, feed-forward, and anti-windup code to inspect | Source inspection is version-specific; it does not show a user's active parameter values or prove runtime behavior |
| [PX4 parameter definitions at `d6f12ad`](https://github.com/PX4/PX4-Autopilot/blob/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/modules/mc_pos_control/multicopter_position_control_params.c) | Names, defaults, units, and metadata for the referenced multicopter parameters | Defaults are not a vehicle snapshot; verify the running build and read back values |
| [PX4 uLog format](https://docs.px4.io/main/en/dev_log/ulog_file_format.html) and [PX4 Flight Review](https://review.px4.io/) | Structured log fields and a visual first pass over runs | A plotted trace is not a metric definition; use the actual log schema and a deterministic scorer |
| [Brian Douglas, Control Systems Lectures](https://www.youtube.com/@BrianBDouglas) | Transfer functions, feedback, PID, Bode/root-locus intuition, and practical control explanations | Tutorials are educational; linear analysis is local to the chosen operating point and does not model every PX4 nonlinear limit. Do not infer an educator's identity from an unrelated GitHub username |
| [Data-Driven Science and Engineering companion site](https://databookuw.com/) and [authors' MATLAB examples](https://github.com/dynamicslab/databook_matlab) | SVD/POD, regression, DMD/Koopman, system identification, and data-driven control examples | Companion code is instructional; retain the exact commit and test data if an example is adapted |
| [Brunton et al., SINDy, PNAS (2016)](https://doi.org/10.1073/pnas.1517384113) | Sparse identification of candidate governing equations from measured trajectories | Sparse equations depend on library, sampling, noise, and excitation; they are hypotheses to validate, not a substitute for PX4 source |
| [Brunton et al., Koopman invariant subspaces for control, PLOS ONE (2016)](https://doi.org/10.1371/journal.pone.0150171) | Lifting nonlinear measurements into a finite linear model for analysis/control experiments | A finite lifted model is an approximation over its data distribution; it does not establish global stability or safe extrapolation |
| [Brunton et al., Modern Koopman Theory, SIAM Review (2022)](https://doi.org/10.1137/21M1401243) | A modern overview of Koopman representations, spectra, and limitations | Use the review to choose a method, then report conditioning, validation split, and reconstruction error |
| [Brunton, Proctor & Kutz, SINDY with control (SINDYc) preprint (2016)](https://doi.org/10.48550/arxiv.1605.06682) | Including measured inputs when identifying dynamics | Inputs must be measured and sufficiently exciting; an arbitrary mission trace can make parameters unidentifiable |

## How to combine the sources / 如何组合

### 1. Start with PX4's implemented loop

1. Identify the task signal (`trajectory_setpoint`, local position/velocity, attitude,
   rate, or actuator output), its frame, timestamp, and the module that consumes it.
2. Trace the parameter from its definition to the update function and the consuming
   control law. For the v1.17.0 snapshot, the multicopter position controller is a
   useful anchor: position error contributes to velocity demand, and velocity error
   contributes to acceleration/thrust demand, subject to limits and estimator validity.
3. Check whether the observed behavior can be explained by a limit, feed-forward,
   hover-thrust estimate, mode-specific path, or estimator reset before attributing it
   to a gain.
4. Save a parameter snapshot and the exact PX4/vehicle/simulator revision. A source
   default or a parameter name alone is not evidence that the candidate is active.

中文：先找到任务信号、坐标系、时间戳和实际消费它的模块；然后从参数定义追到
更新函数和控制律。先检查速度/加速度/推力限制、前馈、悬停推力估计、模式路径
和估计器重置，再判断是否真的是增益问题。每次实验都保存当前参数、PX4 版本、
机型/仿真器和随机种子。

### 2. Use Douglas-style classical analysis as a hypothesis tool

For a small, declared operating region, treat a loop as an approximate input-output
system. Define the reference, measured output, disturbance, and actuator/control effort;
then compare the same step or disturbance window across runs.

- **Time domain:** rise time, peak deviation/overshoot, settling or recovery time,
  steady-state error, and oscillation should each have a formula, tolerance, dwell
  time, and observation horizon.
- **Frequency domain:** when an excitation and sampling rate support it, estimate a
  frequency response and inspect bandwidth, phase margin, gain margin, and coherent
  peaks. Use this to identify a plausible robustness or resonance issue, not to infer
  the full nonlinear PX4 loop from one plot.
- **PID interpretation:** a proportional change affects immediate error response, an
  integral change affects accumulated bias and wind-up risk, and a derivative change
  affects damping/noise sensitivity. Map this vocabulary to the actual PX4 loop and
  parameter names; do not assume that every `P/I/D` parameter controls the same signal.
- **Loop-shaping caution:** when a signal reaches a velocity, acceleration, thrust, or
  actuator limit, the linear model no longer predicts the observed response. Log and
  report saturation instead of compensating by blindly increasing gains.

This is a working hypothesis, not an online controller. The agent may calculate
metrics and propose a bounded candidate offline; applying parameters to a vehicle is a
separate authorized action with a rollback plan.

### 3. Use Brunton-style data-driven modeling for diagnosis and held-out checks

Apply data-driven methods in a staged order:

1. **SVD/POD:** compress a synchronized state/feature matrix and inspect singular-value
   decay. Use the retained rank as a diagnostic choice, report the reconstruction error,
   and do not confuse a low-rank representation with a physical state model.
2. **DMD/Koopman:** fit a linear evolution model in measured or lifted features to
   summarize dominant frequencies and decay/growth over a declared window. Test a
   one-step and multi-step forecast on held-out runs; a visually plausible mode is not
   proof of causality.
3. **SINDy:** build a candidate library from measured states and derivatives, use
   regularization/thresholding, and report the library, derivative estimator, sample
   interval, noise handling, and selected terms. Treat the result as a falsifiable
   equation hypothesis.
4. **SINDYc or regression with inputs:** include measured parameter-independent inputs
   (setpoints, disturbances, thrust/actuator commands) when identifying controlled
   dynamics. Check input excitation and collinearity; otherwise the agent can select a
   stable-looking but unidentifiable model.
5. **Validation:** reserve seeds, disturbances, or trajectories that were not used for
   candidate selection. Report prediction error, failure cases, conditioning, and the
   range in which the model was trained. Never extrapolate a learned model into a
   flight-safety claim.

中文：先用 SVD/POD 看数据是否低秩，再用 DMD/Koopman 做频率和演化摘要，最后在
有足够激励时尝试 SINDy/SINDYc。模型必须用留出的试验验证，并报告库函数、导数
估计、采样间隔、噪声处理、条件数和失败案例。数据驱动模型只能支持限定工况下
的假设与比较，不能替代 PX4 源码、参数边界或安全验证。

## PX4 experiment template / PX4 实验模板

Use this record for every agent-assisted parameter proposal:

```yaml
scenario: "declared task and disturbance"
px4_revision: "commit or release"
vehicle_simulator: "vehicle, SITL/HITL/hardware, model revision"
baseline_runs: ["run-id ..."]
candidate_runs: ["run-id ..."]
signals: ["reference", "measured state", "control/actuator", "validity flags"]
window_rule: "event start, tolerance, dwell, horizon"
metrics: ["RMSE", "peak deviation", "recovery time", "effort/saturation"]
allowed_parameters: ["exact names and bounds"]
candidate: "current -> proposed -> rollback"
classical_hypothesis: "loop, bandwidth, damping, limit, or estimator explanation"
data_model: "none/SVD/DMD/Koopman/SINDy/SINDYc; fit and holdout definition"
hard_constraints: ["safety and task limits"]
decision: "accept / reject-restore / inconclusive"
```

The agent should preserve raw logs, parameter snapshots, unsuccessful attempts, model
artifacts, prompts, and the reason for each human decision. Compare baseline and
candidate under the same mission, simulator physics, scorer, timing rules, and seeds
where possible. Five successful baseline flights can define a conditional reference;
they cannot establish an overall success rate if failed attempts were omitted.

## Suggested skill behavior / 建议加入技能的行为

- Ask which loop and signal are being optimized before naming a parameter.
- Produce a source trace: parameter definition → update/binding → consuming law →
  limits/failsafe → logged evidence.
- Separate a classical-control explanation, a data-driven model result, and a causal
  claim. Mark the last one as unverified unless the experiment discriminates it.
- Require a bounded candidate, current/readback value, rollback value, and a metric
  acceptance rule before recommending a parameter change.
- Use model fitting only for offline analysis and candidate ranking. Preserve manual
  takeover, PX4 failsafe behavior, and the user's authorization boundary.
- Prefer an inconclusive result or a request for one discriminating experiment over a
  confident recommendation from an under-excited or saturated data set.

## Retrieval note / 检索说明

Checked 2026-10-16. Links to papers are DOI-resolved; PX4 links are commit-pinned.
The Douglas channel and Brunton companion repositories are author-maintained moving
resources. If an example is copied into a future release, record its exact commit,
environment, and license rather than vendoring large excerpts.
