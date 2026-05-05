#!/usr/bin/env python3
"""Run the safety_v10 red-team eval pack and print a bilingual report.

Usage:
    python scripts/run_safety_v10.py
    python scripts/run_safety_v10.py --json

Exit codes:
    0  every case reached its expected action
    1  at least one case failed (policy gap)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# Ensure the repo root is on sys.path when invoked directly.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run safety_v10 red-team eval pack")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of bilingual markdown",
    )
    args = parser.parse_args()

    from auto_client_acquisition.safety_v10 import (
        render_report,
        run_safety_eval,
    )

    report = run_safety_eval()

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_report(report))
        # Also print a plain summary table
        print("\n=== Bilingual summary / ملخّص ===")
        print(f"total={report.total} passed={report.passed} failed={report.failed}")

    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
