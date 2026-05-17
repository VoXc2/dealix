"""
Revenue OS master catalog — sources, waterfall, actions, signal normalization.

Read-mostly + pure transforms. No scraping; signals are caller-supplied (MarketRadar policy).
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from auto_client_acquisition.customer_readiness.scores import compute_pricing_power_score
from auto_client_acquisition.growth_beast.market_radar import MarketSignal
from auto_client_acquisition.revenue_os import (
    WATERFALL_ORDER,
    AntiWasteViolation,
    forbidden_sources,
    list_action_catalog,
    next_best_offer,
    normalize_signals_batch,
    source_policies,
    suggest_dedupe_fingerprint,
    validate_pipeline_step,
)
from auto_client_acquisition.revenue_os.revenue_factory_blueprint import (
    revenue_factory_blueprint,
)
from auto_client_acquisition.revenue_os.learning_weekly import weekly_learning_report_skeleton

router = APIRouter(prefix="/api/v1/revenue-os", tags=["Revenue OS"])


class SignalsNormalizeRequest(BaseModel):
    signals: list[MarketSignal] = Field(default_factory=list)


class DedupeHintRequest(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=300)
    domain: str | None = None
    phone: str | None = None
    email: str | None = None
    external_crm_id: str | None = None


class ExpansionOfferRequest(BaseModel):
    primary_pain_keyword: str | None = None
    sector: str | None = None
    max_proof_level: int = 0
    proof_event_count: int = 0


class AntiWasteRequest(BaseModel):
    has_decision_passport: bool = False
    lead_source: str | None = None
    action_external: bool = False
    upsell_attempt: bool = False
    proof_event_count: int = 0
    evidence_level_for_public: int = 0
    public_marketing_attempt: bool = False


def _violations_to_json(v: list[AntiWasteViolation]) -> list[dict[str, str]]:
    return [{"code": x.code, "detail_ar": x.detail_ar, "detail_en": x.detail_en} for x in v]


@router.get("/catalog")
async def revenue_os_catalog() -> dict[str, Any]:
    """Single payload for Founder UI — registry + waterfall + action modes."""
    return {
        "golden_chain_rule": "No Decision Passport = No Action",
        "source_registry": source_policies(),
        "forbidden_sources": forbidden_sources(),
        "enrichment_waterfall_order": WATERFALL_ORDER,
        "action_catalog": list_action_catalog(),
        "factory_blueprint_endpoint": "/api/v1/revenue-os/factory/blueprint",
        "reference_modules": {
            "market_signal_input": "auto_client_acquisition.growth_beast.market_radar.MarketSignal",
            "signal_normalize": "auto_client_acquisition.revenue_os.signal_normalizer",
            "decision_passport": "auto_client_acquisition.decision_passport",
            "proof_ledger": "auto_client_acquisition.proof_ledger",
            "proof_canonical_payload": "auto_client_acquisition.revenue_os.proof_canonical",
            "service_sessions": "auto_client_acquisition.service_sessions",
            "learning_weekly": "auto_client_acquisition.revenue_os.learning_weekly",
            "revenue_factory_blueprint": (
                "auto_client_acquisition.revenue_os.revenue_factory_blueprint"
            ),
        },
    }


@router.post("/signals/normalize")
async def normalize_signals(payload: SignalsNormalizeRequest) -> dict[str, Any]:
    """Turn founder-supplied MarketSignals into Why-Now / Offer / Proof targets."""
    return normalize_signals_batch(payload.signals)


@router.post("/dedupe/hint")
async def dedupe_hint(body: DedupeHintRequest) -> dict[str, Any]:
    hint = suggest_dedupe_fingerprint(
        company_name=body.company_name,
        domain=body.domain,
        phone=body.phone,
        email=body.email,
        external_crm_id=body.external_crm_id,
    )
    return asdict(hint)


@router.post("/expansion/next-offer")
async def expansion_next_offer(body: ExpansionOfferRequest) -> dict[str, Any]:
    return next_best_offer(
        primary_pain_keyword=body.primary_pain_keyword,
        sector=body.sector,
        max_proof_level=body.max_proof_level,
        proof_event_count=body.proof_event_count,
    )


@router.post("/anti-waste/check")
async def anti_waste_check(body: AntiWasteRequest) -> dict[str, Any]:
    v = validate_pipeline_step(
        has_decision_passport=body.has_decision_passport,
        lead_source=body.lead_source,
        action_external=body.action_external,
        upsell_attempt=body.upsell_attempt,
        proof_event_count=body.proof_event_count,
        evidence_level_for_public=body.evidence_level_for_public,
        public_marketing_attempt=body.public_marketing_attempt,
    )
    return {"ok": len(v) == 0, "violations": _violations_to_json(v)}


@router.get("/learning/weekly-template")
async def learning_weekly_template() -> dict[str, Any]:
    """Weekly Learning Report structure — hook retention/analytics sources later."""
    return weekly_learning_report_skeleton()


@router.get("/factory/blueprint")
async def factory_blueprint() -> dict[str, Any]:
    """Founder-led Revenue Company Operating System blueprint."""
    return revenue_factory_blueprint()


@router.get("/scores/pricing-power-demo")
async def pricing_power_demo() -> dict[str, Any]:
    """Example scoring payload — replace with tenant metrics later."""
    return compute_pricing_power_score(
        max_proof_level=3,
        demand_signal_count=2,
        gross_margin_hint=0.42,
        delivery_repeatability=0.6,
        case_study_public_count=0,
        customer_urgency=0.55,
    )
