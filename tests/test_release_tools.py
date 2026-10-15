import ast
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

from test_helpers import ROOT, SKILL, installer, load

scorer = load("tracking_scorer", SKILL / "scripts" / "score_tracking.py")
packager = load("release_packager", ROOT / "scripts" / "package_release.py")


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def table(self, rows):
        path = self.root / "samples.csv"
        with path.open("w", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(scorer.SCHEMA)
            writer.writerows(rows)
        return path

    def run_score(self, path, **kwargs):
        options = {"start": 0, "end": 4, "max_gap": 2.1, "frame": "NED"}
        options.update(kwargs)
        return scorer.score(path, **options)

    def test_known_step_hand_calculation_and_artifact_identity(self):
        path = SKILL / "assets" / "examples" / "tracking-step.csv"
        result = self.run_score(path, step_axis="x", initial_target=0, tolerance=.05, dwell=1)
        self.assertAlmostEqual(result["vector_rmse_m"], math.sqrt(.55 / 4))
        self.assertAlmostEqual(result["step"]["overshoot_percent"], 10)
        self.assertEqual(result["step"]["settling_time_s"], 3)
        self.assertEqual(result["artifact_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_irregular_times_and_multiple_axes_are_time_weighted(self):
        path = self.table([[0, 0, 0, 0, 0, 0, 0, 1],
                           [1, 0, 0, 0, 2, 3, 0, 1],
                           [4, 0, 0, 0, 2, 3, 0, 1]])
        result = self.run_score(path, max_gap=3)
        # Squared x/y errors: [0, 4, 4] / [0, 9, 9]; areas 14 and 31.5.
        self.assertAlmostEqual(result["axis_rmse_m"]["x"], math.sqrt(14 / 4))
        self.assertAlmostEqual(result["vector_rmse_m"], math.sqrt(45.5 / 4))

    def test_negative_step_overshoot_uses_step_direction(self):
        path = self.table([[0, 0, 0, -1, 0, 0, 0, 1],
                           [2, 0, 0, -1, 0, 0, -1.2, 1],
                           [4, 0, 0, -1, 0, 0, -1, 1]])
        result = self.run_score(path, step_axis="z", initial_target=0, tolerance=.05, dwell=1)
        self.assertAlmostEqual(result["step"]["overshoot_percent"], 20)
        self.assertIsNone(result["step"]["settling_time_s"])
        self.assertEqual(result["step"]["status"], "not_settled_within_horizon")

    def test_transient_entry_followed_by_excursion_does_not_count_as_settled(self):
        path = self.table([[0, 1, 0, 0, 0, 0, 0, 1],
                           [1, 1, 0, 0, 1, 0, 0, 1],
                           [2, 1, 0, 0, 1, 0, 0, 1],
                           [3, 1, 0, 0, 1.5, 0, 0, 1],
                           [4, 1, 0, 0, 1, 0, 0, 1]])
        result = self.run_score(path, step_axis="x", initial_target=0, tolerance=.05, dwell=1)
        self.assertIsNone(result["step"]["settling_time_s"])

    def test_invalid_nonfinite_duplicate_and_gap_are_rejected(self):
        clean = [[0, 1, 0, 0, 0, 0, 0, 1], [2, 1, 0, 0, 1, 0, 0, 1], [4, 1, 0, 0, 1, 0, 0, 1]]
        for key, value in [(7, 0), (4, "nan"), (0, 0)]:
            rows = [r[:] for r in clean]
            rows[1][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.run_score(self.table(rows))
        with self.assertRaises(ValueError):
            self.run_score(self.table(clean), max_gap=1)

    def test_window_boundaries_moving_step_and_zero_step_rejected(self):
        path = SKILL / "assets" / "examples" / "tracking-step.csv"
        for kwargs in [{"start": .5}, {"end": 3.5},
                       {"step_axis": "x", "initial_target": 1, "tolerance": .1, "dwell": 1}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.run_score(path, **kwargs)
        moving = self.table([[0, 1, 0, 0, 0, 0, 0, 1], [4, 2, 0, 0, 1, 0, 0, 1]])
        with self.assertRaises(ValueError):
            self.run_score(moving, max_gap=4, step_axis="x", initial_target=0, tolerance=.1, dwell=1)

    def test_invalid_outside_window_not_silently_used_or_zero_filled(self):
        path = self.table([[-1, 0, 0, 0, "nan", 0, 0, 0],
                           [0, 0, 0, 0, 1, 0, 0, 1], [4, 0, 0, 0, 1, 0, 0, 1]])
        self.assertEqual(self.run_score(path, max_gap=4)["vector_rmse_m"], 1)

    def test_cli_invalid_input_is_nonzero_json_without_success_metrics(self):
        path = self.table([[0, 0, 0, 0, "nan", 0, 0, 1], [4, 0, 0, 0, 1, 0, 0, 1]])
        completed = subprocess.run([sys.executable, str(SKILL / "scripts/score_tracking.py"),
                                    str(path), "--start", "0", "--end", "4", "--max-gap", "4", "--frame", "NED"],
                                   capture_output=True, text=True)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(set(json.loads(completed.stdout)), {"error"})


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skills = self.root / "skills"

    def test_update_preserves_old_content_outside_skill_discovery(self):
        target = installer.install(self.skills)
        (target / "user-note").write_text("preserve")
        updated = installer.install(self.skills, update=True)
        self.assertFalse((updated / "user-note").exists())
        backups = list((self.root / "flightdeck-backups").glob("*/px4-flightdeck/user-note"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "preserve")
        self.assertEqual(list(self.skills.iterdir()), [updated])

    def test_failed_update_restores_previous_installation(self):
        target = installer.install(self.skills)
        (target / "user-note").write_text("keep after copy failure")
        with mock.patch.object(installer.shutil, "copytree", side_effect=OSError("copy failed")):
            with self.assertRaises(OSError):
                installer.install(self.skills, update=True)
        self.assertEqual((target / "user-note").read_text(), "keep after copy failure")
        self.assertTrue((target / "SKILL.md").is_file())


class ReleaseTests(unittest.TestCase):
    def test_archives_are_reproducible_and_standalone_installs_without_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, standalone, sums = packager.package(root / "artifacts")
            original = [p.read_bytes() for p in (source, standalone, sums)]
            packager.package(root / "artifacts")
            self.assertEqual(original, [p.read_bytes() for p in (source, standalone, sums)])
            for archive in (source, standalone):
                with zipfile.ZipFile(archive) as z:
                    self.assertIsNone(z.testzip())
                    for name in z.namelist():
                        self.assertFalse(Path(name).is_absolute())
                        self.assertNotIn("..", Path(name).parts)
                        self.assertNotIn("__pycache__", Path(name).parts)
                        self.assertNotIn(".git", Path(name).parts)
                    destination = root / ("source" if archive == source else "standalone")
                    z.extractall(destination)
            # The source archive's installer must work from its extracted location.
            subprocess.run([sys.executable, str(root / "source/px4-flightdeck/scripts/install.py"),
                            "--skills-dir", str(root / "installed")], check=True, capture_output=True)
            installed = root / "installed/px4-flightdeck"
            standalone_root = root / "standalone/px4-flightdeck"
            for file in installed.rglob("*"):
                if file.is_file():
                    counterpart = standalone_root / file.relative_to(installed)
                    self.assertTrue(counterpart.is_file(), str(counterpart))
                    self.assertEqual(file.read_bytes(), counterpart.read_bytes())
            self.assertTrue((installed / "assets/examples/px4-module/LICENSE").is_file())
            self.assertTrue((installed / "assets/examples/ros2-observer/package.xml").is_file())

    def test_all_distributed_python_sources_parse_on_current_interpreter(self):
        # Includes ROS-dependent sources without pretending to import/run ROS.
        for folder in ("scripts", "skills"):
            for file in (ROOT / folder).rglob("*.py"):
                with self.subTest(file=file):
                    ast.parse(file.read_text(), filename=str(file), feature_version=(3, 9))


if __name__ == "__main__":
    unittest.main()
