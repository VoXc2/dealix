"""Generate Call Briefs from account packs (one per top account)."""
from __future__ import annotations

import argparse
import sys

from . import seeds
from .lib import dump_jsonl, load_jsonl
from .generate_account_packs import dict_core


def build_brief(pack):
    need = seeds.need_by_id(pack["primary_need"])
    core_name = dict_core(pack["recommended_core_system"])
    return {
        "company_name": pack["company_name"],
        "buyer_role": pack["buyer_roles"][0],
        "primary_need": pack["primary_need"],
        "core_system": pack["recommended_core_system"],
        "opening_ar": f"أتواصل بخصوص فكرة محددة حول {need['name_ar']} — هل الوقت مناسب لدقيقتين؟",
        "questions": [
            f"كيف تتعاملون حاليًا مع {need['name_ar']}؟",
            "كم عميل محتمل يصلكم أسبوعيًا تقريبًا؟",
            "ما أكبر عائق يمنعكم من إغلاق المزيد من الصفقات؟",
        ],
        "value_points": [
            f"{core_name}: مخرجات واضحة خلال سبرنت قصير",
            "تسعير مبدئي ثابت بلا التزام طويل",
        ],
        "objections_ref": "data/acquisition/objection_responses.jsonl",
        "next_step": "إرسال Mini Proposal بعد الاعتماد",
    }


def build(limit=100, dry_run=False):
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    eligible = [p for p in packs if not p.get("suppressed")][:limit]
    briefs = [build_brief(p) for p in eligible]
    if not dry_run:
        dump_jsonl("data/acquisition/call_briefs.jsonl", briefs)
    return briefs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    briefs = build(limit=args.limit, dry_run=args.dry_run)
    print(f"Generated {len(briefs)} call briefs (dry_run={args.dry_run}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
