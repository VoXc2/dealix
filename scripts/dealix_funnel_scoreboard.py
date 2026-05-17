#!/usr/bin/env python3
"""Dealix Funnel Scoreboard — daily cron generator.

Writes data/revenue_assurance/funnel/{YYYY-MM-DD}.md (+ JSON sidecar).
Funnel counts are supplied via --counts-json; absent stages count as 0.

NO_LIVE_SEND: never auto-sends.

Usage:
  python3 scripts/dealix_funnel_scoreboard.py --counts-json data/funnel.json
  python3 scripts/dealix_funnel_scoreboard.py --period 90d
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix daily Funnel Scoreboard")
    parser.add_argument(
        "--counts-json", type=str, default="", help="JSON file of funnel stage counts."
    )
    parser.add_argument("--period", choices=["30d", "90d"], default="30d")
    args = parser.parse_args()

    from auto_client_acquisition.revenue_assurance_os.funnel_scoreboard import build_scoreboard
    from auto_client_acquisition.revenue_assurance_os.renderers import (
        render_funnel_scoreboard,
    )

    counts: dict[str, int] = {}
    if args.counts_json:
        counts = json.loads(Path(args.counts_json).read_text(encoding="utf-8"))

    board = build_scoreboard(counts, period=args.period)
    md = render_funnel_scoreboard(board)

    date_label = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = _REPO_ROOT / "data" / "revenue_assurance" / "funnel"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{date_label}.md"
    md_path.write_text(md, encoding="utf-8")
    json_path = out_dir / f"{date_label}.json"
    json_path.write_text(
        json.dumps(board.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"=== Dealix Funnel Scoreboard — {date_label} ({args.period}) ===")
    print(f"  on track : {board.on_track}")
    print(f"  bottleneck: {board.bottleneck_stage}")
    print(f"  ✓ {md_path.relative_to(_REPO_ROOT)}")
    print("NO_LIVE_SEND: founder reviews manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
