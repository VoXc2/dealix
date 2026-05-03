"""
Daily Ops Orchestrator — runs all role briefs at scheduled windows.

Four windows match the user's "Daily Operating Rhythm":
    morning      08:30  — full briefs for every role
    midday       12:30  — execution check (sales + growth deltas)
    closing      16:30  — closing window (sales + finance)
    scorecard    18:00  — end-of-day scorecard (ceo + revops + compliance)

This module is PURE orchestration: it composes existing role-brief builders
and writes one DailyOpsRunRecord per window. It does NOT push to WhatsApp /
email by itself — those transports are gated separately.

Usage in a router or cron:
    from auto_client_acquisition.revenue_company_os.daily_ops_orchestrator \\
        import run_window
    out = await run_window(session, window="morning")
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from auto_client_acquisition.revenue_company_os.role_brief_builder import build
from db.models import DailyOpsRunRecord

log = logging.getLogger(__name__)

# Roles processed in each window — matches the user's rhythm.
WINDOWS: dict[str, tuple[str, ...]] = {
    "morning":   ("ceo", "sales_manager", "growth_manager", "customer_success", "compliance"),
    "midday":    ("sales_manager", "growth_manager"),
    "closing":   ("sales_manager", "finance"),
    "scorecard": ("ceo", "revops", "compliance"),
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return f"dor_{uuid.uuid4().hex[:14]}"


async def run_window(
    session: AsyncSession,
    *,
    window: str,
    data_per_role: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Execute one window. Returns a summary dict + persists DailyOpsRunRecord.

    `data_per_role` lets a caller provide the rows each role needs. When
    omitted we run with empty data — the briefs still produce structurally
    valid output (zero decisions for empty inputs).
    """
    if window not in WINDOWS:
        raise ValueError(f"unknown_window: {window}")

    started = _now()
    roles = WINDOWS[window]
    output: dict[str, Any] = {"window": window, "roles": {}}
    decisions_total = 0
    risks_blocked = 0
    error: str | None = None

    for role in roles:
        try:
            brief = build(role, data=(data_per_role or {}).get(role) or {})
            output["roles"][role] = {
                "summary": brief.get("summary") or {},
                "decision_count": len(brief.get("top_decisions") or []),
                "blocked_today_ar": brief.get("blocked_today_ar") or [],
            }
            decisions_total += len(brief.get("top_decisions") or [])
            if role == "compliance":
                risks_blocked = (brief.get("summary") or {}).get("risks_blocked_total", 0)
        except Exception as exc:  # noqa: BLE001
            error = f"{role}:{exc}"
            output["roles"][role] = {"error": str(exc)[:200]}

    finished = _now()
    row = DailyOpsRunRecord(
        id=_new_id(),
        run_window=window,
        started_at=started,
        finished_at=finished,
        roles_processed=list(roles),
        decisions_total=decisions_total,
        risks_blocked_total=int(risks_blocked or 0),
        cost_estimate_sar=0.0,  # Briefs are pure; LLM-backed paths add cost later.
        error=error,
        output_json=output,
    )
    session.add(row)

    return {
        "run_id": row.id,
        "window": window,
        "duration_ms": int((finished - started).total_seconds() * 1000),
        "roles_processed": list(roles),
        "decisions_total": decisions_total,
        "risks_blocked_total": int(risks_blocked or 0),
        "error": error,
        "output": output,
    }


def list_windows() -> list[dict[str, Any]]:
    return [
        {"window": w, "roles": list(roles)}
        for w, roles in WINDOWS.items()
    ]
