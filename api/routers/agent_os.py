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
    from auto_client_acquisition.secure_agent_runtime_os import activate_kill_switch
    result = activate_kill_switch(agent_id=agent_id, reason=body.reason)
    if not result.get("activated"):
        raise HTTPException(status_code=404, detail=result)
    return result


@router.get("/{agent_id}/audit", dependencies=[Depends(require_admin_key)])
async def audit(agent_id: str) -> dict[str, Any]:
    """Audit view: agent card + last 20 audit events that reference it."""
    from auto_client_acquisition.agent_os import get_agent
    from auto_client_acquisition.auditability_os.audit_event import list_events

    card = get_agent(agent_id)
    if card is None:
        raise HTTPException(status_code=404, detail="agent_not_found")
    events = list_events(customer_id="dealix_internal", limit=200)
    relevant = [e.to_dict() for e in events if agent_id in (e.summary or "")][:20]
    return {
        "agent": card.to_dict(),
        "recent_events": relevant,
        "event_count": len(relevant),
        "governance_decision": "allow",
    }
