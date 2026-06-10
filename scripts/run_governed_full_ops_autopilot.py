#!/usr/bin/env python3
"""Canonical alias — governed full ops → founder full autopilot (single pipeline)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser(
        description="Delegates to scripts/run_founder_full_autopilot.py (governed, draft-only)."
    )
    p.add_argument("--morning", action="store_true")
    p.add_argument("--evening", action="store_true")
    p.add_argument("--full", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-gates", action="store_true", help="Ignored — use founder_full_autopilot flags")
    p.add_argument("--skip-expand", action="store_true", help="Ignored")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.dry_run:
        mode = "morning"
        if args.evening:
            mode = "evening"
        elif args.full:
            mode = "full"
        cmd = [
            sys.executable,
            str(ROOT / "scripts/run_founder_full_autopilot.py"),
            "--dry-run",
            "--mode",
            mode,
        ]
        if args.json:
            cmd.append("--json")
        print("== governed_full_ops_autopilot (delegate) ==")
        return subprocess.call(cmd, cwd=ROOT)
    elif args.evening:
        cmd = [sys.executable, str(ROOT / "scripts/run_founder_full_autopilot.py"), "--mode", "evening"]
    elif args.morning:
        cmd = [sys.executable, str(ROOT / "scripts/run_founder_full_autopilot.py"), "--mode", "morning"]
    elif args.full:
        cmd = [sys.executable, str(ROOT / "scripts/run_founder_full_autopilot.py"), "--mode", "full"]
    else:
        cmd = [sys.executable, str(ROOT / "scripts/run_founder_full_autopilot.py"), "--mode", "morning"]

    print("== governed_full_ops_autopilot (delegate) ==")
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
