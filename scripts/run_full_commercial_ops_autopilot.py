#!/usr/bin/env python3
"""Full autonomous commercial ops — snapshot or execute morning core (governed)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--execute", action="store_true", help="Run morning core pipeline")
    p.add_argument("--top-n", type=int, default=15)
    p.add_argument("--no-scripts", action="store_true", help="Skip optional verify scripts")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    from dealix.commercial_ops.full_ops_autopilot import (
        build_full_autonomous_ops_snapshot,
        run_morning_core,
    )

    snap = build_full_autonomous_ops_snapshot(
        top_n=max(1, min(args.top_n, 30)),
        include_nested=False,
        include_value_plan=False,
    )
    if args.execute:
        snap["morning_run"] = run_morning_core(
            top_n=args.top_n,
            run_optional_scripts=not args.no_scripts,
        )

    if args.json:
        print(json.dumps(snap, ensure_ascii=False, indent=2))
    else:
        ar = snap["automation_readiness"]
        print(f"DEALIX_FULL_AUTONOMOUS_OPS={ar['verdict']}")
        print(f"track={(snap['gtm_stack']['dual_track'] or {}).get('recommended_track')}")
        for line in ar.get("blockers_ar") or []:
            print(f"blocker: {line}")
        for line in snap.get("founder_only_actions_ar") or []:
            print(f"founder: {line}")
        if args.execute:
            print(f"morning_run={(snap.get('morning_run') or {}).get('verdict')}")

    return 0 if ar["verdict"] != "BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
