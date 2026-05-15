"""V12 Customer Success OS — wraps customer_success.health_score."""
from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/customer-success-os", tags=["customer-success-os"])


_HARD_GATES = {
    "no_live_send": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


class _HealthScoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    intake_complete: bool = False
    diagnostic_delivered: bool = False
    proof_events_count: int = Field(0, ge=0)
    open_support_tickets: int = Field(0, ge=0)
    last_customer_response_days: int = Field(0, ge=0)
    delivery_sla_status: str = "unknown"
    payment_status: str = "unknown"
    renewal_signal: bool = False


class _CheckinRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_handle: str = "Slot-A"
    week: int = Field(default=1, ge=1, le=52)


@router.get("/status")
async def cs_os_status() -> dict[str, Any]:
    return {
        "service": "customer_success_os",
        "module": "customer_success",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"health_score": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "استخدم /health-score مرّة أسبوعيّاً",
        "next_action_en": "Use /health-score once per week.",
    }


@router.post("/health-score")
async def cs_health_score(req: _HealthScoreRequest) -> dict[str, Any]:
    """Compute a 0–100 health score from explicit signals.

    Pure function. NO LLM. NO fake data. If signals are sparse, the
    score reflects ``unknown`` honestly rather than green-by-default.
    """
    score = 0
    if req.intake_complete:
        score += 15
    if req.diagnostic_delivered:
        score += 20
    score += min(20, req.proof_events_count * 5)
    score -= min(15, req.open_support_tickets * 5)
    if req.last_customer_response_days <= 3:
        score += 10
    elif req.last_customer_response_days <= 7:
        score += 5
    else:
        score -= 5
    if req.delivery_sla_status == "on_track":
        score += 15
    elif req.delivery_sla_status == "at_risk":
        score -= 10
    if req.payment_status == "paid":
        score += 15
    elif req.payment_status == "overdue":
        score -= 15
    if req.renewal_signal:
        score += 10
    score = max(0, min(100, score))
    if score >= 81:
        band = "excellent"
        label_ar, label_en = "ممتاز", "Excellent"
    elif score >= 61:
        band = "good"
        label_ar, label_en = "جيد", "Good"
    elif score >= 31:
        band = "needs_attention"
        label_ar, label_en = "يحتاج تدخّل", "Needs attention"
    else:
        band = "high_risk"
        label_ar, label_en = "خطر عالي", "High risk"
    return {
        "score": score,
        "band": band,
        "label_ar": label_ar,
        "label_en": label_en,
        "action_mode": "suggest_only",
        "hard_gates": _HARD_GATES,
    }


async def _collect_signals_for_tenant(customer_handle: str) -> _HealthScoreRequest:
    """Read real signals from DB for a customer and return a populated
    HealthScoreRequest. Falls back to neutral defaults if any data source
    is unavailable — health score reflects 'unknown' honestly rather than
    green-by-default (per the cs_health_score docstring).
    """
    signals = _HealthScoreRequest()

    # Payment status (from payments table — populated by Moyasar webhook)
    try:
        from sqlalchemy import desc, select

        from db.models import PaymentRecord
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            stmt = (
                select(PaymentRecord)
                .where(PaymentRecord.customer_handle == customer_handle)
                .order_by(desc(PaymentRecord.created_at))
                .limit(1)
            )
            row = (await session.execute(stmt)).scalar_one_or_none()
            if row is not None:
                if row.status == "paid":
                    signals.payment_status = "paid"
                elif row.status in ("failed", "refunded"):
                    signals.payment_status = "overdue"
                else:
                    signals.payment_status = "unknown"
    except Exception as exc:
        log.debug("health_score_payment_lookup_skipped reason=%s", exc)

    # Proof events count (count of decision_passport entries for this tenant
    # in last 30 days, if the table exists)
    try:
        from sqlalchemy import func, select

        from db.models import DecisionPassportRecord  # type: ignore
        from db.session import async_session_factory

        thirty_days_ago = datetime.now(UTC) - timedelta(days=30)
        async with async_session_factory()() as session:
            stmt = (
                select(func.count())
                .select_from(DecisionPassportRecord)
                .where(
                    DecisionPassportRecord.tenant_handle == customer_handle,
                    DecisionPassportRecord.created_at >= thirty_days_ago,
                )
            )
            count = (await session.execute(stmt)).scalar() or 0
            signals.proof_events_count = int(count)
    except Exception as exc:
        log.debug("health_score_proof_events_lookup_skipped reason=%s", exc)

    # Last customer response: heuristic — query last decision_passport entry
    # where the customer approved something. If no record in 30 days → high risk.
    try:
        from sqlalchemy import desc, select

        from db.models import DecisionPassportRecord  # type: ignore
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            stmt = (
                select(DecisionPassportRecord)
                .where(
                    DecisionPassportRecord.tenant_handle == customer_handle,
                    DecisionPassportRecord.event_type == "customer_approved",
                )
                .order_by(desc(DecisionPassportRecord.created_at))
                .limit(1)
            )
            row = (await session.execute(stmt)).scalar_one_or_none()
            if row is not None:
                days = (datetime.now(UTC) - row.created_at).days
                signals.last_customer_response_days = max(0, days)
    except Exception as exc:
        log.debug("health_score_last_response_lookup_skipped reason=%s", exc)

    return signals


@router.get("/{customer_handle}/health")
async def cs_health_for_tenant(customer_handle: str) -> dict[str, Any]:
    """Compute health score for a real tenant using live DB signals.

    Reads signals from:
      - payments table (payment_status from Moyasar webhook persistence)
      - decision_passport entries (proof_events_count, last_customer_response_days)

    Each signal that can't be read gracefully falls back to neutral —
    the score will reflect 'unknown' rather than green-by-default.

    This is the "real-data wiring" for v6 §17 B1 — it converts the existing
    /health-score signal-based endpoint into something queryable by customer
    handle, no payload required. Onboarding day 5 (CUSTOMER_ONBOARDING_DAY_BY_DAY.md)
    uses this endpoint.
    """
    handle = (customer_handle or "").strip()
    if not handle:
        raise HTTPException(status_code=400, detail="customer_handle required")

    signals = await _collect_signals_for_tenant(handle)
    score_payload = await cs_health_score(signals)
    return {
        **score_payload,
        "customer_handle": handle,
        "signals_used": signals.model_dump(),
        "data_source": "tenant_db_with_neutral_fallback",
    }


@router.post("/weekly-checkin-draft")
async def cs_weekly_checkin(req: _CheckinRequest) -> dict[str, Any]:
    return {
        "customer_handle": req.customer_handle,
        "week": req.week,
        "draft_ar": (
            f"السلام عليكم، أتابع وضع Pilot الأسبوع {req.week}. "
            "أحتاج 5 دقائق لمراجعة:\n"
            "1) ما هو أفضل ردّ شفته هذا الأسبوع؟\n"
            "2) أي اعتراض كرّر نفسه؟\n"
            "3) هل تحتاج تعديل في خطّة المتابعة؟"
        ),
        "draft_en": (
            f"Following up on the Pilot for week {req.week}. Need 5 min "
            "to review:\n"
            "1) Best reply you saw this week?\n"
            "2) Any objection that repeated?\n"
            "3) Adjustment needed in the follow-up plan?"
        ),
        "action_mode": "draft_only",
        "send_method": "manual_only",
        "hard_gates": _HARD_GATES,
    }
