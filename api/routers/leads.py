"""Leads (Phase 8) endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_acquisition_pipeline
from api.schemas import LeadCreateRequest, LeadResponse, PipelineResponse
from auto_client_acquisition.agents.intake import LeadSource
from auto_client_acquisition.pipeline import AcquisitionPipeline

router = APIRouter(prefix="/api/v1/leads", tags=["leads"])


@router.post("", response_model=PipelineResponse)
async def create_lead(
    payload: LeadCreateRequest,
    pipeline: AcquisitionPipeline = Depends(get_acquisition_pipeline),
    auto_book: bool = True,
    auto_proposal: bool = False,
) -> PipelineResponse:
    """Submit a new lead — runs through the full acquisition pipeline."""
    try:
        source = LeadSource(payload.source)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid source: {e}") from e

    result = await pipeline.run(
        payload=payload.model_dump(exclude_none=True),
        source=source,
        auto_book=auto_book,
        auto_proposal=auto_proposal,
    )
    return PipelineResponse(
        lead=LeadResponse(
            id=result.lead.id,
            source=result.lead.source.value,
            company_name=result.lead.company_name,
            contact_name=result.lead.contact_name,
            contact_email=result.lead.contact_email,
            contact_phone=result.lead.contact_phone,
            sector=result.lead.sector,
            region=result.lead.region,
            status=result.lead.status.value,
            fit_score=result.lead.fit_score,
            urgency_score=result.lead.urgency_score,
            pain_points=result.lead.pain_points,
            locale=result.lead.locale,
            created_at=result.lead.created_at,
        ),
        fit_score=result.fit_score.to_dict() if result.fit_score else None,
        extraction=result.extraction.to_dict() if result.extraction else None,
        qualification=result.qualification.to_dict() if result.qualification else None,
        crm_sync=result.crm_sync.to_dict() if result.crm_sync else None,
        booking=result.booking.to_dict() if result.booking else None,
        proposal=result.proposal.to_dict() if result.proposal else None,
        warnings=result.warnings,
    )
