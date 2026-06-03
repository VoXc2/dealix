#!/usr/bin/env python3
"""Full commercial expansion + gates — canonical entry (delegates to expand_commercial_ops_all)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _run(cmd: list[str], *, label: str, fail_on_error: bool = True) -> int:
    print(f"\n== {label} ==")
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode != 0:
        msg = f"FAIL: {label} exit={proc.returncode}"
        print(msg)
        if fail_on_error:
            return proc.returncode
    return proc.returncode


def _py(*args: str) -> list[str]:
    return [sys.executable, *args]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--wave2", action="store_true", help="150 targeting rows")
    p.add_argument("--wave3", action="store_true", help="200 targeting rows")
    p.add_argument("--wave4", action="store_true", help="250 targeting rows (max pool)")
    p.add_argument(
        "--full",
        action="store_true",
        help="Wave4 + 28w social + warm enrich + all motion briefs (default if no wave flag)",
    )
    p.add_argument("--skip-gates", action="store_true")
    p.add_argument("--skip-go-live", action="store_true")
    p.add_argument("--with-founder-day", action="store_true")
    p.add_argument("--meetings", type=int, default=10)
    p.add_argument("--touch-drafts", type=int, default=20)
    args = p.parse_args()

    full = args.full or not (args.wave2 or args.wave3 or args.wave4)

    expand_cmd = [
        str(ROOT / "scripts/expand_commercial_ops_all.py"),
        "--meetings",
        str(max(1, min(args.meetings, 15))),
        "--touch-drafts",
        str(max(1, min(args.touch_drafts, 25))),
        "--cycle-weeks",
        "28",
        "--enrich-warm",
    ]
    if args.wave2:
        expand_cmd.append("--wave2")
    elif args.wave3:
        expand_cmd.append("--wave3")
    elif args.wave4 or full:
        expand_cmd.append("--wave4")

    fail = 0
    if _run(_py(*expand_cmd), label="expand_commercial_ops_all") != 0:
        fail = 1

    _run(_py("scripts/founder_expansion_status.py"), label="expansion status", fail_on_error=False)

    if not args.skip_gates:
        for label, script in (
            ("launch strict", ["scripts/verify_commercial_launch_ready.py", "--strict"]),
            ("FE/BE", ["scripts/verify_commercial_fe_be.py"]),
            ("soft-to-paid", ["scripts/founder_paid_launch_gate.py"]),
        ):
            if _run(_py(*script), label=label) != 0:
                fail = 1

        if not args.skip_go_live and sys.platform == "win32":
            if (
                _run(
                    ["powershell", "-File", "scripts/verify_dealix_commercial_go_live.ps1"],
                    label="unified go-live",
                )
                != 0
            ):
                fail = 1
        elif not args.skip_go_live:
            if _run(["bash", "scripts/verify_dealix_commercial_go_live.sh"], label="unified go-live") != 0:
                fail = 1

    if args.with_founder_day:
        if sys.platform == "win32":
            if (
                _run(
                    ["powershell", "-File", "scripts/run_founder_commercial_day.ps1"],
                    label="founder commercial day",
                )
                != 0
            ):
                fail = 1
        elif _run(["bash", "scripts/run_founder_commercial_day.sh"], label="founder commercial day") != 0:
            fail = 1

    if fail:
        print("\nCOMMERCIAL_EXPANSION_VERDICT=FAIL")
        return 1
    print("\nCOMMERCIAL_EXPANSION_VERDICT=PASS")
    print("Morning: powershell -File scripts/founder_morning.ps1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
