"""AI Workforce endpoints over Dealix's canonical five-agent machine.

The historical runtime exposes bounded specialist roles for compatibility and
capability reuse. They are not additional permanent agents or authority owners.
Pure local composition; no LLM, no external HTTP, no live send.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.ai_workforce import (
    AGENT_REGISTRY,
    CANONICAL_AGENTS,
    RUNTIME_SPECIALIST_DELEGATION,
    SPECIALIST_ROLE_SEMANTICS,
    WorkforceGoal,
    build_revenue_factory_blueprint,
    get_agent,
    list_agents,
    run_workforce_goal,
)

router = APIRouter(prefix="/api/v1/ai-workforce", tags=["ai-workforce"])


@router.get("/status")
async def workforce_status() -> dict[str, Any]:
    return {
        "module": "ai_workforce",
        "status": "operational",
        "canonical_agents_total": len(CANONICAL_AGENTS),
        "canonical_agents": list(CANONICAL_AGENTS),
        "specialist_roles_registered": len(AGENT_REGISTRY),
        "specialist_role_semantics": SPECIALIST_ROLE_SEMANTICS,
        "specialist_role_delegation": dict(RUNTIME_SPECIALIST_DELEGATION),
        # Backward-compatible field retained but explicitly demoted from authority truth.
        "agents_registered": len(AGENT_REGISTRY),
        "agents_registered_semantics": "DEPRECATED_SPECIALIST_ROLE_COUNT",
        "guardrails": {
            "no_llm_calls": True,
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "no_autonomous_pricing": True,
            "no_autonomous_payment": True,
            "approval_required_for_external_actions": True,
            "no_self_granted_l5": True,
        },
    }


@router.get("/agents")
async def workforce_agents() -> dict[str, Any]:
    roles = [spec.model_dump(mode="json") for spec in list_agents()]
    for role in roles:
        role["canonical_owner"] = RUNTIME_SPECIALIST_DELEGATION[role["agent_id"]]
        role["role_semantics"] = SPECIALIST_ROLE_SEMANTICS
    return {
        "canonical_agents_total": len(CANONICAL_AGENTS),
        "canonical_agents": list(CANONICAL_AGENTS),
        "specialist_roles_total": len(roles),
        "specialist_role_semantics": SPECIALIST_ROLE_SEMANTICS,
        "specialist_roles": roles,
        # Compatibility aliases only.
        "total": len(roles),
        "agents": roles,
        "total_semantics": "DEPRECATED_SPECIALIST_ROLE_COUNT",
    }


@router.get("/agents/{agent_id}")
async def workforce_agent_detail(agent_id: str) -> dict[str, Any]:
    try:
        spec = get_agent(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    payload = spec.model_dump(mode="json")
    payload["canonical_owner"] = RUNTIME_SPECIALIST_DELEGATION[agent_id]
    payload["role_semantics"] = SPECIALIST_ROLE_SEMANTICS
    return payload


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
        "canonical_agents_total": blueprint["canonical_agents_total"],
        "canonical_agents": blueprint["canonical_agents"],
        "specialist_roles_total": blueprint["specialist_roles_total"],
        "specialist_role_semantics": blueprint["specialist_role_semantics"],
        "automation_plays_total": len(blueprint["automation_plays"]),
        # Backward-compatible alias. It must never be interpreted as permanent agents.
        "agents_total": blueprint["legacy_agent_contracts_total"],
        "agents_total_semantics": "DEPRECATED_SPECIALIST_ROLE_COUNT",
        "blueprint": blueprint,
    }
