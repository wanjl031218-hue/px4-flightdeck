#!/usr/bin/env python3
"""Score an explicitly selected, valid CSV tracking window; standard library only."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

SCHEMA = ("t_s", "target_x_m", "target_y_m", "target_z_m", "x_m", "y_m", "z_m", "valid")
SCORER_VERSION = "1"


def finite(value, name):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(name + " must be finite")
    return number


def score(path, *, start, end, max_gap, frame, step_axis=None,
          initial_target=None, tolerance=None, dwell=None):
    start, end, max_gap = (finite(v, n) for v, n in
                           [(start, "start"), (end, "end"), (max_gap, "max_gap")])
    if end <= start or max_gap <= 0:
        raise ValueError("Require end > start and max_gap > 0")
    if frame not in ("NED", "ENU"):
        raise ValueError("Declare frame as NED or ENU after aligning target and measurement")
    path = Path(path)
    raw = path.read_bytes()
    rows = []
    previous = None
    # Read exactly the bytes whose hash is reported, even if the source changes later.
    reader = csv.DictReader(raw.decode("utf-8-sig").splitlines())
    if reader.fieldnames is None or len(set(reader.fieldnames)) != len(reader.fieldnames):
        raise ValueError("Missing or duplicate CSV headers")
    if set(SCHEMA) - set(reader.fieldnames):
        raise ValueError("Required columns: " + ",".join(SCHEMA))
    for line, item in enumerate(reader, 2):
        t = finite(item["t_s"], "timestamp at row " + str(line))
        if previous is not None and t <= previous:
            raise ValueError("Timestamps must strictly increase, including outside the window")
        previous = t
        if not start <= t <= end:
            continue
        if item["valid"] != "1":
            raise ValueError("Window contains an invalid sample at row " + str(line))
        values = [finite(item[key], key + " at row " + str(line)) for key in SCHEMA[1:7]]
        rows.append((t, values[:3], values[3:]))
    if len(rows) < 2:
        raise ValueError("Need at least two samples in the selected window")
    # No interpolation/extrapolation at requested window boundaries.
    if not math.isclose(rows[0][0], start, rel_tol=0, abs_tol=1e-9) or not math.isclose(
            rows[-1][0], end, rel_tol=0, abs_tol=1e-9):
        raise ValueError("Window start/end must coincide with recorded timestamps")
    gaps = [b[0] - a[0] for a, b in zip(rows, rows[1:])]
    if max(gaps) > max_gap:
        raise ValueError("Window exceeds max_gap; segment or recollect instead of bridging the gap")
    errors = [[actual - target for actual, target in zip(row[2], row[1])] for row in rows]
    duration = end - start
    axis_rmse = [math.sqrt(sum(dt * (a[k] ** 2 + b[k] ** 2) / 2
                                    for dt, a, b in zip(gaps, errors, errors[1:])) / duration)
                 for k in range(3)]
    result = {
        "scorer_version": SCORER_VERSION,
        "artifact_sha256": hashlib.sha256(raw).hexdigest(),
        "frame_declared_by_caller": frame,
        "window_s": [start, end], "samples": len(rows),
        "duration_s": duration, "max_observed_gap_s": max(gaps),
        "weighting": "trapezoidal integration of sampled squared errors / duration",
        "axis_rmse_m": dict(zip("xyz", axis_rmse)),
        "vector_rmse_m": math.hypot(*axis_rmse),
        "peak_vector_error_m": max(math.hypot(*e) for e in errors),
        "step": None,
    }
    if step_axis is not None:
        if step_axis not in "xyz" or len(step_axis) != 1:
            raise ValueError("step_axis must be x, y or z")
        if initial_target is None or tolerance is None or dwell is None:
            raise ValueError("Step scoring needs initial_target, tolerance and dwell")
        initial_target = finite(initial_target, "initial_target")
        tolerance, dwell = finite(tolerance, "tolerance"), finite(dwell, "dwell")
        if tolerance <= 0 or dwell <= 0:
            raise ValueError("tolerance and dwell must be > 0")
        k = "xyz".index(step_axis)
        final = rows[0][1][k]
        if any(not math.isclose(r[1][k], final, rel_tol=0, abs_tol=1e-9) for r in rows):
            raise ValueError("Step-axis target must be constant throughout the post-step window")
        step = final - initial_target
        if step == 0:
            raise ValueError("A zero target step has no percentage overshoot")
        sign = 1 if step > 0 else -1
        overshoot = max(0.0, max(sign * (r[2][k] - final) for r in rows))
        last_outside = max((i for i, e in enumerate(errors) if abs(e[k]) > tolerance), default=-1)
        first = last_outside + 1
        settled = first < len(rows) and end - rows[first][0] >= dwell
        result["step"] = {
            "axis": step_axis, "initial_target_m": initial_target, "final_target_m": final,
            "event_time_s": start, "tolerance_m": tolerance, "dwell_s": dwell,
            "overshoot_m": overshoot, "overshoot_percent": 100 * overshoot / abs(step),
            "settling_time_s": rows[first][0] - start if settled else None,
            "status": "settled_in_observed_samples" if settled else "not_settled_within_horizon",
            "settling_rule": "first sampled entry that remains within tolerance through window end for >= dwell",
        }
    elif any(v is not None for v in (initial_target, tolerance, dwell)):
        raise ValueError("Step options require step_axis")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--start", type=float, required=True, help="Window start; step event time if scoring a step")
    parser.add_argument("--end", type=float, required=True)
    parser.add_argument("--max-gap", type=float, required=True)
    parser.add_argument("--frame", choices=["NED", "ENU"], required=True)
    parser.add_argument("--step-axis", choices=list("xyz"))
    parser.add_argument("--initial-target", type=float)
    parser.add_argument("--tolerance", type=float)
    parser.add_argument("--dwell", type=float)
    args = parser.parse_args(argv)
    try:
        result = score(args.csv, start=args.start, end=args.end, max_gap=args.max_gap,
                       frame=args.frame, step_axis=args.step_axis,
                       initial_target=args.initial_target, tolerance=args.tolerance, dwell=args.dwell)
    except (OSError, ValueError, TypeError, csv.Error, OverflowError) as exc:
        print(json.dumps({"error": str(exc)}, allow_nan=False))
        return 1
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
