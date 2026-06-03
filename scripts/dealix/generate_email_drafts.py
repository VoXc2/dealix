"""Generate personalized email DRAFTS from account packs.

Every draft is built to pass the Email Quality Gate:
  - references a client need card, a core system, and a sector sprint
  - has a CTA
  - contains NO guaranteed claims and NO fake Re:/Fwd: subjects
  - states pain as a question/hypothesis, never as asserted fact
  - skips suppressed accounts
Drafts are never sent by the agent; approval_required is always true.
"""
from __future__ import annotations

import argparse
import sys

from . import seeds
from .lib import dump_jsonl, load_jsonl
from .generate_account_packs import dict_core


def build_draft(pack):
    core_name = dict_core(pack["recommended_core_system"])
    need = seeds.need_by_id(pack["primary_need"])
    sector_ar = dict(seeds.SECTORS).get(pack["sector"], pack["sector"])
    body = (
        f"السلام عليكم،\n\n"
        f"لاحظنا من موقعكم العام أن فرق {sector_ar} غالبًا تواجه تحديًا في «{need['name_ar']}». "
        f"هل هذا صحيح لديكم اليوم؟\n\n"
        f"في Dealix نعالج هذا عبر {core_name} من خلال سبرنت قصير محدد المخرجات "
        f"({pack['sector_specific_sprint']}) دون أي وعود مبالغ فيها — فقط مخرجات واضحة ومعايير قبول.\n\n"
        f"هل تناسبكم مكالمة 15 دقيقة هذا الأسبوع لمراجعة الفكرة؟"
    )
    return {
        "company_name": pack["company_name"],
        "to_role": pack["buyer_roles"][0],
        "subject": f"فكرة لمعالجة {need['name_ar']} لدى {pack['company_name']}",
        "body": body,
        "core_system": pack["recommended_core_system"],
        "sector_specific_sprint": pack["sector_specific_sprint"],
        "cta": "مكالمة 15 دقيقة هذا الأسبوع",
        "client_need_card_ref": f"need-card::{pack['domain']}",
        "approval_required": True,
        "status": "draft",
    }


def build(limit=400, top=100, dry_run=False):
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    eligible = [p for p in packs if not p.get("suppressed")][:limit]
    drafts = [build_draft(p) for p in eligible]
    queue = drafts[:top]
    if not dry_run:
        dump_jsonl("data/outreach/email_drafts.jsonl", drafts)
        dump_jsonl("data/outreach/top_100_approval_queue.jsonl", queue)
    return drafts, queue


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    drafts, queue = build(limit=args.limit, dry_run=args.dry_run)
    print(f"Generated {len(drafts)} email drafts; top {len(queue)} queued for founder approval (dry_run={args.dry_run}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
