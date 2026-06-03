#!/usr/bin/env python3
"""Recompute the Ready-to-Launch score and fail if below the launch threshold.

Threshold defaults to 75 (Soft Launch Ready). Override with --min.
"""
import argparse

import _bootstrap  # noqa: F401
from dealix.lib import ROOT, CheckResult
from dealix.cli import band, compute_launch_score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=float, default=75.0)
    args = ap.parse_args()

    r = CheckResult("ready_to_launch_scorecard")
    rows, total = compute_launch_score()
    for name, earned, weight, present, n in rows:
        (r.ok if present == n else r.fail)(f"{name}: {earned}/{weight} ({present}/{n} files)")
    scorecard = ROOT / "reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md"
    if not scorecard.exists():
        r.fail("scorecard report not generated (run: python dealix.py launch-score)")
    print(f"  -> launch score: {total}/100 = {band(total)}")
    if total < args.min:
        r.fail(f"launch score {total} < required {args.min} ({band(total)})")
    return r.finish()


if __name__ == "__main__":
    main()
