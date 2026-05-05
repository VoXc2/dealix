#!/usr/bin/env python3
"""Founder daily digest — composes the daily growth loop and emails
it to the founder.

Usage:
    python scripts/dealix_morning_digest.py
    python scripts/dealix_morning_digest.py --print   # don't send, just print

Environment:
  RESEND_API_KEY         — required (or another configured email provider)
  DEALIX_FOUNDER_EMAIL   — recipient (defaults to sami.assiri11@gmail.com)
  EMAIL_PROVIDER         — "resend" (default), "sendgrid", or "smtp"

Designed to run via GitHub Actions cron at 4AM UTC = 7AM KSA.
Idempotent: subject includes today's date; running twice in one day
produces two emails with the same subject (founder can spot duplicates).

Never sends to anyone except the founder.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import UTC, datetime

# Adjust path so we can import from repo root when run as a script.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auto_client_acquisition.self_growth_os import daily_growth_loop  # noqa: E402
from core.config.settings import get_settings  # noqa: E402
from integrations.email import EmailClient, EmailResult  # noqa: E402


def _today_label() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def _build_subject() -> str:
    return f"Dealix · موجز اليوم · {_today_label()}"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Founder morning digest")
    p.add_argument(
        "--print", dest="print_only", action="store_true",
        help="render the digest to stdout without sending email",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="render + print + log what WOULD be sent (no actual send)",
    )
    return p.parse_args()


async def _build_and_send(args: argparse.Namespace) -> EmailResult:
    settings = get_settings()
    recipient = settings.dealix_founder_email
    if not recipient and not args.print_only and not args.dry_run:
        return EmailResult(
            success=False,
            provider=settings.email_provider,
            error="dealix_founder_email_not_configured",
        )

    loop = daily_growth_loop.build_today()
    body_text = daily_growth_loop.to_markdown(loop)

    if args.print_only:
        print(body_text)
        return EmailResult(success=True, provider="print_only")

    if args.dry_run:
        print(f"[dry-run] would send to: {recipient}")
        print(f"[dry-run] subject: {_build_subject()}")
        print(f"[dry-run] body length: {len(body_text)} chars")
        print("--- body preview (first 600 chars) ---")
        print(body_text[:600])
        print("---")
        return EmailResult(success=True, provider="dry_run")

    client = EmailClient()
    return await client.send(
        to=recipient,
        subject=_build_subject(),
        body_text=body_text,
    )


def main() -> int:
    args = parse_args()
    try:
        result = asyncio.run(_build_and_send(args))
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if result.success:
        if not (args.print_only or args.dry_run):
            print(f"OK: digest sent via {result.provider} (message_id={result.message_id})")
        return 0
    print(f"FAIL: {result.provider}: {result.error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
