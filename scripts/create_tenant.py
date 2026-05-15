#!/usr/bin/env python3
"""Create a new tenant (customer) record (W7.1).

Used by:
  - docs/ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md Day 1
  - Manual operator action when an enterprise customer signs

The tenant is the multi-tenancy root. Every downstream row (users,
leads, decisions, payments) carries tenant_id for isolation enforced
at both ORM and (in production) row-level-security layers.

Usage:
  python scripts/create_tenant.py \\
    --handle acme_saas \\
    --name "ACME SaaS Co" \\
    --plan growth \\
    --max-leads 1000

  # Dry-run to verify args without committing
  python scripts/create_tenant.py --handle x --name "X" --dry-run

Exit codes:
  0  tenant created (or already existed and --idempotent passed)
  1  tenant with that slug already exists (and --idempotent not passed)
  2  validation error or DB unreachable
"""
from __future__ import annotations

import argparse
import asyncio
import os
import re
import sys
import uuid
from datetime import datetime, timezone


SLUG_RE = re.compile(r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$")
VALID_PLANS = {"pilot", "starter", "growth", "scale"}
VALID_LOCALES = {"ar", "en"}


def _validate_args(args: argparse.Namespace) -> str | None:
    """Return error message if args invalid, None otherwise."""
    if not args.handle or not SLUG_RE.match(args.handle):
        return (
            f"handle must match {SLUG_RE.pattern!r} — got {args.handle!r}. "
            "Use lowercase letters, digits, underscores; 3-64 chars; start with letter, end with alphanumeric."
        )
    if not args.name or len(args.name) > 255:
        return f"name required, ≤ 255 chars — got {len(args.name) if args.name else 0}"
    if args.plan not in VALID_PLANS:
        return f"plan must be one of {VALID_PLANS} — got {args.plan!r}"
    if args.locale not in VALID_LOCALES:
        return f"locale must be one of {VALID_LOCALES} — got {args.locale!r}"
    if args.max_leads <= 0:
        return "max-leads must be > 0"
    if args.max_users <= 0:
        return "max-users must be > 0"
    return None


async def _create(args: argparse.Namespace) -> int:
    try:
        from sqlalchemy import select

        from db.models import TenantRecord
        from db.session import async_session_factory
    except Exception as exc:
        print(f"FATAL: cannot import DB layer: {exc}", file=sys.stderr)
        return 2

    if not os.environ.get("DATABASE_URL"):
        print("FATAL: DATABASE_URL not set", file=sys.stderr)
        return 2

    async with async_session_factory()() as session:
        # Check for existing tenant with same slug (idempotency)
        existing = (
            await session.execute(
                select(TenantRecord).where(TenantRecord.slug == args.handle)
            )
        ).scalar_one_or_none()

        if existing is not None:
            if args.idempotent:
                print(f"OK: tenant slug={args.handle!r} already exists "
                      f"(id={existing.id} plan={existing.plan} status={existing.status})")
                return 0
            print(f"FAIL: tenant slug={args.handle!r} already exists. "
                  "Pass --idempotent to no-op on conflict.", file=sys.stderr)
            return 1

        if args.dry_run:
            print("DRY-RUN: would create tenant with:")
            print(f"  handle:           {args.handle}")
            print(f"  name:             {args.name}")
            print(f"  plan:             {args.plan}")
            print(f"  locale:           {args.locale}")
            print(f"  timezone:         {args.timezone}")
            print(f"  currency:         {args.currency}")
            print(f"  max_users:        {args.max_users}")
            print(f"  max_leads_month:  {args.max_leads}")
            return 0

        tenant_id = f"tn_{uuid.uuid4().hex[:16]}"
        now = datetime.now(timezone.utc)
        tenant = TenantRecord(
            id=tenant_id,
            name=args.name,
            slug=args.handle,
            plan=args.plan,
            status="active",
            timezone=args.timezone,
            locale=args.locale,
            currency=args.currency,
            max_users=args.max_users,
            max_leads_per_month=args.max_leads,
            features={},
            meta_json={
                "created_via": "scripts/create_tenant.py",
                "created_by": os.environ.get("USER") or "system",
            },
            created_at=now,
            updated_at=now,
        )
        session.add(tenant)
        await session.commit()
        print(f"OK: created tenant id={tenant_id} slug={args.handle} plan={args.plan}")
        print(f"Next steps (per docs/ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md Day 1):")
        print(f"  1. Provision WhatsApp Business number → configure webhook routing")
        print(f"  2. Email SPF/DKIM DNS records to customer (15-min task)")
        print(f"  3. Pre-seed 20 prospects from customer CSV import")
        print(f"  4. Schedule Discovery call within 24h")
        return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--handle", required=True,
                   help="lowercase slug, e.g. 'acme_saas' (will be tenant URL key)")
    p.add_argument("--name", required=True, help="display name, e.g. 'ACME SaaS Co'")
    p.add_argument("--plan", default="pilot", choices=sorted(VALID_PLANS))
    p.add_argument("--locale", default="ar", choices=sorted(VALID_LOCALES))
    p.add_argument("--timezone", default="Asia/Riyadh")
    p.add_argument("--currency", default="SAR")
    p.add_argument("--max-users", type=int, default=5)
    p.add_argument("--max-leads", type=int, default=1000,
                   help="max leads per month for this tenant")
    p.add_argument("--dry-run", action="store_true", help="validate + show summary without writing")
    p.add_argument("--idempotent", action="store_true",
                   help="exit 0 instead of 1 if tenant already exists")
    args = p.parse_args()

    err = _validate_args(args)
    if err:
        print(f"VALIDATION: {err}", file=sys.stderr)
        return 2

    try:
        return asyncio.run(_create(args))
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
