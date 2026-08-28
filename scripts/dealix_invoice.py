#!/usr/bin/env python3
"""Admin CLI — create a TEST Moyasar invoice or preview a payment request.

This compatibility CLI is deliberately **not** a live payment executor.

Why: the current canonical Approval Center store is process-scoped/in-memory,
so a separate CLI process cannot safely prove a durable, exact customer/payment
execution authority receipt. Treating ``--allow-live`` as sufficient would make
an operator flag equivalent to payment authority.

Current policy:
- test (`sk_test_*`) invoices are allowed for synthetic verification;
- dry-run previews are allowed and are not commercial commitments;
- live (`sk_live_*`) invoice creation is fail-closed here, even with the legacy
  ``--allow-live`` flag;
- real customer price/payment terms must originate from an approved
  customer-specific quote and execute through a durable controlled-execution
  path (or a specifically approved manual payment action), with payment proof
  recorded separately.

No public fixed Pilot price, generic refund promise, or 7-day package exists in
this CLI.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import UTC, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dealix.payments.moyasar import MoyasarClient
except Exception:
    MoyasarClient = None  # type: ignore[assignment]


LIVE_BLOCK_REASON = (
    "LIVE_INVOICE_BLOCKED: this compatibility CLI cannot validate a durable exact "
    "payment execution-authority receipt. Use the canonical controlled-execution "
    "payment path or a specifically approved manual payment action."
)
NO_GENERIC_REFUND_NOTE = (
    "No generic refund/remedy term is authorized by this CLI. Any refund, remedy, "
    "cancellation, or payment term must come from the approved customer-specific "
    "quote/order/contract authority."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a test Moyasar invoice or dry-run preview (admin compatibility CLI)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--email", required=True, help="customer/test email recorded in metadata")
    parser.add_argument(
        "--amount-sar", required=True, type=float,
        help="explicit amount for test/preview only; this CLI does not authorize the amount",
    )
    parser.add_argument(
        "--description", required=True,
        help="non-binding test/preview description; do not use this field as commercial authority",
    )
    parser.add_argument(
        "--customer-handle", default="",
        help="optional anonymized customer/test handle",
    )
    parser.add_argument(
        "--service-id", default="customer_specific_quote_test",
        help="test metadata only; does not select a commercial price or package",
    )
    parser.add_argument(
        "--quote-evidence-id", default="",
        help="optional quote/proposal evidence reference for traceability; not execution authority",
    )
    parser.add_argument(
        "--callback-url", default="",
        help="optional callback URL for test-mode Moyasar invoice",
    )
    parser.add_argument(
        "--allow-live", action="store_true",
        help="legacy flag retained for compatibility; live execution is still blocked",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="output the full TEST Moyasar response as JSON",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="preview without contacting Moyasar (no API key required)",
    )
    return parser.parse_args()


def _is_live_key(key: str) -> bool:
    return key.strip().startswith("sk_live_")


def _is_test_key(key: str) -> bool:
    return key.strip().startswith("sk_test_")


async def _create(args: argparse.Namespace) -> dict:
    secret = os.getenv("MOYASAR_SECRET_KEY", "")
    if not secret:
        raise SystemExit(
            "MOYASAR_SECRET_KEY is not set. Use a sk_test_* key for synthetic invoice verification."
        )
    if _is_live_key(secret):
        raise SystemExit(LIVE_BLOCK_REASON)
    if not _is_test_key(secret):
        raise SystemExit("Unsupported Moyasar key class. This CLI accepts sk_test_* only.")

    if args.amount_sar <= 0:
        raise SystemExit("--amount-sar must be > 0")
    if args.amount_sar > 50000:
        raise SystemExit(
            "Amount exceeds 50,000 SAR — refusing as a test safety cap. "
            "This is not permission to use a smaller live amount."
        )

    amount_halalas = int(round(args.amount_sar * 100))
    metadata = {
        "customer_email": args.email,
        "customer_handle": args.customer_handle or "",
        "service_id": args.service_id,
        "quote_evidence_id": getattr(args, "quote_evidence_id", "") or "",
        "commercial_truth": "TEST_ONLY_NOT_PAYMENT_OR_REVENUE",
        "created_by": "dealix_invoice_cli_test_only",
        "created_at_utc": datetime.now(UTC).isoformat(),
    }

    if MoyasarClient is None:
        raise SystemExit(
            "MoyasarClient unavailable in this environment. Use --dry-run for offline preview."
        )
    client = MoyasarClient(secret_key=secret)
    invoice = await client.create_invoice(
        amount_halalas=amount_halalas,
        currency="SAR",
        description=args.description,
        callback_url=args.callback_url or None,
        metadata=metadata,
    )
    return invoice


def _resolve_mode() -> str:
    secret = os.getenv("MOYASAR_SECRET_KEY", "")
    if not secret:
        return "preview_only"
    if _is_live_key(secret):
        return "blocked_live"
    if _is_test_key(secret):
        return "test"
    return "unsupported_key"


def main() -> int:
    args = parse_args()

    if args.dry_run:
        amount_halalas = int(round(args.amount_sar * 100))
        mode = _resolve_mode()
        print("DRY_RUN=true")
        print(f"AMOUNT_SAR={args.amount_sar:g}")
        print(f"AMOUNT_HALALAH={amount_halalas}")
        print(f"MODE={mode}")
        print("COMMERCIAL_AUTHORITY=NONE_PREVIEW_ONLY")
        print(f"DESCRIPTION={args.description}")
        print(f"CUSTOMER_EMAIL={args.email}")
        print(f"QUOTE_EVIDENCE_ID={args.quote_evidence_id}")
        print("LIVE_INVOICE_ALLOWED=false")
        print("REFUND_OR_REMEDY_AUTHORIZED=false")
        print(f"POLICY_NOTE={NO_GENERIC_REFUND_NOTE}")
        print("PAYMENT_PROOF_CREATED=false")
        print("REVENUE_CREATED=false")
        return 0

    if args.allow_live:
        # Keep the old flag syntactically compatible while preventing it from
        # becoming an authorization mechanism.
        print(LIVE_BLOCK_REASON, file=sys.stderr)
        return 2

    try:
        invoice = asyncio.run(_create(args))
    except SystemExit:
        raise
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(invoice, indent=2, ensure_ascii=False))
        return 0

    invoice_id = invoice.get("id", "")
    url = invoice.get("url") or invoice.get("source", {}).get("url", "")
    amount_halalas = invoice.get("amount", 0)
    amount_sar = amount_halalas / 100 if amount_halalas else args.amount_sar

    print("TEST_ONLY=true")
    print(f"INVOICE_ID={invoice_id}")
    print(f"TEST_PAYMENT_URL={url}")
    print(f"AMOUNT_SAR={amount_sar:g}")
    print(f"AMOUNT_HALALAH={int(amount_halalas) if amount_halalas else int(round(args.amount_sar * 100))}")
    print("MODE=test")
    print(f"DESCRIPTION={args.description}")
    print(f"CUSTOMER_EMAIL={args.email}")
    print(f"QUOTE_EVIDENCE_ID={args.quote_evidence_id}")
    print("LIVE_INVOICE_ALLOWED=false")
    print("PAYMENT_PROOF_CREATED=false")
    print("REVENUE_CREATED=false")
    print(f"POLICY_NOTE={NO_GENERIC_REFUND_NOTE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
