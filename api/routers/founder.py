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


@router.get("/today")
async def today(days: int = Query(default=7, ge=1, le=30)) -> dict[str, Any]:
    """One-call summary for the founder's morning routine."""
    since = _now() - timedelta(days=days)

    # 1. CEO brief (pure compute, no DB)
    ceo_brief = build_role_brief("ceo", data={})

    # 2. Aggregates (parallelize the DB-bound bits)
    async with get_session() as s:
        # Direct queries (small reads)
        proof_q = await s.execute(
            select(ProofEventRecord).where(ProofEventRecord.occurred_at >= since)
        )
        proof_events = list(proof_q.scalars().all())

        unsafe_q = await s.execute(
            select(UnsafeActionRecord).where(UnsafeActionRecord.occurred_at >= since)
        )
        unsafe_events = list(unsafe_q.scalars().all())

        tickets_q = await s.execute(
            select(SupportTicketRecord).where(SupportTicketRecord.created_at >= since)
        )
        tickets = list(tickets_q.scalars().all())

        objections_q = await s.execute(
            select(ObjectionEventRecord).where(ObjectionEventRecord.occurred_at >= since)
        )
        objections = list(objections_q.scalars().all())

        # Active subscriptions (no time filter — it's global state)
        subs_q = await s.execute(
            select(SubscriptionRecord).where(SubscriptionRecord.status == "active")
        )
        active_subs = list(subs_q.scalars().all())

        ops_q = await s.execute(
            select(DailyOpsRunRecord)
            .order_by(DailyOpsRunRecord.started_at.desc())
            .limit(8)
        )
        recent_ops = list(ops_q.scalars().all())

        # Cost + unsafe summaries reuse the helpers we already have
        cost_summary = await summarize_costs(s, days=days)
        unsafe_summary = await summarize_unsafe(s, days=days)

    quality = compute_quality(
        proof_events=proof_events,
        objection_events=objections,
        tickets=tickets,
        unsafe_actions=unsafe_events,
    )

    # MRR snapshot
    total_mrr = round(sum(float(s.mrr_sar or 0.0) for s in active_subs), 2)

    # Service Tower health
    excellence = all_excellence()

    # Open incidents (P0/P1 unresolved tickets)
    open_incidents = [
        {
            "ticket_id": t.id,
            "priority": t.priority,
            "subject": t.subject[:80],
            # Both sides naive (Mapped[datetime] columns are TIMESTAMP without tz)
            "age_hours": round(
                ((_now() - (t.created_at if t.created_at.tzinfo is None
                            else t.created_at.replace(tzinfo=None))).total_seconds() / 3600.0)
                if t.created_at else 0.0,
                1,
            ),
        }
        for t in tickets
        if t.priority in ("P0", "P1") and t.status not in ("resolved", "closed")
    ]

    return {
        "as_of": _now().isoformat(),
        "window_days": days,
        "ceo_brief": ceo_brief,
        "kpis": {
            "active_paying_subscriptions": len(active_subs),
            "current_mrr_sar": total_mrr,
            "annual_run_rate_sar": round(total_mrr * 12.0, 2),
            "proof_events_emitted": len(proof_events),
            "unsafe_actions_blocked": unsafe_summary["total_blocked"],
            "no_unsafe_action_executed_invariant": unsafe_summary["no_unsafe_action_executed"],
            "support_tickets_opened": len(tickets),
            "objections_handled": len(objections),
            "open_incidents_count": len(open_incidents),
        },
        "quality": quality,
        "cost": {
            "total_sar": cost_summary["total_cost_sar"],
            "run_count": cost_summary["run_count"],
            "avg_latency_ms": cost_summary["avg_latency_ms"],
            "error_rate": cost_summary["error_rate"],
        },
        "recent_daily_ops": [
            {
                "run_id": r.id,
                "window": r.run_window,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "decisions": r.decisions_total,
                "risks_blocked": r.risks_blocked_total,
                "error": r.error,
            }
            for r in recent_ops
        ],
        "open_incidents": open_incidents,
        "policy": {
            "live_action_gates": _gates_status(),
            "service_tower": excellence["summary"],
        },
        "next_morning_actions_ar": [
            "افتح Approval queue ووافق على ما لا يحتاج نقاش",
            "أرسل 5 LinkedIn outreach من docs/READY_OUTREACH_MESSAGES.md",
            "ردّ على inbound (LinkedIn + WhatsApp + Email) خلال ساعة",
            "إذا في Pilot قيد التنفيذ: راجع Proof Pack progress",
        ],
    }


@router.get("/week")
async def week() -> dict[str, Any]:
    """Same as /today but explicitly week-windowed + roll-up."""
    return await today(days=7)
