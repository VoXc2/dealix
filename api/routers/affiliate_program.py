"""Affiliate / Partner Commission Machine — API.

External affiliates/partners (consultants, creators, agencies, CRM/AI
implementers) apply, get scored, receive a referral link on approval,
submit leads, and earn CASH commissions paid only after the referred
customer's invoice is paid — with a 30-day clawback window on refunds.

Distinct from `referral_program.py` (customer referral → non-cash credit).

Doctrine:
  - Commission is gated strictly on a recorded invoice_paid event.
  - A payout settles only admin-APPROVED commissions (approval gate).
  - Affiliate disclosure is required; missing disclosure blocks commission.
  - Partner-facing assets are policy-checked for guaranteed-outcome claims.
  - Public endpoints: apply, referral submission, status, dashboard, terms,
    assets. Every mutating admin endpoint is gated by require_admin_key.

Endpoints:
  Public
    POST /api/v1/affiliates/apply
    POST /api/v1/affiliates/referrals
    GET  /api/v1/affiliates/referrals/{id}/status
    GET  /api/v1/affiliates/partners/{id}/dashboard
    GET  /api/v1/affiliates/assets
    GET  /api/v1/affiliates/_program-terms
  Admin (require_admin_key)
    GET  /api/v1/affiliates/partners
    POST /api/v1/affiliates/partners/{id}/approve | reject | suspend
    POST /api/v1/affiliates/referrals/{id}/qualify | invoice-paid
    POST /api/v1/affiliates/commissions/calculate
    POST /api/v1/affiliates/commissions/{id}/approve | clawback
    POST /api/v1/affiliates/payouts/mark-paid
    POST /api/v1/affiliates/assets
    POST /api/v1/affiliates/compliance-events
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.security.api_key import require_admin_key
from auto_client_acquisition.governance_os import policy_check_draft
from auto_client_acquisition.partnership_os import affiliate_store as store

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/affiliates", tags=["affiliates"])

_HARD_GATES = {
    "commission_only_after_invoice_paid": True,
    "clawback_window_days": store.CLAWBACK_WINDOW_DAYS,
    "payout_requires_admin_approval": True,
    "disclosure_required": True,
    "no_self_referrals": True,
    "no_duplicate_leads": True,
    "no_guaranteed_claims_in_assets": True,
}

_PARTNER_CATEGORIES = {
    "consultant",
    "creator",
    "agency",
    "implementer",
    "community",
    "newsletter",
    "podcast",
    "vc_accelerator",
    "other",
}
_CONSULTANT_OPERATOR_CATEGORIES = {"consultant", "agency", "implementer"}


# ── Request models ───────────────────────────────────────────────────


class _ScoreSignals(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audience_is_b2b: bool = False
    audience_is_gcc: bool = False
    has_prior_referrals: bool = False
    content_quality_good: bool = False
    trusted_brand: bool = False
    spam_history: bool = False
    fake_audience_suspected: bool = False


class _ApplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    display_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    partner_category: str = "other"
    audience_type: str = Field(default="", max_length=64)
    region: str = Field(default="", max_length=64)
    plan_text: str = Field(default="", max_length=2000)
    disclosure_accepted: bool = False
    signals: _ScoreSignals = Field(default_factory=_ScoreSignals)


class _SubmitReferralRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(..., min_length=8, max_length=16)
    lead_company: str = Field(..., min_length=2, max_length=255)
    lead_email: EmailStr


class _ApprovePartnerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tier: str | None = Field(default=None, pattern=r"^tier[1-4]$")


class _ReasonRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reason: str = Field(..., min_length=2, max_length=256)


class _QualifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    disclosure_present: bool


class _InvoicePaidRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    invoice_id: str = Field(..., min_length=1, max_length=64)
    deal_amount_sar: int = Field(..., gt=0, le=10_000_000)


class _CalculateCommissionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    affiliate_referral_id: str = Field(..., min_length=4, max_length=64)
    pct_override: int | None = Field(default=None, ge=0, le=20)
    flat_fee_sar: int | None = Field(default=None, ge=0, le=1_000_000)


class _MarkPayoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_id: str = Field(..., min_length=4, max_length=64)
    commission_ids: list[str] = Field(..., min_length=1, max_length=200)
    method: str = Field(default="bank_transfer", max_length=32)
    reference: str = Field(default="", max_length=128)


class _AddAssetRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: str = Field(..., pattern=r"^(post|email|banner|message)$")
    lang: str = Field(..., pattern=r"^(ar|en)$")
    body: str = Field(..., min_length=4, max_length=4000)


class _ComplianceEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    partner_id: str = Field(..., min_length=4, max_length=64)
    event_type: str = Field(..., min_length=2, max_length=64)
    severity: str = Field(default="low", pattern=r"^(low|medium|high)$")
    detail: str = Field(default="", max_length=512)


# ── Public endpoints ─────────────────────────────────────────────────


@router.get("/_program-terms")
async def program_terms() -> dict[str, Any]:
    """Public program rules — linked from the partner application page."""
    return {
        "program": "Dealix Affiliate & Partner Program",
        "tiers": {
            "tier1": {
                "name": "Affiliate Lead",
                "commission_pct": store.TIER_PCT["tier1"],
                "basis": "first paid Diagnostic",
            },
            "tier2": {
                "name": "Qualified Referral",
                "commission_pct": store.TIER_PCT["tier2"],
                "basis": "first paid deal",
            },
            "tier3": {
                "name": "Strategic Partner",
                "commission_pct": f"{store.TIER_PCT['tier3']}-{store.TIER3_MAX_PCT}",
                "basis": "first paid deal",
            },
            "tier4": {
                "name": "Implementation Partner",
                "commission_pct": "negotiated flat handoff fee",
                "basis": "per agreement",
            },
        },
        "rules": [
            "Commission is paid only after the referred customer's invoice is paid.",
            f"Refunds within {store.CLAWBACK_WINDOW_DAYS} days trigger a clawback.",
            "No commission on unqualified or duplicate leads.",
            "Self-referrals are not allowed.",
            "Partners must use Dealix-approved messaging only.",
            "Affiliate disclosure is required on every promotion.",
            "Payouts are released only after Dealix approves the commission.",
        ],
        "disclosure_required": True,
        "disclosure_text_en": (
            "Disclosure: I may receive a referral fee if you buy through "
            "this link. I only recommend Dealix for teams that need governed "
            "revenue and AI workflows."
        ),
        "disclosure_text_ar": (
            "تنويه: قد أحصل على عمولة إحالة إذا اشتركت عبر هذا الرابط. "
            "أوصي بـDealix فقط للفرق التي تحتاج تشغيل الإيراد والذكاء "
            "الاصطناعي بشكل محكوم وقابل للقياس."
        ),
        "hard_gates": _HARD_GATES,
    }


@router.post("/apply")
async def apply(body: _ApplyRequest) -> dict[str, Any]:
    """Public — an external partner applies. Scored on submission; an admin
    reviews before a referral link is issued."""
    if body.partner_category not in _PARTNER_CATEGORIES:
        raise HTTPException(status_code=422, detail="invalid partner_category")

    signals = body.signals.model_dump()
    signals["is_consultant_operator"] = (
        body.partner_category in _CONSULTANT_OPERATOR_CATEGORIES
    )
    try:
        partner = store.apply_partner(
            display_name=body.display_name,
            email=body.email,
            partner_category=body.partner_category,
            audience_type=body.audience_type,
            region=body.region,
            plan_text=body.plan_text,
            disclosure_accepted=body.disclosure_accepted,
            score_signals=signals,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {
        "status": "received_pending_review",
        "partner_id": partner.partner_id,
        "score": partner.score,
        "score_breakdown": partner.score_breakdown,
        "recommended_tier": partner.tier or "none",
        "next_step_en": (
            "Your application is under review. If approved you will receive "
            "a referral link and the approved-messaging pack."
        ),
        "next_step_ar": (
            "طلبك قيد المراجعة. عند القبول ستصلك رابط الإحالة وحزمة الرسائل "
            "المعتمدة."
        ),
        "governance_decision": "allow_with_review",
        "hard_gates": _HARD_GATES,
    }


@router.post("/referrals")
async def submit_referral(body: _SubmitReferralRequest) -> dict[str, Any]:
    """Public — a partner submits a lead via their referral code."""
    try:
        referral = store.submit_referral(
            code=body.code,
            lead_company=body.lead_company,
            lead_email=body.lead_email,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {
        "status": referral.status,
        "affiliate_referral_id": referral.affiliate_referral_id,
        "lead_company": referral.lead_company,
        "note_en": "Lead recorded. Commission depends on qualification and a paid invoice.",
        "note_ar": "تم تسجيل العميل المحتمل. العمولة مشروطة بالتأهيل ودفع الفاتورة.",
        "governance_decision": "allow",
        "hard_gates": _HARD_GATES,
    }


@router.get("/referrals/{affiliate_referral_id}/status")
async def referral_status(
    affiliate_referral_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    referral = store.get_referral(affiliate_referral_id)
    if referral is None:
        raise HTTPException(status_code=404, detail="referral_not_found")
    return {"referral": referral.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/partners/{partner_id}/dashboard")
async def partner_dashboard(
    partner_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    """Public — partner views their own dashboard (id is unguessable)."""
    data = store.partner_dashboard(partner_id)
    if data is None:
        raise HTTPException(status_code=404, detail="partner_not_found")
    return {**data, "hard_gates": _HARD_GATES}


@router.get("/assets")
async def list_assets() -> dict[str, Any]:
    """Public — approved partner-facing messaging pack."""
    return {
        "assets": [a.to_dict() for a in store.list_approved_assets(active_only=True)],
        "hard_gates": _HARD_GATES,
    }


# ── Admin endpoints ──────────────────────────────────────────────────


@router.get("/partners", dependencies=[Depends(require_admin_key)])
async def list_partners(status: str | None = None) -> dict[str, Any]:
    return {
        "partners": [p.to_dict() for p in store.list_partners(status=status)],
        "hard_gates": _HARD_GATES,
    }


@router.post(
    "/partners/{partner_id}/approve", dependencies=[Depends(require_admin_key)]
)
async def approve_partner(
    body: _ApprovePartnerRequest,
    partner_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    try:
        result = store.approve_partner(partner_id=partner_id, tier=body.tier)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if result is None:
        raise HTTPException(status_code=404, detail="partner_not_found_or_already_approved")
    partner, link = result
    return {
        "status": "approved",
        "partner": partner.to_dict(),
        "referral_code": link.code,
        "governance_decision": "allow",
        "hard_gates": _HARD_GATES,
    }


@router.post(
    "/partners/{partner_id}/reject", dependencies=[Depends(require_admin_key)]
)
async def reject_partner(
    body: _ReasonRequest,
    partner_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    partner = store.reject_partner(partner_id=partner_id, reason=body.reason)
    if partner is None:
        raise HTTPException(status_code=404, detail="partner_not_found")
    return {"status": "rejected", "partner": partner.to_dict()}


@router.post(
    "/partners/{partner_id}/suspend", dependencies=[Depends(require_admin_key)]
)
async def suspend_partner(
    body: _ReasonRequest,
    partner_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    partner = store.suspend_partner(partner_id=partner_id, reason=body.reason)
    if partner is None:
        raise HTTPException(status_code=404, detail="partner_not_found")
    return {"status": "suspended", "partner": partner.to_dict()}


@router.post(
    "/referrals/{affiliate_referral_id}/qualify",
    dependencies=[Depends(require_admin_key)],
)
async def qualify_referral(
    body: _QualifyRequest,
    affiliate_referral_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    referral = store.qualify_referral(
        affiliate_referral_id=affiliate_referral_id,
        disclosure_present=body.disclosure_present,
    )
    if referral is None:
        raise HTTPException(status_code=404, detail="referral_not_found")
    if not body.disclosure_present:
        store.log_compliance_event(
            partner_id=referral.partner_id,
            event_type="disclosure_missing",
            severity="high",
            detail=f"qualified without disclosure: {affiliate_referral_id}",
        )
    return {"status": "qualified", "referral": referral.to_dict()}


@router.post(
    "/referrals/{affiliate_referral_id}/invoice-paid",
    dependencies=[Depends(require_admin_key)],
)
async def referral_invoice_paid(
    body: _InvoicePaidRequest,
    affiliate_referral_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    """Admin — record the trusted invoice_paid signal. The only event that
    makes a commission calculable."""
    try:
        referral = store.mark_invoice_paid(
            affiliate_referral_id=affiliate_referral_id,
            invoice_id=body.invoice_id,
            deal_amount_sar=body.deal_amount_sar,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if referral is None:
        raise HTTPException(
            status_code=409,
            detail="referral_not_found_or_not_qualified",
        )
    return {"status": "invoice_paid", "referral": referral.to_dict()}


@router.post(
    "/commissions/calculate", dependencies=[Depends(require_admin_key)]
)
async def calculate_commission(
    body: _CalculateCommissionRequest,
) -> dict[str, Any]:
    try:
        commission = store.calculate_commission(
            affiliate_referral_id=body.affiliate_referral_id,
            pct_override=body.pct_override,
            flat_fee_sar=body.flat_fee_sar,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {
        "status": "calculated",
        "commission": commission.to_dict(),
        "note": "Commission must be approved before it can be paid out.",
        "governance_decision": "allow_with_review",
        "hard_gates": _HARD_GATES,
    }


@router.post(
    "/commissions/{commission_id}/approve",
    dependencies=[Depends(require_admin_key)],
)
async def approve_commission(
    commission_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    commission = store.approve_commission(commission_id=commission_id)
    if commission is None:
        raise HTTPException(
            status_code=409,
            detail="commission_not_found_or_not_in_calculated_state",
        )
    return {"status": "approved", "commission": commission.to_dict()}


@router.post(
    "/commissions/{commission_id}/clawback",
    dependencies=[Depends(require_admin_key)],
)
async def clawback_commission(
    body: _ReasonRequest,
    commission_id: str = Path(..., min_length=4, max_length=64),
) -> dict[str, Any]:
    try:
        commission = store.clawback_commission(
            commission_id=commission_id, reason=body.reason
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if commission is None:
        raise HTTPException(status_code=404, detail="commission_not_found")
    return {"status": "clawed_back", "commission": commission.to_dict()}


@router.post("/payouts/mark-paid", dependencies=[Depends(require_admin_key)])
async def mark_payout_paid(body: _MarkPayoutRequest) -> dict[str, Any]:
    """Admin — settle a payout. Only approved commissions are eligible."""
    try:
        payout = store.mark_payout_paid(
            partner_id=body.partner_id,
            commission_ids=body.commission_ids,
            method=body.method,
            reference=body.reference,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {
        "status": "paid",
        "payout": payout.to_dict(),
        "governance_decision": "allow",
        "hard_gates": _HARD_GATES,
    }


@router.post("/assets", dependencies=[Depends(require_admin_key)])
async def add_asset(body: _AddAssetRequest) -> dict[str, Any]:
    """Admin — add approved partner messaging. Policy-checked so no
    guaranteed-outcome language can enter the partner pack."""
    verdict = policy_check_draft(body.body)
    if not verdict.allowed:
        raise HTTPException(
            status_code=422,
            detail=f"asset_blocked_by_policy: {list(verdict.issues)}",
        )
    asset = store.add_approved_asset(kind=body.kind, lang=body.lang, body=body.body)
    return {"status": "added", "asset": asset.to_dict()}


@router.post(
    "/compliance-events", dependencies=[Depends(require_admin_key)]
)
async def log_compliance_event(body: _ComplianceEventRequest) -> dict[str, Any]:
    event = store.log_compliance_event(
        partner_id=body.partner_id,
        event_type=body.event_type,
        severity=body.severity,
        detail=body.detail,
    )
    return {"status": "logged", "event": event.to_dict()}
