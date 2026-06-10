#!/usr/bin/env python3
"""Autonomous strongest-plan ops — morning / evening / weekly / full."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_strongest_ops import (  # noqa: E402
    build_strongest_ops_snapshot,
    run_strongest_ops,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--morning",
        action="store_true",
        help="Daily morning brief + weekly decision init if needed",
    )
    p.add_argument("--evening", action="store_true", help="Evening evidence nudge")
    p.add_argument("--weekly", action="store_true", help="Weekly scorecard + full task sections")
    p.add_argument(
        "--full",
        action="store_true",
        help="All sections + run status scripts",
    )
    p.add_argument("--run-checks", action="store_true", help="Execute verify scripts")
    p.add_argument("--json", action="store_true", help="Print full JSON snapshot")
    args = p.parse_args()

    if args.full:
        mode = "full"
    elif args.weekly:
        mode = "weekly"
    elif args.evening:
        mode = "evening"
    else:
        mode = "morning"

    run_checks = args.run_checks or args.full or args.weekly
    snap = run_strongest_ops(mode=mode, run_checks=run_checks, write_brief=True)
    paths = snap.get("brief_paths") or {}

    print(f"FOUNDER_STRONGEST_OPS_VERDICT={snap.get('verdict')}")
    print(f"FOUNDER_STRONGEST_OPS_MODE={mode}")
    print(f"BRIEF_MD={paths['markdown']}")
    print(f"BRIEF_JSON={paths['json']}")
    print(f"TASKS_TODAY={snap.get('tasks_today_count')}")

    if args.json:
        print(json.dumps(snap, ensure_ascii=False, indent=2))

    return 0 if snap.get("verdict") != "FAIL_WIRING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
