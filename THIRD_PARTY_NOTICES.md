# Third-party sources and licenses / 上游来源与许可

PX4 FlightDeck's original instructions, guides, Python helpers and packaging use the
root MIT license. No model weights, original user notes, flight logs, or full PX4/ROS
manuals are distributed.

The C++ module lifecycle and CMake example under
`skills/px4-flightdeck/assets/examples/px4-module` adapt PX4's work-item example:

- Upstream: [PX4-Autopilot work_item](https://github.com/PX4/PX4-Autopilot/tree/d6f12ad1c4f70ad3230afd7d86e971421e02fef4/src/examples/work_item)
- Copyright (c) 2021 PX4 Development Team. All rights reserved.
- Adapted lifecycle/CMake files retain BSD-3-Clause identifiers; the original notice,
  conditions and disclaimer are included in the example's [LICENSE](skills/px4-flightdeck/assets/examples/px4-module/LICENSE).
- Modifications: local-position subscription, periodic read-only reporting, renamed
  module, simplified state and explicit example acceptance procedure.

Technical guides summarize mechanisms and link to source rather than redistributing
manuals. The [reference manifest](skills/px4-flightdeck/references/upstream-snapshot.json)
records upstream revisions and hashes. Refer to the respective upstream repository
for its license when reusing additional content. PX4 and Dronecode names identify
the upstream projects and do not imply endorsement.

中文：本项目原创部分采用 MIT；改编自 PX4 的模块示例保留原 BSD-3-Clause 许可。
安装与打包均保留示例许可。引用资料不等于本项目拥有上游文档或软件的版权。
