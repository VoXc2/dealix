"""Wave 12.7 — Expansion Engine HTTP surface.

Exposes the Wave 12.5 §33.2.5 Expansion Engine via FastAPI:
- GET  /api/v1/expansion-engine/status       — layer health + hard gates
- POST /api/v1/expansion-engine/readiness    — compute Expansion Readiness Score
- POST /api/v1/expansion-engine/recommend    — recommend next-best-offer
- GET  /api/v1/expansion-engine/pain-types   — list known customer pain types

Wraps ``auto_client_acquisition.expansion_engine.readiness_score``.

Hard rule (Article 8): every score is_estimate=True; action_mode is
gated by readiness — no upsell without proof; no auto-execute.
"""
from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from auto_client_acquisition.expansion_engine import (
    compute_readiness_score,
    recommend_next_offer,
)

router = APIRouter(prefix="/api/v1/expansion-engine", tags=["Expansion Engine"])


_HARD_GATES = {
    "no_upsell_without_proof": True,
    "no_auto_execute_offer": True,
    "is_estimate_always_true": True,
    "action_mode_gated_by_readiness": True,
    "approval_required_for_external_actions": True,
}


# ─────────────────────────────────────────────────────────────────────
# Status
# ─────────────────────────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict[str, Any]:
    """Layer status + hard gates (no I/O)."""
    return {
        "service": "expansion_engine",
        "version": "v2",
        "hard_gates": _HARD_GATES,
        "supported_pains": [
            "dormant_data", "follow_up_gap", "support_chaos",
            "executive_visibility", "agency_proof_gap", "unknown",
        ],
        "supported_offers": [
            "data_to_revenue_pack", "managed_growth_ops", "support_os",
            "executive_command_center", "agency_partner_os",
            "no_recommendation_yet",
        ],
        "action_mode_thresholds": {
            "suggest_only": "score < 0.6 OR not ready",
            "draft_only": "0.6 <= score < 0.8 + ready",
            "approval_required": "score >= 0.8 + ready",
        },
    }


@router.get("/pain-types")
async def list_pain_types() -> dict[str, Any]:
    """Catalog of known customer pain types + their offer mappings."""
    return {
        "pains": [
            {
                "pain": "dormant_data",
                "offer": "data_to_revenue_pack",
                "rationale_ar": "تحويل البيانات الخاملة إلى فرص",
                "rationale_en": "Activate dormant CRM data into pipeline",
            },
            {
                "pain": "follow_up_gap",
                "offer": "managed_growth_ops",
                "rationale_ar": "متابعة منظَّمة للفرص",
                "rationale_en": "Structured follow-up for opportunities",
            },
            {
                "pain": "support_chaos",
                "offer": "support_os",
                "rationale_ar": "تنظيم الدعم وتحسين تجربة العميل",
                "rationale_en": "Organize support + lift customer experience",
            },
            {
                "pain": "executive_visibility",
                "offer": "executive_command_center",
                "rationale_ar": "رؤية إدارة شاملة للنمو والمخاطر",
                "rationale_en": "Executive-level growth + risk visibility",
            },
            {
                "pain": "agency_proof_gap",
                "offer": "agency_partner_os",
                "rationale_ar": "بناء proof للوكالات لزيادة الاحتفاظ",
                "rationale_en": "Build proof for agencies to lift retention",
            },
            {
                "pain": "unknown",
                "offer": "no_recommendation_yet",
                "rationale_ar": "تحتاج توضيح مصدر الألم قبل الاقتراح",
                "rationale_en": "Clarify pain source before recommending",
            },
        ],
        "hard_gates": _HARD_GATES,
    }


# ─────────────────────────────────────────────────────────────────────
# Readiness score
# ─────────────────────────────────────────────────────────────────────


class ReadinessRequest(BaseModel):
    """Inputs for computing the Expansion Readiness Score.

    All defaults = 0 / unknown — caller passes what's available.
    Article 8: when most inputs are 0, score is low and `blockers`
    explains why.
    """

    proof_event_count: int = 0
    max_evidence_level: int = 0
    customer_approved_proof_count: int = 0
    public_proof_count: int = 0
    payment_history_paid_count: int = 0
    delivery_sessions_complete_count: int = 0
    support_tickets_open: int = 0
    support_tickets_critical: int = 0
    days_since_last_engagement: int = 30
    customer_health_bucket: str = "unknown"
    budget_tier_match_score: float = Field(0.5, ge=0.0, le=1.0)
    remaining_pain_score: float = Field(0.5, ge=0.0, le=1.0)


