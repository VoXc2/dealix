"""V12 Partnership OS router."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.partnership_os import (
    FTC_DISCLOSURE_TEXT_AR,
    FTC_DISCLOSURE_TEXT_EN,
    TIER_LABELS,
    Partner,
    PartnerStage,
    PartnerType,
    add_referral,
    can_advance,
    compute_fit_score,
    compute_payout,
    flag_forbidden_claims,
    list_referrals,
    next_stage,
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


# ── Full Ops 2.0 — lifecycle, claim guard, payout ────────────────


class _StageAdvanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    from_stage: PartnerStage
    to_stage: PartnerStage
    fit_score: int = Field(default=0, ge=0, le=100)
    trained: bool = False
    has_clean_compliance: bool = True


class _ClaimScanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_copy: str = Field(default="", max_length=8000)


class _PayoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    motion: str = Field(
        default="affiliate_lead",
        pattern=r"^(affiliate_lead|warm_qualified_intro|strategic_partner_deal)$",
    )
    deal_amount_sar: int = Field(default=0, ge=0, le=10_000_000)
    invoice_paid: bool = False
    is_duplicate: bool = False
    is_self_referral: bool = False
    compliance_violation: bool = False
    approved_pct: float | None = Field(default=None, ge=0.0, le=100.0)


@router.get("/lifecycle")
async def lifecycle_overview() -> dict[str, Any]:
    """Read-only — the explicit partner lifecycle stages + tiers."""
    return {
        "stages": [s.value for s in PartnerStage],
        "tiers": TIER_LABELS,
        "ftc_disclosure_en": FTC_DISCLOSURE_TEXT_EN,
        "ftc_disclosure_ar": FTC_DISCLOSURE_TEXT_AR,
        "hard_gates": _HARD_GATES,
    }


@router.post("/lifecycle/advance")
async def lifecycle_advance(req: _StageAdvanceRequest) -> dict[str, Any]:
    """Evaluate whether a partner may move to the next lifecycle stage.

    Advisory — never executes a payout or external action.
    """
    decision = can_advance(
        from_stage=req.from_stage,
        to_stage=req.to_stage,
        fit_score=req.fit_score,
        trained=req.trained,
        has_clean_compliance=req.has_clean_compliance,
    )
    nxt = next_stage(req.from_stage)
    return {
        "allowed": decision.allowed,
        "from_stage": decision.from_stage.value,
        "to_stage": decision.to_stage.value,
        "next_stage": nxt.value if nxt else None,
        "reason_en": decision.reason_en,
        "reason_ar": decision.reason_ar,
        "hard_gates": _HARD_GATES,
    }


@router.post("/claim-scan")
async def claim_scan(req: _ClaimScanRequest) -> dict[str, Any]:
    """Scan partner-submitted marketing copy for forbidden claims.

    Flags only — never sends. Copy with forbidden claims must be
    rewritten before any human approves external use.
    """
    result = flag_forbidden_claims(req.partner_copy)
    return {
        "is_clean": result.is_clean,
        "flagged_claims": result.flagged_claims,
        "requires_review": result.requires_review,
        "reason_en": result.reason_en,
        "reason_ar": result.reason_ar,
        "ftc_disclosure_en": FTC_DISCLOSURE_TEXT_EN,
        "ftc_disclosure_ar": FTC_DISCLOSURE_TEXT_AR,
        "governance_decision": "blocked" if not result.is_clean else "allow_with_review",
        "hard_gates": _HARD_GATES,
    }


@router.post("/payout/compute")
async def payout_compute(req: _PayoutRequest) -> dict[str, Any]:
    """Compute an advisory partner commission.

    DOCTRINE — never pays out. Eligibility is False unless the deal
    invoice is paid and no duplicate/self-referral/compliance flag is
    set. Actual disbursement remains a founder-approved action.
    """
    decision = compute_payout(
        motion=req.motion,
        deal_amount_sar=req.deal_amount_sar,
        invoice_paid=req.invoice_paid,
        is_duplicate=req.is_duplicate,
        is_self_referral=req.is_self_referral,
        compliance_violation=req.compliance_violation,
        approved_pct=req.approved_pct,
    )
    return {
        "eligible": decision.eligible,
        "motion": decision.motion,
        "commission_pct": decision.commission_pct,
        "commission_sar": decision.commission_sar,
        "reason_en": decision.reason_en,
        "reason_ar": decision.reason_ar,
        "governance_decision": "approval_required" if decision.eligible else "blocked",
        "hard_gates": _HARD_GATES,
    }
