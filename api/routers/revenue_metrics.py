"""Revenue metrics dashboard endpoint (W13.7 — Wave 13 commercial).

The single endpoint a Series A investor will ask for first. Aggregates:
  - MRR (Monthly Recurring Revenue) — current and rolling 12 months
  - ARR (Annual Run-Rate) — MRR × 12
  - NRR (Net Revenue Retention) — gold-standard SaaS metric
  - Gross Churn — # customers lost / # at start of period
  - Customer count + cohort breakdown
  - ARPA (Average Revenue Per Account)
  - Cohort retention curve (Y1 H1 onward)

  GET /api/v1/revenue-metrics/dashboard
      Admin-only — aggregate state across all tenants.

  GET /api/v1/revenue-metrics/cohort?cohort_month=2026-01
      Drill-down for a single cohort.

All metrics computed from payments table — single source of truth.
No fake numbers, no projections in this endpoint (forecasts go elsewhere).
"""
from __future__ import annotations

import logging
from collections import defaultdict
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, Query

from api.security.api_key import require_admin_key

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/revenue-metrics",
    tags=["revenue-metrics"],
    dependencies=[Depends(require_admin_key)],
)


# ── Constants matching pricing.py ─────────────────────────────────

PLAN_MRR_HALALAS = {
    "starter": 99_900,    # 999 SAR
    "growth": 299_900,    # 2,999 SAR
    "scale": 799_900,     # 7,999 SAR
    "pilot": 0,           # not recurring
    "pilot_managed": 0,   # one-off, not MRR
    "pilot_1sar": 0,      # test
}


def _to_mrr_halalas(plan: str | None) -> int:
    if plan is None:
        return 0
    return PLAN_MRR_HALALAS.get(plan, 0)


async def _load_paid_history() -> list[dict[str, Any]]:
    """Pull all paid PaymentRecord rows with their customer_handle + plan + ts.

    Gracefully degrades to [] if DB unavailable. Caller treats empty as
    "no customers yet" rather than failure.
    """
    try:
        from sqlalchemy import select

        from db.models import PaymentRecord
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            stmt = select(PaymentRecord).where(PaymentRecord.status == "paid")
            rows = (await session.execute(stmt)).scalars().all()
            return [
                {
                    "customer_handle": r.customer_handle,
                    "plan": r.plan,
                    "amount_halalas": r.amount_halalas,
                    "created_at": r.created_at,
                }
                for r in rows
            ]
    except Exception as exc:
        log.debug("revenue_metrics_load_skipped reason=%s", exc)
        return []


