"""Generate Mini Proposals from account packs.

Every proposal is built to pass the Proposal Gate:
  - has starter_price, deliverables, timeline, required_inputs
  - open_scope is always false; approval_required is always true
  - no guaranteed claims (enforced in the gate over the title/deliverables)
"""
from __future__ import annotations

import argparse
import sys

from . import seeds
from .lib import dump_jsonl, load_jsonl


def build_proposal(pack):
    sprint = next((s for s in seeds.iter_sprints() if s["id"] == pack["sector_specific_sprint"]), None)
    if sprint is None:
        sprint = seeds.iter_sprints()[0]
    return {
        "company_name": pack["company_name"],
        "title": pack["mini_proposal_title"],
        "core_system": pack["recommended_core_system"],
        "sprint_id": sprint["id"],
        "starter_price_sar": sprint["starter_price_sar"],
        "deliverables": sprint["deliverables"],
        "timeline_days": sprint["duration_days"],
        "required_inputs": sprint["required_inputs"],
        "open_scope": False,
        "approval_required": True,
        "status": "draft",
    }


def build(limit=50, dry_run=False):
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    eligible = [p for p in packs if not p.get("suppressed")][:limit]
    proposals = [build_proposal(p) for p in eligible]
    if not dry_run:
        dump_jsonl("data/proposals/mini_proposals.jsonl", proposals)
    return proposals


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    proposals = build(limit=args.limit, dry_run=args.dry_run)
    print(f"Generated {len(proposals)} mini proposals (dry_run={args.dry_run}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
