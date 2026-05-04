"""
Self-Ops router — Dealix's own ops surface.

  POST /api/v1/self-ops/run-daily
       Triggers daily_self_ops() — same as cron.
  GET  /api/v1/self-ops/state
       Returns Dealix's own Customer + prospect funnel + sprint state.
  GET  /api/v1/self-ops/brain
       Read-only Dealix Brain (for transparency).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body
from sqlalchemy import func, select

from auto_client_acquisition.self_ops import DEALIX_BRAIN, daily_self_ops
from db.models import (
    CustomerRecord, ProofEventRecord, ProspectRecord, SprintRecord,
)
from db.session import get_session

router = APIRouter(prefix="/api/v1/self-ops", tags=["self-ops"])


@router.get("/brain")
async def get_brain() -> dict[str, Any]:
    """Read-only Dealix's own Brain."""
    return {"brain": DEALIX_BRAIN}


@router.post("/run-daily")
async def run_daily(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    prospect_target = int((body or {}).get("prospect_target", 6))
    intro_count = int((body or {}).get("intro_count", 5))
    result = await daily_self_ops(
        prospect_target=prospect_target, intro_count=intro_count,
    )
    return {
        "customer_id": result.customer_id,
        "prospects_seeded": result.prospects_seeded,
        "drafts_generated": result.drafts_generated,
        "drafts_used_llm": result.drafts_used_llm,
        "errors": result.errors,
        "notes": result.notes,
    }


@router.get("/state")
async def state() -> dict[str, Any]:
    """Snapshot of Dealix's own funnel + sprint state."""
    async with get_session() as s:
        cust = (await s.execute(
            select(CustomerRecord).where(CustomerRecord.id == "cus_dealix_self")
        )).scalar_one_or_none()
        if cust is None:
            return {
                "initialized": False,
                "note_ar": "Dealix self-ops لم يبدأ بعد. شغّل POST /run-daily.",
            }
        funnel = (await s.execute(
            select(ProspectRecord.status, func.count(ProspectRecord.id))
            .where(ProspectRecord.customer_id == cust.id)
            .group_by(ProspectRecord.status)
        )).all()
        funnel_dict = {st: int(c) for st, c in funnel}

        sprints = list((await s.execute(
            select(SprintRecord)
            .where(SprintRecord.customer_id == cust.id)
            .order_by(SprintRecord.started_at.desc())
            .limit(5)
        )).scalars().all())

        events_count = (await s.execute(
            select(func.count(ProofEventRecord.id))
            .where(ProofEventRecord.customer_id == cust.id)
        )).scalar() or 0

    return {
        "initialized": True,
        "customer_id": cust.id,
        "company_name": getattr(cust, "company_name", "Dealix"),
        "current_service_id": getattr(cust, "current_service_id", None),
        "prospect_funnel": funnel_dict,
        "active_sprints": [
            {
                "sprint_id": sp.id,
                "current_day": sp.current_day,
                "status": sp.status,
                "started_at": sp.started_at.isoformat() if sp.started_at else None,
            }
            for sp in sprints
        ],
        "proof_events_total": events_count,
    }
