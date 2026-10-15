# Publish to GitHub / 发布到 GitHub

This checkout is ready to upload; building an archive does not publish anything.
Choose your actual account/organization and create a repository named
`px4-flightdeck` (or your preferred name). Do not initialize a second README/license
in the remote if you intend to push this complete source tree.

中文：先检查本地内容，再在自己的 GitHub 账号创建空仓库。下面的远程地址须替换为
GitHub 实际给你的地址。推送 tag 会触发发布；准备好后再做。

## Validate and review

From this repository's root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_release.py
git status --short
```

Review the READMEs, license exceptions, source manifest and evaluation record.
Only public skill/source material belongs here. Generated ZIPs in `dist/` are
release assets; `.gitignore` excludes them from source history.

If using an existing empty Git checkout (as for this package), stage only the source:

```bash
git add .github .gitignore VERSION LICENSE THIRD_PARTY_NOTICES.md \
  README.md README.zh-CN.md CONTRIBUTING.md CHANGELOG.md docs evals scripts skills tests
git diff --cached --stat
git diff --cached
git commit -m "Release PX4 FlightDeck v0.2.0"
```

If the downloaded archive is not a Git checkout, run `git init -b codex/en` first.
Configure your Git author if Git requests it. Add the real GitHub remote using the
command GitHub shows, then push `codex/en` and `codex/zh-CN` and set `codex/en` as
the GitHub default branch. See [language branches](LANGUAGES.md) for the homepage
difference. Do not replace an existing remote without inspecting it.

## Release assets

After source review and a green GitHub package-check run:

```bash
git tag -a v0.2.0 -m "PX4 FlightDeck v0.2.0"
git push origin v0.2.0
```

The release workflow verifies the tag against `VERSION`, reruns checks, creates two
archives and `SHA256SUMS.txt`, and attaches them to the GitHub release. Repository
Actions must be enabled; the workflow requests content-write permission for this job.
It does not create the repository or push source for you.

- Full source ZIP: installer, skill, documentation, tests, evals and workflows.
- Standalone skill ZIP: `px4-flightdeck/` containing `SKILL.md`, references, helpers,
  examples and licenses; unzip this folder into the client's skill discovery directory.

If Actions cannot publish, create a release in GitHub's UI from the reviewed tag and
upload the three local `dist/` files instead. Remote CI and release success must be
checked on GitHub; a local package pass does not imply they ran.

Suggested repository description:

> Bilingual PX4 learning and development skill: source-grounded teaching, ROS 2,
> debugging and reproducible parameter experiments for coding agents.

Suggested topics: `px4`, `robotics`, `ros2`, `gazebo`, `agent-skills`, `codex`, `education`.
