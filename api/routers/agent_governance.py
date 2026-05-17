"""Agent Governance v5 — read-only routes."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.agent_governance import (
    evaluate_action,
    get_agent,
    list_agents,
    summary,
)
from auto_client_acquisition.agent_governance.schemas import (
    AutonomyLevel,
    ToolCategory,
)

router = APIRouter(prefix="/api/v1/agent-governance", tags=["agent-governance"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "agent_governance",
        **summary(),
    }


@router.get("/agents")
async def get_agents() -> dict:
    return {"agents": list_agents()}


@router.get("/agents/{agent_id}")
async def get_one_agent(agent_id: str) -> dict:
    try:
        spec = get_agent(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return spec.model_dump(mode="json")


@router.post("/evaluate")
async def evaluate(payload: dict = Body(...)) -> dict:
    """Evaluate whether an action is permitted.

    Body:
      - agent_id: str
      - tool: str (one of ToolCategory)
      - autonomy_level: str (one of AutonomyLevel)
      - allowed_tools: optional list[str] (defaults to agent's spec)
    """
    agent_id = payload.get("agent_id")
    tool = payload.get("tool")
    autonomy = payload.get("autonomy_level")
    if not all([agent_id, tool, autonomy]):
        raise HTTPException(
            status_code=400,
            detail="agent_id, tool, autonomy_level required",
        )
    try:
        # Default allowed_tools to the agent's spec if not overridden.
        allowed = payload.get("allowed_tools")
        if allowed is None:
            try:
                spec = get_agent(str(agent_id))
                allowed = list(spec.allowed_tools)
            except KeyError:
                allowed = []
        result = evaluate_action(
            agent_id=str(agent_id),
            tool=str(tool),
            autonomy_level=str(autonomy),
            allowed_tools=list(allowed) if allowed else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result.to_dict()


# ── Agent Registry — doctrine #9 (owner + scope + audit) ──────────

from auto_client_acquisition.agent_registry import (  # noqa: E402
    AgentRegistryError,
    AgentSpec,
    get_default_registry,
)
from auto_client_acquisition.agent_registry import get as registry_get  # noqa: E402
from auto_client_acquisition.agent_registry import (  # noqa: E402
    list_agents as registry_list,
)
from auto_client_acquisition.agent_registry import register as registry_register  # noqa: E402


@router.get("/registry")
async def registry_list_endpoint(include_disabled: bool = True) -> dict:
    """List every registered agent (doctrine #9 registry)."""
    rows = registry_list(include_disabled=include_disabled)
    return {
        "count": len(rows),
        "agents": [r.model_dump(mode="json") for r in rows],
        "governance_decision": "allow",
    }


@router.get("/registry/{agent_name}")
async def registry_get_endpoint(agent_name: str) -> dict:
    """Fetch one registered agent spec."""
    spec = registry_get(agent_name)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"agent {agent_name!r} not registered")
    body = spec.model_dump(mode="json")
    body["governance_decision"] = "allow"
    return body


@router.post("/registry")
async def registry_register_endpoint(payload: dict = Body(...)) -> dict:
    """Register an agent. Rejected (422) without a non-empty owner + scope."""
    try:
        spec = AgentSpec.model_validate(payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=422, detail=f"invalid agent spec: {exc}") from exc
    try:
        stored = registry_register(spec)
    except AgentRegistryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    body = stored.model_dump(mode="json")
    body["registered"] = True
    body["governance_decision"] = "allow"
    return body


@router.post("/registry/{agent_name}/disable")
async def registry_disable_endpoint(agent_name: str) -> dict:
    """Disable a registered agent (kept for audit; not deleted)."""
    found = get_default_registry().disable(agent_name)
    if not found:
        raise HTTPException(status_code=404, detail=f"agent {agent_name!r} not registered")
    return {"disabled": True, "agent_name": agent_name, "governance_decision": "allow"}
