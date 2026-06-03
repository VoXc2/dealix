#!/usr/bin/env python3
"""Run governed founder full autopilot loop (morning optional + brief + status)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_full_autopilot import (  # noqa: E402
    build_autopilot_snapshot,
    write_autopilot_brief,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def _run(cmd: list[str]) -> int:
    proc = subprocess.run(cmd, cwd=ROOT)
    return int(proc.returncode)


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--mode",
        choices=("full", "morning", "evening", "weekly", "brief-only"),
        default="full",
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-morning", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    fail = 0
    if args.dry_run:
        snap = build_autopilot_snapshot()
        if args.json:
            import json

            print(json.dumps(snap, ensure_ascii=False, indent=2))
        else:
            print("FOUNDER_FULL_AUTOPILOT=DRY_RUN")
            print(f"  verdict: {(snap.get('verdict') or {}).get('level')}")
            print(f"  queue_len: {len(snap.get('queue') or [])}")
        print("FOUNDER_FULL_AUTOPILOT_VERDICT=OK")
        return 0

    mode = args.mode
    if mode in ("full", "morning") and not args.skip_morning:
        # Pool + social (idempotent, wave2 daily)
        _run(
            [
                sys.executable,
                str(ROOT / "scripts/expand_commercial_operating_stack.py"),
                "--daily",
            ]
        )
        import os

        daily_ops = [sys.executable, str(ROOT / "scripts/run_dealix_daily_ops.py")]
        if os.environ.get("DEALIX_ADMIN_API_KEY"):
            daily_ops.append("--api-only")
        else:
            daily_ops.append("--skip-api")
        _run(daily_ops)
        # Canonical autonomous core (War Room, packs, digest, optional verifies)
        rc = _run(
            [
                sys.executable,
                str(ROOT / "scripts/run_full_commercial_ops_autopilot.py"),
                "--execute",
            ]
        )
        if rc != 0:
            fail = rc

    if mode in ("full", "evening"):
        rc = _run([sys.executable, str(ROOT / "scripts/founder_evening_evidence.py")])
        if rc != 0 and mode == "evening":
            fail = rc

    if mode in ("full", "weekly"):
        from datetime import UTC, datetime

        if datetime.now(UTC).weekday() == 4 or mode == "weekly":
            if sys.platform == "win32":
                _run(
                    [
                        "powershell",
                        "-File",
                        str(ROOT / "scripts/founder_cadence.ps1"),
                        "-Weekly",
                    ]
                )
            else:
                _run(["bash", str(ROOT / "scripts/founder_cadence.sh"), "--weekly"])

    brief_path = write_autopilot_brief()
    snap = build_autopilot_snapshot()

    if args.json:
        import json

        out = {**snap, "brief_path": str(brief_path.relative_to(ROOT)).replace("\\", "/")}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        v = snap.get("verdict") or {}
        print("== Founder Full Autopilot ==")
        print(f"  verdict: {v.get('level')} — {v.get('summary_ar')}")
        print(f"  brief: {brief_path.relative_to(ROOT)}")
        for item in snap.get("queue") or []:
            print(f"  [{item.get('priority')}] {item.get('title_ar')}")

    print("FOUNDER_FULL_AUTOPILOT_VERDICT=OK" if fail == 0 else "FOUNDER_FULL_AUTOPILOT_VERDICT=PARTIAL")
    return fail


if __name__ == "__main__":
    raise SystemExit(main())
