#!/usr/bin/env python3
"""Single canonical founder day — strongest ops + morning core + commercial day (governed)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.commercial_ops.unified_founder_day import run_unified_founder_day  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--quick", action="store_true", help="Skip full commercial day shell script")
    p.add_argument("--top-n", type=int, default=15)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    payload = run_unified_founder_day(
        quick=args.quick,
        top_n=args.top_n,
        run_commercial_subprocess=not args.quick,
    )

    print(f"\nDEALIX_UNIFIED_FOUNDER_DAY_VERDICT={payload['verdict']}")
    for ph in payload.get("phases") or []:
        print(f"  - {ph.get('label')}: {ph.get('verdict')}")
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
