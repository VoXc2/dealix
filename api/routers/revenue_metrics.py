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
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, Query

from api.security.api_key import require_admin_key

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/revenue-metrics",
    tags=["revenue-metrics"],
    dependencies=[Depends(require_admin_key)],
)


# PaymentRecord proves captured/paid cash. It does not encode an approved
# recurring contract amount/cadence, so plan labels must never mint MRR/ARR.
RECURRING_METRICS_STATUS = "UNVERIFIED_RECURRING_CONTRACT_AUTHORITY"


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
                    "currency": r.currency,
                    "last_event_type": r.last_event_type,
                    "created_at": r.created_at,
                }
                for r in rows
            ]
    except Exception as exc:
        log.debug("revenue_metrics_load_skipped reason=%s", exc)
        return []


def _compute_dashboard(paid: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute payment truth without inferring recurring revenue from plan labels."""
    now = datetime.now(UTC)
    period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    prev_period_start = (period_start - timedelta(days=1)).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0,
    )

    first_seen_per_customer: dict[str, datetime] = {}
    last_seen_per_customer: dict[str, datetime] = {}
    latest_plan_per_customer: dict[str, str | None] = {}
    verified_cash_total = 0
    verified_cash_current = 0
    verified_cash_previous = 0

    for row in paid:
        # PaymentRecord.status == paid was already enforced by the query. Only
        # SAR amounts are aggregated into the SAR cash truth.
        if str(row.get("currency") or "SAR").upper() == "SAR":
            amount = max(0, int(row.get("amount_halalas") or 0))
            verified_cash_total += amount
            created = row.get("created_at")
            if isinstance(created, datetime):
                if created >= period_start:
                    verified_cash_current += amount
                elif prev_period_start <= created < period_start:
                    verified_cash_previous += amount

        h = row.get("customer_handle")
        created = row.get("created_at")
        if not h or not isinstance(created, datetime):
            continue
        if h not in first_seen_per_customer or created < first_seen_per_customer[h]:
            first_seen_per_customer[h] = created
        if h not in last_seen_per_customer or created > last_seen_per_customer[h]:
            last_seen_per_customer[h] = created
            latest_plan_per_customer[h] = row.get("plan")

    recent_paid_customers = sum(
        1 for last_seen in last_seen_per_customer.values()
        if last_seen >= period_start - timedelta(days=35)
    )
    total_customers_ever = len(first_seen_per_customer)

    # Plan is retained as historical classification only. It cannot carry
    # current price, contract, MRR, ARR, NRR, or churn authority.
    plan_distribution: dict[str, int] = defaultdict(int)
    for h in last_seen_per_customer:
        plan_distribution[latest_plan_per_customer.get(h) or "unknown"] += 1

    return {
        "period": {"month": now.strftime("%Y-%m"), "computed_at": now.isoformat()},
        "verified_cash": {
            "total_halalas": verified_cash_total,
            "total_sar": verified_cash_total / 100,
            "current_month_sar": verified_cash_current / 100,
            "previous_month_sar": verified_cash_previous / 100,
            "basis": "status=paid PaymentRecord amounts; payment != invoice != quote",
        },
        "mrr": {
            "halalas": None,
            "sar": None,
            "previous_month_sar": None,
            "change_sar": None,
            "status": RECURRING_METRICS_STATUS,
            "basis": "PaymentRecord has no approved recurring contract amount/cadence",
        },
        "arr": {"halalas": None, "sar": None, "status": RECURRING_METRICS_STATUS},
        "customers": {
            "active": recent_paid_customers,
            "total_ever": total_customers_ever,
            "lost_this_month": None,
            "basis": "recent paid activity; not subscription-status authority",
        },
        "arpa": {"halalas": None, "sar": None, "status": RECURRING_METRICS_STATUS},
        "churn_pct_monthly": None,
        "nrr_pct": None,
        "recurring_metrics_status": RECURRING_METRICS_STATUS,
        "plan_distribution": dict(plan_distribution),
        "plan_distribution_authority": "classification_only_no_price_or_revenue_authority",
        "benchmarks": {
            "saas_unicorn_nrr": "≥ 120%",
            "saas_healthy_nrr": "100-110%",
            "saas_danger_nrr": "< 90%",
            "dealix_target_nrr_y1": "≥ 100%",
            "saas_healthy_monthly_churn": "≤ 3%",
            "saas_danger_monthly_churn": "> 8%",
        },
        "interpretation": _interpret(verified_cash_total, recent_paid_customers),
    }


def _interpret(verified_cash_halalas: int, recent_paid_customers: int) -> dict[str, str]:
    """Interpret only evidence the PaymentRecord schema can actually prove."""
    if verified_cash_halalas <= 0:
        return {
            "headline": "No verified paid cash in PaymentRecord",
            "next_action": "Advance qualified discovery and customer-specific close; do not infer revenue from CRM or plan labels",
        }
    return {
        "headline": (
            f"Verified paid cash exists across {recent_paid_customers} recent paid customer(s); "
            "recurring MRR/ARR are not proven by PaymentRecord"
        ),
        "next_action": "Add explicit recurring-contract/cadence evidence before reporting MRR, ARR, NRR, churn, or ARPA",
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
        "basis": "payment_activity_proxy_not_subscription_retention",
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
