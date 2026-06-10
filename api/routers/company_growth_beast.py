"""V12.5 Company Growth Beast — service-for-clients router."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.company_growth_beast import (
    build_company_profile,
    build_content_pack,
    build_growth_diagnostic,
    build_offer_recommendation,
    build_target_segments,
    build_weekly_report,
    support_to_growth_insight,
)

router = APIRouter(
    prefix="/api/v1/company-growth-beast", tags=["company-growth-beast"],
)

_HARD_GATES = {
    "no_live_send": True, "no_scraping": True, "no_cold_outreach": True,
    "no_fake_proof": True, "consent_required_for_diagnostic": True,
    "approval_required_for_external_actions": True,
}


class _ProfileRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company_handle: str = Field(min_length=1, max_length=80)
    sector: str = "tbd"
    offer: str = ""
    ideal_customer: str = ""
    current_channels: str = ""
    biggest_problem: str = ""
    consent_for_diagnostic: bool = False


class _SupportInsightRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ticket_categories: dict[str, int] = Field(default_factory=dict)


class _WeeklyReportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company_handle: str = "Slot-A"
    sector: str = "b2b_services"
    diagnostics_done: int = 0
    pilots_offered: int = 0
    paid_pilots: int = 0
    proof_events: int = 0
    support_categories: dict[str, int] = Field(default_factory=dict)


@router.get("/status")
async def status() -> dict[str, Any]:
    return {"service": "company_growth_beast", "version": "v12.5",
            "hard_gates": _HARD_GATES,
            "next_action_ar": "ابدأ بإنشاء profile للشركة العميلة",
            "next_action_en": "Start by creating the client company profile."}


@router.post("/profile")
async def profile(req: _ProfileRequest) -> dict[str, Any]:
    p = build_company_profile(**req.model_dump())
    return {"profile": p.__dict__, "hard_gates": _HARD_GATES}


@router.post("/diagnostic")
async def diagnostic(req: _ProfileRequest) -> dict[str, Any]:
    p = build_company_profile(**req.model_dump())
    return {"diagnostic": build_growth_diagnostic(p), "hard_gates": _HARD_GATES}


@router.post("/targets")
async def targets(req: _ProfileRequest) -> dict[str, Any]:
    p = build_company_profile(**req.model_dump())
    return {"targets": build_target_segments(p), "hard_gates": _HARD_GATES}


@router.post("/offer")
async def offer(req: _ProfileRequest) -> dict[str, Any]:
    p = build_company_profile(**req.model_dump())
    return {"offer": build_offer_recommendation(p), "hard_gates": _HARD_GATES}


@router.post("/content-pack")
async def content_pack(req: _ProfileRequest) -> dict[str, Any]:
    p = build_company_profile(**req.model_dump())
    return {"content_pack": build_content_pack(p), "hard_gates": _HARD_GATES}


@router.post("/support-to-growth")
async def support_to_growth(req: _SupportInsightRequest) -> dict[str, Any]:
    return {"insight": support_to_growth_insight(
        ticket_categories=req.ticket_categories,
    ), "hard_gates": _HARD_GATES}


@router.post("/weekly-report")
async def weekly_report(req: _WeeklyReportRequest) -> dict[str, Any]:
    p = build_company_profile(
        company_handle=req.company_handle, sector=req.sector,
        consent_for_diagnostic=True,
    )
    return {"report": build_weekly_report(
        profile=p, diagnostics_done=req.diagnostics_done,
        pilots_offered=req.pilots_offered, paid_pilots=req.paid_pilots,
        proof_events=req.proof_events,
        support_categories=req.support_categories,
    ), "hard_gates": _HARD_GATES}