@router.post("/readiness")
async def readiness(req: ReadinessRequest) -> dict[str, Any]:
    """Compute Expansion Readiness Score (numeric).

    Returns the full ExpansionReadinessScore as a dict including
    sub-scores + ready bool + blockers + notes (audit trail).
    """
    score = compute_readiness_score(
        proof_event_count=req.proof_event_count,
        max_evidence_level=req.max_evidence_level,
        customer_approved_proof_count=req.customer_approved_proof_count,
        public_proof_count=req.public_proof_count,
        payment_history_paid_count=req.payment_history_paid_count,
        delivery_sessions_complete_count=req.delivery_sessions_complete_count,
        support_tickets_open=req.support_tickets_open,
        support_tickets_critical=req.support_tickets_critical,
        days_since_last_engagement=req.days_since_last_engagement,
        customer_health_bucket=req.customer_health_bucket,
        budget_tier_match_score=req.budget_tier_match_score,
        remaining_pain_score=req.remaining_pain_score,
    )
    return {
        "score": score.score,
        "ready": score.ready,
        "proof_signal_score": score.proof_signal_score,
        "engagement_score": score.engagement_score,
        "friction_score": score.friction_score,
        "budget_fit_score": score.budget_fit_score,
        "is_estimate": score.is_estimate,
        "blockers": list(score.blockers),
        "notes": list(score.notes),
    }


# ─────────────────────────────────────────────────────────────────────
# Next-best-offer
# ─────────────────────────────────────────────────────────────────────


class RecommendRequest(BaseModel):
    """Inputs for recommending the next-best-offer."""

    readiness: ReadinessRequest
    primary_pain: Literal[
        "dormant_data", "follow_up_gap", "support_chaos",
        "executive_visibility", "agency_proof_gap", "unknown",
    ] = "unknown"


@router.post("/recommend")
async def recommend(req: RecommendRequest) -> dict[str, Any]:
    """Recommend the next-best-offer based on pain + readiness.

    Hard rule (Article 8): action_mode is GATED by readiness:
    - not ready → suggest_only (founder considers, no draft)
    - ready + score < 0.8 → draft_only (founder drafts, holds)
    - ready + score >= 0.8 → approval_required (proceed after approval)
    """
    # First compute readiness from the embedded inputs
    readiness_score = compute_readiness_score(
        proof_event_count=req.readiness.proof_event_count,
        max_evidence_level=req.readiness.max_evidence_level,
        customer_approved_proof_count=req.readiness.customer_approved_proof_count,
        public_proof_count=req.readiness.public_proof_count,
        payment_history_paid_count=req.readiness.payment_history_paid_count,
        delivery_sessions_complete_count=req.readiness.delivery_sessions_complete_count,
        support_tickets_open=req.readiness.support_tickets_open,
        support_tickets_critical=req.readiness.support_tickets_critical,
        days_since_last_engagement=req.readiness.days_since_last_engagement,
        customer_health_bucket=req.readiness.customer_health_bucket,
        budget_tier_match_score=req.readiness.budget_tier_match_score,
        remaining_pain_score=req.readiness.remaining_pain_score,
    )
    offer = recommend_next_offer(
        readiness=readiness_score,
        primary_pain=req.primary_pain,
    )
    return {
        "offer_key": offer.offer_key,
        "offer_name_ar": offer.offer_name_ar,
        "offer_name_en": offer.offer_name_en,
        "rationale_ar": offer.rationale_ar,
        "rationale_en": offer.rationale_en,
        "confidence": offer.confidence,
        "action_mode": offer.action_mode,
        "is_estimate": offer.is_estimate,
        # Echo readiness for audit
        "readiness_score": readiness_score.score,
        "readiness_ready": readiness_score.ready,
        "blockers": list(readiness_score.blockers),
    }
