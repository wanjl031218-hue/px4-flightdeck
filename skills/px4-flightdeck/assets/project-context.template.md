# PX4 project context / PX4 项目上下文

Keep this filled document in the user's project, separate from the reusable skill.
Leave unknown facts explicitly unknown. Fill only fields relevant to the current task.

## Goal and current task / 目标与当前任务

- Goal / 总目标:
- Current behavior and desired change / 现状与本次改动:
- Acceptance evidence / 验收证据:
- Language and explanation depth / 语言与解释深度:

## Execution environment / 执行环境

- Host vs execution machine; accessible resources / 主机、执行机和可访问资源:
- SITL, HITL, or hardware; vehicle / 环境类型与机型:
- PX4 release, commit, dirty state / PX4 版本、提交与改动:
- Simulator/world/model / 仿真器、世界和模型:
- ROS 2, px4_msgs, DDS Agent / ROS 2、消息包与通信桥:
- Workspace/package, build target, installed prefix / 工作区、包、构建目标与安装路径:
- Source, installed, runtime build evidence / 源码、安装程序和运行版本证据:

## Task and control ownership / 任务与控制权

- Architecture and active command owner / 架构与当前控制指令来源:
- Coordinate frame, units, reference origin / 坐标系、单位与原点:
- Clock domains, freshness and reset handling / 时间域、新鲜度与重置处理:
- Completion, timeout, takeover and handover behavior / 完成、超时、接管和交接:
- Authorized actions and target / 已授权操作与目标:

## Experiments, when relevant / 实验信息（需要时）

- Scenario/configuration, fixed conditions / 科目、配置与固定工况:
- Baseline and all attempted run IDs / 基线与全部尝试的运行编号:
- Data schema, event/quality labels, metric windows / 数据结构、事件、质量标签与指标窗口:
- Parameter snapshot and allowlist / 参数快照与可调范围:
- Change budget and current policy revision / 修改范围与当前规则版本:
- Scorer revision, acceptance and regression rules / 评分器版本、接受与回归条件:
- Held-out validation conditions / 独立验证工况:

## Progress and open questions / 进度与待确认事项

For each item record date, status, artifact, and evidence origin (assistant-executed,
user-reported, planned, or unverified). Keep normal-path success separate from verified
failure handling. Add unresolved contradictions and the decision that supersedes them.
