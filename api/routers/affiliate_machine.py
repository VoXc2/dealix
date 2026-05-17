"""Affiliate & Partner machine — public + ops + portal API.

Thin HTTP layer over ``partnership_os``:
  - ``tiers`` / ``commission_engine`` — money rules;
  - ``partner_scoring`` — application scoring;
  - ``compliance_guard`` — doctrine refusal of cold channels + claims;
  - ``approved_assets`` — AR/EN messaging library;
  - ``affiliate_store`` — JSONL persistence (DEALIX_AFFILIATE_*_PATH).

Doctrine enforced here:
  - partner approval + payout mark-paid queue an ``ApprovalRequest`` —
    never auto-acted (non-negotiable #8);
  - disclosure must be accepted before a partner can be activated;
  - contact emails are stored HASHED only (non-negotiable #6);
  - self-referrals, unqualified / out-of-ICP / consent-less and
    not-yet-paid deals never yield a commission;
  - clawbacks and payout disputes emit a ``friction_log`` event;
  - every response carries a ``hard_gates`` dict + ``governance_decision``.
"""

from __future__ import annotations

import secrets
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.security.api_key import require_admin_key
from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    get_default_approval_store,
    render_approval_card,
)
from auto_client_acquisition.friction_log.store import emit as friction_emit
from auto_client_acquisition.partnership_os import affiliate_store as store
from auto_client_acquisition.partnership_os import approved_assets
from auto_client_acquisition.partnership_os import commission_engine
from auto_client_acquisition.partnership_os import compliance_guard
from auto_client_acquisition.partnership_os.partner_scoring import score_partner
from auto_client_acquisition.partnership_os.tiers import VALID_TIERS, ladder_summary

router = APIRouter(prefix="/api/v1", tags=["affiliate-machine"])

# Hard gates surfaced on every response — a stable, auditable contract.
_HARD_GATES: dict[str, bool] = {
    "approval_required_for_partner_activation": True,
    "approval_required_for_payout": True,
    "disclosure_required_to_activate": True,
    "contact_email_stored_hashed_only": True,
    "no_commission_before_invoice_paid": True,
    "no_self_referral_commission": True,
    "no_cold_whatsapp_linkedin_scraping": True,
}


def _envelope(payload: dict[str, Any], decision: str) -> dict[str, Any]:
    """Wrap a payload with the mandatory governance fields."""
    return {**payload, "hard_gates": dict(_HARD_GATES), "governance_decision": decision}


# ── Request models ──────────────────────────────────────────────────


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PartnerApplyRequest(_Strict):
    company_name: str = Field(..., min_length=2, max_length=255)
    contact_name: str = Field(..., min_length=2, max_length=255)
    contact_email: EmailStr
    country: str = Field(..., min_length=2, max_length=64)
    audience_type: str = Field(..., min_length=2, max_length=64)
    audience_size: int = Field(0, ge=0)
    main_channel: str = Field(..., min_length=2, max_length=64)
    plan: str = Field("", max_length=2000)
    prior_referrals: int = Field(0, ge=0)
    content_quality: bool = False
    trusted_brand: bool = False
    disclosure_accepted: bool = False


class PartnerApproveRequest(_Strict):
    approver: str = Field(..., min_length=2, max_length=64)
    tier: str = Field(..., min_length=2, max_length=32)


class LinkRequest(_Strict):
    utm_source: str = Field("", max_length=64)
    utm_medium: str = Field("", max_length=64)
    utm_campaign: str = Field("", max_length=64)
    target_url: str = Field("https://dealix.me", max_length=512)


class ReferralRequest(_Strict):
    contact_email: EmailStr
    lead_id: str = Field("", max_length=64)
    link_id: str = Field("", max_length=64)
    tier: str = Field("affiliate_lead", min_length=2, max_length=32)


class CommissionCalcRequest(_Strict):
    referral_id: str = Field(..., min_length=2, max_length=64)
    deal_id: str = Field(..., min_length=2, max_length=64)
    amount_sar: float = Field(..., gt=0)
    invoice_paid: bool = False
    invoice_paid_at: str = Field("", max_length=64)
    tier: str = Field("", max_length=32)
    in_icp: bool = True
    duplicate: bool = False
    consent: bool = True


class ClawbackRequest(_Strict):
    refund_date: str = Field(..., min_length=4, max_length=64)
    notes: str = Field("", max_length=500)


class PayoutBuildRequest(_Strict):
    partner_id: str = Field(..., min_length=2, max_length=64)
    period: str = Field(..., min_length=4, max_length=16)


