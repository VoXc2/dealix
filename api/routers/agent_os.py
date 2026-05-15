"""Agent OS router — register / list / kill agents. Admin-key gated.

Honors the 11 non-negotiables: no agent without identity, owner,
autonomy_level. L4+ requires kill_switch_owner. Forbidden tools rejected.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/agents", tags=["agent-os"])


class _RegisterBody(BaseModel):
    agent_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    purpose: str = Field(..., min_length=1)
    autonomy_level: int = Field(1, ge=0, le=5)
    allowed_tools: list[str] = Field(default_factory=list)
    kill_switch_owner: str = ""
    notes: str = ""


class _KillBody(BaseModel):
    reason: str = Field(..., min_length=3)


@router.post("/register", dependencies=[Depends(require_admin_key)])
async def register(body: _RegisterBody) -> dict[str, Any]:
    from auto_client_acquisition.agent_os import (
        new_card,
        register_agent,
    )
    try:
        card = new_card(
            agent_id=body.agent_id,
            name=body.name,
            owner=body.owner,
            purpose=body.purpose,
            autonomy_level=body.autonomy_level,
            allowed_tools=body.allowed_tools,
            kill_switch_owner=body.kill_switch_owner,
            notes=body.notes,
        )
        registered = register_agent(card)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return {
        "agent": registered.to_dict(),
        "governance_decision": "allow_with_review",
    }


@router.get("", dependencies=[Depends(require_admin_key)])
async def list_all(
    status: str | None = None,
    owner: str | None = None,
) -> dict[str, Any]:
    from auto_client_acquisition.agent_os import list_agents
    agents = list_agents(status=status, owner=owner)
    return {
        "count": len(agents),
        "agents": [a.to_dict() for a in agents],
        "governance_decision": "allow",
    }


@router.get("/{agent_id}", dependencies=[Depends(require_admin_key)])
async def get_one(agent_id: str) -> dict[str, Any]:
    from auto_client_acquisition.agent_os import get_agent
    card = get_agent(agent_id)
    if card is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    return {"agent": card.to_dict(), "governance_decision": "allow"}


@router.post("/{agent_id}/kill", dependencies=[Depends(require_admin_key)])
async def kill(agent_id: str, body: _KillBody) -> dict[str, Any]:
    from auto_client_acquisition.agent_os import kill_agent
    try:
        card = kill_agent(agent_id, body.reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {
        "activated": True,
        "agent": card.to_dict(),
        "governance_decision": "allow",
    }


@router.get("/{agent_id}/audit", dependencies=[Depends(require_admin_key)])
async def audit(agent_id: str) -> dict[str, Any]:
    """Audit view: agent card + performance summary + recent friction events."""
    from auto_client_acquisition.agent_os import get_agent, summarize_agent
    from auto_client_acquisition.friction_log import list_events

    card = get_agent(agent_id)
    if card is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    performance = summarize_agent(agent_id)
    events = list_events(customer_id="dealix_internal", since_days=90, limit=200)
    friction = [
        e.to_dict() for e in events if getattr(e, "workflow_id", "") == agent_id
    ][:20]
    return {
        "agent": card.to_dict(),
        "performance": performance.to_dict() if performance else None,
        "friction_events": friction,
        "event_count": len(friction),
        "governance_decision": "allow",
    }


@router.get("/{agent_id}/performance", dependencies=[Depends(require_admin_key)])
async def performance(agent_id: str) -> dict[str, Any]:
    """Performance dashboard data — quality / latency / cost / compliance."""
    from auto_client_acquisition.agent_os import summarize_agent

    summary = summarize_agent(agent_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    return {"performance": summary.to_dict(), "governance_decision": "allow"}
