"""V12 Partnership OS router."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.partnership_os import (
    Partner,
    PartnerType,
    add_referral,
    compute_fit_score,
    list_referrals,
    recommend_motion,
)

router = APIRouter(prefix="/api/v1/partnership-os", tags=["partnership-os"])


_HARD_GATES = {
    "no_fake_partner_names": True,
    "no_white_label_before_3_paid_pilots": True,
    "no_revenue_share_without_referral_data": True,
    "no_exclusivity": True,
    "approval_required_for_external_actions": True,
}


class _FitScoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_id: str = "partner_placeholder"
    placeholder_name: str = Field(default="Partner-A", max_length=80)
    partner_type: PartnerType
    sector: str = "tbd"
    region: str = "riyadh"
    customer_segment: str = "b2b_services"
    serves_b2b: bool = True
    has_existing_customers: bool = True
    saudi_market_focus: bool = True
    paid_pilots_count: int = Field(default=0, ge=0, le=999)
    has_referral_data: bool = False


class _IntroDraftRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_placeholder_name: str = "Partner-A"
    customer_placeholder: str = "Customer-Slot-A"


class _LogReferralRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_id: str
    customer_placeholder: str


@router.get("/status")
async def partnership_os_status() -> dict[str, Any]:
    return {
        "service": "partnership_os",
        "module": "partnership_os",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {
            "fit_score": "ok",
            "motion": "ok",
            "referral_tracker": "ok",
        },
        "hard_gates": _HARD_GATES,
        "next_action_ar": "احسب /fit-score ثم /intro-draft",
        "next_action_en": "Compute /fit-score then /intro-draft.",
    }


@router.post("/fit-score")
async def fit_score_endpoint(req: _FitScoreRequest) -> dict[str, Any]:
    partner = Partner(
        partner_id=req.partner_id,
        placeholder_name=req.placeholder_name,
        partner_type=req.partner_type,
        sector=req.sector,
        region=req.region,
    )
    score = compute_fit_score(
        partner=partner,
        customer_segment=req.customer_segment,
        serves_b2b=req.serves_b2b,
        has_existing_customers=req.has_existing_customers,
        saudi_market_focus=req.saudi_market_focus,
    )
    motion = recommend_motion(
        partner=partner,
        fit_score=score,
        paid_pilots_count=req.paid_pilots_count,
        has_referral_data=req.has_referral_data,
    )
    return {
        "partner": partner.model_dump(mode="json"),
        "score": score,
        "motion": motion.motion,
        "motion_reason_ar": motion.reason_ar,
        "motion_reason_en": motion.reason_en,
        "action_mode": motion.action_mode,
        "blocked": motion.blocked,
        "hard_gates": _HARD_GATES,
    }


@router.post("/intro-draft")
async def intro_draft(req: _IntroDraftRequest) -> dict[str, Any]:
    ar = (
        f"السلام عليكم، أعرّفكم على {req.partner_placeholder_name} — شريك "
        f"محتمل لـ {req.customer_placeholder}. شراكة مرتكزة على الإحالات "
        "أوّلاً، بدون white-label وبدون حصريّة. هل نتكلّم 30 دقيقة؟"
    )
    en = (
        f"Hi, introducing {req.partner_placeholder_name} — a potential "
        f"partner for {req.customer_placeholder}. Referral-first, no "
        "white-label, no exclusivity. Want to talk for 30 min?"
    )
    return {
        "action_mode": "draft_only",
        "draft_ar": ar,
        "draft_en": en,
        "send_method": "manual_only",
        "hard_gates": _HARD_GATES,
    }


@router.post("/log-referral")
async def log_referral(req: _LogReferralRequest) -> dict[str, Any]:
    ref = add_referral(
        partner_id=req.partner_id,
        customer_placeholder=req.customer_placeholder,
    )
    return {
        "referral": ref.model_dump(mode="json"),
        "total_for_partner": len(list_referrals(partner_id=req.partner_id)),
        "hard_gates": _HARD_GATES,
    }