class PayoutMarkPaidRequest(_Strict):
    payout_id: str = Field(..., min_length=2, max_length=64)
    partner_invoice_ref: str = Field(..., min_length=2, max_length=128)
    marked_by: str = Field(..., min_length=2, max_length=64)
    disputed: bool = False
    dispute_notes: str = Field("", max_length=500)


class ComplianceEventRequest(_Strict):
    kind: str = Field(..., min_length=2, max_length=32)
    severity: str = Field("low", max_length=16)
    evidence_ref: str = Field("", max_length=255)
    notes: str = Field("", max_length=500)


# ── Helpers ─────────────────────────────────────────────────────────


def _get_partner_or_404(partner_id: str) -> dict[str, Any]:
    partner = store.get("partners", partner_id)
    if partner is None:
        raise HTTPException(status_code=404, detail="partner_not_found")
    return partner


def _referral_code(company_name: str) -> str:
    slug = "".join(c for c in company_name.upper() if c.isalnum())[:6] or "DLX"
    return f"{slug}-{secrets.token_hex(3).upper()}"


# ── Public endpoints ────────────────────────────────────────────────


@router.get("/affiliate/tiers")
async def affiliate_tiers() -> dict[str, Any]:
    """Public — the unified 4-tier commission ladder."""
    return _envelope({"tiers": ladder_summary()}, "allow")


@router.get("/affiliate/approved-assets")
async def affiliate_approved_assets(
    locale: str | None = None, asset_type: str | None = None
) -> dict[str, Any]:
    """Public — approved AR/EN messaging library partners may use verbatim."""
    return _envelope(
        {
            "assets": approved_assets.list_assets(
                locale=locale, asset_type=asset_type
            ),
            "disclosure_mandatory": True,
        },
        "allow",
    )


@router.post("/public/partner-apply")
async def partner_apply(body: PartnerApplyRequest) -> dict[str, Any]:
    """Public — submit a partner application.

    Creates a ``prospecting`` partner, scores the application, and refuses
    any go-to-market plan that proposes cold WhatsApp / LinkedIn
    automation / scraping (non-negotiables #1-3).
    """
    scan = compliance_guard.scan_recruitment_request(body.plan)
    if not scan.ok:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "recruitment_plan_violates_doctrine",
                "violations": [v.to_dict() for v in scan.violations],
                "governance_decision": "block",
            },
        )

    app_dict = body.model_dump()
    score = score_partner(app_dict)

    partner_id = store.new_id("ptn")
    now = store.now_iso()
    partner = {
        "id": partner_id,
        "company_name": body.company_name,
        "partner_type": "REFERRAL",
        "contact_name": body.contact_name,
        "contact_email_hash": store.hash_email(body.contact_email),
        "country": body.country,
        "audience_type": body.audience_type,
        "audience_size": body.audience_size,
        "main_channel": body.main_channel,
        "status": "prospecting",
        "partner_score": score.score,
        "score_recommendation": score.recommendation,
        "tier": None,
        "referral_code": None,
        "disclosure_accepted": body.disclosure_accepted,
        "applied_at": now,
        "approved_at": None,
        "approved_by": None,
        "created_at": now,
        "deleted_at": None,
    }
    store.insert("partners", partner)

    return _envelope(
        {
            "status": "application_received",
            "partner_id": partner_id,
            "score": score.to_dict(),
            "next_step": "Dealix reviews the application; activation queues "
            "a human ApprovalRequest before any partner goes live.",
        },
        "allow_with_review",
    )


# ── Ops endpoints (admin-gated) ─────────────────────────────────────


