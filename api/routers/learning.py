"""
Learning router — canonical /api/v1/learning/* endpoints.

This is the canonical URL for the **Learning Layer** (Doctrine layer 4).
It wraps the existing self_growth_mode functions so the URL shape matches
the vision document exactly:

    GET /api/v1/learning/weekly?days=7
    GET /api/v1/learning/today

The existing /api/v1/self-growth/* endpoints stay live for backwards
compatibility.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Query
from sqlalchemy import select

from auto_client_acquisition.revenue_company_os.self_growth_mode import (
    build_daily_plan,
    build_weekly_learning,
    daily_plan_to_dict,
)
from db.models import ProofEventRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


@router.get("/weekly")
async def weekly(days: int = Query(default=7, ge=1, le=90)) -> dict[str, Any]:
    """Weekly learning report. Pulls last N days of proof events,
    delegates to build_weekly_learning(), returns the dict + as_of."""
    errors: dict[str, str] = {}
    events: list = []
    since = _now() - timedelta(days=days)

    try:
        async with get_session() as s:
            events = list((await s.execute(
                select(ProofEventRecord).where(ProofEventRecord.occurred_at >= since)
            )).scalars().all())
    except Exception as exc:  # noqa: BLE001
        errors["fetch"] = f"{type(exc).__name__}: {str(exc)[:200]}"

    try:
        report = build_weekly_learning(events)
    except Exception as exc:  # noqa: BLE001
        errors["build"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        report = {
            "totals_by_unit": {},
            "actors_active": [],
            "high_risk_blocked": 0,
            "pending_approvals": 0,
            "bottleneck_ar": "—",
            "next_experiment_ar": "—",
            "no_unsafe_action_executed": True,
        }

    response: dict[str, Any] = {
        "as_of": _now().isoformat(),
        "since": since.isoformat(),
        "days": days,
        **report,
    }
    if errors:
        response["_errors"] = errors
    return response


@router.get("/today")
async def today() -> dict[str, Any]:
    """Today's deterministic plan (focus segment, channels, message variants)."""
    return daily_plan_to_dict(build_daily_plan())
