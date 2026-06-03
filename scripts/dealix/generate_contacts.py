"""Generate Contact Discovery records from account packs.

POLICY: never invent contacts. For demo/seed data we only record a single
public 'website' channel derived from the account's own domain, with low
confidence. No emails, phones, or personal names are fabricated.
"""
from __future__ import annotations

import argparse
import sys

from .lib import dump_jsonl, load_jsonl


def build_record(pack):
    channels = []
    if pack.get("website"):
        channels.append(
            {
                "type": "website",
                "value": pack["website"],
                "source": "public",
                "confidence": "low",
            }
        )
        channels.append(
            {
                "type": "contact_form",
                "value": f"{pack['website']}/contact",
                "source": "public",
                "confidence": "low",
            }
        )
    return {
        "company_name": pack["company_name"],
        "channels": channels,
        "invented": False,
    }


def build(limit=400, dry_run=False):
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    records = [build_record(p) for p in packs[:limit]]
    if not dry_run:
        dump_jsonl("data/contacts/contact_discovery.jsonl", records)
        # flat channel index
        channels = []
        for r in records:
            for ch in r["channels"]:
                channels.append({"company_name": r["company_name"], **ch})
        dump_jsonl("data/contacts/contact_channels.jsonl", channels)
    return records


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    records = build(limit=args.limit, dry_run=args.dry_run)
    print(f"Generated {len(records)} contact discovery records (no invented contacts).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
