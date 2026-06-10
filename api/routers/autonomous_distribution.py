"""
Autonomous Distribution API — product routing, proposal queue, sector campaigns.
يُعرِّف نقاط النهاية الخاصة بمحرك التوزيع الذاتي.

All proposals start as 'pending_approval'.  No outbound communication happens
until the founder explicitly calls POST /approve/{proposal_id}.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from autonomous_growth.distribution_engine import AutonomousDistributionEngine
from autonomous_growth.product_catalog import PRODUCT_CATALOG

router = APIRouter(
    prefix="/api/v1/autonomous-distribution",
    tags=["autonomous-distribution"],
)

_engine = AutonomousDistributionEngine()


# ── Request / Response models ────────────────────────────────────────────────


class ProcessLeadRequest(BaseModel):
    name: str = ""
    company: str = ""
    sector: str = "general"
    company_size: str = "medium"
    icp_score: float = Field(default=0.4, ge=0.0, le=1.0)
    budget_signal: str | None = None
    locale: str = "ar"
    lead_id: str | None = None


class SectorCampaignRequest(BaseModel):
    sector: str
    channels: list[str] = Field(default_factory=lambda: ["linkedin", "email"])


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.post("/process-lead", summary="Process a single lead through the distribution engine")
async def process_lead(body: ProcessLeadRequest) -> dict[str, Any]:
    """
    Run a lead through the full distribution engine:
    ICP scoring → product routing → proposal draft generation (pending_approval).
    """
    payload = body.model_dump(exclude_none=True)
    result = await _engine.process_lead(payload)
    return result.to_dict()


@router.post("/sector-campaign", summary="Run a sector-wide distribution campaign")
async def sector_campaign(body: SectorCampaignRequest) -> dict[str, Any]:
    """Identify sector prospects and route each to the appropriate product tier."""
    results = await _engine.run_sector_distribution(
        sector=body.sector,
        channels=body.channels,
    )
    return {
        "sector": body.sector,
        "prospects_processed": len(results),
        "results": [r.to_dict() for r in results],
    }


@router.get("/pending-approvals", summary="List proposals awaiting founder approval")
async def pending_approvals() -> dict[str, Any]:
    """Return all proposal drafts with status 'pending_approval'."""
    drafts = await _engine.get_pending_approvals()
    return {
        "count": len(drafts),
        "proposals": [d.to_dict() for d in drafts],
    }


@router.post("/approve/{proposal_id}", summary="Approve a proposal draft")
async def approve_proposal(proposal_id: str) -> dict[str, Any]:
    """
    Mark a proposal draft as 'approved'.
    The approved draft can then be sent manually by the founder.
    Raises 404 if the proposal is not found or already processed.
    """
    updated = await _engine.approve_proposal(proposal_id)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"Proposal '{proposal_id}' not found or not in pending_approval state.",
        )
    return {"status": "approved", "proposal_id": proposal_id}


@router.get("/product-catalog", summary="Return the full Dealix product catalog")
async def product_catalog() -> dict[str, Any]:
    """Return all 5 product tiers with full details."""
    return {
        "products": [p.to_dict() for p in PRODUCT_CATALOG.values()],
        "count": len(PRODUCT_CATALOG),
    }


@router.get("/stats", summary="Return engine aggregate statistics")
async def stats() -> dict[str, Any]:
    """Return totals: processed, pending, approved, sent."""
    return _engine.get_stats()
