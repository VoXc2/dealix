#!/usr/bin/env python3
"""Run full commercial expansion — delegates to expand_commercial_ops_all (idempotent)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--wave2", action="store_true", help="150 targeting rows")
    p.add_argument("--wave3", action="store_true", help="200 targeting rows")
    p.add_argument("--wave4", action="store_true", help="250 targeting + 28w social + all motions")
    p.add_argument(
        "--all",
        action="store_true",
        help="Maximum governed expansion (wave4 + 28w, default)",
    )
    p.add_argument("--meetings", type=int, default=12)
    p.add_argument("--touch-drafts", type=int, default=25)
    p.add_argument("--skip-import", action="store_true")
    args = p.parse_args()

    if not (args.wave2 or args.wave3 or args.wave4 or args.all):
        args.all = True

    cycle_weeks = "28" if (args.wave4 or args.all) else "24"
    cmd = [
        sys.executable,
        str(ROOT / "scripts/expand_commercial_ops_all.py"),
        "--meetings",
        str(max(1, min(args.meetings, 15))),
        "--touch-drafts",
        str(max(1, min(args.touch_drafts, 25))),
        "--cycle-weeks",
        cycle_weeks,
    ]
    if args.wave4 or args.all:
        cmd.extend(["--wave4", "--enrich-warm"])
    elif args.wave3:
        cmd.extend(["--wave3", "--enrich-warm"])
    elif args.wave2:
        cmd.append("--wave2")
    if args.skip_import:
        cmd.append("--skip-import")

    print("== expand_commercial_stack ==")
    rc = subprocess.call(cmd, cwd=ROOT)
    if rc != 0:
        print("\nEXPAND_COMMERCIAL_STACK=FAIL")
        return rc
    print("\nEXPAND_COMMERCIAL_STACK=OK")
    print("Next: powershell -File scripts/founder_morning.ps1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
