#!/usr/bin/env python3
"""Seed 5 referral codes for the first paying customers — Wave 15 (A11).

Pre-generates 5 referral codes in the referral_store JSONL ledger. Each
code is tied to a placeholder `referrer_id` like `dealix_seed_001..005`
so the founder hands them to the first 5 paying customers as
"share this code with 1 peer for 5K SAR credit each".

NEVER reassigns codes that already exist. Idempotent: re-running just
re-prints the existing codes.

Output: `data/seeded_referrals.json` (gitignored — codes are
hash-derived but still treated as credentials).

Usage:
    python scripts/seed_referral_codes.py
    python scripts/seed_referral_codes.py --count 10
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--out", default="data/seeded_referrals.json")
    args = parser.parse_args()

    from auto_client_acquisition.partnership_os.referral_store import (
        REFERRER_CREDIT_SAR,
        create_referral_code,
        list_codes_by_referrer,
    )

    seeded: list[dict] = []
    for i in range(1, args.count + 1):
        referrer_id = f"dealix_seed_{i:03d}"
        existing = list_codes_by_referrer(referrer_id)
        if existing:
            seeded.append({
                "referrer_id": referrer_id,
                "code": existing[0].code,
                "credit_sar": existing[0].credit_sar,
                "discount_pct": existing[0].discount_pct,
                "created_at": existing[0].created_at,
                "status": "already_existed",
            })
        else:
            rc = create_referral_code(
                referrer_id=referrer_id,
                referrer_email="",
                plan_required="managed_revenue_ops_starter",
                credit_sar=REFERRER_CREDIT_SAR,
                discount_pct=50,
            )
            seeded.append({
                "referrer_id": referrer_id,
                "code": rc.code,
                "credit_sar": rc.credit_sar,
                "discount_pct": rc.discount_pct,
                "created_at": rc.created_at,
                "status": "seeded_now",
            })

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(seeded),
        "credit_sar_per_closed_deal": 5000,
        "discount_pct_for_referred": 50,
        "codes": seeded,
        "doctrine": [
            "Hand these codes to the first 5 paying customers only.",
            "Each code is single-use per referred customer.",
            "Self-referrals + same-domain referrals will be auto-rejected.",
            "No unsafe automation, no guaranteed claims (Partner Covenant).",
        ],
    }
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"✓ {len(seeded)} referral codes ready at {out_path.relative_to(REPO_ROOT)}")
    print()
    for s in seeded:
        marker = "🔆" if s["status"] == "seeded_now" else "·"
        print(f"  {marker} {s['referrer_id']} → {s['code']} ({s['credit_sar']} SAR credit)")
    print()
    print("Hand out one code per first-5 paying customer. Example message:")
    print(
        '  "Thanks for being our first customer. Share this code <CODE> with one '
        'peer — they get 50% off month 1, you get 5,000 SAR credit applied to '
        'your next invoice when they pay."'
    )
    print()
    print("_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
