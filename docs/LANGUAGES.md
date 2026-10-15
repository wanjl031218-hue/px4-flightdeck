# Language branches / 语言分支

| Branch | Root homepage | Purpose |
| --- | --- | --- |
| `codex/en` (default) | English `README.md` | Canonical source, English landing page and tagged releases |
| `codex/zh-CN` | Chinese `README.md` | Chinese landing page, with the same bilingual skill and helpers |

Both branches include `README.zh-CN.md`. The Chinese branch also keeps the English
homepage as `README.en.md` so its English navigation works without assuming a GitHub
account or repository URL. The skill answers in English or Chinese on either branch;
the branch chooses the homepage language, not the model's capabilities.

Develop changes on the English branch. When syncing the Chinese branch, bring across
the same source changes, copy the English homepage to `README.en.md`, then render
the Chinese homepage from `README.zh-CN.md` with its English link pointing to
`README.en.md`. Keep the language-only delta limited to those two homepage files.
Create release tags on `codex/en` so published source ZIPs open in English.

中文：默认英文首页，中文有独立分支入口。修复与工具以英文分支为准，中文分支同步相同
源码，只调整首页及英文镜像。切换分支不会改变 skill 的双语能力，发布 tag 放在英文分支。
