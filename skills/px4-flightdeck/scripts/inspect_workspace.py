#!/usr/bin/env python3
"""Read local PX4/ROS source metadata. No network, build, or vehicle operations."""

import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


def git_output(root, *args):
    if not shutil.which("git"):
        return None
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    try:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(root), *args],
            capture_output=True, text=True, timeout=8, env=env, check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired, UnicodeError):
        return None


def git_identity(root):
    top = git_output(root, "rev-parse", "--show-toplevel")
    if not top or Path(top).resolve() != root.resolve():
        return {"commit": None, "description": None, "tracked_changes": None,
                "note": "No Git root at this path; parent repository identity is not used."}
    changes = git_output(root, "status", "--porcelain", "--untracked-files=no",
                         "--ignore-submodules=all")
    return {
        "commit": git_output(root, "rev-parse", "HEAD"),
        "description": git_output(root, "describe", "--tags", "--always", "--dirty"),
        "tracked_changes": bool(changes) if changes is not None else None,
        "note": "Tracked changes only; untracked files and submodule dirtiness are not checked.",
    }


def inspect_px4(path):
    root = Path(path).expanduser().resolve()
    markers = ["CMakeLists.txt", "src/modules", "boards", "msg"]
    missing = [item for item in markers if not (root / item).exists()]
    if missing:
        raise ValueError("PX4 source root is missing expected entries: " + ", ".join(missing))
    candidates = ["src/examples/work_item", "src/modules/work_item",
                  "src/modules/uxrce_dds_client/dds_topics.yaml"]
    return {
        "path": str(root), "git": git_identity(root),
        "source_entries": [p for p in candidates if (root / p).exists()],
        "runtime_version": None,
        "note": "Source metadata only; the running PX4 build and vehicle are not inspected.",
    }


def inspect_ros_workspace(path):
    root = Path(path).expanduser().resolve()
    source = root / "src"
    if not source.is_dir():
        raise ValueError("ROS workspace must contain a src directory")
    packages, errors = [], []
    skipped = {"build", "install", "log", "node_modules", "__pycache__"}
    visited = 0
    truncated = False
    for current, dirs, files in os.walk(source, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in skipped and not d.startswith(".")
                         and not (Path(current) / d).is_symlink())
        visited += 1
        if visited > 5000 or len(packages) >= 200:
            truncated = True
            break
        if "package.xml" not in files:
            continue
        manifest = Path(current) / "package.xml"
        rel = str(manifest.relative_to(root))
        # Inspect metadata only, never execute setup.py, launch files, or package code.
        try:
            if manifest.is_symlink():
                raise ValueError("symlinked manifest is not read")
            if manifest.stat().st_size > 200_000:
                raise ValueError("manifest exceeds 200 KB limit")
            tree = ET.fromstring(manifest.read_bytes())
            packages.append({"name": tree.findtext("name"),
                             "version": tree.findtext("version"), "manifest": rel})
        except (OSError, ET.ParseError, ValueError) as exc:
            errors.append({"manifest": rel, "error": str(exc)})
    return {
        "path": str(root), "packages": packages, "manifest_errors": errors,
        "scan_truncated": truncated,
        "build_directory_present": (root / "build").is_dir(),
        "install_directory_present": (root / "install").is_dir(),
        "runtime_build": None,
        "note": "Directory presence does not prove a successful build or identify a running node.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--px4", help="PX4 source root on this machine")
    parser.add_argument("--ros-workspace", help="ROS workspace containing src/")
    args = parser.parse_args(argv)
    if not args.px4 and not args.ros_workspace:
        parser.error("provide --px4 and/or --ros-workspace")
    report = {
        "schema_version": 1,
        "scope": "Local source metadata; no runtime or flight verification",
        "host": {"os": platform.system(), "architecture": platform.machine(),
                 "python": platform.python_version(),
                 "ros_distro_in_this_shell": os.environ.get("ROS_DISTRO")},
        "commands_available_in_this_shell": {
            name: shutil.which(name) is not None
            for name in ("git", "cmake", "colcon", "ros2", "gz", "MicroXRCEAgent")
        },
        "errors": [],
    }
    for key, path, inspect in (("px4", args.px4, inspect_px4),
                               ("ros_workspace", args.ros_workspace, inspect_ros_workspace)):
        if path:
            try:
                report[key] = inspect(path)
            except (OSError, ValueError) as exc:
                report["errors"].append({"component": key, "error": str(exc)})
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
