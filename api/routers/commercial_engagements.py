"""Commercial engagement sprint endpoints (reports only; draft/approval-first)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.commercial_engagements import (
    CampaignIntelligenceSprintInput,
    LeadIntelligenceSprintInput,
    QuickWinOpsInput,
    SupportDeskSprintInput,
    run_campaign_intelligence_sprint,
    run_lead_intelligence_sprint,
    run_quick_win_ops,
    run_support_desk_sprint,
)
from auto_client_acquisition.commercial_engagements.delivery_catalog import (
    delivery_catalog_snapshot,
)

router = APIRouter(
    prefix="/api/v1/commercial/engagements",
    tags=["Sales"],
)


@router.get("/delivery-catalog")
def get_delivery_catalog() -> dict[str, Any]:
    """Service lines mapped to docs, session types, and engagement APIs."""
    return delivery_catalog_snapshot()


@router.post("/lead-intelligence-sprint")
def post_lead_intelligence_sprint(body: LeadIntelligenceSprintInput) -> dict:
    """Run Lead Intelligence Sprint — JSON report; no external sends."""
    return run_lead_intelligence_sprint(body).model_dump()


@router.post("/support-desk-sprint")
def post_support_desk_sprint(body: SupportDeskSprintInput) -> dict:
    """Classify + draft replies + SLA hints; drafts are not sent."""
    return run_support_desk_sprint(body).model_dump()


@router.post("/quick-win-ops")
def post_quick_win_ops(body: QuickWinOpsInput) -> dict:
    """Weekly-style rollup + BUILD/VALIDATE checklist snippets."""
    return run_quick_win_ops(body).model_dump()


@router.post("/campaign-intelligence-sprint")
def post_campaign_intelligence_sprint(body: CampaignIntelligenceSprintInput) -> dict:
    """Deterministic campaign angles + audited draft snippets."""
    return run_campaign_intelligence_sprint(body).model_dump()
