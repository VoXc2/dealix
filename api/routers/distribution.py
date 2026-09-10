"""Distribution API — the Revenue Execution OS surface (approval-first).

Every response carries a ``governance_decision``. There is deliberately NO
endpoint that sends an external message or charges a customer: drafts are
approved/copied manually, proposals are quote-evidence-bound, and
``payments/handoff`` only records a founder-controlled step.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.distribution_os import (
    catalog,
    draft_factory,
    followup,
    metrics,
    payment_handoff,
    proof_pack,
    proposal,
    prospect,
    renewal,
    win_loss,
)
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision

router = APIRouter(prefix="/api/v1/distribution", tags=["distribution"])

_ALLOW = GovernanceDecision.ALLOW.value


def _ok(payload: dict[str, Any], decision: str = _ALLOW) -> dict[str, Any]:
    payload["governance_decision"] = decision
    return payload


class ProspectBody(BaseModel):
    company: str = Field(..., min_length=1)
    sector: str = ""
    region: str = ""
    source: str = ""
    decision_maker: str = ""
    pain_hypothesis: str = ""
    offer_angle: str = ""
    estimated_value_sar: int = 0
    preferred_channel: str = "email"
    risk: str = "medium"
    evidence_level: int = 0


class GenerateDraftBody(BaseModel):
    prospect_id: str = Field(..., min_length=1)
    draft_type: str = "outreach_first"
    channel: str | None = None
    locale: str = "ar"


class GenerateProposalBody(BaseModel):
    prospect_id: str = Field(..., min_length=1)
    product_id: str = Field(..., min_length=1)
    sector: str = ""
    problem: str = ""
    proposed_solution: str = ""
    scope: list[str] = Field(default_factory=list)
    out_of_scope: list[str] = Field(..., min_length=1)
    timeline: str = ""
    discovery_ref: str = ""
    quote_id: str = ""
    customer_specific_quote_sar: float | None = Field(default=None, gt=0)
    evidence_level: int = 0


class GenerateProofPackBody(BaseModel):
    customer_id: str = Field(..., min_length=1)
    current_process: str = ""
    leakage_points: list[str] = Field(default_factory=list)
    quick_win: str = ""
    before_after: str = ""
    measurement_method: str = ""
    evidence_level: int = 0
    recommended_pilot: str = ""


class PaymentHandoffBody(BaseModel):
    """Public/internal API input for a payment handoff request.

    Approval truth is intentionally NOT an input. The caller must reference an
    existing approved proposal and the Approval Center quote authority that
    commits to the exact customer, amount, discovery, and scope fingerprint.
    Caller-supplied approval flags remain forbidden.
    """

    model_config = ConfigDict(extra="forbid")

    proposal_id: str = Field(..., min_length=1)
    customer_id: str = ""
    product_id: str = Field(..., min_length=1)
    discovery_ref: str = Field(..., min_length=1)
    quote_id: str = Field(..., min_length=1)
    quote_authority_ref: str = Field(..., min_length=1)
    customer_specific_scope_ref: str = Field(..., min_length=1)
    amount_sar: float = Field(..., gt=0)
    notes: str = ""


@router.get("/overview")
async def overview() -> dict[str, Any]:
    return _ok({"metrics": metrics.daily_kpis(), "ladder": catalog.ladder_summary()})


@router.get("/catalog")
async def get_catalog() -> dict[str, Any]:
    return _ok({"ladder": catalog.ladder_summary()})


@router.get("/metrics")
async def get_metrics() -> dict[str, Any]:
    return _ok({"snapshot": metrics.snapshot()})


@router.get("/prospects")
async def list_prospects(status: str | None = Query(None)) -> dict[str, Any]:
    rows = prospect.list_prospects(status=status)
    return _ok({"count": len(rows), "prospects": [p.to_dict() for p in rows]})


@router.post("/prospects")
async def add_prospect(body: ProspectBody) -> dict[str, Any]:
    try:
        p = prospect.add_prospect(**body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    q = prospect.qualify(p)
    return _ok({"prospect": p.to_dict(), "qualified": q.qualified, "reasons": list(q.reasons)})


@router.get("/drafts")
async def list_drafts(status: str | None = Query(None)) -> dict[str, Any]:
    rows = draft_factory.list_drafts(status=status)
    return _ok({"count": len(rows), "drafts": [d.to_dict() for d in rows]})


@router.post("/drafts/generate")
async def generate_draft(body: GenerateDraftBody) -> dict[str, Any]:
    p = prospect.get_prospect(body.prospect_id)
    if p is None:
        raise HTTPException(status_code=404, detail=f"unknown prospect {body.prospect_id}")
    try:
        d = draft_factory.generate_draft(
            prospect=p, draft_type=body.draft_type, channel=body.channel, locale=body.locale
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    decision = GovernanceDecision.BLOCK.value if d.governance_status == "blocked" else _ALLOW
    return _ok({"draft": d.to_dict()}, decision)


@router.post("/drafts/{draft_id}/approve")
async def approve_draft(draft_id: str) -> dict[str, Any]:
    try:
        d = draft_factory.approve_draft(draft_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    if d is None:
        raise HTTPException(status_code=404, detail=f"unknown draft {draft_id}")
    return _ok({"draft": d.to_dict()})


@router.post("/drafts/{draft_id}/reject")
async def reject_draft(draft_id: str, reason: str = Query("")) -> dict[str, Any]:
    d = draft_factory.reject_draft(draft_id, reason=reason)
    if d is None:
        raise HTTPException(status_code=404, detail=f"unknown draft {draft_id}")
    return _ok({"draft": d.to_dict()})


@router.post("/drafts/{draft_id}/mark-copied")
async def mark_copied(draft_id: str) -> dict[str, Any]:
    try:
        d = draft_factory.mark_copied(draft_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    if d is None:
        raise HTTPException(status_code=404, detail=f"unknown draft {draft_id}")
    return _ok({"draft": d.to_dict()})


@router.get("/followups")
async def list_followups() -> dict[str, Any]:
    rows = followup.due_followups()
    return _ok({"count": len(rows), "followups": [f.to_dict() for f in rows]})


@router.post("/followups/{followup_id}/complete")
async def complete_followup(followup_id: str, message_ref: str = Query("")) -> dict[str, Any]:
    f = followup.complete_followup(followup_id, message_ref=message_ref)
    if f is None:
        raise HTTPException(status_code=404, detail=f"unknown followup {followup_id}")
    return _ok({"followup": f.to_dict()})


@router.get("/proposals")
async def list_proposals(approval_status: str | None = Query(None)) -> dict[str, Any]:
    rows = proposal.list_proposals(approval_status=approval_status)
    return _ok({"count": len(rows), "proposals": [p.to_dict() for p in rows]})


@router.post("/proposals/generate")
async def generate_proposal(body: GenerateProposalBody) -> dict[str, Any]:
    try:
        p = proposal.generate_proposal(**body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return _ok({"proposal": p.to_dict()})


@router.get("/proof-packs")
async def list_proof_packs(customer_id: str | None = Query(None)) -> dict[str, Any]:
    rows = proof_pack.list_proof_packs(customer_id=customer_id)
    return _ok({"count": len(rows), "proof_packs": [p.to_dict() for p in rows]})


@router.post("/proof-packs/generate")
async def generate_proof_pack(body: GenerateProofPackBody) -> dict[str, Any]:
    try:
        p = proof_pack.build_proof_pack(**body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return _ok({"proof_pack": p.to_dict()})


@router.get("/payments")
async def list_payments(status: str | None = Query(None)) -> dict[str, Any]:
    rows = payment_handoff.list_handoffs(status=status)
    return _ok({"count": len(rows), "payment_handoffs": [h.to_dict() for h in rows]})


@router.post("/payments/handoff")
async def prepare_payment_handoff(body: PaymentHandoffBody) -> dict[str, Any]:
    try:
        h = payment_handoff.prepare_handoff(
            proposal_id=body.proposal_id,
            customer_id=body.customer_id,
            product_id=body.product_id,
            discovery_ref=body.discovery_ref,
            quote_id=body.quote_id,
            quote_authority_ref=body.quote_authority_ref,
            customer_specific_scope_ref=body.customer_specific_scope_ref,
            amount_sar=body.amount_sar,
            notes=body.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    decision = (
        _ALLOW if h.governance_status == "approved" else GovernanceDecision.REQUIRE_APPROVAL.value
    )
    return _ok({"payment_handoff": h.to_dict()}, decision)


@router.get("/renewals")
async def list_renewals() -> dict[str, Any]:
    due = renewal.list_due()
    return _ok(
        {
            "count": len(due),
            "due": [s.to_dict() for s in due],
            "triggers": list(renewal.RENEWAL_TRIGGERS),
        }
    )


@router.get("/win-loss")
async def get_win_loss() -> dict[str, Any]:
    return _ok(
        {"summary": win_loss.summarize(), "weekly_questions": list(win_loss.WEEKLY_QUESTIONS)}
    )


__all__ = ["router"]