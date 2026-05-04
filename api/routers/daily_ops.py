"""
Daily Ops router — orchestrate role briefs across the day.

  GET  /api/v1/daily-ops/windows         list scheduled windows + roles
  POST /api/v1/daily-ops/run             body: {"window": "morning"}
  GET  /api/v1/daily-ops/history         last N runs
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query
from sqlalchemy import select

from auto_client_acquisition.revenue_company_os.daily_ops_orchestrator import (
    WINDOWS, list_windows, run_window,
)
from db.models import DailyOpsRunRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/daily-ops", tags=["daily-ops"])


@router.get("/windows")
async def get_windows() -> dict[str, Any]:
    return {"count": len(WINDOWS), "windows": list_windows()}


@router.post("/run")
async def run_now(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    window = str(body.get("window") or "")
    if window not in WINDOWS:
        raise HTTPException(status_code=400, detail=f"unknown_window: {window}")
    async with get_session() as s:
        return await run_window(s, window=window)


@router.get("/history")
async def get_history(
    limit: int = Query(default=20, ge=1, le=200),
) -> dict[str, Any]:
    async with get_session() as s:
        rows = list((await s.execute(
            select(DailyOpsRunRecord)
            .order_by(DailyOpsRunRecord.started_at.desc())
            .limit(limit)
        )).scalars().all())
    return {
        "count": len(rows),
        "runs": [
            {
                "run_id": r.id,
                "window": r.run_window,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "finished_at": r.finished_at.isoformat() if r.finished_at else None,
                "roles": r.roles_processed,
                "decisions_total": r.decisions_total,
                "risks_blocked_total": r.risks_blocked_total,
                "error": r.error,
            }
            for r in rows
        ],
    }
