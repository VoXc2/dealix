"""System 35 — Self-Evolving Enterprise Fabric router.

Analyze control-plane history, propose improvements, and apply them — but only
after the proposal's approval ticket has been granted.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.self_evolving_os.core import (
    ProposalNotApprovedError,
    SelfEvolvingError,
    get_self_evolving_fabric,
)
from auto_client_acquisition.self_evolving_os.schemas import ImprovementTarget

router = APIRouter(prefix="/api/v1/self-evolving", tags=["self-evolving"])


class ProposalBody(BaseModel):
    target: ImprovementTarget
    target_id: str = Field(..., min_length=1)
    current_state: dict[str, Any] = Field(default_factory=dict)
    proposed_change: dict[str, Any] = Field(default_factory=dict)
    rationale: str = ""
    expected_gain: dict[str, Any] = Field(default_factory=dict)


class ApplyBody(BaseModel):
    actor: str = "system"


@router.post("/analyze")
async def analyze() -> dict[str, Any]:
    insights = get_self_evolving_fabric().analyze()
    return {
        "count": len(insights),
        "insights": [i.model_dump(mode="json") for i in insights],
    }


@router.post("/proposals", status_code=201)
async def create_proposal(body: ProposalBody) -> dict[str, Any]:
    proposal = get_self_evolving_fabric().propose_improvement(**body.model_dump())
    return proposal.model_dump(mode="json")


@router.get("/proposals")
async def list_proposals(status: str | None = None) -> dict[str, Any]:
    proposals = get_self_evolving_fabric().list_proposals(status=status)
    return {
        "count": len(proposals),
        "proposals": [p.model_dump(mode="json") for p in proposals],
    }


@router.get("/proposals/{proposal_id}")
async def get_proposal(proposal_id: str) -> dict[str, Any]:
    proposal = get_self_evolving_fabric().get_proposal(proposal_id)
    if proposal is None:
        raise HTTPException(status_code=404, detail=f"proposal not found: {proposal_id}")
    return proposal.model_dump(mode="json")


@router.post("/proposals/{proposal_id}/apply")
async def apply_proposal(proposal_id: str, body: ApplyBody) -> dict[str, Any]:
    try:
        proposal = get_self_evolving_fabric().apply_proposal(
            proposal_id, actor=body.actor
        )
    except ProposalNotApprovedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except SelfEvolvingError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return proposal.model_dump(mode="json")
