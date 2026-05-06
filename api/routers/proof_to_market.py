"""Proof-to-market planning API — approval-gated outputs only."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.proof_to_market import build_proof_to_market_plan

router = APIRouter(prefix="/api/v1/proof-to-market", tags=["proof-to-market"])


class _ProofPlanBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    proof_events: list[dict[str, Any]] = Field(default_factory=list)
    sector: str = "general"
    has_written_approval: bool = False


@router.get("/status")
async def proof_to_market_status() -> dict[str, Any]:
    return {
        "service": "proof_to_market",
        "status": "operational",
        "version": "v12_5",
        "action_mode": "approval_required",
    }


@router.post("/plan")
async def proof_plan(body: _ProofPlanBody = Body(default_factory=_ProofPlanBody)) -> dict[str, Any]:
    return build_proof_to_market_plan(
        body.proof_events,
        sector=body.sector,
        has_written_approval=body.has_written_approval,
    )
