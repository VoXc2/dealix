#!/usr/bin/env python3
"""Idempotent expansion — daily (wave2) or full weekly (wave4+28w)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _build_cmd(
    *,
    wave2: bool,
    wave3: bool,
    wave4: bool,
    meetings: int,
    touch_drafts: int,
    cycle_weeks: int,
    enrich: bool,
    skip_import: bool,
) -> list[str]:
    cmd = [
        sys.executable,
        str(ROOT / "scripts/expand_commercial_ops_all.py"),
        "--meetings",
        str(max(1, min(meetings, 15))),
        "--touch-drafts",
        str(max(1, min(touch_drafts, 20))),
        "--cycle-weeks",
        str(cycle_weeks),
    ]
    if wave4:
        cmd.append("--wave4")
    elif wave3:
        cmd.append("--wave3")
    elif wave2:
        cmd.append("--wave2")
    if enrich:
        cmd.append("--enrich-warm")
    if skip_import:
        cmd.append("--skip-import")
    return cmd


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--daily", action="store_true", help="Morning default: wave2 + 20w social")
    p.add_argument("--full", action="store_true", help="Weekly: wave4 + 28w + warm enrich")
    p.add_argument("--wave2", action="store_true")
    p.add_argument("--wave3", action="store_true")
    p.add_argument("--wave4", action="store_true")
    p.add_argument("--all", action="store_true", help="Alias for --daily")
    p.add_argument("--meetings", type=int, default=10)
    p.add_argument("--touch-drafts", type=int, default=15)
    p.add_argument("--skip-import", action="store_true")
    args = p.parse_args()

    if args.full:
        cmd = _build_cmd(
            wave2=False,
            wave3=False,
            wave4=True,
            meetings=args.meetings,
            touch_drafts=args.touch_drafts,
            cycle_weeks=28,
            enrich=True,
            skip_import=args.skip_import,
        )
    elif args.wave3:
        cmd = _build_cmd(
            wave2=False,
            wave3=True,
            wave4=False,
            meetings=args.meetings,
            touch_drafts=args.touch_drafts,
            cycle_weeks=24,
            enrich=True,
            skip_import=args.skip_import,
        )
    else:
        # daily default
        cmd = _build_cmd(
            wave2=args.wave2 or args.daily or args.all or True,
            wave3=False,
            wave4=args.wave4,
            meetings=args.meetings,
            touch_drafts=args.touch_drafts,
            cycle_weeks=20 if not args.wave4 else 28,
            enrich=args.wave2 or args.daily or args.all,
            skip_import=args.skip_import,
        )

    print("== expand_commercial_operating_stack ==")
    print(f"  >> {' '.join(cmd)}")
    rc = subprocess.call(cmd, cwd=ROOT)
    if rc != 0:
        print("\nCOMMERCIAL_STACK_EXPAND=FAIL")
        return rc
    print("\nCOMMERCIAL_STACK_EXPAND=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
