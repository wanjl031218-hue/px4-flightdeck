#!/usr/bin/env python3
"""Build reproducible source and standalone-skill ZIPs with SHA-256 checksums."""

import argparse
import hashlib
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "px4-flightdeck"
DIRECTORIES = ("skills", "scripts", "tests", "evals", "docs", ".github")
FILES = ("VERSION", "README.md", "README.zh-CN.md", "LICENSE", "THIRD_PARTY_NOTICES.md",
         "CONTRIBUTING.md", "CHANGELOG.md", ".gitignore")
EXCLUDED = {"__pycache__", ".DS_Store", ".git", "dist", ".venv"}


def eligible(path):
    return (not any(p in EXCLUDED for p in path.parts)
            and path.suffix not in {".pyc", ".pyo", ".ulg", ".bag", ".db3"})


def write_zip(output, entries):
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source, name in sorted(entries, key=lambda item: item[1]):
            if source.is_symlink():
                raise ValueError("Release input must not be a symlink: " + str(source))
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, source.read_bytes())


def package(output):
    version = (ROOT / "VERSION").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must contain a numeric semantic version")
    frontmatter = (ROOT / "skills" / SKILL_NAME / "SKILL.md").read_text()
    if 'version: "' + version + '"' not in frontmatter.split("---", 2)[1]:
        raise ValueError("VERSION and skill metadata disagree")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    paths = [ROOT / name for name in FILES]
    # A Chinese-homepage branch retains an English navigation target.
    if (ROOT / "README.en.md").is_file():
        paths.append(ROOT / "README.en.md")
    for directory in DIRECTORIES:
        paths.extend(p for p in (ROOT / directory).rglob("*") if p.is_file() and eligible(p.relative_to(ROOT)))
    source = output / (SKILL_NAME + "-v" + version + ".zip")
    write_zip(source, [(p, SKILL_NAME + "/" + p.relative_to(ROOT).as_posix()) for p in paths])
    skill_root = ROOT / "skills" / SKILL_NAME
    skill = output / (SKILL_NAME + "-skill-v" + version + ".zip")
    write_zip(skill, [(p, SKILL_NAME + "/" + p.relative_to(skill_root).as_posix())
                     for p in skill_root.rglob("*") if p.is_file() and eligible(p.relative_to(skill_root))])
    checksum = output / "SHA256SUMS.txt"
    checksum.write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n"
                                for p in (source, skill)), encoding="utf-8")
    return source, skill, checksum


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for path in package(args.output):
        print(path)


if __name__ == "__main__":
    main()
