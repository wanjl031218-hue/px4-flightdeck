# PX4 FlightDeck

**让 AI 陪你学懂、构建并调试 PX4，用证据确认每一步。**

[English](README.md) · [技能入口](skills/px4-flightdeck/SKILL.md) · [技术指南](skills/px4-flightdeck/references/sources.md) · [验证记录](evals/results.md) · [许可说明](THIRD_PARTY_NOTICES.md)

仓库默认分支为 `codex/en`，首次进入显示英文首页。需要中文首页时，可在 GitHub
分支选择器切换到 `codex/zh-CN`。两个分支均包含双语 skill 与同一套工具；详见
[语言分支说明](docs/LANGUAGES.md)。

从“帮我生成代码”，走到“我能运行、解释和验证这个项目”。
PX4 FlightDeck 是面向学习者和开发者的双语 agent skill，覆盖教学、
C++/CMake/WorkQueue、ROS 2 与 Gazebo、排错以及受限的参数实验。
它根据你的实际版本和项目材料工作。

**三种回答风格，同一套证据标准。**

| 风格 | 怎么说 | 回答重点 |
| --- | --- | --- |
| 通俗教学 / Plain | “通俗一点，结合我的代码讲” | 先讲现象，再解释术语、关键路径和可观察的验证 |
| 工程实战 / Engineering | “工程模式，给我排查和修改步骤” | 证据、假设、执行位置、预期输出、验证与回退 |
| 学术研究 / Academic | “学术模式，我要设计实验或写报告” | 问题、假设、机制、指标定义、证据与局限 |

中文或英文都可使用，随时用自然语言切换风格。双语支持指按需使用任一语言，
不用每条回答都重复翻译；代码标识、命令和报错保留原文。

## 能帮助你什么

- **边交付边教学：**说明你当前代码的输入、处理、输出、反馈与完成条件。
- **核对真正跑起来的版本：**区分源码、构建目标、安装程序和运行进程。
- **讲清系统分工：**区分任务节点、DDS 通信、PX4 控制、仿真物理和地面站。
- **先诊断再调参：**检查旧程序、时钟、估计器重置、通信和模式交接等竞争解释。
- **让实验可追溯：**固定指标和窗口、保留失败、记录参数快照，做回归和独立验证。

skill 包含工作指令、技术指南、只读示例与分析脚本，不改变模型权重。
模型与工具由你的 agent 客户端提供。仅加载 skill 不需要新的 API Key、云服务或
PX4 环境；实际编译和仿真仍需要对应运行环境。安装过程不会启动飞行。

## 包含哪些内容

| 内容 | 对应入口 |
| --- | --- |
| 目标 → 接口 → 控制器 → 状态反馈 | [架构指南](skills/px4-flightdeck/references/architecture.md) |
| C++ / CMake / Kconfig / WorkQueue | [模块指南](skills/px4-flightdeck/references/modules-build.md)与[完整示例](skills/px4-flightdeck/assets/examples/px4-module/README.md) |
| ROS 2 / DDS / Offboard / 坐标与时钟 | [接口指南](skills/px4-flightdeck/references/ros2-offboard.md)与[只读订阅包](skills/px4-flightdeck/assets/examples/ros2-observer/README.md) |
| 参数定义与控制器使用位置 | [控制链与参数追踪](skills/px4-flightdeck/references/controllers-parameters.md) |
| 日志对齐、RMSE、超调和调节时间 | [指标定义与可运行脚本](skills/px4-flightdeck/references/logs-metrics.md) |

技术资料以 PX4 **v1.17.0** 固定 commit 为参考，记录 `px4_msgs` 快照和来源文件哈希。
这是核对源码的参考环境，不代表已验证整个软件栈兼容。技术指南以英文为主，并附中文
关键说明；助手按你要求的语言讲解。两个只读示例提供完整文件和验收步骤，但本版
**尚未通过 PX4/ROS 编译或 SITL 验收**。

## 一分钟安装

在 GitHub 克隆仓库，或点击 **Code → Download ZIP** 后解压。下载 Release 时，
可选择完整源码 ZIP，进入解压后的 `px4-flightdeck` 文件夹。仅加载 skill 不需要
安装 ROS 或 PX4。

克隆或下载完整仓库后，在仓库根目录使用 Python 3.9 或更高版本执行：

```bash
python3 scripts/install.py
```

