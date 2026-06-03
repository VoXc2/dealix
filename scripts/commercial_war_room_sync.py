#!/usr/bin/env python3
"""Sync agency targets CSV → data/war_room_today.json; optional daily-targeting API."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.api_client import trigger_daily_targeting  # noqa: E402
from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts  # noqa: E402
from dealix.commercial_ops.paths import WAR_ROOM_TODAY_JSON  # noqa: E402
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets  # noqa: E402
from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=15)
    p.add_argument("--trigger-targeting", action="store_true")
    p.add_argument("--no-rotation", action="store_true", help="Use full CSV ranking only")
    p.add_argument("--out", default=str(WAR_ROOM_TODAY_JSON))
    args = p.parse_args()

    all_rows = load_targets()
    pool = all_rows if args.no_rotation else select_daily_p0_targets(all_rows, top_n=args.top_n)
    payload = attach_outreach_drafts(build_war_room_today(pool, top_n=args.top_n))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE · {out} · targets={len(payload['targets']['items'])}")

    if args.trigger_targeting:
        result = trigger_daily_targeting()
        if result:
            print(json.dumps({"daily_targeting": result}, ensure_ascii=False, indent=2))
        else:
            print("SKIP daily-targeting (set DEALIX_API_BASE + admin key)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
