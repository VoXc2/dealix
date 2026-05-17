"""Revenue Ops Machine — daily operator dashboard.

GET /api/v1/revenue-ops/dashboard
  Consolidates the funnel into one daily view: leads per funnel state, the
  A/B/C/D grade mix, drafts waiting for approval, leads stuck without movement,
  recent proof events, and hard-rule blocks. Aggregates EXISTING data only —
  no new tables. Admin-key gated.
"""

from __future__ import annotations

import logging
from collections import Counter
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.api_key import require_admin_key
from auto_client_acquisition.proof_ledger.factory import recent_events
from auto_client_acquisition.revenue_ops_machine import FunnelState, load_context
from auto_client_acquisition.revenue_ops_machine.funnel_state import TERMINAL_STATES
from db.models import LeadRecord, OutreachQueueRecord
from db.session import get_db

router = APIRouter(
    prefix="/api/v1/revenue-ops",
    tags=["revenue-ops-machine"],
    dependencies=[Depends(require_admin_key)],
)
log = logging.getLogger(__name__)

_STUCK_WARN_HOURS = 24
_STUCK_ALERT_HOURS = 72


def _hours_since(dt: datetime | None) -> float | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return (datetime.now(UTC) - dt).total_seconds() / 3600.0


@router.get("/dashboard")
async def revenue_ops_dashboard(
    session: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """The daily Revenue Ops command view."""
    leads = (
        (await session.execute(select(LeadRecord).where(LeadRecord.deleted_at.is_(None))))
        .scalars()
        .all()
    )

    funnel_counts: Counter[str] = Counter()
    grade_counts: Counter[str] = Counter()
    stuck_warn: list[dict[str, Any]] = []
    stuck_alert: list[dict[str, Any]] = []
    retainer_candidates: list[dict[str, Any]] = []
    active = 0

    for lead in leads:
        ctx = load_context(lead.id, lead.meta_json)
        # Only count leads that have actually entered the machine.
        if ctx.funnel_state == FunnelState.visitor and not ctx.history:
            continue
        state = str(ctx.funnel_state)
        funnel_counts[state] += 1
        if ctx.abcd_grade:
            grade_counts[ctx.abcd_grade] += 1

        is_terminal = (
            ctx.funnel_state in TERMINAL_STATES or ctx.funnel_state == FunnelState.closed_lost
        )
        if not is_terminal:
            active += 1
            idle_hours = _hours_since(lead.updated_at)
            if idle_hours is not None and idle_hours >= _STUCK_ALERT_HOURS:
                stuck_alert.append(
                    {"lead_id": lead.id, "state": state, "idle_hours": round(idle_hours, 1)}
                )
            elif idle_hours is not None and idle_hours >= _STUCK_WARN_HOURS:
                stuck_warn.append(
                    {"lead_id": lead.id, "state": state, "idle_hours": round(idle_hours, 1)}
                )

        if ctx.funnel_state == FunnelState.retainer_candidate:
            retainer_candidates.append(
                {"lead_id": lead.id, "company": lead.company_name, "abcd_grade": ctx.abcd_grade}
            )

    # Drafts waiting for founder approval.
    pending_approvals = (
        await session.execute(
            select(func.count())
            .select_from(OutreachQueueRecord)
            .where(OutreachQueueRecord.status == "queued")
        )
    ).scalar_one()

    # Recent proof events (last 7 days) + hard-rule blocks.
    since = datetime.now(UTC) - timedelta(days=7)
    try:
        events = recent_events(since=since, limit=300)
    except Exception as exc:  # noqa: BLE001 - ledger read must not 500 the view
        log.warning("revenue_ops_dashboard_ledger_unavailable:%s", type(exc).__name__)
        events = []
    risk_blocked = sum(1 for e in events if e.get("event_type") == "risk_blocked")

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "funnel_snapshot": {
            "by_state": dict(funnel_counts),
            "total_in_machine": sum(funnel_counts.values()),
            "active": active,
        },
        "abcd_distribution": dict(grade_counts),
        "pending_approvals": pending_approvals,
        "stuck_leads": {
            "warn_24h": stuck_warn,
            "alert_72h": stuck_alert,
        },
        "proof_events_last_7d": len(events),
        "hard_rule_blocks_last_7d": risk_blocked,
        "retainer_candidates": retainer_candidates,
    }
