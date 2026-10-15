#!/usr/bin/env python3
"""Install locally; explicit updates preserve the previous installation as a backup."""

import argparse
from pathlib import Path
import shutil
import sys
import uuid

SKILL_NAME = "px4-flightdeck"
REPOSITORY = Path(__file__).resolve().parents[1]


def install(skills_dir, link=False, update=False):
    source = REPOSITORY / "skills" / SKILL_NAME
    if not (source / "SKILL.md").is_file():
        raise ValueError("Run the installer from a complete PX4 FlightDeck checkout")
    parent = Path(skills_dir).expanduser().absolute()
    target = parent / SKILL_NAME
    backup = None
    if target.exists() or target.is_symlink():
        if link and target.is_symlink() and target.resolve() == source:
            return target
        if not update:
            raise FileExistsError("Installation already exists; use --update to back up and replace: " + str(target))
        # Keep backup skills outside the discovery directory to avoid duplicate loading.
        backup = parent.parent / "flightdeck-backups" / uuid.uuid4().hex / SKILL_NAME
        backup.parent.mkdir(parents=True)
        target.rename(backup)
    parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        if link:
            target.symlink_to(source, target_is_directory=True)
            created = True
        else:
            # Reserve only our new directory; never merge into an existing installation.
            target.mkdir()
            created = True
            shutil.copytree(source, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
            shutil.copy2(REPOSITORY / "LICENSE", target / "LICENSE")
    except BaseException:
        if created:
            if target.is_symlink():
                target.unlink()
            else:
                shutil.rmtree(target)
        if backup is not None and not target.exists() and not target.is_symlink():
            backup.rename(target)
        raise
    if backup is not None:
        print("Previous installation preserved at: " + str(backup))
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path,
                        default=Path.home() / ".agents" / "skills",
                        help="Skill discovery directory (default: ~/.agents/skills)")
    parser.add_argument("--link", action="store_true",
                        help="Link to this checkout for local development; keep the checkout")
    parser.add_argument("--update", action="store_true",
                        help="Back up an existing installation outside discovery, then replace it")
    args = parser.parse_args(argv)
    try:
        target = install(args.skills_dir, args.link, args.update)
    except (OSError, ValueError) as exc:
        print("Installation failed: " + str(exc), file=sys.stderr)
        return 1
    print("Installed PX4 FlightDeck: " + str(target))
    print("Invoke $px4-flightdeck. If it is not visible, restart your agent client.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
