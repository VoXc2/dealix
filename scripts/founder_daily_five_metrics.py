#!/usr/bin/env python3
"""Founder daily five metrics — David Sacks-style 90-second CEO scan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.ceo_master_plan import build_daily_five_metrics  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    blob = build_daily_five_metrics()
    m = blob["metrics"]

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print(f"Date: {blob['date']}")
        print("== Founder Daily Five Metrics (90 sec) ==")
        print(f"  1) Paid revenue events today:     {m['1_new_paid_revenue_events_today']}")
        print(f"  2) payment_received (real total): {m['2_payment_received_real_total']}")
        print(f"  3) proof_pack_delivered (total):  {m['3_proof_packs_delivered_total']}")
        print(f"  4) Open pipeline (real leads):     {m['4_open_pipeline_leads_real']}")
        pct = m["5_production_layers_pct"]
        print(f"  5) Production layers %:           {pct if pct is not None else 'n/a'}")
        print(f"\n  Evidence today/week: {blob['evidence_today_total']}/{blob['evidence_week_total']}")
        print(f"  Phase 0–1: {blob['phase_0_1_verdict']} | first_close_ready={blob['first_close_ready']}")
        print(f"  Action: {blob['founder_action_ar']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
