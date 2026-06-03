#!/usr/bin/env python3
"""CEO Master Plan status — unified PASS/FAIL for all 6 plan workstreams."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.ceo_master_plan import (  # noqa: E402
    analyze_ceo_master_plan,
    build_ceo_master_plan_snapshot,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    blob = build_ceo_master_plan_snapshot()

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== CEO Master Plan Status ==")
        for key in (
            "p0_revenue_close",
            "p0_production_trust",
            "p0_ceo_decision",
            "p0_gtm_blitz",
            "p1_trust_pack",
            "p2_repeatability",
        ):
            ws = blob[key]
            print(f"  {key}: {ws['verdict']}")
        print(f"\nCEO_MASTER_PLAN_VERDICT={blob['overall_verdict']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
