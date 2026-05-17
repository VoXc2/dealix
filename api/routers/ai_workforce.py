"""AI Workforce Router — v7 Phase 1 + Phase 2 endpoints.

Endpoints under ``/api/v1/ai-workforce``:
    GET  /status           — module health + registered agents + guardrails
    GET  /agents           — list of all 12 AgentSpec dicts
    GET  /agents/{agent_id} — one AgentSpec
    POST /run              — WorkforceGoal -> WorkforceRun (full pipeline)

Pure local composition; no LLM, no external HTTP.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.ai_workforce import (
    AGENT_REGISTRY,
    WorkforceGoal,
    build_revenue_factory_blueprint,
    get_agent,
    list_agents,
    run_workforce_goal,
)


router = APIRouter(
    prefix="/api/v1/ai-workforce",
    tags=["ai-workforce"],
)


@router.get("/status")
async def workforce_status() -> dict[str, Any]:
    return {
        "module": "ai_workforce",
        "status": "operational",
        "agents_registered": len(AGENT_REGISTRY),
        "guardrails": {
            "no_llm_calls": True,
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }


@router.get("/agents")
async def workforce_agents() -> dict[str, Any]:
    return {
        "total": len(AGENT_REGISTRY),
        "agents": [a.model_dump(mode="json") for a in list_agents()],
    }


@router.get("/agents/{agent_id}")
async def workforce_agent_detail(agent_id: str) -> dict[str, Any]:
    try:
        spec = get_agent(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return spec.model_dump(mode="json")


@router.post("/run")
async def workforce_run(payload: WorkforceGoal) -> dict[str, Any]:
    result = run_workforce_goal(payload)
    return result.model_dump(mode="json")


@router.get("/revenue-factory-blueprint")
async def workforce_revenue_factory_blueprint() -> dict[str, Any]:
    blueprint = build_revenue_factory_blueprint()
    return {
        "model": blueprint["model"],
        "north_star": blueprint["north_star"],
        "doctrine_chain": blueprint["doctrine_chain"],
        "agents_total": len(blueprint["agent_contracts"]),
        "automation_plays_total": len(blueprint["automation_plays"]),
        "blueprint": blueprint,
    }
