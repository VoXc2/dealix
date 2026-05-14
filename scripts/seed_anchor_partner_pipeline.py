#!/usr/bin/env python3
"""Seed 3 anchor-partner placeholder pipeline records — Wave 17.

Wave 17 strategic move #5: open the partner channel with three archetype
outreach contacts the founder books in week 1. This script seeds the
three placeholders so the founder dashboard surfaces them as "first 3
calls of next week".

NEVER sends a message. NEVER scrapes. Idempotent: re-running prints the
same three placeholders without duplicating them.

Output: `data/anchor_partner_pipeline.json` (gitignored — partner intent
metadata; the actual partner names are filled in by the founder before
each call).

Usage:
    python scripts/seed_anchor_partner_pipeline.py
    python scripts/seed_anchor_partner_pipeline.py --reset   # rewrite from scratch
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


_ARCHETYPES = (
    {
        "id": "anchor_partner_big_four",
        "archetype": "Big 4 advisory Saudi practice",
        "archetype_ar": "ممارسة استشارات Big 4 السعودية",
        "examples": ["PwC Saudi", "Deloitte Saudi", "EY Saudi", "KPMG Saudi"],
        "owner_role": "PDPL/NDMO advisory partner OR governance practice lead",
        "value_to_partner": (
            "PDPL + NDMO compliance referral mechanism + Sprint delivery "
            "partner so the advisory keeps the consulting layer."
        ),
        "value_to_dealix": "Enterprise referrals with credibility moat.",
        "draft_path": "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md#archetype-1",
    },
    {
        "id": "anchor_partner_sama_processor",
        "archetype": "SAMA-licensed payment processor",
        "archetype_ar": "معالج مدفوعات مرخّص من ساما",
        "examples": ["Moyasar", "HyperPay", "PayTabs"],
        "owner_role": "Risk / Fraud / AML lead OR partnerships head",
        "value_to_partner": (
            "Governance + Trust Pack layer for processor's mid-market "
            "merchants who need PDPL audit trail without building it in-house."
        ),
        "value_to_dealix": "Merchant referrals + SAMA-aligned audit story.",
        "draft_path": "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md#archetype-2",
    },
    {
        "id": "anchor_partner_saudi_vc",
        "archetype": "Saudi VC fund",
        "archetype_ar": "صندوق رأس مال جريء سعودي",
        "examples": ["Sanabil", "STV", "Wa'ed Ventures", "Raed Ventures"],
        "owner_role": "Portfolio operating partner OR platform lead",
        "value_to_partner": (
            "Portco revenue intelligence + governance gap unblocker "
            "before Series A diligence stalls on data quality."
        ),
        "value_to_dealix": "Pre-qualified portco referrals + brand halo.",
        "draft_path": "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md#archetype-3",
    },
)


def _build_record(archetype: dict, now: str) -> dict:
    return {
        "id": archetype["id"],
        "archetype": archetype["archetype"],
        "archetype_ar": archetype["archetype_ar"],
        "candidate_partners": archetype["examples"],
        "owner_role_to_target": archetype["owner_role"],
        "value_to_partner": archetype["value_to_partner"],
        "value_to_dealix": archetype["value_to_dealix"],
        "outreach_draft_ref": archetype["draft_path"],
        "rev_share_terms": (
            "20% / first 12 months / capped at 200,000 SAR per closed referral. "
            "Partner Covenant binding."
        ),
        "status": "queued_for_founder_call",
        "tag": "anchor_partner",
        "created_at": now,
        "founder_action_required": (
            "Pick the specific company name + the specific contact + book "
            "a 60-min call. Use the bilingual draft in outreach_draft_ref. "
            "DRAFT ONLY — founder approval required before send."
        ),
        "doctrine": {
            "no_cold_send": True,
            "no_scraping": True,
            "no_linkedin_automation": True,
            "approval_required_before_send": True,
        },
        "is_estimate": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out", default="data/anchor_partner_pipeline.json",
        help="Output JSON file path",
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Rewrite from scratch (default: keep existing if present)",
    )
    args = parser.parse_args()

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists() and not args.reset:
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
            print(f"✓ Pipeline already exists: {out_path}")
            print(f"  - {len(existing.get('partners', []))} partner archetypes")
            for p in existing.get("partners", []):
                print(f"    · {p.get('archetype', '?')} → status={p.get('status', '?')}")
            print(f"\nRe-run with --reset to rebuild from scratch.")
            return 0
        except Exception:
            pass  # fall through to rebuild

    now = datetime.now(timezone.utc).isoformat()
    payload = {
        "version": "1.0",
        "wave": "17",
        "generated_at": now,
        "doctrine_note": (
            "Anchor partner outreach is DRAFT ONLY. Founder reviews + approves "
            "every send. NEVER autonomous. NEVER cold send. NEVER scraping. "
            "Cross-link: docs/40_partners/PARTNER_COVENANT.md."
        ),
        "partners": [_build_record(a, now) for a in _ARCHETYPES],
        "next_action": (
            "Open docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md, pick one "
            "company name per archetype, book the call. Target: 3 first "
            "calls within 7 days, 1 LOI within 30 days."
        ),
        "is_estimate": False,
        "governance_decision": "allow",
    }

    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"✓ Seeded {len(payload['partners'])} anchor partner placeholders → {out_path}")
    for p in payload["partners"]:
        print(f"  · {p['archetype']} (candidates: {', '.join(p['candidate_partners'][:3])})")
    print(
        "\nNext: open docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md, pick one "
        "company per archetype, book three 60-min calls."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
