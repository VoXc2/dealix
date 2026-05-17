"""Affiliate OS router — Dealix Full Ops Affiliate Network.

Tiered affiliate commission engine with the doctrine enforced at the
API edge:
  - a commission is computed as a DRAFT only;
  - a payout cannot be requested until the deal invoice is ``paid`` and
    the originating lead carries no disqualifying flag;
  - a payout is only confirmed after a founder ApprovalRequest is
    approved through the existing Approval Command Center;
  - a refund inside the clawback window reverses the commission;
  - every affiliate-authored message is checked for a referral
    disclosure and forbidden patterns before it can be shared.

Endpoints:
  GET  /api/v1/affiliate-os/status                              (public)
  GET  /api/v1/affiliate-os/program-terms                       (public)
  POST /api/v1/affiliate-os/apply                               (public)
  POST /api/v1/affiliate-os/compliance/check                    (public)
  POST /api/v1/affiliate-os/commission/compute                  (admin)
  GET  /api/v1/affiliate-os/commission/list                     (admin)
  GET  /api/v1/affiliate-os/commission/{commission_id}          (admin)
  POST /api/v1/affiliate-os/commission/{commission_id}/request-payout  (admin)
  POST /api/v1/affiliate-os/commission/{commission_id}/confirm-payout  (admin)
  POST /api/v1/affiliate-os/commission/{commission_id}/clawback        (admin)
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.security.api_key import require_admin_key
from auto_client_acquisition.affiliate_os import (
    DISCLOSURE_AR,
    DISCLOSURE_EN,
    AffiliateTier,
    PartnerApplication,
    apply_clawback,
    check_affiliate_message,
    commission_eligible,
    compute_commission,
    score_application,
    should_clawback,
    store,
    tier_table,
)
from auto_client_acquisition.affiliate_os.commission import CommissionStatus

router = APIRouter(prefix="/api/v1/affiliate-os", tags=["affiliate-os"])


_HARD_GATES = {
    "no_payout_before_invoice_paid": True,
    "no_payout_without_founder_approval": True,
    "clawback_on_refund_within_window": True,
    "disclosure_required_on_affiliate_messages": True,
    "no_cold_whatsapp": True,
    "no_guaranteed_outcomes": True,
    "no_commission_for_unqualified_leads": True,
}

_ANTI_ABUSE = [
    "Commission only after the deal invoice is paid.",
    "Clawback if the deal is refunded within 30 days.",
    "No self-referrals.",
    "No payout for traffic-only, duplicate, or out-of-ICP leads.",
    "No cold WhatsApp in Dealix's name.",
    "No misleading or guaranteed-outcome claims.",
    "Approved messaging only; referral disclosure is mandatory.",
]


# ── Request models ───────────────────────────────────────────────────


class _ApplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    handle: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    partner_type: str = Field(default="affiliate_marketer", max_length=60)
    audience_type: str = Field(default="unknown", max_length=20)
    audience_in_gcc: bool = False
    is_consultant_or_operator: bool = False
    previous_b2b_referrals: int = Field(default=0, ge=0, le=9999)
    content_quality_good: bool = False
    trusts_brand: bool = False
    spam_behavior: bool = False
    fake_audience_suspected: bool = False
    accepts_disclosure: bool = True
    promotion_plan_clear: bool = False


class _ComplianceCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(..., min_length=1, max_length=4000)
    channel: str = Field(default="", max_length=40)


class _ComputeCommissionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    affiliate_id: str = Field(..., min_length=1, max_length=80)
    tier: AffiliateTier
    deal_amount_sar: int = Field(..., gt=0, le=500000)
    referral_id: str = Field(default="", max_length=80)
    deal_invoice_id: str = Field(default="", max_length=80)
    invoice_status: str = Field(default="draft", max_length=20)
    lead_flags: list[str] = Field(default_factory=list)


class _RequestPayoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    requested_by: str = Field(default="founder", max_length=60)


class _ConfirmPayoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirmed_by: str = Field(default="founder", max_length=60)
    notes: str = Field(default="", max_length=500)


class _ClawbackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    invoice_status: str = Field(..., max_length=20)
    paid_at: str = Field(default="", max_length=40)
    refunded_at: str = Field(default="", max_length=40)


# ── Helpers ──────────────────────────────────────────────────────────


def _emit_evidence(*, evidence_type: Any, customer_id: str, summary: str,
                    linked: list[str] | None = None) -> str:
    """Best-effort evidence write — never fails the request."""
    try:
        from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
            create_evidence,
        )

        item = create_evidence(
            type=evidence_type,
            customer_id=customer_id,
            project_id="affiliate_os",
            summary=summary,
            linked_artifacts=linked or [],
        )
        return item.evidence_id
    except Exception:
        return ""


def _open_approval(*, object_id: str, action_type: str, risk_level: str,
                   summary_ar: str, summary_en: str,
                   proof_target: str) -> str:
    """Create a pending ApprovalRequest in the Approval Command Center."""
    from auto_client_acquisition.approval_center.approval_store import (
        get_default_approval_store,
    )
    from auto_client_acquisition.approval_center.schemas import ApprovalRequest

    req = ApprovalRequest(
        object_type="affiliate_os",
        object_id=object_id,
        action_type=action_type,
        action_mode="approval_required",
        risk_level=risk_level,
        summary_ar=summary_ar,
        summary_en=summary_en,
        proof_impact=f"affiliate_os:{action_type}",
        proof_target=proof_target,
    )
    get_default_approval_store().create(req)
    return req.approval_id


# ── Endpoints ────────────────────────────────────────────────────────


@router.get("/status")
async def affiliate_os_status() -> dict[str, Any]:
    return {
        "service": "affiliate_os",
        "module": "affiliate_os",
        "status": "operational",
        "version": "v1",
        "degraded": False,
        "guardrails": {
            "no_llm_calls": True,
            "no_external_sends": True,
            "approval_required_for_payouts": True,
        },
        "hard_gates": _HARD_GATES,
        "tiers": [t.value for t in AffiliateTier],
        "next_action_ar": "راجع /program-terms ثم استقبل الطلبات عبر /apply",
        "next_action_en": "Review /program-terms, then intake applications via /apply.",
    }


@router.get("/program-terms")
async def program_terms() -> dict[str, Any]:
    """Public affiliate program rules — linked from landing/affiliate.html."""
    return {
        "program_version": "1.0",
        "tiers": tier_table(),
        "anti_abuse": _ANTI_ABUSE,
        "disclosure_ar": DISCLOSURE_AR,
        "disclosure_en": DISCLOSURE_EN,
        "payout_rule": (
            "Commission is paid only after the deal invoice is paid and a "
            "founder approval is granted; refunds inside 30 days are clawed back."
        ),
        "hard_gates": _HARD_GATES,
    }


@router.post("/apply")
async def apply(body: _ApplyRequest) -> dict[str, Any]:
    """Public — submit a partner/affiliate application.

    The application is scored (spec §9) and ALWAYS routed to a founder
    ApprovalRequest. Registration is ``pending`` — never auto-activated.
    """
    application = PartnerApplication(
        handle=body.handle,
        audience_type=body.audience_type,
        audience_in_gcc=body.audience_in_gcc,
        is_consultant_or_operator=body.is_consultant_or_operator,
        previous_b2b_referrals=body.previous_b2b_referrals,
        content_quality_good=body.content_quality_good,
        trusts_brand=body.trusts_brand,
        spam_behavior=body.spam_behavior,
        fake_audience_suspected=body.fake_audience_suspected,
        accepts_disclosure=body.accepts_disclosure,
        promotion_plan_clear=body.promotion_plan_clear,
    )
    scored = score_application(application)

    affiliate = store.register_affiliate(
        handle=body.handle,
        email=body.email,
        partner_type=body.partner_type,
        application_score=scored.score,
        application_recommendation=scored.recommendation,
    )

    approval_id = _open_approval(
        object_id=affiliate.affiliate_id,
        action_type="affiliate_application_review",
        risk_level="medium",
        summary_ar=(
            f"طلب أفلييت جديد ({affiliate.handle}) — النتيجة {scored.score}، "
            f"التوصية: {scored.recommendation}."
        ),
        summary_en=(
            f"New affiliate application ({affiliate.handle}) — score "
            f"{scored.score}, recommendation: {scored.recommendation}."
        ),
        proof_target="affiliate_application_decision",
    )

    evidence_id = _emit_evidence(
        evidence_type="governance_decision",
        customer_id=affiliate.affiliate_id,
        summary=(
            f"Affiliate application scored {scored.score} "
            f"({scored.recommendation}); routed to approval {approval_id}."
        ),
        linked=[approval_id],
    )

    return {
        "status": "received_pending_approval",
        "affiliate_id": affiliate.affiliate_id,
        "handle": affiliate.handle,
        "application_score": scored.score,
        "recommendation": scored.recommendation,
        "score_breakdown": scored.breakdown,
        "approval_id": approval_id,
        "evidence_id": evidence_id,
        "affiliate_status": "pending",
        "next_step_en": (
            "Your application is queued for founder review. Activation is "
            "manual — no auto-acceptance."
        ),
        "governance_decision": "allow_with_review",
        "hard_gates": _HARD_GATES,
    }


@router.post("/compliance/check")
async def compliance_check(body: _ComplianceCheckRequest) -> dict[str, Any]:
    """Public — check an affiliate-authored message for compliance."""
    result = check_affiliate_message(body.text, channel=body.channel)
    return {
        "compliant": result.compliant,
        "has_disclosure": result.has_disclosure,
        "violations": result.violations,
        "notes_ar": result.notes_ar,
        "notes_en": result.notes_en,
        "disclosure_ar": DISCLOSURE_AR,
        "disclosure_en": DISCLOSURE_EN,
    }


@router.post("/commission/compute", dependencies=[Depends(require_admin_key)])
async def commission_compute(body: _ComputeCommissionRequest) -> dict[str, Any]:
    """Admin — compute a DRAFT commission and persist it.

    Sets status ``eligible`` only when the deal invoice is paid and the
    lead is clean; ``void`` when the lead is disqualified; otherwise
    ``pending``. Never pays anything.
    """
    try:
        commission = compute_commission(
            affiliate_id=body.affiliate_id,
            tier=body.tier,
            deal_amount_sar=body.deal_amount_sar,
            referral_id=body.referral_id,
            deal_invoice_id=body.deal_invoice_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    eligible, reasons = commission_eligible(
        invoice_status=body.invoice_status,
        lead_flags=body.lead_flags,
    )
    commission.eligibility_reasons = list(reasons)
    if any(r.startswith("disallowed_lead:") for r in reasons):
        commission.status = CommissionStatus.VOID.value
    elif eligible:
        commission.status = CommissionStatus.ELIGIBLE.value
    else:
        commission.status = CommissionStatus.PENDING.value

    store.save_commission(commission)
    _emit_evidence(
        evidence_type="value",
        customer_id=commission.affiliate_id,
        summary=(
            f"Commission {commission.commission_id} computed: "
            f"{commission.amount_sar} SAR ({commission.tier}), "
            f"status={commission.status}."
        ),
        linked=[commission.deal_invoice_id] if commission.deal_invoice_id else [],
    )
    return {
        "commission": commission.to_dict(),
        "eligible_for_payout_request": eligible,
        "eligibility_reasons": list(reasons),
        "hard_gates": _HARD_GATES,
    }


@router.get("/commission/list", dependencies=[Depends(require_admin_key)])
async def commission_list(
    status: str | None = None,
    affiliate_id: str | None = None,
) -> dict[str, Any]:
    """Admin — list commissions, optionally filtered by status/affiliate."""
    rows = store.list_commissions(status=status, affiliate_id=affiliate_id)
    total_owed = sum(
        c.amount_sar
        for c in rows
        if c.status in (
            CommissionStatus.ELIGIBLE.value,
            CommissionStatus.PAYOUT_REQUESTED.value,
        )
    )
    return {
        "count": len(rows),
        "total_owed_sar": round(total_owed, 2),
        "commissions": [c.to_dict() for c in rows],
    }


@router.get("/commission/{commission_id}", dependencies=[Depends(require_admin_key)])
async def commission_get(
    commission_id: str = Path(..., max_length=80),
) -> dict[str, Any]:
    """Admin — fetch a single commission."""
    commission = store.get_commission(commission_id)
    if commission is None:
        raise HTTPException(status_code=404, detail="commission_not_found")
    return {"commission": commission.to_dict()}


@router.post(
    "/commission/{commission_id}/request-payout",
    dependencies=[Depends(require_admin_key)],
)
async def commission_request_payout(
    body: _RequestPayoutRequest,
    commission_id: str = Path(..., max_length=80),
) -> dict[str, Any]:
    """Admin — open a founder ApprovalRequest for a commission payout.

    Refuses unless the commission is ``eligible`` (invoice paid + clean
    lead). Does NOT pay — it only queues the approval.
    """
    commission = store.get_commission(commission_id)
    if commission is None:
        raise HTTPException(status_code=404, detail="commission_not_found")
    if commission.status != CommissionStatus.ELIGIBLE.value:
        raise HTTPException(
            status_code=409,
            detail=(
                f"commission status is {commission.status!r}; only "
                "'eligible' commissions can request a payout"
            ),
        )

    approval_id = _open_approval(
        object_id=commission.commission_id,
        action_type="affiliate_payout",
        risk_level="high",
        summary_ar=(
            f"طلب صرف عمولة أفلييت {commission.amount_sar} ريال "
            f"({commission.tier}) للمحيل {commission.affiliate_id}."
        ),
        summary_en=(
            f"Affiliate payout request: {commission.amount_sar} SAR "
            f"({commission.tier}) for affiliate {commission.affiliate_id}."
        ),
        proof_target="affiliate_payout_confirmation",
    )
    updated = store.update_commission(
        commission_id,
        status=CommissionStatus.PAYOUT_REQUESTED.value,
        approval_id=approval_id,
    )
    _emit_evidence(
        evidence_type="approval",
        customer_id=commission.affiliate_id,
        summary=(
            f"Payout requested for commission {commission_id}; "
            f"approval {approval_id} opened by {body.requested_by}."
        ),
        linked=[approval_id],
    )
    return {
        "status": "payout_requested",
        "commission": (updated or commission).to_dict(),
        "approval_id": approval_id,
        "next_step_en": (
            f"Founder must approve {approval_id} via "
            "/api/v1/approvals before the payout can be confirmed."
        ),
        "governance_decision": "approval_required",
        "hard_gates": _HARD_GATES,
    }


@router.post(
    "/commission/{commission_id}/confirm-payout",
    dependencies=[Depends(require_admin_key)],
)
async def commission_confirm_payout(
    body: _ConfirmPayoutRequest,
    commission_id: str = Path(..., max_length=80),
) -> dict[str, Any]:
    """Admin — confirm a payout AFTER its ApprovalRequest is approved.

    Reads the linked ApprovalRequest from the Approval Command Center
    and refuses unless it is in ``approved`` status.
    """
    from auto_client_acquisition.approval_center.approval_store import (
        get_default_approval_store,
    )
    from auto_client_acquisition.approval_center.schemas import ApprovalStatus

    commission = store.get_commission(commission_id)
    if commission is None:
        raise HTTPException(status_code=404, detail="commission_not_found")
    if commission.status != CommissionStatus.PAYOUT_REQUESTED.value:
        raise HTTPException(
            status_code=409,
            detail=(
                f"commission status is {commission.status!r}; only "
                "'payout_requested' commissions can be confirmed"
            ),
        )
    if not commission.approval_id:
        raise HTTPException(status_code=409, detail="commission has no approval_id")

    approval = get_default_approval_store().get(commission.approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="linked_approval_not_found")
    if ApprovalStatus(approval.status) != ApprovalStatus.APPROVED:
        raise HTTPException(
            status_code=409,
            detail=(
                f"approval {commission.approval_id} is "
                f"{ApprovalStatus(approval.status).value}; payout needs an "
                "approved request"
            ),
        )

    payout = store.record_payout(
        commission_id=commission.commission_id,
        affiliate_id=commission.affiliate_id,
        amount_sar=commission.amount_sar,
        approval_id=commission.approval_id,
        notes=body.notes,
    )
    updated = store.update_commission(
        commission_id,
        status=CommissionStatus.PAID.value,
    )
    _emit_evidence(
        evidence_type="output",
        customer_id=commission.affiliate_id,
        summary=(
            f"Affiliate payout {payout.payout_id} confirmed: "
            f"{payout.amount_sar} SAR for commission {commission_id} "
            f"by {body.confirmed_by} (approval {commission.approval_id})."
        ),
        linked=[payout.payout_id, commission.approval_id],
    )
    return {
        "status": "paid",
        "commission": (updated or commission).to_dict(),
        "payout": payout.to_dict(),
        "governance_decision": "allow",
    }


@router.post(
    "/commission/{commission_id}/clawback",
    dependencies=[Depends(require_admin_key)],
)
async def commission_clawback(
    body: _ClawbackRequest,
    commission_id: str = Path(..., max_length=80),
) -> dict[str, Any]:
    """Admin — reverse a commission when the deal is refunded in-window."""
    commission = store.get_commission(commission_id)
    if commission is None:
        raise HTTPException(status_code=404, detail="commission_not_found")

    must_clawback = should_clawback(
        invoice_status=body.invoice_status,
        paid_at=body.paid_at,
        refunded_at=body.refunded_at,
    )
    if not must_clawback:
        return {
            "status": "no_clawback",
            "commission": commission.to_dict(),
            "reason_en": (
                "Invoice is not refunded, or the refund is outside the "
                "30-day clawback window."
            ),
        }

    clawed = apply_clawback(commission)
    updated = store.update_commission(
        commission_id,
        status=clawed.status,
        notes=f"{commission.notes} | clawed_back:refund_in_window".strip(" |"),
    )
    _emit_evidence(
        evidence_type="governance_decision",
        customer_id=commission.affiliate_id,
        summary=(
            f"Commission {commission_id} clawed back — deal refunded "
            f"inside the 30-day window."
        ),
        linked=[commission.deal_invoice_id] if commission.deal_invoice_id else [],
    )
    return {
        "status": "clawed_back",
        "commission": (updated or clawed).to_dict(),
        "governance_decision": "allow",
        "hard_gates": _HARD_GATES,
    }
