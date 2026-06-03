#!/usr/bin/env python3
"""Print GTM Blitz 90d tracker status."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.gtm_blitz_tracker import build_gtm_blitz_snapshot  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()
    blob = build_gtm_blitz_snapshot()
    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print(f"GTM_BLITZ_VERDICT={blob['verdict']} ({blob['pct']}%)")
        print(f"  actuals: {blob['actuals']}")
    if args.strict and blob["verdict"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
