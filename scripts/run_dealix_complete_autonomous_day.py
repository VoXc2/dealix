#!/usr/bin/env python3
"""Maximum governed autonomous day — CLI entry (see complete_autonomous_day.py)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.complete_autonomous_day import (  # noqa: E402
    build_complete_autonomous_plan,
    run_complete_autonomous_day,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-commercial-day", action="store_true")
    p.add_argument("--evening", action="store_true")
    p.add_argument("--weekly", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument(
        "--subprocess-only",
        action="store_true",
        help="Skip in-process unified day (shell commercial day only)",
    )
    args = p.parse_args()

    if args.dry_run:
        plan = build_complete_autonomous_plan(
            weekly=args.weekly,
            evening=args.evening,
            skip_commercial_day=args.skip_commercial_day,
        )
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        print("DEALIX_COMPLETE_AUTONOMOUS_DAY=DRY_RUN")
        return 0

    payload = run_complete_autonomous_day(
        weekly=args.weekly,
        evening=args.evening,
        skip_commercial_day=args.skip_commercial_day,
        use_unified_in_process=not args.subprocess_only,
    )
    verdict = payload.get("verdict", "DEGRADED")
    print(f"\nDEALIX_COMPLETE_AUTONOMOUS_DAY_VERDICT={verdict}")
    print(f"ARTIFACT={payload.get('artifact_path')}")
    print(f"STRONGEST_OPS={(payload.get('strongest_ops') or {}).get('verdict')}")

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 1 if verdict == "FAIL_WIRING" else 0


if __name__ == "__main__":
    raise SystemExit(main())
