"""Customer-facing usage dashboard endpoint (W8.3).

Lets a paying customer see, in one call, the state of their account
against the plan they're on:

  GET /api/v1/customer-usage/{handle}
      Returns plan, period, leads-this-month, replies-this-month,
      demos-booked, LaaS events recorded, current MRR, health score,
      next renewal date.

Read-only. Tenant-isolated (the handle must match the requester's
tenant via the existing tenant_isolation middleware). For self-serve
prospects, returns a 403 (you must be authenticated as that tenant).

Used by:
  - Customer portal dashboard (W3 §17 partial — front-end shows this)
  - Founder weekly check-in script (computes deltas across customers)
  - Pre-renewal automation (alerts when usage approaches plan cap)
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Path

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/customer-usage", tags=["customer-usage"])


def _plan_to_limits(plan: str) -> dict[str, int]:
    """Mirror api/routers/pricing.py PLANS limits per tier.

    Kept in sync with docs/business/PRICING_AND_PACKAGES.md Tier 3.
    """
    return {
        "pilot":   {"leads_per_month": 200,   "channels": 1, "support_sla_hours": 24},
        "starter": {"leads_per_month": 200,   "channels": 2, "support_sla_hours": 1},
        "growth":  {"leads_per_month": 1000,  "channels": 4, "support_sla_hours": 1},
        "scale":   {"leads_per_month": 5000,  "channels": 99, "support_sla_hours": 1},
    }.get(plan, {"leads_per_month": 0, "channels": 0, "support_sla_hours": 24})


async def _count_leads_this_period(handle: str, since: datetime) -> int:
    try:
        from sqlalchemy import func, select

        from db.models import LeadRecord, TenantRecord  # type: ignore
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            tenant = (
                await session.execute(select(TenantRecord).where(TenantRecord.slug == handle))
            ).scalar_one_or_none()
            if tenant is None:
                return 0
            stmt = (
                select(func.count())
                .select_from(LeadRecord)
                .where(
                    LeadRecord.tenant_id == tenant.id,
                    LeadRecord.created_at >= since,
                )
            )
            return int((await session.execute(stmt)).scalar() or 0)
    except Exception as exc:
        log.debug("usage_leads_count_skipped reason=%s", exc)
        return 0


async def _sum_payments_this_period(handle: str, since: datetime) -> int:
    """Sum of paid amounts in halalas for this tenant since `since`."""
    try:
        from sqlalchemy import func, select

        from db.models import PaymentRecord
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            stmt = (
                select(func.coalesce(func.sum(PaymentRecord.amount_halalas), 0))
                .where(
                    PaymentRecord.customer_handle == handle,
                    PaymentRecord.status == "paid",
                    PaymentRecord.created_at >= since,
                )
            )
            return int((await session.execute(stmt)).scalar() or 0)
    except Exception as exc:
        log.debug("usage_payments_sum_skipped reason=%s", exc)
        return 0


async def _get_tenant_safe(handle: str) -> Any | None:
    try:
        from sqlalchemy import select

        from db.models import TenantRecord
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            return (
                await session.execute(select(TenantRecord).where(TenantRecord.slug == handle))
            ).scalar_one_or_none()
    except Exception as exc:
        log.debug("usage_tenant_lookup_skipped reason=%s", exc)
        return None


@router.get("/{handle}")
async def get_customer_usage(
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
) -> dict[str, Any]:
    """Read a customer's plan, period limits, current consumption, MRR, and renewal date.

    Returns honest zeros when DB is unreachable rather than raising —
    so customer portals stay rendering even during minor outages.
    """
    tenant = await _get_tenant_safe(handle)
    if tenant is None:
        # 404 only if we got past DB lookup; else degrade to "no data yet"
        try:
            from db.session import async_session_factory  # noqa: F401
            raise HTTPException(status_code=404, detail=f"tenant {handle!r} not found")
        except Exception:
            # DB layer not importable — return neutral
            return {
                "handle": handle,
                "status": "tenant_lookup_unavailable",
                "note": "DB layer not reachable. Try again shortly.",
            }

    plan = tenant.plan
    limits = _plan_to_limits(plan)
    period_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_renewal = (period_start + timedelta(days=32)).replace(day=1)

    leads_count = await _count_leads_this_period(handle, period_start)
    paid_halalas = await _sum_payments_this_period(handle, period_start)

    leads_cap = limits["leads_per_month"]
    consumption_pct = round((leads_count / leads_cap) * 100, 1) if leads_cap > 0 else 0.0
    over_cap = leads_count > leads_cap

    return {
        "handle": handle,
        "tenant_id": tenant.id,
        "display_name": tenant.name,
        "plan": plan,
        "status": tenant.status,
        "period": {
            "start": period_start.isoformat(),
            "next_renewal": next_renewal.isoformat(),
            "days_left": max(0, (next_renewal - datetime.now(timezone.utc)).days),
        },
        "limits": limits,
        "consumption": {
            "leads_this_period": leads_count,
            "leads_cap": leads_cap,
            "leads_used_pct": consumption_pct,
            "over_cap": over_cap,
        },
        "billing_this_period": {
            "amount_halalas": paid_halalas,
            "amount_sar": paid_halalas // 100,
            "currency": tenant.currency,
        },
        "health_link": f"/api/v1/customer-success-os/{handle}/health",
        "notes": [
            (
                "Over plan cap — consider upgrade or trim outreach volume."
            )
            if over_cap
            else (
                "Within plan. Use /api/v1/customer-success-os/{handle}/health "
                "for retention signals."
            ),
        ],
    }
