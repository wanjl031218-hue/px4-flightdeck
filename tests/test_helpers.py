import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "px4-flightdeck"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inspector = load("workspace_inspector", SKILL / "scripts" / "inspect_workspace.py")
installer = load("local_installer", ROOT / "scripts" / "install.py")


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def px4_root(self, root):
        root.mkdir(parents=True, exist_ok=True)
        (root / "CMakeLists.txt").write_text("# fixture\n")
        for d in ("src/modules", "boards", "msg"):
            (root / d).mkdir(parents=True)
        return root

    def test_source_export_is_not_runtime_verification(self):
        root = self.px4_root(self.root / "px4")
        report = inspector.inspect_px4(root)
        self.assertIsNone(report["git"]["commit"])
        self.assertIsNone(report["runtime_version"])

    def test_wrong_px4_directory_rejected(self):
        with self.assertRaises(ValueError):
            inspector.inspect_px4(self.root)

    @unittest.skipUnless(shutil.which("git"), "Git not installed")
    def test_parent_git_identity_is_not_attributed_to_source_export(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        source = self.px4_root(self.root / "exported_px4")
        report = inspector.inspect_px4(source)
        self.assertIsNone(report["git"]["commit"])
        self.assertIn("parent", report["git"]["note"])

    @unittest.skipUnless(shutil.which("git"), "Git not installed")
    def test_git_checkout_identity_and_tracked_change(self):
        source = self.px4_root(self.root / "px4")
        subprocess.run(["git", "init", "-q", str(source)], check=True)
        subprocess.run(["git", "-C", str(source), "add", "CMakeLists.txt"], check=True)
        subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                        "-C", str(source), "commit", "-qm", "fixture"], check=True)
        clean = inspector.inspect_px4(source)
        self.assertRegex(clean["git"]["commit"], r"^[a-f0-9]{40,64}$")
        self.assertFalse(clean["git"]["tracked_changes"])
        (source / "CMakeLists.txt").write_text("# modified\n")
        self.assertTrue(inspector.inspect_px4(source)["git"]["tracked_changes"])

    def test_ros_manifest_read_without_executing_package_or_generated_trees(self):
        pkg = self.root / "src" / "demo"
        pkg.mkdir(parents=True)
        (pkg / "package.xml").write_text("<package><name>demo</name><version>0.1</version></package>")
        (pkg / "setup.py").write_text("raise RuntimeError('must not execute')")
        ignored = self.root / "src" / "build" / "bad"
        ignored.mkdir(parents=True)
        (ignored / "package.xml").write_text("bad XML")
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        report = inspector.inspect_ros_workspace(self.root)
        after = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        self.assertEqual([p["name"] for p in report["packages"]], ["demo"])
        self.assertEqual(report["manifest_errors"], [])
        self.assertIsNone(report["runtime_build"])
        self.assertEqual(before, after)

    def test_bad_manifest_is_reported_without_losing_other_packages(self):
        for name, text in [("good", "<package><name>good</name></package>"), ("bad", "<bad")]:
            pkg = self.root / "src" / name
            pkg.mkdir(parents=True)
            (pkg / "package.xml").write_text(text)
        report = inspector.inspect_ros_workspace(self.root)
        self.assertEqual(len(report["packages"]), 1)
        self.assertEqual(len(report["manifest_errors"]), 1)

    def test_cli_error_is_structured_and_nonzero(self):
        result = subprocess.run([sys.executable, str(SKILL / "scripts" / "inspect_workspace.py"),
                                 "--px4", str(self.root / "missing")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["errors"][0]["component"], "px4")


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_copy_is_self_contained_and_preserves_existing_install(self):
        target = installer.install(self.root)
        self.assertTrue((target / "LICENSE").is_file())
        self.assertEqual((target / "SKILL.md").read_bytes(), (SKILL / "SKILL.md").read_bytes())
        (target / "local-note.txt").write_text("keep")
        with self.assertRaises(FileExistsError):
            installer.install(self.root)
        self.assertEqual((target / "local-note.txt").read_text(), "keep")

    def test_link_is_idempotent_and_keeps_source(self):
        try:
            target = installer.install(self.root, link=True)
        except OSError as exc:
            self.skipTest("Symlinks unavailable: " + str(exc))
        self.assertEqual(target.resolve(), SKILL)
        self.assertEqual(installer.install(self.root, link=True), target)
        target.unlink()
        self.assertTrue((SKILL / "SKILL.md").is_file())

    def test_dangling_symlink_is_not_overwritten(self):
        target = self.root / installer.SKILL_NAME
        try:
            target.symlink_to(self.root / "missing", target_is_directory=True)
        except OSError as exc:
            self.skipTest("Symlinks unavailable: " + str(exc))
        with self.assertRaises(FileExistsError):
            installer.install(self.root)
        self.assertTrue(target.is_symlink())


class PackageTests(unittest.TestCase):
    def test_disclosed_local_references_resolve(self):
        for file in ROOT.rglob("*.md"):
            if ".git" in file.parts:
                continue
            for target in re.findall(r"\]\(([^\s)]+)\)", file.read_text()):
                if "://" in target or target.startswith(("#", "mailto:", "tel:")):
                    continue
                relative = target.split("#", 1)[0]
                self.assertTrue((file.parent / relative).exists(), str(file) + ": " + target)


if __name__ == "__main__":
    unittest.main()