默认复制到 `~/.agents/skills/px4-flightdeck`，这是
[OpenAI 官方文档](https://developers.openai.com/codex/skills/)列出的用户级发现位置。
如果客户端使用其他技能目录，可以明确指定：

```bash
python3 scripts/install.py --skills-dir ~/.codex/skills
```

开发时可加 `--link`，让 skill 跟随当前仓库里的修改；链接模式需要保留仓库。
安装器只使用本地文件，默认遇到已有安装会停止。下载新版后，在新版仓库根目录执行：

```bash
python3 scripts/install.py --update
```

更新会把旧目录或链接保存在技能发现目录旁的 `flightdeck-backups`，打印备份路径，
再安装新版；复制失败会恢复旧安装。如果原来用了 `--skills-dir`，更新时必须传同一
目录。使用 `--link` 的开发安装会直接跟随仓库里的修改。

也可以下载 Release 的**独立 skill ZIP**，解压到客户端技能目录，最终布局应为
`skills/px4-flightdeck/SKILL.md`，避免多套一层同名目录。两种包都保留许可文件。

如果客户端没显示 skill，重启客户端。其他 agent 客户端可按自己的发现
规则使用同一份 `SKILL.md`，但本版尚未验证其他客户端兼容性。

## 使用示例

```text
用 $px4-flightdeck，通俗教学模式。结合我的任务节点，讲清楚目标怎样到达
PX4，程序又靠什么反馈确认到点。先读实际文件。
```

```text
用 $px4-flightdeck，工程实战模式。源码写着 r8，节点启动却显示 r5。
先排查构建和部署链路，再决定是否修改任务逻辑。
```

```text
用 $px4-flightdeck，学术研究模式。审阅我的基准数据，设计只修改 PX4 参数
的对照实验。把数据质量限制和控制性能假设分开说明。
```

提供当前任务和相关文件即可，助手应复用已知信息，只问影响任务的缺失事实。
长期项目可以把[上下文模板](skills/px4-flightdeck/assets/project-context.template.md)
复制到自己的项目里填写。个人学习笔记和实验记录留在项目中，不写入公共 skill。

可选的只读检查脚本，要在源码实际所在的机器上执行：

```bash
python3 skills/px4-flightdeck/scripts/inspect_workspace.py \
  --px4 /path/to/PX4-Autopilot \
  --ros-workspace /path/to/ros_workspace
```

将示例路径替换为真实路径，也可以只提供其中一个参数。JSON 输出到终端，可能包含
本地路径；脚本只读源码元数据，不代表运行中 PX4 或安装程序的状态，不构建、
不启动进程、不连接飞控，也不上传数据。

## 当前状态与边界

`0.2.0` 补充了有源码依据的技术指南、示例与可复现发布工具。工作流程来自真实 PX4、ROS 2 和 Gazebo 学习开发
记录中反复出现的问题。某个用户的版本、机型、发送频率和参数修改预算不会被当作
所有项目的统一规则。

本地结构和脚本检查、人工或独立 agent 行为审阅，与仿真验收是不同层次。
方法和结果见[评估说明](evals/README.md)。本版不宣称已通过 PX4/ROS 2 编译、仿真或实机
验收，不宣称量化的效率提升，也不宣称跨客户端兼容。

影响车辆的操作须在用户授权的实际目标上执行。仿真证据仅支持已测工况。
这是独立社区项目，与 PX4/Dronecode 无官方从属关系。

## 参与改进

建议带一个可复现问题：任务、相关版本、脱敏后的输入或日志、实际回答、预期行为
与验证结果。保持模型、工具、预算和输入一致，对比启用前后；优先改进助手的判断
和验证方法。分享材料前去掉凭据、个人路径、车辆标识和位置数据。引用上游资料，
避免复制整本手册。修改对外行为时同步两份 README。原创部分采用 MIT，改编自 PX4
的模块示例保留 BSD-3-Clause；详见[贡献指南](CONTRIBUTING.md)与[上游许可说明](THIRD_PARTY_NOTICES.md)。

## 构建发布包

使用 Python 3.9+，不需要额外 Python 依赖：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py
```

`dist/` 下生成完整源码 ZIP、独立 skill ZIP 和 `SHA256SUMS.txt`。文件顺序和时间戳
固定，排除 Git 内部文件、缓存与飞行记录扩展名。GitHub 配置包含 push/PR 检查与 tag
触发的 Release 打包发布；实际操作见[发布指南](docs/PUBLISHING.md)与[更新记录](CHANGELOG.md)。
