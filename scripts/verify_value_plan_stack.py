#!/usr/bin/env python3
"""Run all Value Plan verification gates (soft + modules + pytest slice)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []


def _run(label: str, cmd: list[str]) -> None:
    print(f"\n== {label} ==")
    r = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        FAILURES.append(label)


def main() -> int:
    py = sys.executable
    _run("commercial_launch_ready", [py, str(ROOT / "scripts/verify_commercial_launch_ready.py")])
    _run("first_paid_tracker", [py, str(ROOT / "scripts/verify_first_paid_diagnostic_tracker.py")])
    _run("paid_launch_readiness", [py, str(ROOT / "scripts/verify_paid_launch_readiness.py")])
    _run(
        "value_plan_pytest",
        [
            py,
            "-m",
            "pytest",
            "tests/test_value_plan_ops.py",
            "tests/test_commercial_value_map_status.py",
            "tests/test_founder_daily_pack_api.py",
            "-q",
            "--no-cov",
        ],
    )
    _run("commercial_value_map_status", [py, str(ROOT / "scripts/commercial_value_map_status.py")])
    _run("value_plan_snapshot", [py, str(ROOT / "scripts/export_value_plan_snapshot.py")])

    if FAILURES:
        print("\nVALUE_PLAN_STACK: FAIL")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("\nVALUE_PLAN_STACK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
