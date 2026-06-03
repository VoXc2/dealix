#!/usr/bin/env python3
"""
Dealix Nightly 400 Account Packs — generator.

Produces the canonical data backbone for the Maximum Revenue Factory:
  data/account_intelligence/account_packs.jsonl   (400 packs)
  data/contacts/contact_discovery.jsonl
  data/contacts/contact_channels.jsonl
  data/proposals/mini_proposals.jsonl
  data/finance/cash_priority_scores.jsonl

Deterministic: same seed + run_date => byte-identical output.
Seed data is synthetic; no phone numbers or emails are invented.

Usage:
  python3 scripts/generate_account_packs.py [--seed N] [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import dealix_account_lib as lib


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_contact_discovery(pack: dict) -> dict:
    if pack["contact_confidence"] == "C0":
        status = "missing"
        sources = []
    elif pack["contact_confidence"] == "C1":
        status = "partial"
        sources = ["official_website"] if pack["evidence_level"] != "L0" else []
    else:
        status = "found"
        sources = ["official_website", "contact_page"]
    return {
        "pack_id": pack["pack_id"],
        "company_name": pack["company_name"],
        "website": pack["website"],
        "country": pack["country"],
        "city": pack["city"],
        "sector": pack["sector"],
        "public_contact_channels": pack["public_contact_channels"],
        "phone_if_public": pack["phone_if_public"],
        "email_if_public": pack["email_if_public"],
        "contact_page_url": pack["contact_page_url"],
        "social_links": pack["social_links"],
        "google_business_hint": pack["google_business_hint"],
        "likely_decision_maker_role": pack["likely_decision_maker_role"],
        "secondary_contact_role": pack["secondary_contact_role"],
        "best_contact_route": pack["best_contact_route"],
        "contact_confidence": pack["contact_confidence"],
        "missing_contact": pack["missing_contact"],
        "discovery_status": status,
        "discovery_sources": sources,
        "generated_at": pack["generated_at"],
    }


def build_contact_channel(pack: dict) -> dict:
    # We never invent a value; seed channels carry null values and remain unverified.
    src_map = {"role_based_outreach": "none", "contact_form": "official_website",
               "public_social": "public_social"}
    return {
        "pack_id": pack["pack_id"],
        "company_name": pack["company_name"],
        "channel_type": pack["best_contact_route"],
        "channel_value": None,
        "is_public": pack["best_contact_route"] != "role_based_outreach",
        "verified": False,
        "source": src_map.get(pack["best_contact_route"], "none"),
        "confidence": pack["contact_confidence"],
    }


def build_mini_proposal(pack: dict, idx: int) -> dict:
    fields = lib.build_mini_proposal_fields(pack)
    bucket = lib.account_bucket(pack["account_score"])
    status = "approval_queue" if bucket in ("top_priority", "approval_queue") else "draft"
    return {
        "proposal_id": f"MP-{idx:06d}",
        "pack_id": pack["pack_id"],
        "company_name": pack["company_name"],
        "title": fields["title"],
        "recommended_system": fields["recommended_system"],
        "public_signal": fields["public_signal"],
        "likely_pain": fields["likely_pain"],
        "why_this_system": fields["why_this_system"],
        "first_sprint": fields["first_sprint"],
        "deliverables": fields["deliverables"],
        "timeline": fields["timeline"],
        "starter_price_sar": fields["starter_price_sar"],
        "required_inputs": fields["required_inputs"],
        "expected_first_proof": fields["expected_first_proof"],
        "risks_assumptions": fields["risks_assumptions"],
        "next_step": fields["next_step"],
        "approval_required": True,
        "status": status,
        "generated_at": pack["generated_at"],
    }


def build_cash_score(pack: dict) -> dict:
    sys = lib.SYSTEMS[pack["recommended_system"]]
    return {
        "pack_id": pack["pack_id"],
        "company_name": pack["company_name"],
        "recommended_system": pack["recommended_system"],
        "expected_starter_price_sar": sys["starter_price_sar"],
        "delivery_complexity": sys["delivery_complexity"],
        "estimated_delivery_hours": sys["delivery_hours"],
        "gross_margin_hint": "مرتفع (خدمة قائمة على المعرفة، تكلفة تشغيل منخفضة)",
        "upsell_potential": sys["upsell_potential"],
        "cash_priority_score": pack["cash_priority_score"],
        "breakdown": pack["cash_priority_breakdown"],
        "generated_at": pack["generated_at"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Dealix nightly 400 account packs")
    parser.add_argument("--seed", type=int, default=20260603)
    parser.add_argument("--date", type=str, default=None, help="run date YYYY-MM-DD")
    args = parser.parse_args()

    run_date = args.date or datetime.now().strftime("%Y-%m-%d")
    packs_full = lib.generate_packs(seed=args.seed, run_date=run_date)
    # Derived records read from the full packs (which still carry helper fields
    # such as _pain_list); the account file itself is written stripped.
    packs = [lib.strip_internal(p) for p in packs_full]

    contact_discovery = [build_contact_discovery(p) for p in packs_full]
    contact_channels = [build_contact_channel(p) for p in packs_full]
    mini_proposals = [build_mini_proposal(p, i + 1) for i, p in enumerate(packs_full)]
    cash_scores = [build_cash_score(p) for p in packs_full]

    write_jsonl(lib.DATA_DIR / "account_intelligence" / "account_packs.jsonl", packs)
    write_jsonl(lib.DATA_DIR / "contacts" / "contact_discovery.jsonl", contact_discovery)
    write_jsonl(lib.DATA_DIR / "contacts" / "contact_channels.jsonl", contact_channels)
    write_jsonl(lib.DATA_DIR / "proposals" / "mini_proposals.jsonl", mini_proposals)
    write_jsonl(lib.DATA_DIR / "finance" / "cash_priority_scores.jsonl", cash_scores)

    # quick distribution summary
    by_system: dict[str, int] = {}
    for p in packs:
        by_system[p["recommended_system"]] = by_system.get(p["recommended_system"], 0) + 1
    missing = sum(1 for p in packs if p["missing_contact"])
    suppressed = sum(1 for p in packs if p["do_not_contact"])

    print("=" * 72)
    print(f"  DEALIX NIGHTLY 400 ACCOUNT PACKS — {run_date} (seed={args.seed})")
    print("=" * 72)
    print(f"  Total packs: {len(packs)}")
    for name in lib.SYSTEM_NAMES:
        print(f"    - {name:<28} {by_system.get(name, 0)}")
    print(f"  Missing contact (role-based fallback): {missing}")
    print(f"  Suppressed / do-not-contact: {suppressed}")
    print(f"  Mini proposals: {len(mini_proposals)}  |  Cash scores: {len(cash_scores)}")
    print("  Written to data/account_intelligence, data/contacts, data/proposals, data/finance")
    print("=" * 72)


if __name__ == "__main__":
    main()
