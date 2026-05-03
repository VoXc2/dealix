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

    # Each query in its OWN session — so a single failed query (e.g., schema
    # drift on subscriptions table) doesn't abort the transaction and cascade
    # to all subsequent queries (asyncpg InFailedSQLTransactionError).

    async def _q(name: str, runner):
        try:
            async with get_session() as s:
                return await runner(s)
        except Exception as exc:  # noqa: BLE001
            errors[name] = f"{type(exc).__name__}: {str(exc)[:200]}"
            return None

    proof_events = await _q("proof_events", lambda s: s.execute(
        select(ProofEventRecord).where(ProofEventRecord.occurred_at >= since)
    )) or []
    if proof_events and not isinstance(proof_events, list):
        proof_events = list(proof_events.scalars().all())

    unsafe_events = await _q("unsafe_events", lambda s: s.execute(
        select(UnsafeActionRecord).where(UnsafeActionRecord.occurred_at >= since)
    )) or []
    if unsafe_events and not isinstance(unsafe_events, list):
        unsafe_events = list(unsafe_events.scalars().all())

    tickets = await _q("tickets", lambda s: s.execute(
        select(SupportTicketRecord).where(SupportTicketRecord.created_at >= since)
    )) or []
    if tickets and not isinstance(tickets, list):
        tickets = list(tickets.scalars().all())

    objections = await _q("objections", lambda s: s.execute(
        select(ObjectionEventRecord).where(ObjectionEventRecord.occurred_at >= since)
    )) or []
    if objections and not isinstance(objections, list):
        objections = list(objections.scalars().all())

    active_subs = await _q("active_subs", lambda s: s.execute(
        select(SubscriptionRecord).where(SubscriptionRecord.status == "active")
    )) or []
    if active_subs and not isinstance(active_subs, list):
        active_subs = list(active_subs.scalars().all())

    recent_ops = await _q("recent_ops", lambda s: s.execute(
        select(DailyOpsRunRecord).order_by(DailyOpsRunRecord.started_at.desc()).limit(8)
    )) or []
    if recent_ops and not isinstance(recent_ops, list):
        recent_ops = list(recent_ops.scalars().all())

    # Cost + unsafe summaries — each in its own session so a failure
    # in one doesn't poison the other.
    try:
        async with get_session() as s:
            cost_summary = await summarize_costs(s, days=days)
    except Exception as exc:  # noqa: BLE001
        errors["cost_summary"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    try:
        async with get_session() as s:
            unsafe_summary = await summarize_unsafe(s, days=days)
    except Exception as exc:  # noqa: BLE001
        errors["unsafe_summary"] = f"{type(exc).__name__}: {str(exc)[:200]}"

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


@router.get("/digest")
async def digest() -> dict[str, Any]:
    """One-call Founder Daily Digest — replaces 6 separate calls.

    Aggregates today's actionable surface:
      - prospect standup queue (due today + stale messaged)
      - pending approvals (count + top 5 oldest)
      - active sprints (current_day + days_remaining)
      - best channel pick (ChannelOrchestrator + warm Brain proxy)
      - 3 LLM-drafted LinkedIn intros (or fallbacks) for top 3 prospects
      - live-action gates snapshot
      - LLM provider status

    Defensive: per-section _errors map; never 500s.
    """
    from auto_client_acquisition.intelligence.channel_orchestrator import recommend
    from auto_client_acquisition.intelligence.smart_drafter import get_drafter
    from db.models import (
        CustomerRecord, ProofEventRecord, ProspectRecord, SprintRecord,
    )

    now = _now()
    errors: dict[str, str] = {}

    # 1. Standup queue
    standup = {"due_today": [], "stale_messaged": [], "wins_yesterday": []}
    try:
        eod = now.replace(hour=23, minute=59, second=59)
        cutoff_3d = now - timedelta(days=3)
        async with get_session() as s:
            due = list((await s.execute(
                select(ProspectRecord)
                .where(
                    ProspectRecord.next_step_due_at <= eod,
                    ProspectRecord.status.notin_(("closed_won", "closed_lost", "retainer_won")),
                )
                .order_by(ProspectRecord.next_step_due_at.asc())
                .limit(10)
            )).scalars().all())
            stale = list((await s.execute(
                select(ProspectRecord)
                .where(
                    ProspectRecord.status == "messaged",
                    ProspectRecord.last_message_at <= cutoff_3d,
                )
                .order_by(ProspectRecord.last_message_at.asc())
                .limit(5)
            )).scalars().all())
        standup["due_today"] = [
            {"id": p.id, "name": p.name, "company": p.company,
             "next_step_ar": p.next_step_ar} for p in due
        ]
        standup["stale_messaged"] = [
            {"id": p.id, "name": p.name, "company": p.company} for p in stale
        ]
    except Exception as exc:  # noqa: BLE001
        errors["standup"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 2. Pending approvals
    approvals = {"count": 0, "top_oldest": []}
    try:
        async with get_session() as s:
            rows = list((await s.execute(
                select(ProofEventRecord)
                .where(
                    ProofEventRecord.approval_required == True,  # noqa: E712
                    ProofEventRecord.approved == False,  # noqa: E712
                )
                .order_by(ProofEventRecord.occurred_at.asc())
                .limit(5)
            )).scalars().all())
        approvals["count"] = len(rows)
        approvals["top_oldest"] = [
            {
                "event_id": r.id,
                "unit_type": r.unit_type,
                "label_ar": r.label_ar,
                "customer_id": r.customer_id,
                "age_hours": (
                    round((now - r.occurred_at).total_seconds() / 3600.0, 1)
                    if r.occurred_at else 0.0
                ),
            }
            for r in rows
        ]
    except Exception as exc:  # noqa: BLE001
        errors["approvals"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 3. Active sprints
    active_sprints: list[dict[str, Any]] = []
    try:
        async with get_session() as s:
            rows = list((await s.execute(
                select(SprintRecord)
                .where(SprintRecord.status.notin_(("completed", "aborted")))
                .order_by(SprintRecord.started_at.desc())
                .limit(10)
            )).scalars().all())
        for r in rows:
            elapsed = (
                (now - r.started_at).days if r.started_at else 0
            )
            active_sprints.append({
                "sprint_id": r.id,
                "customer_id": r.customer_id,
                "service_id": r.service_id,
                "current_day": r.current_day,
                "days_remaining": max(0, 7 - max(r.current_day, elapsed)),
                "status": r.status,
            })
    except Exception as exc:  # noqa: BLE001
        errors["sprints"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 4. Best channel pick (proxy: most-recent customer's Brain or default)
    best_channel: dict[str, Any] | None = None
    try:
        async with get_session() as s:
            cust = (await s.execute(
                select(CustomerRecord).order_by(CustomerRecord.created_at.desc()).limit(1)
            )).scalar_one_or_none()
        brain = {
            "approved_channels": list(getattr(cust, "approved_channels", []) or [])
                                 if cust else ["linkedin_manual"],
            "blocked_channels": list(getattr(cust, "blocked_channels", []) or [])
                                if cust else [],
        }
        recs = recommend(prospect={}, brain=brain, gates=_gates_status())
        first = next((r for r in recs if r.allowed), None)
        if first:
            best_channel = {
                "channel": first.channel,
                "score": first.score,
                "reason_ar": first.reason_ar,
            }
    except Exception as exc:  # noqa: BLE001
        errors["best_channel"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 5. 3 LLM-drafted LinkedIn intros for the first 3 due_today prospects
    intros: list[dict[str, Any]] = []
    try:
        drafter = get_drafter()
        targets = (standup.get("due_today") or [])[:3]
        # Use most-recent customer's Brain as the "voice"
        async with get_session() as s:
            cust = (await s.execute(
                select(CustomerRecord).order_by(CustomerRecord.created_at.desc()).limit(1)
            )).scalar_one_or_none()
        brain = {
            "company_name": getattr(cust, "company_name", "Dealix") if cust else "Dealix",
            "offer_ar": getattr(cust, "offer_ar", None) or "Saudi Revenue OS",
            "ideal_customer_ar": getattr(cust, "ideal_customer_ar", None) or "B2B 10-50",
            "tone_ar": getattr(cust, "tone_ar", None) or "professional_saudi_arabic",
            "forbidden_claims": list(getattr(cust, "forbidden_claims", []) or []),
        }
        for t in targets:
            fallback = (
                f"السلام عليكم {t.get('name', '')}، شفت آخر post لك — "
                f"عندي زاوية ربما تفيد {t.get('company', 'شركتك')}. "
                f"هل تتفضّل بـ ١٥ دقيقة هذا الأسبوع؟ (STOP للإلغاء)"
            )
            r = await drafter.draft_outreach_message(
                brain,
                prospect_hint=t.get("company") or t.get("name", ""),
                fallback=fallback,
            )
            intros.append({
                "prospect_id": t["id"],
                "company": t.get("company"),
                "draft_ar": r.text,
                "llm_used": r.used_llm,
                "provider": r.provider,
                "fallback_reason": r.fallback_reason,
                "approval_required": True,
            })
    except Exception as exc:  # noqa: BLE001
        errors["intros"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    # 6. LLM provider status (one-line)
    llm_providers: list[str] = []
    try:
        from core.llm.router import get_router
        r = get_router()
        llm_providers = [p.value for p in r.available_providers()]
    except Exception:  # noqa: BLE001
        llm_providers = []

    response = {
        "as_of": now.isoformat(),
        "standup": standup,
        "approvals": approvals,
        "active_sprints": active_sprints,
        "best_channel": best_channel,
        "intros": intros,
        "live_action_gates": _gates_status(),
        "llm": {
            "available_providers": llm_providers,
            "providers_count": len(llm_providers),
            "fallback_active": len(llm_providers) == 0,
        },
        "advice_ar": (
            "إذا 0 ردود رغم 30 رسالة → بدّل القناة (WhatsApp 1st-degree)."
            if len(standup["stale_messaged"]) >= 5 else
            "ابدأ بالأهم: أرسل 6 رسائل LinkedIn warm من due_today الآن."
        ),
    }
    if errors:
        response["_errors"] = errors
    return response
