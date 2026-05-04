#!/usr/bin/env python3
"""Admin CLI — create a one-off Moyasar invoice for a customer.

Usage:
    python scripts/dealix_invoice.py \\
      --email customer@example.sa \\
      --amount-sar 499 \\
      --description "Dealix Pilot 7 days"

Environment:
  MOYASAR_SECRET_KEY  — required. ``sk_test_*`` for test mode (default safe);
                        ``sk_live_*`` requires explicit ``--allow-live`` flag.

Output:
  INVOICE_ID=inv_xxxxx
  PAYMENT_URL=https://checkout.moyasar.com/...
  AMOUNT=499 SAR
  ID_FOR_FOUNDER=...

Safety:
  - Refuses to run with a sk_live_ key unless ``--allow-live`` is passed.
  - Prints only what the founder copies to send to the customer.
  - NEVER stores card data; Moyasar hosts the checkout.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import UTC, datetime

# Adjust path so we can import from repo root when run as a script.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dealix.payments.moyasar import MoyasarClient  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Create a one-off Moyasar invoice (admin only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--email", required=True, help="customer email (recorded in metadata)")
    p.add_argument(
        "--amount-sar", required=True, type=float,
        help="amount in SAR (e.g. 499 for the Pilot)",
    )
    p.add_argument(
        "--description", required=True,
        help='invoice description, e.g. "Dealix Pilot 7 days"',
    )
    p.add_argument(
        "--customer-handle", default="",
        help="optional anonymized customer handle to record in metadata",
    )
    p.add_argument(
        "--service-id", default="growth_starter",
        help="service_id from the YAML matrix (default: growth_starter)",
    )
    p.add_argument(
        "--callback-url", default="",
        help="optional URL Moyasar redirects to after payment",
    )
    p.add_argument(
        "--allow-live", action="store_true",
        help="ONLY use this if MOYASAR_SECRET_KEY is sk_live_* and you are intentionally creating a live invoice",
    )
    p.add_argument(
        "--json", action="store_true",
        help="output the full Moyasar response as JSON instead of the founder-friendly summary",
    )
    return p.parse_args()


def _is_live_key(key: str) -> bool:
    return key.strip().startswith("sk_live_")


async def _create(args: argparse.Namespace) -> dict:
    secret = os.getenv("MOYASAR_SECRET_KEY", "")
    if not secret:
        raise SystemExit(
            "MOYASAR_SECRET_KEY is not set. "
            "Use sk_test_* for test mode (preferred at this stage)."
        )
    if _is_live_key(secret) and not args.allow_live:
        raise SystemExit(
            "MOYASAR_SECRET_KEY is a sk_live_ key. Refusing to run.\n"
            "Pass --allow-live ONLY if you are intentionally charging "
            "real money for an authorized customer with founder approval. "
            "See docs/EXECUTIVE_DECISION_PACK.md."
        )

    if args.amount_sar <= 0:
        raise SystemExit("--amount-sar must be > 0")
    if args.amount_sar > 50000:
        # Defensive cap. Anything bigger requires manual SQL or a flag.
        raise SystemExit(
            "Amount exceeds 50,000 SAR — refusing as a safety cap. "
            "If this is intentional, run via the Moyasar dashboard."
        )

    amount_halalas = int(round(args.amount_sar * 100))
    metadata = {
        "customer_email": args.email,
        "customer_handle": args.customer_handle or "",
        "service_id": args.service_id,
        "created_by": "dealix_invoice_cli",
        "created_at_utc": datetime.now(UTC).isoformat(),
    }

    client = MoyasarClient(secret_key=secret)
    invoice = await client.create_invoice(
        amount_halalas=amount_halalas,
        currency="SAR",
        description=args.description,
        callback_url=args.callback_url or None,
        metadata=metadata,
    )
    return invoice


def main() -> int:
    args = parse_args()
    try:
        invoice = asyncio.run(_create(args))
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(invoice, indent=2, ensure_ascii=False))
        return 0

    invoice_id = invoice.get("id", "")
    url = invoice.get("url") or invoice.get("source", {}).get("url", "")
    amount_halalas = invoice.get("amount", 0)
    amount_sar = amount_halalas / 100 if amount_halalas else args.amount_sar

    print(f"INVOICE_ID={invoice_id}")
    print(f"PAYMENT_URL={url}")
    print(f"AMOUNT={amount_sar:g} SAR")
    print(f"DESCRIPTION={args.description}")
    print(f"CUSTOMER_EMAIL={args.email}")
    print()
    print("Send the PAYMENT_URL to the customer manually (WhatsApp / email).")
    print("This script never sends anything on your behalf.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
