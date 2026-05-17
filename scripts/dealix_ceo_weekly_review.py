#!/usr/bin/env python3
"""Dealix Weekly CEO Review — Friday cron generator.

Writes data/revenue_assurance/ceo_review/{YYYY-WW}.md (+ JSON sidecar):
11 standard questions and 5 required decision slots for the founder.

NO_LIVE_SEND: never auto-sends.

Usage:
  python3 scripts/dealix_ceo_weekly_review.py
  python3 scripts/dealix_ceo_weekly_review.py --counts-json data/funnel.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Weekly CEO Review generator")
    parser.add_argument(
        "--counts-json", type=str, default="", help="Optional JSON file of funnel stage counts."
    )
    args = parser.parse_args()

    from auto_client_acquisition.revenue_assurance_os.ceo_review import build_ceo_review
    from auto_client_acquisition.revenue_assurance_os.renderers import render_ceo_review

    funnel_counts = None
    if args.counts_json:
        funnel_counts = json.loads(Path(args.counts_json).read_text(encoding="utf-8"))

    review = build_ceo_review(funnel_counts=funnel_counts)
    md = render_ceo_review(review)

    out_dir = _REPO_ROOT / "data" / "revenue_assurance" / "ceo_review"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{review.week_label}.md"
    md_path.write_text(md, encoding="utf-8")
    json_path = out_dir / f"{review.week_label}.json"
    json_path.write_text(
        json.dumps(review.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"=== Dealix Weekly CEO Review — {review.week_label} ===")
    print(f"  ✓ {md_path.relative_to(_REPO_ROOT)}")
    print("NO_LIVE_SEND: founder fills 5 decisions, reviews manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
