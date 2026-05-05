"""AI Workforce v10 router — Planner + Reviewer + memory."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.ai_workforce import WorkforceGoal
from auto_client_acquisition.ai_workforce_v10 import (
    list_memory,
    run_planner,
    run_reviewer,
    run_workforce_v10,
)


router = APIRouter(
    prefix="/api/v1/ai-workforce-v10",
    tags=["ai-workforce-v10"],
)


_GUARDRAILS = {
    "no_llm_calls": True,
    "no_live_send": True,
    "no_scraping": True,
    "memory_never_crosses_customers": True,
}


class _PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    goal_ar: str = ""
    goal_en: str = ""
    available_agents: list[str] = Field(default_factory=list)


class _ReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prior_outputs: list[dict[str, Any]] = Field(default_factory=list)


@router.get("/status")
async def workforce_v10_status() -> dict[str, Any]:
    return {
        "module": "ai_workforce_v10",
        "status": "operational",
        "guardrails": _GUARDRAILS,
        "endpoints": [
            "/status", "/plan", "/review", "/run",
            "/memory/{customer_handle}",
        ],
    }


@router.post("/plan")
async def workforce_v10_plan(payload: _PlanRequest) -> dict[str, Any]:
    out = run_planner(
        payload.goal_ar, payload.goal_en, payload.available_agents,
    )
    return out.model_dump(mode="json")


@router.post("/review")
async def workforce_v10_review(payload: _ReviewRequest) -> dict[str, Any]:
    out = run_reviewer(payload.prior_outputs)
    return out.model_dump(mode="json")


@router.post("/run")
async def workforce_v10_run(payload: WorkforceGoal) -> dict[str, Any]:
    return run_workforce_v10(payload)


@router.get("/memory/{customer_handle}")
async def workforce_v10_memory(customer_handle: str) -> dict[str, Any]:
    entries = list_memory(customer_handle)
    return {
        "customer_handle": customer_handle,
        "count": len(entries),
        "entries": [e.model_dump(mode="json") for e in entries],
    }
