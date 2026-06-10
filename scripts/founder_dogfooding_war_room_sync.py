#!/usr/bin/env python3
"""Sync Dealix internal milestones → data/dealix_dogfooding_war_room.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.dogfooding_war_room import build_dogfooding_payload  # noqa: E402
from dealix.commercial_ops.paths import DEALIX_DOGFOODING_WAR_ROOM_JSON  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=10)
    p.add_argument("--out", default=str(DEALIX_DOGFOODING_WAR_ROOM_JSON))
    p.add_argument("--json", action="store_true", help="Print payload to stdout")
    args = p.parse_args()

    payload = build_dogfooding_payload(top_n=args.top_n)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n = len((payload.get("targets") or {}).get("items") or [])
    print(f"DEALIX_DOGFOODING_WAR_ROOM_WROTE={out} targets={n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