@router.post("/partners/{partner_id}/approve")
async def approve_partner(
    body: PartnerApproveRequest,
    partner_id: str = Path(..., max_length=64),
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — queue partner activation as a human ApprovalRequest.

    Does NOT auto-activate (non-negotiable #8). Disclosure must already
    be accepted. On approval through the Approval Center the caller
    completes activation via ``/partners/{id}/activate``.
    """
    partner = _get_partner_or_404(partner_id)
    if body.tier not in VALID_TIERS:
        raise HTTPException(status_code=422, detail=f"unknown_tier:{body.tier}")
    if not bool(partner.get("disclosure_accepted")):
        raise HTTPException(
            status_code=422,
            detail={
                "error": "disclosure_not_accepted",
                "message": "partner must accept the mandatory disclosure "
                "before activation can be queued",
                "governance_decision": "block",
            },
        )

    req = ApprovalRequest(
        object_type="partner",
        object_id=partner_id,
        action_type="partner_intro",
        action_mode="approval_required",
        risk_level="medium",
        summary_en=f"Activate affiliate partner {partner.get('company_name')} "
        f"at tier {body.tier}",
        summary_ar=f"تفعيل شريك الإحالة {partner.get('company_name')} "
        f"على المستوى {body.tier}",
        proof_impact="partner_activated",
    )
    get_default_approval_store().create(req)
    store.update("partners", partner_id, {"tier": body.tier, "status": "pending_activation"})

    return _envelope(
        {
            "status": "approval_queued",
            "partner_id": partner_id,
            "approval": render_approval_card(req),
            "note": "Partner is NOT active. Approve in the Approval Center, "
            "then call /partners/{id}/activate.",
        },
        "require_approval",
    )


@router.post("/partners/{partner_id}/activate")
async def activate_partner(
    partner_id: str = Path(..., max_length=64),
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — complete activation after the ApprovalRequest is approved.

    Generates the referral code + a default tracked link. Refuses if the
    partner's approval is still pending (non-negotiable #8) or if the
    disclosure was never accepted.
    """
    partner = _get_partner_or_404(partner_id)
    if not bool(partner.get("disclosure_accepted")):
        raise HTTPException(status_code=422, detail="disclosure_not_accepted")

    pending = [
        r
        for r in get_default_approval_store().list_pending()
        if r.object_type == "partner" and r.object_id == partner_id
    ]
    if pending:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "approval_still_pending",
                "message": "partner activation is awaiting human approval",
                "governance_decision": "require_approval",
            },
        )

    code = partner.get("referral_code") or _referral_code(partner["company_name"])
    now = store.now_iso()
    store.update(
        "partners",
        partner_id,
        {
            "status": "active",
            "referral_code": code,
            "approved_at": now,
            "approved_by": "approval_center",
        },
    )
    link_id = store.new_id("lnk")
    link = {
        "id": link_id,
        "partner_id": partner_id,
        "code": code,
        "utm_source": "partner",
        "utm_medium": "referral",
        "utm_campaign": "default",
        "target_url": "https://dealix.me",
        "clicks": 0,
        "created_at": now,
        "deleted_at": None,
    }
    store.insert("links", link)

    return _envelope(
        {
            "status": "activated",
            "partner_id": partner_id,
            "referral_code": code,
            "default_link_id": link_id,
        },
        "allow",
    )


@router.post("/partners/{partner_id}/links")
async def create_link(
    body: LinkRequest,
    partner_id: str = Path(..., max_length=64),
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — create a tracked referral link for an active partner."""
    partner = _get_partner_or_404(partner_id)
    if partner.get("status") != "active":
        raise HTTPException(status_code=409, detail="partner_not_active")

    link_id = store.new_id("lnk")
    link = {
        "id": link_id,
        "partner_id": partner_id,
        "code": partner.get("referral_code") or "",
        "utm_source": body.utm_source or "partner",
        "utm_medium": body.utm_medium or "referral",
        "utm_campaign": body.utm_campaign or "default",
        "target_url": body.target_url,
        "clicks": 0,
        "created_at": store.now_iso(),
        "deleted_at": None,
    }
    store.insert("links", link)
    return _envelope({"status": "created", "link": link}, "allow")


@router.post("/partners/{partner_id}/referrals")
async def log_referral(
    body: ReferralRequest,
    partner_id: str = Path(..., max_length=64),
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — log a referral attributed to a partner.

    Rejects self-referrals: a referral whose contact email hash matches
    the partner's own contact email hash earns no commission.
    """
    partner = _get_partner_or_404(partner_id)
    if body.tier not in VALID_TIERS:
        raise HTTPException(status_code=422, detail=f"unknown_tier:{body.tier}")

    email_hash = store.hash_email(body.contact_email)
    if email_hash == partner.get("contact_email_hash"):
        raise HTTPException(
            status_code=422,
            detail={
                "error": "self_referral_rejected",
                "message": "a partner cannot refer themselves",
                "governance_decision": "block",
            },
        )

    referral_id = store.new_id("ref")
    referral = {
        "id": referral_id,
        "partner_id": partner_id,
        "link_id": body.link_id or None,
        "lead_id": body.lead_id or None,
        "deal_id": None,
        "contact_email_hash": email_hash,
        "stage": "submitted",
        "qualified": False,
        "tier": body.tier,
        "self_referral": False,
        "created_at": store.now_iso(),
        "deleted_at": None,
    }
    store.insert("referrals", referral)
    return _envelope({"status": "logged", "referral": referral}, "allow")


@router.post("/referrals/{referral_id}/qualify")
async def qualify_referral(
    referral_id: str = Path(..., max_length=64),
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — mark a referral as qualified (decision-maker meeting booked)."""
    referral = store.get("referrals", referral_id)
    if referral is None:
        raise HTTPException(status_code=404, detail="referral_not_found")
    updated = store.update(
        "referrals", referral_id, {"qualified": True, "stage": "qualified"}
    )
    return _envelope({"status": "qualified", "referral": updated}, "allow")


@router.post("/commissions/calculate")
async def calculate_commission(
    body: CommissionCalcRequest,
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — calculate a commission for a paid deal.

    Refuses (HTTP 422) when the invoice is not yet paid, the referral is
    a self-referral, the lead is out-of-ICP / duplicate / consent-less,
    or the tier requires a qualified referral that is not qualified.
    """
    referral = store.get("referrals", body.referral_id)
    if referral is None:
        raise HTTPException(status_code=404, detail="referral_not_found")

    deal = {
        "id": body.deal_id,
        "invoice_paid": body.invoice_paid,
        "invoice_paid_at": body.invoice_paid_at,
        "amount_sar": body.amount_sar,
        "tier": body.tier or referral.get("tier"),
        "in_icp": body.in_icp,
        "duplicate": body.duplicate,
    }
    referral_view = {**referral, "consent": body.consent}
    try:
        line = commission_engine.calculate(referral_view, deal)
    except commission_engine.CommissionRefused as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "commission_refused",
                "reason": str(exc),
                "governance_decision": "block",
            },
        ) from exc

    record = line.to_dict()
    record["deleted_at"] = None
    store.insert("commissions", record)
    store.update("referrals", body.referral_id, {"deal_id": body.deal_id, "stage": "won"})
    return _envelope({"status": "calculated", "commission": record}, "allow")


