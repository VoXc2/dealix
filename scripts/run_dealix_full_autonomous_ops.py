#!/usr/bin/env python3
"""Maximum governed autonomous ops — delegates to complete_autonomous_day (canonical)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.autonomous_ops import build_autonomous_ops_status  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--status-only", action="store_true")
    p.add_argument("--quick", action="store_true", help="Expansion + status only (no full day)")
    p.add_argument("--skip-commercial-day", action="store_true")
    p.add_argument("--evening", action="store_true")
    p.add_argument("--weekly", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.status_only:
        print(json.dumps(build_autonomous_ops_status(), ensure_ascii=False, indent=2))
        return 0

    if args.quick:
        cmd = [
            sys.executable,
            str(ROOT / "scripts/expand_commercial_ops_all.py"),
            "--wave4",
            "--cycle-weeks",
            "28",
            "--enrich-warm",
        ]
        proc = subprocess.run(cmd, cwd=ROOT)
        if proc.returncode != 0:
            print("COMMERCIAL_EXPANSION_VERDICT=FAIL")
            return 1
        subprocess.run([sys.executable, str(ROOT / "scripts/founder_expansion_status.py")], cwd=ROOT)
        print("COMMERCIAL_EXPANSION_VERDICT=PASS")
        return 0

    cmd = [sys.executable, str(ROOT / "scripts/run_dealix_complete_autonomous_day.py")]
    if args.dry_run:
        cmd.append("--dry-run")
    if args.skip_commercial_day:
        cmd.append("--skip-commercial-day")
    if args.evening:
        cmd.append("--evening")
    if args.weekly:
        cmd.append("--weekly")
    if args.json:
        cmd.append("--json")

    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode != 0:
        print("DEALIX_FULL_AUTONOMOUS_OPS_VERDICT=FAIL")
        return proc.returncode
    print("DEALIX_FULL_AUTONOMOUS_OPS_VERDICT=PASS")
    print("Canonical: scripts/run_dealix_complete_autonomous_day.py")
    print("UI: POST /api/v1/ops-autopilot/founder/complete-autonomous-day/run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
