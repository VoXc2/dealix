#!/usr/bin/env python3
"""Render the canonical Dealix Free Mini Diagnostic draft.

This renderer is intentionally non-commercial-authoritative: it cannot select
historical priced diagnostic templates, generate a Pilot price, create an
invoice/payment link, or make outcome commitments.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs/commercial/operations/proposals/FREE_MINI_DIAGNOSTIC_CANONICAL_AR_EN.md"
OUT_DIR = ROOT / "data/founder_briefs"
AUTHORITY = ["docs/DEALIX_BUSINESS_MODEL.md", "COMMERCIAL_IDENTITY.md"]


def _slug(name: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE)
    cleaned = re.sub(r"[\s_-]+", "_", cleaned.strip())
    return cleaned[:48] or "company"


def _render(company: str, contact: str) -> str:
    if not TEMPLATE.is_file():
        raise FileNotFoundError(TEMPLATE)
    body = TEMPLATE.read_text(encoding="utf-8")
    body = body.replace("{{company}}", company.strip())
    body = body.replace("{{contact}}", contact.strip() or "—")
    return body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", required=True)
    parser.add_argument("--contact", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        body = _render(args.company, args.contact)
    except FileNotFoundError:
        print(f"Missing canonical template: {TEMPLATE}", file=sys.stderr)
        return 1

    now = datetime.now(UTC)
    date = now.date().isoformat()
    slug = _slug(args.company)
    out_path = OUT_DIR / f"free_mini_diagnostic_{slug}_{date}.md"

    receipt = {
        "schema": "dealix.free_mini_diagnostic_draft.v1",
        "generated_at": now.isoformat(),
        "company": args.company.strip(),
        "contact": args.contact.strip() or None,
        "truth_class": "DRAFT_NOT_SENT",
        "commercial_authority": AUTHORITY,
        "price_authorized": False,
        "payment_authorized": False,
        "contract_authorized": False,
        "outcome_guarantee_authorized": False,
        "external_send_authorized_by_this_artifact": False,
        "next_paid_motion": "customer_specific_quote_after_qualified_discovery_and_applicable_gates",
        "pilot_duration_days": None,
        "pilot_duration_policy": "customer_specific_after_qualified_discovery",
        "output": str(out_path.relative_to(ROOT)),
    }

    if args.dry_run:
        if args.as_json:
            print(json.dumps(receipt, ensure_ascii=False, indent=2))
        else:
            print(f"DRY-RUN -> {out_path.relative_to(ROOT)}")
            print(body)
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    receipt_path = out_path.with_suffix(".json")
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.as_json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    else:
        print(f"WROTE {out_path.relative_to(ROOT)}")
        print(f"RECEIPT {receipt_path.relative_to(ROOT)}")
        print("STATUS=DRAFT_NOT_SENT")
        print("PRICE_AUTHORIZED=false")
        print("NEXT=QUALIFY_THEN_CUSTOMER_SPECIFIC_QUOTE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
