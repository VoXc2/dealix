"""
Companies router — Customer Workspace + Company Brain.

Endpoints:
    GET   /api/v1/companies/{customer_id}/workspace
        Aggregator. Pulls from CustomerRecord, ProofEventRecord,
        MeetingRecord, PaymentRecord, ServiceSessionRecord — filtered
        to one customer. Defensive: per-query session, _errors map
        on failure (mirrors api/routers/founder.py pattern).

    GET   /api/v1/companies/{customer_id}/brain
        Returns the 12 Company Brain fields + computed proof_summary.
        The brain is the per-customer profile that personalizes every
        role brief, draft, and Proof Pack.

    PATCH /api/v1/companies/{customer_id}/brain
        Founder edits the brain after onboarding intake.

    GET   /api/v1/companies
        Paginated list of customers (admin-ish view).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy import desc, func, select

from db.models import (
    CustomerRecord, MeetingRecord, PaymentRecord, ProofEventRecord,
    ServiceSessionRecord,
)
from db.session import get_session

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])


_BRAIN_FIELDS = (
    "company_name", "website", "sector", "city",
    "offer_ar", "ideal_customer_ar", "average_deal_value_sar",
    "approved_channels", "blocked_channels", "tone_ar",
    "forbidden_claims", "current_service_id",
)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _serialize_brain(c: CustomerRecord) -> dict[str, Any]:
    return {
        "customer_id": c.id,
        "plan": c.plan,
        "onboarding_status": c.onboarding_status,
        "company_name": getattr(c, "company_name", "") or "",
        "website": getattr(c, "website", None),
        "sector": getattr(c, "sector", None),
        "city": getattr(c, "city", None),
        "offer_ar": getattr(c, "offer_ar", None),
        "ideal_customer_ar": getattr(c, "ideal_customer_ar", None),
        "average_deal_value_sar": float(getattr(c, "average_deal_value_sar", 0) or 0),
        "approved_channels": list(getattr(c, "approved_channels", []) or []),
        "blocked_channels": list(getattr(c, "blocked_channels", []) or []),
        "tone_ar": getattr(c, "tone_ar", "professional_saudi_arabic"),
        "forbidden_claims": list(getattr(c, "forbidden_claims", []) or []),
        "current_service_id": getattr(c, "current_service_id", None),
        "churn_risk": c.churn_risk,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
    }


@router.get("")
async def list_companies(limit: int = Query(default=50, ge=1, le=500)) -> dict[str, Any]:
    """Paginated list of customers (newest first)."""
    async with get_session() as session:
        rows = list((await session.execute(
            select(CustomerRecord)
            .order_by(desc(CustomerRecord.created_at))
            .limit(limit)
        )).scalars().all())
    return {
        "count": len(rows),
        "companies": [
            {
                "customer_id": r.id,
                "company_name": getattr(r, "company_name", "") or "",
                "plan": r.plan,
                "sector": getattr(r, "sector", None),
                "city": getattr(r, "city", None),
                "current_service_id": getattr(r, "current_service_id", None),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ],
    }


@router.get("/{customer_id}/brain")
async def get_brain(customer_id: str) -> dict[str, Any]:
    """Return the Company Brain — the 12 fields that personalize every
    Dealix action for this customer + a computed proof_summary."""
    async with get_session() as session:
        cust = (await session.execute(
            select(CustomerRecord).where(CustomerRecord.id == customer_id)
        )).scalar_one_or_none()
        if cust is None:
            raise HTTPException(status_code=404, detail="customer_not_found")

        # Compute proof summary
        events = list((await session.execute(
            select(ProofEventRecord).where(ProofEventRecord.customer_id == customer_id)
        )).scalars().all())

    proof_summary = {
        "events_total": len(events),
        "by_unit": {},
        "approvals_pending": 0,
        "estimated_revenue_impact_sar": 0.0,
    }
    for e in events:
        proof_summary["by_unit"][e.unit_type] = proof_summary["by_unit"].get(e.unit_type, 0) + 1
        if e.approval_required and not e.approved:
            proof_summary["approvals_pending"] += 1
        if not e.approval_required or e.approved:
            proof_summary["estimated_revenue_impact_sar"] += float(e.revenue_impact_sar or 0)
    proof_summary["estimated_revenue_impact_sar"] = round(
        proof_summary["estimated_revenue_impact_sar"], 2
    )

    brain = _serialize_brain(cust)
    brain["proof_summary"] = proof_summary
    return brain


@router.patch("/{customer_id}/brain")
async def update_brain(customer_id: str, body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Founder edits the Company Brain. Only the 12 brain fields are mutable."""
    async with get_session() as session:
        cust = (await session.execute(
            select(CustomerRecord).where(CustomerRecord.id == customer_id)
        )).scalar_one_or_none()
        if cust is None:
            raise HTTPException(status_code=404, detail="customer_not_found")
        for field in _BRAIN_FIELDS:
            if field in body:
                setattr(cust, field, body[field])
        await session.commit()
        await session.refresh(cust)
        return _serialize_brain(cust)


