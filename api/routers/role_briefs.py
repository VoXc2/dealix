"""
Role Briefs router — daily decisions per role.

Endpoint:
    GET /api/v1/role-briefs/daily?role={ceo|sales_manager|growth_manager|
                                       revops|customer_success|agency_partner|
                                       finance|compliance}

The router fetches minimal projections from DB + delegates to
role_brief_builder.build(role, data=...). All briefs are pure data; no
auto-send. The Top-3 decisions come back ranked by card_priority_ranker.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from auto_client_acquisition.business.commission_calculator import (
    expected_monthly_commission,
)
from auto_client_acquisition.revenue_company_os.card_priority_ranker import rank
from auto_client_acquisition.revenue_company_os.role_brief_builder import (
    SUPPORTED_ROLES, build,
)
from auto_client_acquisition.revenue_company_os.proof_pack_builder import build_pack
from core.config.settings import get_settings
from db.models import (
    CustomerRecord, DealRecord, FunnelEventRecord, MeetingRecord, ObjectionEventRecord,
    PartnerRecord, PaymentRecord, ProofEventRecord, ServiceSessionRecord,
    SubscriptionRecord, SupportTicketRecord,
)
from db.session import get_session

router = APIRouter(prefix="/api/v1/role-briefs", tags=["role-briefs"])


@router.get("/roles")
async def list_roles() -> dict[str, Any]:
    return {"roles": list(SUPPORTED_ROLES)}


@router.get("/daily")
async def daily(
    role: str = Query(..., description="ceo|sales_manager|growth_manager|revops|customer_success|agency_partner|finance|compliance"),
    partner_id: str | None = Query(default=None),
    customer_id: str | None = Query(default=None),
) -> dict[str, Any]:
    """Defensive: never 500. Captures gather/build errors into _errors so
    the consumer (CLI / dashboard) keeps working with a degraded brief
    instead of an opaque server error."""
    role = role.lower()
    if role not in SUPPORTED_ROLES:
        raise HTTPException(status_code=400, detail=f"unknown_role: {role}")

    errors: dict[str, str] = {}
    try:
        data = await _gather_data(role, partner_id=partner_id, customer_id=customer_id)
    except HTTPException:
        # 4xx semantic errors (e.g., partner_id required for agency) must
        # propagate so FastAPI returns the correct status code.
        raise
    except Exception as exc:  # noqa: BLE001
        errors["_gather_data"] = f"{type(exc).__name__}: {str(exc)[:300]}"
        data = {}

    try:
        brief = build(role, data=data)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        errors["build"] = f"{type(exc).__name__}: {str(exc)[:300]}"
        brief = {
            "role": role,
            "brief_type": "degraded",
            "summary": {},
            "top_decisions": [],
            "blocked_today_ar": [],
        }

    try:
        decisions = brief.get("top_decisions") or []
        brief["top_decisions"] = rank(decisions, top_n=3)
    except Exception as exc:  # noqa: BLE001
        errors["rank"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    if errors:
        brief["_errors"] = errors
    return brief


# ── Data gatherers ───────────────────────────────────────────────


async def _gather_data(role: str, *, partner_id: str | None, customer_id: str | None) -> dict[str, Any]:
    """Pull just enough rows for the requested role. Pure read."""
    settings = get_settings()
    # Naive UTC for compatibility with existing TIMESTAMP (no tz) columns
    _now = datetime.now(timezone.utc).replace(tzinfo=None)
    one_day_ago = _now - timedelta(days=1)
    seven_days_ago = _now - timedelta(days=7)

    out: dict[str, Any] = {"settings": settings}

    if role in ("sales_manager", "ceo"):
        async with get_session() as s:
            deals = list((await s.execute(select(DealRecord).limit(500))).scalars().all())
            sessions = list((await s.execute(select(ServiceSessionRecord).limit(500))).scalars().all())
            objections = list((await s.execute(
                select(ObjectionEventRecord).where(ObjectionEventRecord.outcome == "open").limit(200)
            )).scalars().all())
        out["deals"] = deals
        out["sessions"] = sessions
        out["objection_events"] = objections

    if role == "growth_manager":
        async with get_session() as s:
            yesterday = list((await s.execute(
                select(ProofEventRecord).where(ProofEventRecord.occurred_at >= one_day_ago)
            )).scalars().all())
        out["yesterday_events"] = yesterday

    if role == "revops":
        async with get_session() as s:
            events = list((await s.execute(
                select(FunnelEventRecord).where(FunnelEventRecord.occurred_at >= seven_days_ago)
            )).scalars().all())
        counts: Counter[str] = Counter()
        for e in events:
            counts[e.stage] += 1
        out["funnel_event_counts"] = dict(counts)

    if role == "customer_success":
        async with get_session() as s:
            customers = list((await s.execute(select(CustomerRecord).limit(500))).scalars().all())
            tickets = list((await s.execute(select(SupportTicketRecord).limit(500))).scalars().all())
            sessions = list((await s.execute(select(ServiceSessionRecord).limit(500))).scalars().all())
        out["customers"] = customers
        out["tickets"] = tickets
        out["sessions"] = sessions

    if role == "agency_partner":
        if not partner_id:
            raise HTTPException(status_code=400, detail="partner_id_required_for_agency_brief")
        async with get_session() as s:
            partner = (await s.execute(
                select(PartnerRecord).where(PartnerRecord.id == partner_id)
            )).scalar_one_or_none()
            if partner is None:
                raise HTTPException(status_code=404, detail="partner_not_found")
            subs = list((await s.execute(
                select(SubscriptionRecord).where(SubscriptionRecord.partner_id == partner_id)
            )).scalars().all())
            cust_ids = sorted({sub.customer_id for sub in subs if sub.customer_id})
            customers = []
            if cust_ids:
                customers = list((await s.execute(
                    select(CustomerRecord).where(CustomerRecord.id.in_(cust_ids))
                )).scalars().all())
            sessions = list((await s.execute(
                select(ServiceSessionRecord).where(ServiceSessionRecord.partner_id == partner_id).limit(500)
            )).scalars().all())
        out["partner"] = partner
        out["customers"] = customers
        out["sessions"] = sessions
        out["expected_commission_sar"] = expected_monthly_commission(partner, subs)

    if role == "finance":
        async with get_session() as s:
            sessions = list((await s.execute(select(ServiceSessionRecord).limit(500))).scalars().all())
            payments = list((await s.execute(
                select(PaymentRecord).where(PaymentRecord.paid_at >= seven_days_ago).limit(500)
            )).scalars().all())
        out["sessions"] = sessions
        out["payments"] = payments
        out["expected_partner_commission_sar"] = 0.0

    if role == "compliance":
        async with get_session() as s:
            events = list((await s.execute(
                select(ProofEventRecord).where(ProofEventRecord.occurred_at >= one_day_ago).limit(500)
            )).scalars().all())
        out["proof_events"] = events

    if role == "meeting_intelligence":
        async with get_session() as s:
            meetings = list((await s.execute(
                select(MeetingRecord).where(MeetingRecord.occurred_at >= seven_days_ago).limit(500)
            )).scalars().all())
            events = list((await s.execute(
                select(ProofEventRecord).where(ProofEventRecord.occurred_at >= seven_days_ago).limit(500)
            )).scalars().all())
        out["meetings"] = meetings
        out["proof_events"] = events

    if role == "ceo":
        # Compose mini-summaries that ceo_command_os needs
        sales_summary = {
            "deals_at_risk": 0,
            "pilot_offers_ready": 0,
        }
        if "sessions" in out:
            sales_summary["pilot_offers_ready"] = sum(
                1 for x in out["sessions"]
                if x.service_id == "growth_starter" and x.status in ("new", "waiting_inputs")
            )
        out["sales_summary"] = sales_summary
        out["growth_summary"] = {"focus_segment": "وكالات B2B في الرياض"}
        async with get_session() as s:
            evs = list((await s.execute(
                select(ProofEventRecord).where(ProofEventRecord.occurred_at >= seven_days_ago).limit(500)
            )).scalars().all())
        out["proof_summary"] = build_pack(evs)
        out["partner_summary"] = {"hot_partners": 0}

    return out
