#!/usr/bin/env python3
"""Print GTM stack status — ABM wave 1, dual track, TTV."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    parser = argparse.ArgumentParser(description="GTM stack snapshot for founder")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--top-n", type=int, default=10)
    args = parser.parse_args()

    from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot

    snap = build_gtm_stack_snapshot(abm_top_n=max(1, min(args.top_n, 30)))
    if args.json:
        print(json.dumps(snap, ensure_ascii=False, indent=2))
        return 0

    dual = snap["dual_track"]
    abm = snap["abm_wave1"]
    ttv = snap["ttv"]
    print("DEALIX_GTM_STACK=ok")
    print(f"track={dual['recommended_track']} | {dual['reason_ar']}")
    print(
        f"abm_wave1: active={abm['active_rows']} eligible={abm['eligible_wave1']} "
        f"ready={abm['wave1_ready']}"
    )
    if ttv.get("ttv_discovery_days_avg") is not None:
        print(f"ttv_discovery_avg_days={ttv['ttv_discovery_days_avg']}")
    print("\nTop ABM targets:")
    for t in abm.get("top_targets") or []:
        print(f"  - {t.get('company')} score={t.get('abm_score')} [{t.get('priority')}]")
    for line in snap.get("focus_ar") or []:
        print(f"focus: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
