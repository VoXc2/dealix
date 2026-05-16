"""Governed Revenue Ops engagement surface — `/api/v1/revenue-ops`.

Backs the Governed Revenue & AI Operations Company repositioning (2026-05-16).
Implements the diagnostic, CRM upload/score, decision passport, follow-up
drafts, evidence events, approvals, and invoice-draft endpoints — all
draft-first. There is NO autonomous-send endpoint: an external send requires an
explicit `approved` state transition (founder approval).

Distinct from the legacy `/api/v1/revenue-os` autonomous-layers surface.
"""

from __future__ import annotations

import threading
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.revenue_ops.diagnostics import run_diagnostic
from auto_client_acquisition.revenue_ops.state_machine import (
    EngagementStateError,
    next_states,
    validate_transition,
)

router = APIRouter(prefix="/api/v1/revenue-ops", tags=["revenue-ops"])

_DISCLAIMER = "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"

_LOCK = threading.Lock()
# In-memory store; production swaps for a persistent repository.
_ENGAGEMENTS: dict[str, dict[str, Any]] = {}
_EVIDENCE: list[dict[str, Any]] = []


def clear_revenue_ops_state_for_tests() -> None:
    """Reset module state — test hook only."""
    with _LOCK:
        _ENGAGEMENTS.clear()
        _EVIDENCE.clear()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _gov(decision: GovernanceDecision, *, rules: tuple[str, ...] = ()) -> dict[str, Any]:
    return {
        "governance_decision": decision.value,
        "matched_rules": list(rules),
        "risk_level": "low" if decision == GovernanceDecision.ALLOW else "medium",
    }


