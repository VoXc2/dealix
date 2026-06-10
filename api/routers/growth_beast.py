"""V12.5 Growth Beast router — Dealix self-growth engine."""
from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.growth_beast import (
    MarketSignal,
    SignalSource,
    SignalType,
    compute_icp_score,
    draft_content,
    draft_warm_route,
    evaluate_signals,
    match_offer,
    next_experiment,
    proof_to_content_idea,
    rank_accounts,
    weekly_summary,
)

router = APIRouter(prefix="/api/v1/growth-beast", tags=["growth-beast"])

_HARD_GATES = {
    "no_live_send": True, "no_scraping": True, "no_cold_outreach": True,
    "no_linkedin_automation": True, "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


class _SignalsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    signals: list[MarketSignal] = Field(default_factory=list)


class _ICPRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    placeholder: str = "Slot-X"
    pain_intensity: int = 0
    ability_to_pay: int = 0
    urgency: int = 0
    proof_potential: int = 0
    founder_access: int = 0
    referral_potential: int = 0
    sector_repeatability: int = 0
    delivery_complexity: int = 0
    compliance_risk: int = 0


class _OfferRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sector: str
    signal_type: str


class _ContentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sector: str
    angle: str
    content_type: Literal["linkedin_post", "sector_insight", "diagnostic_cta",
                          "case_snippet", "objection_post"] = "linkedin_post"


class _WarmRouteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    channel: str
    sector: str
    placeholder_name: str = "[الاسم]"
    pain_hint: str = "growth_clarity"


class _ExperimentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sector_focus: str = "marketing_agency"
    last_week_summary: dict | None = None


class _ProofToContentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    proof_event: dict


@router.get("/status")
async def status() -> dict[str, Any]:
    return {"service": "growth_beast", "version": "v12.5", "degraded": False,
            "hard_gates": _HARD_GATES,
            "next_action_ar": "استخدم /today لرؤية أهم 3 قرارات",
            "next_action_en": "Use /today for top-3 decisions."}


@router.post("/signals/evaluate")
async def signals_evaluate(req: _SignalsRequest) -> dict[str, Any]:
    return {"evaluation": evaluate_signals(req.signals), "hard_gates": _HARD_GATES}


@router.post("/targets/rank")
async def targets_rank(req: _ICPRequest) -> dict[str, Any]:
    score = compute_icp_score(
        pain_intensity=req.pain_intensity, ability_to_pay=req.ability_to_pay,
        urgency=req.urgency, proof_potential=req.proof_potential,
        founder_access=req.founder_access, referral_potential=req.referral_potential,
        sector_repeatability=req.sector_repeatability,
        delivery_complexity=req.delivery_complexity,
        compliance_risk=req.compliance_risk,
    )
    ranked = rank_accounts([(req.placeholder, score)])
    return {"ranked": ranked, "icp_score": score.score, "hard_gates": _HARD_GATES}


@router.post("/offer/match")
async def offer_match(req: _OfferRequest) -> dict[str, Any]:
    return {"offer": match_offer(sector=req.sector, signal_type=req.signal_type),
            "hard_gates": _HARD_GATES}


@router.post("/content/draft")
async def content_draft(req: _ContentRequest) -> dict[str, Any]:
    return {"draft": draft_content(sector=req.sector, angle=req.angle,
                                   content_type=req.content_type),
            "hard_gates": _HARD_GATES}


@router.post("/warm-route/draft")
async def warm_route_draft(req: _WarmRouteRequest) -> dict[str, Any]:
    return {"route": draft_warm_route(channel=req.channel, sector=req.sector,
                                      placeholder_name=req.placeholder_name,
                                      pain_hint=req.pain_hint),
            "hard_gates": _HARD_GATES}


@router.post("/experiment/next")
async def experiment_next(req: _ExperimentRequest) -> dict[str, Any]:
    return {"experiment": next_experiment(sector_focus=req.sector_focus,
                                          last_week_summary=req.last_week_summary),
            "hard_gates": _HARD_GATES}


@router.post("/proof-to-content")
async def proof_to_content_endpoint(req: _ProofToContentRequest) -> dict[str, Any]:
    return {"content_idea": proof_to_content_idea(proof_event=req.proof_event),
            "hard_gates": _HARD_GATES}


@router.get("/today")
async def today() -> dict[str, Any]:
    """Composed daily snapshot — uses default values when no real data yet."""
    return {
        "top_3_targets": ["agency_with_no_proof", "b2b_with_weak_followup",
                          "consulting_with_offer_clarity_gap"],
        "best_segment_today": "marketing_agency",
        "best_offer": match_offer(sector="marketing_agency",
                                  signal_type="no_proof_visible"),
        "best_content": draft_content(sector="marketing_agency",
                                      angle="proof_pack_visibility"),
        "next_experiment": next_experiment(sector_focus="marketing_agency"),
        "blocked_actions": [
            "cold_whatsapp", "scraping", "linkedin_dm_automation",
            "purchased_list_blast",
        ],
        "hard_gates": _HARD_GATES,
    }