@router.get("/{customer_id}/workspace")
async def get_workspace(customer_id: str) -> dict[str, Any]:
    """Single per-customer view: current sprint + open decisions + recent
    activity + risks blocked + next-7-day plan. Defensive — never 500."""
    errors: dict[str, str] = {}
    now = _now()

    # 1. Customer brain
    brain: dict[str, Any] = {}
    try:
        brain = await get_brain(customer_id)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        errors["brain"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 2. Service session (most recent)
    current_sprint: dict[str, Any] | None = None
    try:
        async with get_session() as s:
            row = (await s.execute(
                select(ServiceSessionRecord)
                .where(ServiceSessionRecord.customer_id == customer_id)
                .order_by(desc(ServiceSessionRecord.created_at))
                .limit(1)
            )).scalar_one_or_none()
        if row is not None:
            started = getattr(row, "created_at", None)
            day = 0
            if started:
                day = max(0, (now - started).days)
            current_sprint = {
                "session_id": row.id,
                "service_id": row.service_id,
                "status": row.status,
                "started_at": started.isoformat() if started else None,
                "day": day,
                "sla_days": 7,
            }
    except Exception as exc:  # noqa: BLE001
        errors["current_sprint"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 3. Open decisions (pending approvals scoped to this customer)
    open_decisions: list[dict[str, Any]] = []
    try:
        async with get_session() as s:
            rows = list((await s.execute(
                select(ProofEventRecord)
                .where(
                    ProofEventRecord.customer_id == customer_id,
                    ProofEventRecord.approval_required == True,  # noqa: E712
                    ProofEventRecord.approved == False,  # noqa: E712
                )
                .order_by(desc(ProofEventRecord.occurred_at))
                .limit(20)
            )).scalars().all())
        for r in rows:
            open_decisions.append({
                "event_id": r.id,
                "unit_type": r.unit_type,
                "label_ar": r.label_ar,
                "occurred_at": r.occurred_at.isoformat() if r.occurred_at else None,
                "risk_level": r.risk_level,
            })
    except Exception as exc:  # noqa: BLE001
        errors["open_decisions"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 4. Counts (opportunities, drafts) + risks blocked
    counts: dict[str, int] = {}
    risks_blocked: list[dict[str, Any]] = []
    try:
        async with get_session() as s:
            unit_counts = (await s.execute(
                select(ProofEventRecord.unit_type, func.count(ProofEventRecord.id))
                .where(ProofEventRecord.customer_id == customer_id)
                .group_by(ProofEventRecord.unit_type)
            )).all()
            counts = {u: int(c) for u, c in unit_counts}
            risk_rows = list((await s.execute(
                select(ProofEventRecord)
                .where(
                    ProofEventRecord.customer_id == customer_id,
                    ProofEventRecord.unit_type == "risk_blocked",
                )
                .order_by(desc(ProofEventRecord.occurred_at))
                .limit(10)
            )).scalars().all())
        for r in risk_rows:
            risks_blocked.append({
                "event_id": r.id,
                "label_ar": r.label_ar,
                "risk_level": r.risk_level,
                "occurred_at": r.occurred_at.isoformat() if r.occurred_at else None,
            })
    except Exception as exc:  # noqa: BLE001
        errors["counts"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 5. Meetings (recent)
    meetings: list[dict[str, Any]] = []
    try:
        async with get_session() as s:
            rows = list((await s.execute(
                select(MeetingRecord)
                .where(MeetingRecord.customer_id == customer_id)
                .order_by(desc(MeetingRecord.occurred_at))
                .limit(10)
            )).scalars().all())
        for r in rows:
            meetings.append({
                "meeting_id": r.id,
                "occurred_at": r.occurred_at.isoformat() if r.occurred_at else None,
                "outcome": r.outcome,
                "channel": r.channel,
                "next_action_ar": r.next_action_ar,
            })
    except Exception as exc:  # noqa: BLE001
        errors["meetings"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 6. Invoices
    invoices: list[dict[str, Any]] = []
    try:
        async with get_session() as s:
            rows = list((await s.execute(
                select(PaymentRecord)
                .where(PaymentRecord.customer_id == customer_id)
                .order_by(desc(PaymentRecord.created_at))
                .limit(10)
            )).scalars().all())
        for r in rows:
            invoices.append({
                "invoice_id": r.id,
                "amount_sar": float(r.amount_sar or 0),
                "status": r.status,
                "url": r.invoice_url,
                "paid_at": r.paid_at.isoformat() if r.paid_at else None,
            })
    except Exception as exc:  # noqa: BLE001
        errors["invoices"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 7. Proof Packs (HMAC-signed reports recorded as proof_generated events)
    proof_packs: list[dict[str, Any]] = []
    try:
        async with get_session() as s:
            rows = list((await s.execute(
                select(ProofEventRecord)
                .where(
                    ProofEventRecord.customer_id == customer_id,
                    ProofEventRecord.unit_type == "proof_generated",
                )
                .order_by(desc(ProofEventRecord.occurred_at))
                .limit(5)
            )).scalars().all())
        for r in rows:
            proof_packs.append({
                "event_id": r.id,
                "occurred_at": r.occurred_at.isoformat() if r.occurred_at else None,
                "url": f"/api/v1/proof-ledger/customer/{customer_id}/pack.html",
            })
    except Exception as exc:  # noqa: BLE001
        errors["proof_packs"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 8. Next 7-day plan (lightweight: from open decisions + scheduled
    #    follow-ups + sprint day). For now we surface the sprint plan +
    #    pending approvals as the canonical "next 7 days".
    next_7_days_plan: list[dict[str, Any]] = []
    if current_sprint:
        next_7_days_plan.append({
            "kind": "sprint_progress",
            "label_ar": f"اليوم {current_sprint.get('day', 0)} من {current_sprint.get('sla_days', 7)}",
        })
    for d in open_decisions[:3]:
        next_7_days_plan.append({
            "kind": "approval",
            "label_ar": d["label_ar"] or d["unit_type"],
            "event_id": d["event_id"],
        })

    response: dict[str, Any] = {
        "customer_id": customer_id,
        "as_of": now.isoformat(),
        "company_name": brain.get("company_name") if brain else "",
        "brain": brain,
        "current_sprint": current_sprint,
        "open_decisions": open_decisions,
        "opportunities_count": int(counts.get("opportunity_created", 0)),
        "drafts_count": int(counts.get("draft_created", 0)),
        "meetings": meetings,
        "invoices": invoices,
        "proof_packs": proof_packs,
        "risks_blocked": risks_blocked,
        "next_7_days_plan": next_7_days_plan,
    }
    if errors:
        response["_errors"] = errors
    return response
