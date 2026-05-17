#!/usr/bin/env python3
"""Dealix Monthly Board Pack — month-end cron generator.

Writes data/revenue_assurance/board_pack/{YYYY-MM}.md (+ JSON sidecar):
8 sections (Revenue, Funnel, Delivery, Support, Partners, Governance,
Product, Decision Needed). Sections without hard evidence say so.

NO_LIVE_SEND: never auto-sends.

Usage:
  python3 scripts/dealix_board_pack.py
  python3 scripts/dealix_board_pack.py --counts-json data/funnel.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Monthly Board Pack generator")
    parser.add_argument(
        "--counts-json", type=str, default="", help="Optional JSON file of funnel stage counts."
    )
    args = parser.parse_args()

    from auto_client_acquisition.revenue_assurance_os.board_pack import build_board_pack
    from auto_client_acquisition.revenue_assurance_os.renderers import render_board_pack

    funnel_counts = None
    if args.counts_json:
        funnel_counts = json.loads(Path(args.counts_json).read_text(encoding="utf-8"))

    pack = build_board_pack(funnel_counts=funnel_counts)
    md = render_board_pack(pack)

    out_dir = _REPO_ROOT / "data" / "revenue_assurance" / "board_pack"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{pack.month_label}.md"
    md_path.write_text(md, encoding="utf-8")
    json_path = out_dir / f"{pack.month_label}.json"
    json_path.write_text(json.dumps(pack.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"=== Dealix Monthly Board Pack — {pack.month_label} ===")
    print(f"  ✓ {md_path.relative_to(_REPO_ROOT)}")
    print("NO_LIVE_SEND: founder reviews manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
