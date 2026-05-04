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