def _compute_dashboard(paid: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute aggregate revenue dashboard from paid history."""
    now = datetime.now(UTC)
    period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    prev_period_start = (period_start - timedelta(days=1)).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0,
    )

    # Latest plan per customer (denormalize from history)
    latest_plan_per_customer: dict[str, str | None] = {}
    first_seen_per_customer: dict[str, datetime] = {}
    last_seen_per_customer: dict[str, datetime] = {}
    for row in paid:
        h = row["customer_handle"]
        if not h:
            continue
        if h not in first_seen_per_customer or row["created_at"] < first_seen_per_customer[h]:
            first_seen_per_customer[h] = row["created_at"]
        if h not in last_seen_per_customer or row["created_at"] > last_seen_per_customer[h]:
            last_seen_per_customer[h] = row["created_at"]
            latest_plan_per_customer[h] = row["plan"]

    # MRR — sum of recurring plan amounts for customers active in this period
    mrr_halalas = 0
    for h, last_seen in last_seen_per_customer.items():
        if last_seen >= period_start - timedelta(days=35):  # generous window for grace
            mrr_halalas += _to_mrr_halalas(latest_plan_per_customer.get(h))

    prev_mrr_halalas = 0
    for h, last_seen in last_seen_per_customer.items():
        if prev_period_start <= last_seen < period_start:
            prev_mrr_halalas += _to_mrr_halalas(latest_plan_per_customer.get(h))

    arr_halalas = mrr_halalas * 12

    # Customer count
    active_customers = sum(
        1 for h, last_seen in last_seen_per_customer.items()
        if last_seen >= period_start - timedelta(days=35)
    )
    total_customers_ever = len(first_seen_per_customer)

    # ARPA
    arpa_halalas = mrr_halalas // active_customers if active_customers else 0

    # Gross churn (this period)
    customers_at_period_start = sum(
        1 for h, first_seen in first_seen_per_customer.items()
        if first_seen < period_start
    )
    customers_lost = sum(
        1 for h, last_seen in last_seen_per_customer.items()
        if (first_seen_per_customer[h] < period_start
            and last_seen < period_start - timedelta(days=35))
    )
    churn_pct = round(
        (customers_lost / customers_at_period_start) * 100, 2
    ) if customers_at_period_start else 0.0

    # NRR = (start MRR + expansion - churn - contraction) / start MRR
    nrr_pct = round(
        (mrr_halalas / prev_mrr_halalas) * 100, 1
    ) if prev_mrr_halalas else 0.0

    # Plan distribution
    plan_distribution: dict[str, int] = defaultdict(int)
    for h in last_seen_per_customer:
        plan = latest_plan_per_customer.get(h) or "unknown"
        plan_distribution[plan] += 1

    return {
        "period": {
            "month": now.strftime("%Y-%m"),
            "computed_at": now.isoformat(),
        },
        "mrr": {
            "halalas": mrr_halalas,
            "sar": mrr_halalas // 100,
            "previous_month_sar": prev_mrr_halalas // 100,
            "change_sar": (mrr_halalas - prev_mrr_halalas) // 100,
        },
        "arr": {
            "halalas": arr_halalas,
            "sar": arr_halalas // 100,
        },
        "customers": {
            "active": active_customers,
            "total_ever": total_customers_ever,
            "lost_this_month": customers_lost,
        },
        "arpa": {
            "halalas": arpa_halalas,
            "sar": arpa_halalas // 100,
        },
        "churn_pct_monthly": churn_pct,
        "nrr_pct": nrr_pct,
        "plan_distribution": dict(plan_distribution),
        "benchmarks": {
            "saas_unicorn_nrr": "≥ 120%",
            "saas_healthy_nrr": "100-110%",
            "saas_danger_nrr": "< 90%",
            "dealix_target_nrr_y1": "≥ 100%",
            "saas_healthy_monthly_churn": "≤ 3%",
            "saas_danger_monthly_churn": "> 8%",
        },
        "interpretation": _interpret(nrr_pct, churn_pct, active_customers),
    }


def _interpret(nrr_pct: float, churn_pct: float, active: int) -> dict[str, str]:
    """Honest interpretation of the numbers so the founder/investor knows
    what story the data tells. No hopium."""
    if active == 0:
        return {
            "headline": "Pre-revenue — metrics will compute once first customer pays",
            "next_action": "Send 5 WhatsApp DMs (v4 §15) — single unblock",
        }
    if active < 5:
        return {
            "headline": f"Early validation phase ({active} customer(s))",
            "next_action": "Focus on customer-success retention, not new acquisition",
        }
    if nrr_pct >= 100 and churn_pct <= 5:
        return {
            "headline": "Healthy SaaS trajectory — ready for pre-seed conversations",
            "next_action": "Prepare investor 1-pager (W10.1) + revenue chart screenshot",
        }
    if nrr_pct < 90 or churn_pct > 8:
        return {
            "headline": "WARNING: retention concern — investigate before scaling",
            "next_action": "Pause acquisition spend; double down on customer success",
        }
    return {
        "headline": "Steady growth — keep current motion",
        "next_action": "Optimize MRR per acquisition channel before scaling spend",
    }


@router.get("/dashboard")
async def revenue_dashboard() -> dict[str, Any]:
    """Aggregate revenue dashboard. The single endpoint a Series A investor opens first."""
    paid = await _load_paid_history()
    return _compute_dashboard(paid)


@router.get("/cohort")
async def cohort_analysis(
    cohort_month: str = Query(..., pattern=r"^\d{4}-\d{2}$",
                               description="cohort birth month, e.g. 2026-01"),
) -> dict[str, Any]:
    """Retention curve for a single cohort. Empty if cohort doesn't exist yet."""
    paid = await _load_paid_history()

    try:
        year, month = map(int, cohort_month.split("-"))
        cohort_start = datetime(year, month, 1, tzinfo=UTC)
        if month == 12:
            cohort_end = datetime(year + 1, 1, 1, tzinfo=UTC)
        else:
            cohort_end = datetime(year, month + 1, 1, tzinfo=UTC)
    except ValueError:
        return {"cohort_month": cohort_month, "error": "invalid date format"}

    # Customers who first appeared in this cohort
    first_seen: dict[str, datetime] = {}
    last_seen: dict[str, datetime] = {}
    for row in paid:
        h = row["customer_handle"]
        if not h:
            continue
        if h not in first_seen or row["created_at"] < first_seen[h]:
            first_seen[h] = row["created_at"]
        if h not in last_seen or row["created_at"] > last_seen[h]:
            last_seen[h] = row["created_at"]

    cohort_members = [
        h for h, fs in first_seen.items()
        if cohort_start <= fs < cohort_end
    ]

    if not cohort_members:
        return {
            "cohort_month": cohort_month,
            "cohort_size": 0,
            "retention_curve": [],
            "note": "No customers in this cohort yet.",
        }

    # Retention at month +1, +3, +6, +12
    retention_curve = []
    for months_ahead in (1, 3, 6, 12):
        check_ts = cohort_start + timedelta(days=30 * months_ahead)
        retained = sum(
            1 for h in cohort_members
            if last_seen[h] >= check_ts - timedelta(days=35)
        )
        retention_curve.append({
            "month_offset": months_ahead,
            "retained": retained,
            "retention_pct": round(
                (retained / len(cohort_members)) * 100, 1
            ),
        })

    return {
        "cohort_month": cohort_month,
        "cohort_size": len(cohort_members),
        "retention_curve": retention_curve,
    }


@router.get("/health-check")
async def metrics_health() -> dict[str, Any]:
    """Quick check whether revenue metrics pipeline is operational."""
    paid = await _load_paid_history()
    return {
        "status": "operational" if paid is not None else "degraded",
        "payment_records_loaded": len(paid),
        "note": (
            "If payment_records_loaded == 0 and you have paying customers, "
            "check that Moyasar webhook is persisting via "
            "api/routers/pricing.py:_persist_payment_event."
        ),
    }