def _record_evidence(engagement_id: str, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Append an evidence event. Refuses to store anything resembling PII."""
    event = {
        "event_id": uuid.uuid4().hex[:12],
        "engagement_id": engagement_id,
        "kind": kind,
        "occurred_at": _now(),
        "payload": payload,
    }
    with _LOCK:
        _EVIDENCE.append(event)
    return event


def _engagement(engagement_id: str) -> dict[str, Any]:
    with _LOCK:
        eng = _ENGAGEMENTS.get(engagement_id)
    if eng is None:
        raise HTTPException(
            status_code=404,
            detail={"ar": "ارتباط غير معروف", "en": f"unknown engagement: {engagement_id}"},
        )
    return eng


# ─────────────────────────────────────────────────────────────────
# 1. DIAGNOSTIC
# ─────────────────────────────────────────────────────────────────
class DiagnosticBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_label: str | None = Field(default=None, max_length=200)
    crm_rows: list[dict[str, Any]] = Field(default_factory=list)
    ai_usage_ungoverned: bool = False
    has_decision_trail: bool = True


@router.post("/diagnostics")
def post_diagnostic(body: DiagnosticBody = Body(...)) -> dict[str, Any]:
    """Create a Governed Revenue Ops Diagnostic engagement (state: draft)."""
    engagement_id = f"rvo_{uuid.uuid4().hex[:10]}"
    result = run_diagnostic(
        engagement_id,
        crm_rows=body.crm_rows,
        ai_usage_ungoverned=body.ai_usage_ungoverned,
        has_decision_trail=body.has_decision_trail,
    )
    eng = {
        "engagement_id": engagement_id,
        "service_id": "governed_revenue_ops_diagnostic",
        "client_label": body.client_label,
        "state": "draft",
        "created_at": _now(),
        "crm_rows": body.crm_rows,
        "diagnostic": result.to_dict(),
        "decision_passport": None,
        "follow_up_drafts": [],
        "invoice_draft": None,
    }
    with _LOCK:
        _ENGAGEMENTS[engagement_id] = eng
    _record_evidence(engagement_id, "diagnostic_created", {"service_id": "governed_revenue_ops_diagnostic"})
    return {
        **_gov(GovernanceDecision.ALLOW),
        "engagement_id": engagement_id,
        "state": "draft",
        "diagnostic": result.to_dict(),
    }


# ─────────────────────────────────────────────────────────────────
# 2. UPLOAD CRM EXPORT
# ─────────────────────────────────────────────────────────────────
class UploadBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    engagement_id: str
    crm_rows: list[dict[str, Any]] = Field(default_factory=list)


@router.post("/upload")
def post_upload(body: UploadBody = Body(...)) -> dict[str, Any]:
    """Attach / replace a client CRM export on an existing engagement."""
    eng = _engagement(body.engagement_id)
    if not body.crm_rows:
        raise HTTPException(status_code=422, detail={"ar": "لا توجد صفوف", "en": "crm_rows required"})
    with _LOCK:
        eng["crm_rows"] = body.crm_rows
    _record_evidence(body.engagement_id, "crm_upload", {"row_count": len(body.crm_rows)})
    return {
        **_gov(GovernanceDecision.ALLOW),
        "engagement_id": body.engagement_id,
        "row_count": len(body.crm_rows),
    }


# ─────────────────────────────────────────────────────────────────
# 3. SCORE / RE-RUN DIAGNOSTIC
# ─────────────────────────────────────────────────────────────────
@router.post("/score")
def post_score(engagement_id: str = Body(..., embed=True)) -> dict[str, Any]:
    """Re-run the diagnostic scoring over the engagement's current CRM rows."""
    eng = _engagement(engagement_id)
    result = run_diagnostic(engagement_id, crm_rows=eng.get("crm_rows") or [])
    with _LOCK:
        eng["diagnostic"] = result.to_dict()
    _record_evidence(engagement_id, "diagnostic_scored", {"crm_quality_score": result.crm_quality_score})
    return {
        **_gov(GovernanceDecision.ALLOW),
        "engagement_id": engagement_id,
        "diagnostic": result.to_dict(),
    }


# ─────────────────────────────────────────────────────────────────
# 4. DECISION PASSPORT
# ─────────────────────────────────────────────────────────────────
@router.get("/{engagement_id}/decision-passport")
def get_decision_passport(engagement_id: str) -> dict[str, Any]:
    """Build a decision passport from the engagement's diagnostic findings."""
    eng = _engagement(engagement_id)
    diag = eng.get("diagnostic") or {}
    findings = diag.get("findings") or []
    if not findings:
        raise HTTPException(
            status_code=400,
            detail={"ar": "شغّل التشخيص أولًا", "en": "run diagnostics first"},
        )
    sources = sorted({f["source_ref"] for f in findings})
    passport = {
        "engagement_id": engagement_id,
        "client_label": eng.get("client_label"),
        "decision": f"Recommend: {diag.get('recommended_next')}",
        "decision_ar": f"التوصية: {diag.get('recommended_next_ar')}",
        "evidence_findings": findings,
        "source_refs": sources,
        "proof_target": "decision-ready sprint/retainer plan",
        "owner": "founder",
        "blocked_actions": ["autonomous_external_send", "cold_whatsapp", "linkedin_automation", "scraping"],
        "built_at": _now(),
    }
    with _LOCK:
        eng["decision_passport"] = passport
    _record_evidence(engagement_id, "decision_passport_built", {"source_ref_count": len(sources)})
    return {
        **_gov(GovernanceDecision.ALLOW_WITH_REVIEW, rules=("decision_passport_human_review",)),
        "decision_passport": passport,
        "disclaimer": _DISCLAIMER,
    }


# ─────────────────────────────────────────────────────────────────
# 5. FOLLOW-UP DRAFTS
# ─────────────────────────────────────────────────────────────────
class FollowUpBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_cold_whatsapp: bool = False
    request_linkedin_automation: bool = False
    request_scraping: bool = False


@router.post("/{engagement_id}/follow-up-drafts")
def post_follow_up_drafts(
    engagement_id: str, body: FollowUpBody = Body(default_factory=FollowUpBody)
) -> dict[str, Any]:
    """Generate follow-up message DRAFTS. Drafts are never sent."""
    eng = _engagement(engagement_id)
    if body.request_cold_whatsapp or body.request_linkedin_automation or body.request_scraping:
        raise HTTPException(
            status_code=403,
            detail={
                "ar": "رُفض — مخالف لقواعد الحوكمة",
                "en": "Blocked — cold WhatsApp / LinkedIn automation / scraping are forbidden by doctrine",
            },
        )
    diag = eng.get("diagnostic") or {}
    drafts = [
        {
            "draft_id": uuid.uuid4().hex[:10],
            "channel": "email",
            "state": "draft",
            "approval_required": True,
            "subject_en": "Following up on your revenue workflow review",
            "subject_ar": "متابعة بخصوص مراجعة سير الإيراد لديكم",
            "body_en": (
                "Hi, sharing the next step from your Governed Revenue Ops "
                f"Diagnostic — recommended path: {diag.get('recommended_next')}."
            ),
            "body_ar": (
                "مرحبًا، نشارك الخطوة التالية من تشخيص عمليات الإيراد المحكومة — "
                f"المسار الموصى به: {diag.get('recommended_next_ar')}."
            ),
        }
    ]
    with _LOCK:
        eng["follow_up_drafts"] = drafts
    _record_evidence(engagement_id, "follow_up_drafts_created", {"draft_count": len(drafts)})
    return {
        **_gov(GovernanceDecision.DRAFT_ONLY, rules=("external_channels_draft_only",)),
        "engagement_id": engagement_id,
        "follow_up_drafts": drafts,
        "note": "Drafts only. No message is sent without an approved engagement transition.",
    }


# ─────────────────────────────────────────────────────────────────
# 6. EVIDENCE EVENTS
# ─────────────────────────────────────────────────────────────────
class EvidenceBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    engagement_id: str
    kind: str = Field(..., max_length=80)
    payload: dict[str, Any] = Field(default_factory=dict)


@router.post("/evidence/events")
def post_evidence_event(body: EvidenceBody = Body(...)) -> dict[str, Any]:
    """Append an evidence event to an engagement's audit trail."""
    _engagement(body.engagement_id)
    event = _record_evidence(body.engagement_id, body.kind, body.payload)
    return {**_gov(GovernanceDecision.ALLOW), "event": event}


@router.get("/{engagement_id}/evidence")
def get_evidence(engagement_id: str) -> dict[str, Any]:
    """Return the full evidence trail for an engagement."""
    _engagement(engagement_id)
    with _LOCK:
        events = [e for e in _EVIDENCE if e["engagement_id"] == engagement_id]
    return {**_gov(GovernanceDecision.ALLOW), "engagement_id": engagement_id, "events": events}


# ─────────────────────────────────────────────────────────────────
# 7. APPROVALS — engagement state machine transitions
# ─────────────────────────────────────────────────────────────────
class ApprovalBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    engagement_id: str
    target_state: str
    approved_by: str = Field(..., max_length=120)
    note: str = Field(default="", max_length=500)


@router.post("/approvals")
def post_approval(body: ApprovalBody = Body(...)) -> dict[str, Any]:
    """Advance an engagement through the governed state machine.

    The only path to any external action (`sent` and beyond) runs through an
    explicit approval here. `draft → sent` is rejected by the state machine.
    """
    eng = _engagement(body.engagement_id)
    current = eng["state"]
    try:
        validate_transition(current, body.target_state)
    except EngagementStateError as exc:
        raise HTTPException(
            status_code=409,
            detail={"ar": "انتقال حالة غير مسموح", "en": str(exc)},
        ) from exc
    with _LOCK:
        eng["state"] = body.target_state
    _record_evidence(
        body.engagement_id,
        "state_transition",
        {"from": current, "to": body.target_state, "approved_by": body.approved_by, "note": body.note},
    )
    return {
        **_gov(GovernanceDecision.ALLOW_WITH_REVIEW, rules=("engagement_state_machine",)),
        "engagement_id": body.engagement_id,
        "from_state": current,
        "to_state": body.target_state,
        "next_states": sorted(next_states(body.target_state)),
    }


# ─────────────────────────────────────────────────────────────────
# 8. INVOICE DRAFT
# ─────────────────────────────────────────────────────────────────
class InvoiceBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    engagement_id: str
    service_id: str
    amount_sar: float = Field(..., gt=0)
    description: str = Field(default="", max_length=500)


@router.post("/invoices")
def post_invoice_draft(body: InvoiceBody = Body(...)) -> dict[str, Any]:
    """Create an invoice DRAFT. Does not charge — Moyasar live mode is

    founder-flipped only. The invoice is not 'sent' until the engagement
    reaches the `invoice_sent` state via an approval.
    """
    eng = _engagement(body.engagement_id)
    if eng["state"] not in ("scope_requested", "invoice_sent", "invoice_paid"):
        raise HTTPException(
            status_code=409,
            detail={
                "ar": "لا يمكن إنشاء فاتورة قبل طلب النطاق",
                "en": "invoice draft requires engagement state >= scope_requested",
            },
        )
    invoice = {
        "invoice_id": f"inv_{uuid.uuid4().hex[:10]}",
        "engagement_id": body.engagement_id,
        "service_id": body.service_id,
        "amount_sar": body.amount_sar,
        "description": body.description,
        "state": "draft",
        "charged": False,
        "created_at": _now(),
    }
    with _LOCK:
        eng["invoice_draft"] = invoice
    _record_evidence(body.engagement_id, "invoice_draft_created", {"amount_sar": body.amount_sar})
    return {
        **_gov(GovernanceDecision.ALLOW_WITH_REVIEW, rules=("invoice_draft_no_charge",)),
        "invoice": invoice,
        "note": "Draft invoice. No charge is made; Moyasar live mode is founder-controlled.",
    }


@router.get("/{engagement_id}")
def get_engagement(engagement_id: str) -> dict[str, Any]:
    """Return the full engagement record (diagnostic, state, drafts, invoice)."""
    eng = _engagement(engagement_id)
    return {**_gov(GovernanceDecision.ALLOW), "engagement": eng}