@router.post("/commissions/{commission_id}/clawback")
async def clawback_commission(
    body: ClawbackRequest,
    commission_id: str = Path(..., max_length=64),
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — apply a refund clawback to a commission.

    Voids the commission if the refund falls inside the 30-day window.
    Emits a ``friction_log`` event in all cases (the refund itself is
    operational friction worth tracking).
    """
    commission = store.get("commissions", commission_id)
    if commission is None:
        raise HTTPException(status_code=404, detail="commission_not_found")

    patch = commission_engine.clawback(commission, body.refund_date)
    updated = store.update("commissions", commission_id, patch)

    friction_emit(
        customer_id=str(commission.get("deal_id") or commission_id),
        kind="manual_override",
        severity="med" if patch["clawed_back"] else "low",
        workflow_id="affiliate_clawback",
        evidence_ref=commission_id,
        notes=f"commission clawback: {patch['reason']}; {body.notes}",
    )
    return _envelope(
        {"status": "clawback_processed", "commission": updated, "result": patch},
        "allow_with_review",
    )


@router.post("/payouts/build")
async def build_payout(
    body: PayoutBuildRequest,
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — batch a partner's eligible commissions into a payout."""
    _get_partner_or_404(body.partner_id)
    commissions = [
        c
        for c in store.list_records("commissions", partner_id=body.partner_id)
        if c.get("status") == "eligible"
    ]
    if not commissions:
        raise HTTPException(status_code=409, detail="no_eligible_commissions")

    total = round(sum(float(c.get("amount_sar") or 0.0) for c in commissions), 2)
    payout_id = store.new_id("pay")
    payout = {
        "id": payout_id,
        "partner_id": body.partner_id,
        "period": body.period,
        "commission_ids": [c["id"] for c in commissions],
        "total_sar": total,
        "status": "pending",
        "partner_invoice_ref": None,
        "marked_paid_at": None,
        "marked_paid_by": None,
        "created_at": store.now_iso(),
        "deleted_at": None,
    }
    store.insert("payouts", payout)
    for c in commissions:
        store.update("commissions", c["id"], {"status": "approved"})

    return _envelope(
        {"status": "payout_built", "payout": payout, "commission_count": len(commissions)},
        "allow",
    )


@router.post("/payouts/mark-paid")
async def mark_payout_paid(
    body: PayoutMarkPaidRequest,
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — queue a payout 'mark paid' as a human ApprovalRequest.

    Money out of the door is never auto-acted (non-negotiable #8).
    Requires ``partner_invoice_ref``. A disputed payout emits a
    ``friction_log`` event.
    """
    payout = store.get("payouts", body.payout_id)
    if payout is None:
        raise HTTPException(status_code=404, detail="payout_not_found")

    if body.disputed:
        friction_emit(
            customer_id=str(payout.get("partner_id") or body.payout_id),
            kind="support_ticket",
            severity="high",
            workflow_id="affiliate_payout_dispute",
            evidence_ref=body.payout_id,
            notes=f"payout dispute: {body.dispute_notes}",
        )

    req = ApprovalRequest(
        object_type="payout",
        object_id=body.payout_id,
        action_type="payment_reminder",
        action_mode="approval_required",
        risk_level="high",
        summary_en=f"Mark partner payout {body.payout_id} as paid "
        f"({payout.get('total_sar')} SAR, invoice {body.partner_invoice_ref})",
        summary_ar=f"تأكيد دفع عمولة الشريك {body.payout_id} "
        f"({payout.get('total_sar')} ريال)",
        proof_impact="partner_paid",
    )
    get_default_approval_store().create(req)
    store.update(
        "payouts",
        body.payout_id,
        {
            "status": "awaiting_approval",
            "partner_invoice_ref": body.partner_invoice_ref,
            "marked_paid_by": body.marked_by,
        },
    )
    return _envelope(
        {
            "status": "approval_queued",
            "payout_id": body.payout_id,
            "approval": render_approval_card(req),
            "note": "Payout is NOT paid. A human must approve in the "
            "Approval Center.",
        },
        "require_approval",
    )


@router.post("/partners/{partner_id}/compliance-event")
async def record_compliance_event(
    body: ComplianceEventRequest,
    partner_id: str = Path(..., max_length=64),
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — record a compliance flag against a partner."""
    _get_partner_or_404(partner_id)
    event_id = store.new_id("cpe")
    event = {
        "id": event_id,
        "partner_id": partner_id,
        "kind": body.kind,
        "severity": body.severity,
        "evidence_ref": body.evidence_ref or None,
        "notes": body.notes or None,
        "created_at": store.now_iso(),
        "deleted_at": None,
    }
    store.insert("compliance", event)
    return _envelope({"status": "recorded", "event": event}, "allow_with_review")


@router.get("/ops/partners/dashboard")
async def partners_dashboard(
    _admin: None = Depends(require_admin_key),
) -> dict[str, Any]:
    """Ops — affiliate machine dashboard."""
    partners = store.list_records("partners")
    referrals = store.list_records("referrals")
    commissions = store.list_records("commissions")
    compliance = store.list_records("compliance")

    active = [p for p in partners if p.get("status") == "active"]
    qualified = [r for r in referrals if r.get("qualified")]
    commission_due = round(
        sum(
            float(c.get("amount_sar") or 0.0)
            for c in commissions
            if c.get("status") in {"eligible", "approved"}
        ),
        2,
    )
    sourced_revenue = round(
        sum(float(c.get("basis_amount_sar") or 0.0) for c in commissions), 2
    )
    return _envelope(
        {
            "active_partners": len(active),
            "total_partners": len(partners),
            "referrals_submitted": len(referrals),
            "referrals_qualified": len(qualified),
            "partner_sourced_revenue_sar": sourced_revenue,
            "commission_due_sar": commission_due,
            "compliance_flags": len(compliance),
        },
        "allow",
    )


# ── Partner portal ──────────────────────────────────────────────────


@router.get("/partner/{partner_id}/portal")
async def partner_portal(
    partner_id: str = Path(..., max_length=64),
) -> dict[str, Any]:
    """Partner portal — referral link, assets, referrals, commission, rules."""
    partner = _get_partner_or_404(partner_id)
    links = store.list_records("links", partner_id=partner_id)
    referrals = store.list_records("referrals", partner_id=partner_id)
    commissions = store.list_records("commissions", partner_id=partner_id)
    payouts = store.list_records("payouts", partner_id=partner_id)

    earned = round(
        sum(
            float(c.get("amount_sar") or 0.0)
            for c in commissions
            if c.get("status") != "clawed_back"
        ),
        2,
    )
    return _envelope(
        {
            "partner": {
                "id": partner_id,
                "company_name": partner.get("company_name"),
                "status": partner.get("status"),
                "tier": partner.get("tier"),
                "referral_code": partner.get("referral_code"),
            },
            "links": links,
            "referrals_submitted": len(referrals),
            "referrals_qualified": sum(1 for r in referrals if r.get("qualified")),
            "commission_earned_sar": earned,
            "payouts": [
                {"id": p["id"], "period": p.get("period"), "status": p.get("status"),
                 "total_sar": p.get("total_sar")}
                for p in payouts
            ],
            "approved_assets": approved_assets.list_assets(),
            "compliance_rules": [
                "Always show the mandatory paid-referral disclosure.",
                "No guaranteed ROI / revenue / compliance claims.",
                "No cold WhatsApp, LinkedIn automation, or scraping.",
                "No self-referrals — they earn no commission.",
            ],
        },
        "allow",
    )


__all__ = ["router"]
