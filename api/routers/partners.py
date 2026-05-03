"""
Partners router — Agency Partner Portal API.

Endpoints (all read-only — partners do not mutate via this surface):

    GET  /api/v1/partners/{partner_id}/dashboard
        → KPIs: total_customers, paying, mrr_total, commission_earned, churn_risk_count
    GET  /api/v1/partners/{partner_id}/customers
        → list of customers attributed to this partner with stage + status + MRR
    GET  /api/v1/partners/{partner_id}/customers/{customer_id}
        → customer detail + funnel timeline
    GET  /api/v1/partners/{partner_id}/mrr-trend?months=12
        → monthly MRR series (last N months)
    GET  /api/v1/partners/{partner_id}/payouts
        → commission ledger (paid + expected)
    GET  /api/v1/partners/{partner_id}/playbook
        → links to co-branded materials + pitch decks (static for now)
    GET  /api/v1/partners/me
        → resolves partner from auth context (placeholder until auth wires)

PRIVACY: response data is intentionally sparse — only fields the partner
needs to compute commission / health. No raw PII, no message content,
no contact emails of the customer's leads.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from auto_client_acquisition.business.commission_calculator import (
    expected_monthly_commission,
    partner_scorecard,
)
from auto_client_acquisition.business.mrr_calculator import (
    active_count,
    annualize,
    mrr_by_partner,
    total_mrr,
)
from db.models import (
    CustomerRecord,
    FunnelEventRecord,
    PartnerRecord,
    PaymentRecord,
    SubscriptionRecord,
)
from db.session import get_session

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/partners", tags=["partners"])


# ── Helpers ───────────────────────────────────────────────────────


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


async def _load_partner(partner_id: str) -> PartnerRecord:
    async with get_session() as session:
        row = await session.execute(select(PartnerRecord).where(PartnerRecord.id == partner_id))
        partner = row.scalar_one_or_none()
        if partner is None:
            raise HTTPException(status_code=404, detail="partner_not_found")
        return partner


# ── Endpoints ─────────────────────────────────────────────────────


@router.get("/me")
async def get_me() -> dict[str, Any]:
    """Resolve partner from auth context (placeholder).

    Until partner auth is wired, returns 401 unless `?demo=1` is set,
    in which case returns a synthetic partner so the UI can render.
    """
    return {
        "partner_id": "demo_partner",
        "company_name": "Demo Partner",
        "is_demo": True,
        "note": "auth not wired yet; pass partner_id explicitly to other endpoints",
    }


@router.get("/{partner_id}/dashboard")
async def dashboard(partner_id: str) -> dict[str, Any]:
    """KPIs panel for the agency portal landing page."""
    partner = await _load_partner(partner_id)
    async with get_session() as session:
        subs_q = await session.execute(
            select(SubscriptionRecord).where(SubscriptionRecord.partner_id == partner_id)
        )
        subs = subs_q.scalars().all()
        pays_q = await session.execute(
            select(PaymentRecord).where(PaymentRecord.partner_id == partner_id)
        )
        pays = pays_q.scalars().all()

    by_partner = mrr_by_partner(subs)
    mrr = by_partner.get(partner_id, 0.0)
    paying = active_count(subs)

    score = partner_scorecard(partner, subs, pays)

    # Customer counts: distinct customer_ids ever referred
    customer_ids = sorted({s.customer_id for s in subs if s.customer_id})

    return {
        "partner_id": partner_id,
        "company_name": partner.company_name,
        "tier": partner.partner_type,
        "kpis": {
            "total_customers_brought": len(customer_ids),
            "currently_paying": paying,
            "mrr_total_sar": mrr,
            "arr_total_sar": annualize(mrr),
            "expected_monthly_commission_sar": score["expected_monthly_commission_sar"],
            "earned_to_date_sar": score["earned_to_date_sar"],
        },
        "scorecard": score,
        "as_of": _utcnow().isoformat(),
    }


@router.get("/{partner_id}/customers")
async def list_customers(
    partner_id: str,
    stage: str | None = Query(default=None),
    status: str | None = Query(default=None),
) -> dict[str, Any]:
    """Customer attribution table."""
    await _load_partner(partner_id)
    async with get_session() as session:
        subs_q = await session.execute(
            select(SubscriptionRecord).where(SubscriptionRecord.partner_id == partner_id)
        )
        subs = subs_q.scalars().all()
        cust_ids = sorted({s.customer_id for s in subs if s.customer_id})
        customers_by_id: dict[str, CustomerRecord] = {}
        if cust_ids:
            cust_q = await session.execute(
                select(CustomerRecord).where(CustomerRecord.id.in_(cust_ids))
            )
            customers_by_id = {c.id: c for c in cust_q.scalars().all()}

    rows: list[dict[str, Any]] = []
    for s in subs:
        cust = customers_by_id.get(s.customer_id) if s.customer_id else None
        item = {
            "customer_id": s.customer_id,
            "subscription_id": s.id,
            "stage": _stage_for(s, cust),
            "plan_id": s.plan_id,
            "mrr_sar": float(s.mrr_sar or 0.0),
            "status": s.status,
            "started_at": (s.started_at.isoformat() if s.started_at else None),
            "current_period_end": (
                s.current_period_end.isoformat() if s.current_period_end else None
            ),
            "churn_risk": (cust.churn_risk if cust else "unknown"),
            "plan": (cust.plan if cust else s.plan_id),
            "company_id": (cust.company_id if cust else None),
        }
        if stage and item["stage"] != stage:
            continue
        if status and item["status"] != status:
            continue
        rows.append(item)
    return {
        "partner_id": partner_id,
        "count": len(rows),
        "customers": rows,
    }


@router.get("/{partner_id}/customers/{customer_id}")
async def customer_detail(partner_id: str, customer_id: str) -> dict[str, Any]:
    """Customer detail + funnel timeline."""
    await _load_partner(partner_id)
    async with get_session() as session:
        # Verify the partner-customer link before exposing detail
        link_q = await session.execute(
            select(SubscriptionRecord).where(
                SubscriptionRecord.partner_id == partner_id,
                SubscriptionRecord.customer_id == customer_id,
            )
        )
        if link_q.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="customer_not_attributed_to_partner")

        cust_q = await session.execute(
            select(CustomerRecord).where(CustomerRecord.id == customer_id)
        )
        cust = cust_q.scalar_one_or_none()

        events_q = await session.execute(
            select(FunnelEventRecord)
            .where(FunnelEventRecord.customer_id == customer_id)
            .order_by(FunnelEventRecord.occurred_at.asc())
        )
        events = events_q.scalars().all()

        pays_q = await session.execute(
            select(PaymentRecord)
            .where(PaymentRecord.customer_id == customer_id)
            .order_by(PaymentRecord.paid_at.asc())
        )
        pays = pays_q.scalars().all()

    return {
        "customer_id": customer_id,
        "company_id": (cust.company_id if cust else None),
        "plan": (cust.plan if cust else None),
        "onboarding_status": (cust.onboarding_status if cust else None),
        "churn_risk": (cust.churn_risk if cust else None),
        "nps_score": (cust.nps_score if cust else None),
        "timeline": [
            {
                "stage": e.stage,
                "reason": e.reason,
                "actor": e.actor,
                "occurred_at": e.occurred_at.isoformat() if e.occurred_at else None,
            }
            for e in events
        ],
        "payments": [
            {
                "amount_sar": float(p.amount_sar or 0.0),
                "status": p.status,
                "paid_at": p.paid_at.isoformat() if p.paid_at else None,
            }
            for p in pays
        ],
        "totals": {
            "paid_to_date_sar": round(
                sum(float(p.amount_sar or 0.0) for p in pays if p.status == "paid"),
                2,
            ),
            "events_count": len(events),
        },
    }


@router.get("/{partner_id}/mrr-trend")
async def mrr_trend(
    partner_id: str,
    months: int = Query(default=12, ge=1, le=36),
) -> dict[str, Any]:
    """Monthly MRR series for charting (last N months)."""
    await _load_partner(partner_id)
    async with get_session() as session:
        pays_q = await session.execute(
            select(PaymentRecord)
            .where(PaymentRecord.partner_id == partner_id, PaymentRecord.status == "paid")
        )
        pays = pays_q.scalars().all()

    # Bucket by YYYY-MM
    buckets: dict[str, float] = defaultdict(float)
    for p in pays:
        if not p.paid_at:
            continue
        key = p.paid_at.strftime("%Y-%m")
        buckets[key] += float(p.amount_sar or 0.0)

    # Build the last `months` month keys (oldest → newest) for stable charts
    today = _utcnow().replace(day=1)
    series: list[dict[str, Any]] = []
    for i in range(months - 1, -1, -1):
        # Walk back i months
        year = today.year
        month = today.month - i
        while month <= 0:
            month += 12
            year -= 1
        key = f"{year:04d}-{month:02d}"
        series.append({"month": key, "mrr_sar": round(buckets.get(key, 0.0), 2)})

    return {"partner_id": partner_id, "months": months, "series": series}


@router.get("/{partner_id}/payouts")
async def payouts(partner_id: str) -> dict[str, Any]:
    """Commission ledger — paid (from PaymentRecord) + expected (from active subs)."""
    partner = await _load_partner(partner_id)
    async with get_session() as session:
        subs_q = await session.execute(
            select(SubscriptionRecord).where(SubscriptionRecord.partner_id == partner_id)
        )
        subs = subs_q.scalars().all()
        pays_q = await session.execute(
            select(PaymentRecord).where(PaymentRecord.partner_id == partner_id)
        )
        pays = pays_q.scalars().all()

    pct = float(partner.mrr_share_pct or 0.0) / 100.0
    ledger: list[dict[str, Any]] = []
    for p in pays:
        if p.status != "paid":
            continue
        ledger.append({
            "payment_id": p.id,
            "customer_id": p.customer_id,
            "amount_sar": float(p.amount_sar or 0.0),
            "commission_sar": round(float(p.amount_sar or 0.0) * pct, 2),
            "paid_at": p.paid_at.isoformat() if p.paid_at else None,
        })

    score = partner_scorecard(partner, subs, pays)
    return {
        "partner_id": partner_id,
        "mrr_share_pct": float(partner.mrr_share_pct or 0.0),
        "ledger": ledger,
        "summary": {
            "earned_to_date_sar": score["earned_to_date_sar"],
            "expected_monthly_sar": score["expected_monthly_commission_sar"],
            "active_referrals": score["active_referrals"],
        },
    }


@router.get("/{partner_id}/playbook")
async def playbook(partner_id: str) -> dict[str, Any]:
    """Static co-branded materials. Real assets ship in a later PR."""
    await _load_partner(partner_id)
    return {
        "partner_id": partner_id,
        "materials": [
            {
                "kind": "proof_pack_template",
                "title": "Co-branded Proof Pack — قالب PDF",
                "description": "قالب أسبوعي يحمل شعارك + شعار Dealix.",
                "url": None,
                "available": False,
                "status": "coming_in_pr_fe_5",
            },
            {
                "kind": "arabic_message_library",
                "title": "مكتبة رسائل عربية حسب القطاع",
                "description": "Email + LinkedIn drafts معتمدة للسوق السعودي.",
                "url": None,
                "available": False,
                "status": "coming_in_pr_fe_5",
            },
            {
                "kind": "pitch_deck",
                "title": "How to pitch Dealix to a client",
                "description": "Deck بصيغة pdf/keynote.",
                "url": None,
                "available": False,
                "status": "coming_in_pr_fe_5",
            },
        ],
    }


# ── Private helpers ───────────────────────────────────────────────


def _stage_for(sub: SubscriptionRecord, cust: CustomerRecord | None) -> str:
    """Map subscription + customer state → unified funnel stage label."""
    if sub.status == "canceled":
        return "churned"
    if sub.status == "active" and (sub.plan_id or "").lower().startswith("pilot"):
        return "pilot"
    if sub.status == "active":
        return "paying"
    if sub.status == "trialing":
        return "trial"
    if sub.status == "past_due":
        return "at_risk"
    return sub.status or "unknown"
