# Contributing / 参与贡献

Useful contributions improve a real decision, explanation, implementation or test.
Start with the task and observable acceptance, then the smallest supported change.
Keep `SKILL.md` short; route topic-specific detail to references. Preserve both
English and Chinese entry points, and keep identifiers/diagnostics exact in examples.

For a bug, include sanitized input, PX4/ROS/simulator revisions, execution machine,
actual outcome, expected behavior and commands already tried. Do not share original
flight logs, coordinates, credentials or personal paths without reviewing them.

For technical guides, cite matching source symbols with commit-pinned links. Record
whether an example was source-inspected, compiled, run or behavior-accepted, with its
environment. When adding a supported reference revision, update the source manifest
from files actually fetched/read; a hash is provenance, not proof of compatibility.
Retain upstream licenses when adapting code.

Before submitting, from the repository root (Python 3.9+):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py
```

For skill behavior, use the [evaluation protocol](evals/README.md). New prompts should
include held-out tasks, not only wording already shown in a guide. Never replace a
not-run simulator result with a successful Python/package test.

Contributions use MIT for original material; existing third-party exceptions retain
their licenses. No CLA is required by this project.

中文：欢迎提交复现案例、源码依据、经过验证的小例子和双语说明。说明改动解决什么问题，
实际验到了哪一步；不要用“专家”“更可靠”等形容词替代证据。发布包不收录个人学习笔记。
