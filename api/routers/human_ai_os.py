"""System 33 — Human-AI Operating Model router.

Delegation, escalation, explainability and the human oversight queue.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.control_plane_os.approval_gate import ApprovalGateError
from auto_client_acquisition.human_ai_os.core import HumanAIError, get_human_ai_model

router = APIRouter(prefix="/api/v1/human-ai", tags=["human-ai"])


class DelegationBody(BaseModel):
    from_human: str = Field(..., min_length=1)
    to_agent: str = Field(..., min_length=1)
    scope: list[str] = Field(default_factory=list)
    ttl_hours: float = Field(..., gt=0.0)


class EscalationBody(BaseModel):
    run_id: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)
    escalated_to: str = "founder"


class DecisionBody(BaseModel):
    approver: str = Field(..., min_length=1)
    reason: str = ""


@router.post("/delegations", status_code=201)
async def create_delegation(body: DelegationBody) -> dict[str, Any]:
    try:
        delegation = get_human_ai_model().delegate(
            from_human=body.from_human,
            to_agent=body.to_agent,
            scope=body.scope,
            ttl_hours=body.ttl_hours,
        )
    except HumanAIError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return delegation.model_dump(mode="json")


@router.delete("/delegations/{delegation_id}")
async def revoke_delegation(delegation_id: str, actor: str = "system") -> dict[str, Any]:
    try:
        delegation = get_human_ai_model().revoke_delegation(delegation_id, actor=actor)
    except HumanAIError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return delegation.model_dump(mode="json")


@router.post("/escalations", status_code=201)
async def create_escalation(body: EscalationBody) -> dict[str, Any]:
    escalation = get_human_ai_model().escalate(
        run_id=body.run_id, reason=body.reason, escalated_to=body.escalated_to
    )
    return escalation.model_dump(mode="json")


@router.get("/explain/{subject_id}")
async def explain(subject_id: str) -> dict[str, Any]:
    return get_human_ai_model().explain(subject_id).model_dump(mode="json")


@router.get("/oversight-queue")
async def oversight_queue(source_module: str | None = None) -> dict[str, Any]:
    items = get_human_ai_model().oversight_queue(source_module=source_module)
    return {"count": len(items), "items": [i.model_dump(mode="json") for i in items]}


@router.post("/oversight/{ticket_id}/grant")
async def grant(ticket_id: str, body: DecisionBody) -> dict[str, Any]:
    try:
        return get_human_ai_model().grant(ticket_id, body.approver)
    except ApprovalGateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/oversight/{ticket_id}/reject")
async def reject(ticket_id: str, body: DecisionBody) -> dict[str, Any]:
    try:
        return get_human_ai_model().reject(ticket_id, body.approver, body.reason)
    except ApprovalGateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
