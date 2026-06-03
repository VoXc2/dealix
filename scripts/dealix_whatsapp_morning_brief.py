#!/usr/bin/env python3
"""Wave 13 Phase 7 — WhatsApp Morning Brief CLI.

Runs 8AM KSA cron-able. Generates the brief text for founder to
COPY/PASTE into WhatsApp manually. NEVER auto-sends.

Article 4 NO_LIVE_SEND: this script does NOT call any WhatsApp send API.
It writes to stdout (and optionally to disk).

Usage:
  python3 scripts/dealix_whatsapp_morning_brief.py --customer-handle acme
  python3 scripts/dealix_whatsapp_morning_brief.py --customer-handle acme --out-md data/wave13/whatsapp/today.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dealix WhatsApp Morning Brief — generates text only (NEVER auto-sends)"
    )
    parser.add_argument("--customer-handle", required=True, help="Customer handle")
    parser.add_argument("--p0-leads", type=int, default=0, help="P0 leads count")
    parser.add_argument("--pending-approvals", type=int, default=0, help="Pending approvals count")
    parser.add_argument("--proof-packs-due", type=int, default=0, help="Proof packs due count")
    parser.add_argument("--support-alerts", type=int, default=0, help="Support alerts count")
    parser.add_argument("--top-decision", type=str, default=None,
                        help="Top decision summary (Arabic)")
    parser.add_argument("--out-md", type=str, default=None,
                        help="Optional file to write the brief to (otherwise stdout only)")
    args = parser.parse_args()

    from auto_client_acquisition.whatsapp_decision_bot.morning_brief import (
        build_morning_brief,
        format_morning_brief,
    )

    brief = build_morning_brief(
        customer_handle=args.customer_handle,
        p0_leads_count=args.p0_leads,
        pending_approvals_count=args.pending_approvals,
        proof_packs_due_count=args.proof_packs_due,
        support_alerts_count=args.support_alerts,
        top_decision_summary=args.top_decision,
    )
    text = format_morning_brief(brief)

    print("=" * 60)
    print("Dealix WhatsApp Morning Brief — copy & paste manually")
    print("Article 4 NO_LIVE_SEND: this script never auto-sends.")
    print("=" * 60)
    print()
    print(text)
    print()
    print("=" * 60)

    if args.out_md:
        out_path = Path(args.out_md)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"Saved to: {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
