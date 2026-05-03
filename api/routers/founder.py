"""
Founder router — single-call "today" aggregator.

Designed to back the `dealix today` CLI: replaces 6 separate API calls
with one rich JSON response that the founder can read in 30 seconds.

Endpoints:
    GET /api/v1/founder/today
        Aggregates the CEO brief, last-7-day KPIs, refusal counts,
        cost summary, recent daily-ops runs, and a few sanity checks
        (live-action gates, service excellence). No paths for write.

    GET /api/v1/founder/week
        Same shape but with 7-day windows + week-over-week deltas
        where the underlying data supports it.

The response is intentionally flat and shallow — easy to render in a
terminal table or print to a Slack message.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Query
from sqlalchemy import select

from auto_client_acquisition.agent_observability.cost_tracker import summarize as summarize_costs
from auto_client_acquisition.agent_observability.quality_metrics import compute as compute_quality
from auto_client_acquisition.agent_observability.unsafe_action_monitor import (
    summarize as summarize_unsafe,
)
from auto_client_acquisition.revenue_company_os.role_brief_builder import build as build_role_brief
from auto_client_acquisition.service_tower.excellence_score import all_excellence
from core.config.settings import get_settings
from db.models import (
    DailyOpsRunRecord, ObjectionEventRecord, ProofEventRecord,
    SubscriptionRecord, SupportTicketRecord, UnsafeActionRecord,
)
from db.session import get_session

router = APIRouter(prefix="/api/v1/founder", tags=["founder"])


_GATES = (
    "whatsapp_allow_live_send",
    "gmail_allow_live_send",
    "moyasar_allow_live_charge",
    "linkedin_allow_auto_dm",
    "resend_allow_live_send",
    "whatsapp_allow_internal_send",
    "whatsapp_allow_customer_send",
    "calls_allow_live_dial",
)


def _now() -> datetime:
    # Naive UTC for compatibility with existing TIMESTAMP (no tz) columns
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _gates_status() -> dict[str, bool]:
    s = get_settings()
    return {g: bool(getattr(s, g, False)) for g in _GATES}


def _to_naive(dt):
    """Strip tz from a datetime if present (matches Mapped[datetime] columns)."""
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt


@router.get("/today")
async def today(days: int = Query(default=7, ge=1, le=30)) -> dict[str, Any]:
    """One-call summary for the founder's morning routine.

    Defensive: each block is wrapped so a single bad row / missing table
    doesn't 500 the whole endpoint. Errors are surfaced in `_errors` so
    the caller can see what failed without losing the working sections.
    """
    since = _now() - timedelta(days=days)
    errors: dict[str, str] = {}

    # 1. CEO brief (pure compute, no DB) ────────────────────────
    try:
        ceo_brief = build_role_brief("ceo", data={})
    except Exception as exc:  # noqa: BLE001
        errors["ceo_brief"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        ceo_brief = {"role": "ceo", "summary": {}, "top_decisions": []}

    # 2. DB reads — each query independently fault-tolerant ────
    proof_events: list = []
    unsafe_events: list = []
    tickets: list = []
    objections: list = []
    active_subs: list = []
    recent_ops: list = []
    cost_summary: dict = {"total_cost_sar": 0.0, "run_count": 0, "avg_latency_ms": 0.0, "error_rate": 0.0}
    unsafe_summary: dict = {"total_blocked": 0, "no_unsafe_action_executed": True}

    try:
        async with get_session() as s:
            try:
                proof_events = list((await s.execute(
                    select(ProofEventRecord).where(ProofEventRecord.occurred_at >= since)
                )).scalars().all())
            except Exception as exc:  # noqa: BLE001
                errors["proof_events"] = f"{type(exc).__name__}: {str(exc)[:200]}"

            try:
                unsafe_events = list((await s.execute(
                    select(UnsafeActionRecord).where(UnsafeActionRecord.occurred_at >= since)
                )).scalars().all())
            except Exception as exc:  # noqa: BLE001
                errors["unsafe_events"] = f"{type(exc).__name__}: {str(exc)[:200]}"

            try:
                tickets = list((await s.execute(
                    select(SupportTicketRecord).where(SupportTicketRecord.created_at >= since)
                )).scalars().all())
            except Exception as exc:  # noqa: BLE001
                errors["tickets"] = f"{type(exc).__name__}: {str(exc)[:200]}"

            try:
                objections = list((await s.execute(
                    select(ObjectionEventRecord).where(ObjectionEventRecord.occurred_at >= since)
                )).scalars().all())
            except Exception as exc:  # noqa: BLE001
                errors["objections"] = f"{type(exc).__name__}: {str(exc)[:200]}"

            try:
                active_subs = list((await s.execute(
                    select(SubscriptionRecord).where(SubscriptionRecord.status == "active")
                )).scalars().all())
            except Exception as exc:  # noqa: BLE001
                errors["active_subs"] = f"{type(exc).__name__}: {str(exc)[:200]}"

            try:
                recent_ops = list((await s.execute(
                    select(DailyOpsRunRecord)
                    .order_by(DailyOpsRunRecord.started_at.desc())
                    .limit(8)
                )).scalars().all())
            except Exception as exc:  # noqa: BLE001
                errors["recent_ops"] = f"{type(exc).__name__}: {str(exc)[:200]}"

            try:
                cost_summary = await summarize_costs(s, days=days)
            except Exception as exc:  # noqa: BLE001
                errors["cost_summary"] = f"{type(exc).__name__}: {str(exc)[:200]}"

            try:
                unsafe_summary = await summarize_unsafe(s, days=days)
            except Exception as exc:  # noqa: BLE001
                errors["unsafe_summary"] = f"{type(exc).__name__}: {str(exc)[:200]}"
    except Exception as exc:  # noqa: BLE001
        errors["session"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 3. Pure computes (no DB) ──────────────────────────────────
    try:
        quality = compute_quality(
            proof_events=proof_events,
            objection_events=objections,
            tickets=tickets,
            unsafe_actions=unsafe_events,
        )
    except Exception as exc:  # noqa: BLE001
        errors["quality"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        quality = {}

    try:
        total_mrr = round(sum(float(getattr(x, "mrr_sar", 0) or 0.0) for x in active_subs), 2)
    except Exception as exc:  # noqa: BLE001
        errors["mrr"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        total_mrr = 0.0

    try:
        excellence = all_excellence()
    except Exception as exc:  # noqa: BLE001
        errors["excellence"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        excellence = {"summary": {}, "services": []}

    # 4. Open incidents (defensive against any missing field) ──
    open_incidents: list = []
    try:
        for t in tickets:
            if getattr(t, "priority", None) not in ("P0", "P1"):
                continue
            if getattr(t, "status", None) in ("resolved", "closed"):
                continue
            try:
                created = _to_naive(getattr(t, "created_at", None))
                age_hours = round((_now() - created).total_seconds() / 3600.0, 1) if created else 0.0
            except Exception:
                age_hours = 0.0
            open_incidents.append({
                "ticket_id": getattr(t, "id", None),
                "priority": getattr(t, "priority", None),
                "subject": (getattr(t, "subject", "") or "")[:80],
                "age_hours": age_hours,
            })
    except Exception as exc:  # noqa: BLE001
        errors["open_incidents"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # Defensive recent_daily_ops serializer
    recent_ops_out = []
    try:
        for r in recent_ops:
            try:
                recent_ops_out.append({
                    "run_id": getattr(r, "id", None),
                    "window": getattr(r, "run_window", None),
                    "started_at": (r.started_at.isoformat()
                                   if getattr(r, "started_at", None) else None),
                    "decisions": getattr(r, "decisions_total", 0),
                    "risks_blocked": getattr(r, "risks_blocked_total", 0),
                    "error": getattr(r, "error", None),
                })
            except Exception:
                pass
    except Exception as exc:  # noqa: BLE001
        errors["recent_ops_serializer"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    response = {
        "as_of": _now().isoformat(),
        "window_days": days,
        "ceo_brief": ceo_brief,
        "kpis": {
            "active_paying_subscriptions": len(active_subs),
            "current_mrr_sar": total_mrr,
            "annual_run_rate_sar": round(total_mrr * 12.0, 2),
            "proof_events_emitted": len(proof_events),
            "unsafe_actions_blocked": unsafe_summary.get("total_blocked", 0),
            "no_unsafe_action_executed_invariant": unsafe_summary.get(
                "no_unsafe_action_executed", True
            ),
            "support_tickets_opened": len(tickets),
            "objections_handled": len(objections),
            "open_incidents_count": len(open_incidents),
        },
        "quality": quality,
        "cost": {
            "total_sar": cost_summary.get("total_cost_sar", 0.0),
            "run_count": cost_summary.get("run_count", 0),
            "avg_latency_ms": cost_summary.get("avg_latency_ms", 0.0),
            "error_rate": cost_summary.get("error_rate", 0.0),
        },
        "recent_daily_ops": recent_ops_out,
        "open_incidents": open_incidents,
        "policy": {
            "live_action_gates": _gates_status(),
            "service_tower": excellence.get("summary", {}),
        },
        "next_morning_actions_ar": [
            "افتح Approval queue ووافق على ما لا يحتاج نقاش",
            "أرسل 5 LinkedIn outreach من docs/READY_OUTREACH_MESSAGES.md",
            "ردّ على inbound (LinkedIn + WhatsApp + Email) خلال ساعة",
            "إذا في Pilot قيد التنفيذ: راجع Proof Pack progress",
        ],
    }
    if errors:
        response["_errors"] = errors  # surface what failed without 500ing
    return response


@router.get("/week")
async def week() -> dict[str, Any]:
    """Same as /today but explicitly week-windowed + roll-up."""
    return await today(days=7)
