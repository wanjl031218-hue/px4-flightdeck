# PX4 FlightDeck v0.3.0

A bilingual, source-grounded control and data-driven analysis layer for PX4
parameter experiments. Adds practical connections to PX4's implemented control
path, Brian Douglas's classical control explanations, and Steven Brunton's SVD/POD,
DMD/Koopman and SINDy/SINDYc methods. The guide includes a YAML experiment record,
held-out validation requirements, and explicit boundaries around model transfer and
flight safety.

**Install:** download the full source ZIP, extract it, enter `px4-flightdeck`, and
run `python3 scripts/install.py` (Python 3.9+). Or extract the standalone skill ZIP's
`px4-flightdeck` folder into your client's skill directory. Invoke `$px4-flightdeck`.

**Validation:** see the included `evals/results.md`. Python/helper/package checks do
not establish PX4/ROS build or flight behavior; SITL/hardware acceptance and
with/without-skill performance comparison remain unrun.

中文：v0.3.0 增加基于公开来源的控制与数据驱动分析指南，将 PX4 实际控制链、
Brian Douglas 的经典控制讲解，以及 Steven Brunton 的 SVD/POD、DMD/Koopman、
SINDy/SINDYc 方法连接到受约束的参数实验。内容要求保留数据、留出验证和安全边界，
不把数据驱动模型当作飞行安全证明。

---

# PX4 FlightDeck v0.2.0

A bilingual PX4 learning/development skill with Plain, Engineering and Academic
explanation styles. Includes five focused technical guides, version-pinned source
references, two read-only example projects, a deterministic CSV scorer, and local
installation with backed-up updates.

**Install:** download the full source ZIP, extract it, enter `px4-flightdeck`, and
run `python3 scripts/install.py` (Python 3.9+). Or extract the standalone skill ZIP's
`px4-flightdeck` folder into your client's skill directory. Invoke `$px4-flightdeck`.

**Validation:** see the included `evals/results.md`. Python/helper/package checks
do not establish PX4/ROS build or flight behavior; SITL/hardware acceptance and
with/without-skill performance comparison remain unrun.

中文：双语 PX4 助教，提供通俗、工程、学术三种回答方式。补充版本化技术指南、只读示例、
指标脚本和便捷安装更新。下载完整源码包解压后执行安装器，或将独立 skill 包解压到
客户端技能目录。尚未通过 PX4/ROS 仿真或实机验收。
