"""
Self-Growth router — Dealix uses itself.

Endpoints:
    GET  /api/v1/self-growth/today        daily plan (segment + channels + experiment)
    GET  /api/v1/self-growth/weekly-learning   weekly learning report
    POST /api/v1/self-growth/experiments  record a growth experiment row
    GET  /api/v1/self-growth/experiments?week=YYYY-Www
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy import select

from auto_client_acquisition.revenue_company_os.proof_ledger import fetch_for_partner
from auto_client_acquisition.revenue_company_os.self_growth_mode import (
    build_daily_plan, build_weekly_learning, daily_plan_to_dict,
)
from db.models import GrowthExperimentRecord, ProofEventRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/self-growth", tags=["self-growth"])


@router.get("/today")
async def today() -> dict[str, Any]:
    return daily_plan_to_dict(build_daily_plan())


@router.get("/weekly-learning")
async def weekly_learning() -> dict[str, Any]:
    """Read last 7 days of proof events (any partner/customer) and summarize."""
    since = datetime.now(timezone.utc) - timedelta(days=7)
    async with get_session() as s:
        rows = (await s.execute(
            select(ProofEventRecord).where(ProofEventRecord.occurred_at >= since)
        )).scalars().all()
    return {
        "since": since.isoformat(),
        "event_count": len(rows),
        "learning": build_weekly_learning(rows),
    }


@router.post("/experiments")
async def add_experiment(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    week_iso = str(body.get("week_iso") or "")
    hypothesis = str(body.get("hypothesis_ar") or "")
    if not week_iso or not hypothesis:
        raise HTTPException(status_code=400, detail="week_iso_and_hypothesis_required")
    eid = f"exp_{uuid.uuid4().hex[:14]}"
    async with get_session() as s:
        s.add(GrowthExperimentRecord(
            id=eid,
            week_iso=week_iso,
            hypothesis_ar=hypothesis,
            segment=body.get("segment"),
            channel=body.get("channel"),
            message_ar=body.get("message_ar"),
            n_targets_planned=int(body.get("n_targets_planned") or 0),
            status=str(body.get("status") or "planned"),
        ))
    return {"id": eid, "week_iso": week_iso}


@router.get("/experiments")
async def list_experiments(
    week: str | None = Query(default=None),
) -> dict[str, Any]:
    async with get_session() as s:
        q = select(GrowthExperimentRecord)
        if week:
            q = q.where(GrowthExperimentRecord.week_iso == week)
        rows = list((await s.execute(q.order_by(GrowthExperimentRecord.started_at.desc()))).scalars().all())
    return {
        "count": len(rows),
        "experiments": [
            {
                "id": r.id,
                "week_iso": r.week_iso,
                "segment": r.segment,
                "channel": r.channel,
                "status": r.status,
                "hypothesis_ar": r.hypothesis_ar,
            }
            for r in rows
        ],
    }
