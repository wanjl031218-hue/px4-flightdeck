# Evaluation / 评估

The cases in [cases.md](cases.md) are a starting evaluation set, not a performance
claim. Fixtures are synthetic reproductions of failure patterns; they contain no
original flight logs, personal notes, or measured performance data.

## Run a behavioral comparison

1. Fix the agent/model version, tool permissions, time/token budget, and case input.
2. Use fresh conversations: one without this skill and one with it. To measure the
   technical references specifically, add a third arm with the previous workflow-only
   release, while keeping the full v0.2.0 skill as the documentation arm. Ensure the
   baseline cannot implicitly load this skill. Give the same raw artifacts to both.
3. Give the agent only the case prompt and raw input, not reviewer criteria. Do not
   carry previous diagnoses or expected answers into the evaluated conversation.
4. Record answer/artifacts, evidence consulted, commands executed, remaining questions,
   and whether the behavior works. Evaluate both Chinese and English requests and
   style switches. Repeat when measuring variance rather than reporting a single run
   as a reliable success rate.
5. Score each dimension 0 (wrong/missing), 1 (partial), or 2 (supported and usable):
   correctness, evidence, task completion, teaching/style fit, and reproducibility.
   Record authorization/ownership violations separately as hard failures; do not hide
   them in an average. Distinguish response review from execution acceptance.

For implementation cases, run builds and acceptance only in an explicitly authorized
environment. A reviewer liking an answer does not establish flight behavior. For
metrics, use an independently checked calculation on a known dataset before evaluating
interpretation. The bundled scorer now has analytic table-based tests; it does not
validate a ULog parser or an arbitrary project's metric engine.

## Automated helper checks

From the repository root, using Python 3.9+ (standard library only):

```bash
python3 -m unittest discover -s tests -v
```

Tests exercise read-only metadata collection, missing/corrupt input, Git root identity,
installation/update recovery, declared metric calculations, package references and
reproducible source/skill archives with extracted installation. They do not execute PX4, ROS 2,
flight commands, or a language model. A maintained GitHub Actions workflow runs these
checks; a local pass does not imply that remote CI has run.

## Results / 结果

Record actual results in [results.md](results.md). Keep “not run” explicit. Do not claim
an A/B improvement from structural checks or one independent-agent review.

中文：保持模型、工具、预算与输入一致，分别测试启用和未启用 skill 的新对话。
基线对话必须确保不会自动加载本 skill。只把任务和原始材料给被测 agent，
评分标准由评审者持有。分别检查正确性、证据、任务完成、教学风格和复现性；
越权操作单列为失败。脚本通过、回答合理、仿真通过，是不同的验收结果。
