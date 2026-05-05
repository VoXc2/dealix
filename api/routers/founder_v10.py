"""Founder v10 router — composed daily brief endpoints."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from auto_client_acquisition.founder_v10 import (
    build_daily_brief,
    compute_next_action,
    find_blockers,
    summarize_cost,
    summarize_evidence,
)


router = APIRouter(
    prefix="/api/v1/founder-v10",
    tags=["founder-v10"],
)


_GUARDRAILS = {
    "no_live_send": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "approval_required_for_external_actions": True,
    "no_llm_calls": True,
    "no_pii_in_brief": True,
}


@router.get("/status")
async def founder_v10_status() -> dict[str, Any]:
    return {
        "module": "founder_v10",
        "status": "operational",
        "guardrails": _GUARDRAILS,
        "endpoints": [
            "/status", "/today", "/blockers",
            "/evidence", "/cost", "/next-action",
        ],
    }


@router.get("/today")
async def founder_v10_today() -> dict[str, Any]:
    brief = build_daily_brief()
    return brief.model_dump(mode="json")


@router.get("/blockers")
async def founder_v10_blockers() -> dict[str, Any]:
    blockers = find_blockers()
    return {
        "count": len(blockers),
        "items": [b.model_dump(mode="json") for b in blockers],
    }


@router.get("/evidence")
async def founder_v10_evidence() -> dict[str, Any]:
    return summarize_evidence(limit=10)


@router.get("/cost")
async def founder_v10_cost(
    days: int = Query(default=7, ge=1, le=90),
) -> dict[str, Any]:
    return summarize_cost(period_days=days)


@router.get("/next-action")
async def founder_v10_next_action() -> dict[str, Any]:
    return compute_next_action()
