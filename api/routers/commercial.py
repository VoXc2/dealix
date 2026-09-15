"""Dealix commercial API — current first-launch authority.

One product: Dealix — Saudi-first AI Business Operating System.
First wedge: Revenue + Proof + Command.

This router deliberately fails closed for live send, public fixed pricing, live
payment, and automatic expansion.  It keeps the existing diagnostic/proof/case
study helpers, while the customer progression contract is:

Free Mini Diagnostic -> qualified discovery -> founder-approved named scope ->
customer-specific governed Pilot -> source-backed proof -> manual
STOP / EXPAND / REDESIGN decision.
"""

from __future__ import annotations

import logging
from datetime import UTC, date, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from api.security.api_key import require_founder_admin_key
from dealix.commercial.buyer_outputs import BuyerEvidenceSnapshot, BuyerOutputsEngine
from dealix.commercial.case_study_generator import CaseStudyGenerator, CaseStudyRequest
from dealix.commercial.diagnostic_engine import DiagnosticEngine, DiagnosticRequest
from dealix.commercial.pilot_delivery import PilotDeliveryKit, PilotStartRequest
from dealix.commercial.proof_builder import ProofBuilder, ProofBuildRequest
from dealix.commercial.roi_calculator import ROIInput, estimate_roi
from dealix.commercial.transformation_proposal import (
    TransformationProposalError,
    TransformationProposalGenerator,
    TransformationProposalRequest,
)
from dealix.commercial.warm_intro_generator import WarmIntroGenerator, WarmIntroRequest

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/commercial", tags=["commercial"])
_require_admin = require_founder_admin_key

_LAUNCH_AUTHORITY = "customer_specific_governed_pilot"
_LEGACY_LAUNCH_AUTHORITY_ALIASES = ("revenue_command_pilot_30d",)
_EXTERNAL_SEND_ALLOWED = False
_LIVE_CHARGE_ALLOWED = False
_PUBLIC_FIXED_PRICE = False
_PRICE_AUTHORITY = "founder_approved_named_customer_quote"


class CurrentWarmIntroRequest(BaseModel):
    name: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1)
    role: str = ""
    sector: str = "b2b_services"
    known_pain: str = ""
    relationship: str = Field(..., min_length=1)
    referrer_name: str = ""
    warm_context_ref: str = Field(..., min_length=1)


class GovernedPilotStartRequest(BaseModel):
    account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    pain_points: list[str] = Field(default_factory=list)
    start_date: date
    approved_duration_days: int = Field(..., ge=1)
    approved_duration_ref: str = Field(..., min_length=1)
    approved_scope_ref: str = Field(..., min_length=1)
    baseline_source_ref: str = Field(..., min_length=1)
    approved_data_boundary_ref: str = Field(..., min_length=1)
    approval_path_ref: str = Field(..., min_length=1)
    acceptance_criteria_ref: str = Field(..., min_length=1)
    customer_specific_quote_ref: str = Field(..., min_length=1)
    customer_acceptance_ref: str = Field(..., min_length=1)
    start_condition_ref: str = Field(..., min_length=1)


class RevenueRunRequest(BaseModel):
    trigger: str = "manual"
    dry_run: bool = True


class TransformationReviewRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    selected_modules: list[str] = Field(..., min_length=1)
    pilot_proof_ref: str = Field(..., min_length=1)
    approved_scope_ref: str = Field(..., min_length=1)


def _commercial_authority() -> dict[str, Any]:
    return {
        "launch_authority": _LAUNCH_AUTHORITY,
        "wedge": "Revenue + Proof + Command",
        "quote_only_after_discovery": True,
        "public_fixed_price": _PUBLIC_FIXED_PRICE,
        "external_send_allowed": _EXTERNAL_SEND_ALLOWED,
        "live_charge_allowed": _LIVE_CHARGE_ALLOWED,
        "automatic_upsell": False,
        "price_authority": _PRICE_AUTHORITY,
        "legacy_launch_authority_aliases": list(_LEGACY_LAUNCH_AUTHORITY_ALIASES),
        "legacy_aliases_authoritative": False,
    }


@router.get("/status")
async def commercial_status(_: None = Depends(_require_admin)) -> dict[str, Any]:
    """Truthful internal readiness status; not a production/customer-value claim."""
    return {
        "status": "ready_for_governed_internal_commercial_ops",
        "wedge": "Revenue + Proof + Command",
        "quote_only_after_discovery": True,
        "public_fixed_price": False,
        "live_charge": False,
        "automatic_upsell": False,
        "external_send": False,
        "components": {
            "diagnostic": "internal_governed",
            "warm_intro": "draft_only_real_context_required",
            "pilot_delivery": "customer_specific_duration_start_gated",
            "proof": "source_bound",
            "payment_link": "blocked_no_live_charge",
            "expansion": "manual_post_proof_review",
        },
    }


# ---------------------------------------------------------------------------
# Diagnostic endpoints — existing governed implementation
# ---------------------------------------------------------------------------


@router.post("/diagnostic/generate")
async def diagnostic_generate(
    req: DiagnosticRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    engine = DiagnosticEngine()
    report = engine.generate(req)
    log.info("diagnostic_generated", report_id=report.report_id, company=req.company_name)
    return report.to_dict()


@router.post("/diagnostic/generate/markdown", response_class=PlainTextResponse)
async def diagnostic_generate_markdown(
    req: DiagnosticRequest,
    _: None = Depends(_require_admin),
) -> str:
    return DiagnosticEngine().generate(req).markdown_ar_en

# ---------------------------------------------------------------------------
# Deterministic buyer outputs — one evidence snapshot, three governed views
# ---------------------------------------------------------------------------


@router.post("/buyer-outputs/generate")
async def buyer_outputs_generate(
    req: BuyerEvidenceSnapshot,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    try:
        bundle = BuyerOutputsEngine().build(req)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "EVIDENCE_CONTRACT_FAILED",
                "message": str(exc),
            },
        ) from exc
    return bundle.to_dict()


# ---------------------------------------------------------------------------
# Warm-intro endpoints — drafts only; a real relationship/context ref is required
# ---------------------------------------------------------------------------


@router.post("/warm-intro/generate")
async def warm_intro_generate(
    req: CurrentWarmIntroRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    return {
        "status": "draft_only",
        "external_send_allowed": False,
        "next_action": "founder_review_only",
        "warm_context_ref": req.warm_context_ref,
        "company": req.company,
        "name": req.name,
        "relationship": req.relationship,
        "consent_inferred": False,
    }


@router.get("/warm-intro/templates")
async def warm_intro_templates(_: None = Depends(_require_admin)) -> dict[str, Any]:
    return {
        "status": "internal_reference_only",
        "external_send_allowed": False,
        "message": (
            "Templates never imply consent. A real warm/inbound/referral context, "
            "lawful channel basis, suppression check, and action-specific approval "
            "are required before any external send."
        ),
    }


# Backward-compatible internal draft helper. It never sends.
@router.post("/warm-intro/draft")
async def warm_intro_draft(
    req: WarmIntroRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    bundle = WarmIntroGenerator().generate(req)
    return bundle.to_dict()


# ---------------------------------------------------------------------------
# Pilot — customer-specific governed duration, no send/charge authority
# ---------------------------------------------------------------------------


@router.post("/pilot/start")
async def pilot_start(
    req: GovernedPilotStartRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    pilot_req = PilotStartRequest(
        account_id=req.account_id,
        company_name=req.company_name,
        sector=req.sector,
        pain_points=req.pain_points,
        start_date=req.start_date.isoformat(),
        approved_duration_days=req.approved_duration_days,
        approved_duration_ref=req.approved_duration_ref,
        approved_scope_ref=req.approved_scope_ref,
        baseline_source_ref=req.baseline_source_ref,
        approved_data_boundary_ref=req.approved_data_boundary_ref,
        approval_path_ref=req.approval_path_ref,
        acceptance_criteria_ref=req.acceptance_criteria_ref,
        customer_specific_quote_ref=req.customer_specific_quote_ref,
        customer_acceptance_ref=req.customer_acceptance_ref,
        start_condition_ref=req.start_condition_ref,
    )
    plan = PilotDeliveryKit().create_pilot_plan(pilot_req).to_dict()
    if plan["governance_decision"] != "ready_for_manual_approval":
        raise HTTPException(
            status_code=409,
            detail={
                "code": "PILOT_START_GATE_INCOMPLETE",
                "missing_start_refs": plan["missing_start_refs"],
            },
        )
    plan.update(
        {
            "launch_authority": _LAUNCH_AUTHORITY,
            "price_authority": "customer_specific_quote_after_qualified_discovery",
            "legacy_launch_authority_aliases": list(_LEGACY_LAUNCH_AUTHORITY_ALIASES),
            "legacy_aliases_authoritative": False,
            "gate_refs": {
                "approved_duration_ref": req.approved_duration_ref,
                "approved_scope_ref": req.approved_scope_ref,
                "baseline_source_ref": req.baseline_source_ref,
                "approved_data_boundary_ref": req.approved_data_boundary_ref,
                "approval_path_ref": req.approval_path_ref,
                "acceptance_criteria_ref": req.acceptance_criteria_ref,
                "customer_specific_quote_ref": req.customer_specific_quote_ref,
                "customer_acceptance_ref": req.customer_acceptance_ref,
                "start_condition_ref": req.start_condition_ref,
            },
        }
    )
    return {
        "status": "plan_prepared_approval_required",
        "external_send_allowed": False,
        "live_charge_allowed": False,
        "plan": plan,
    }


@router.get("/pilot/week1-template")
async def pilot_week1_template(_: None = Depends(_require_admin)) -> dict[str, Any]:
    return {
        "status": "template_only",
        "launch_authority": _LAUNCH_AUTHORITY,
        "external_send_allowed": False,
        "sections": ["baseline", "actions", "approvals", "outcomes", "evidence_gaps"],
    }


# ---------------------------------------------------------------------------
# Proof — existing source-bound builder
# ---------------------------------------------------------------------------


@router.post("/proof/build")
async def proof_build(
    req: ProofBuildRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    pack = ProofBuilder().build(req)
    log.info("proof_pack_built", pack_id=pack.pack_id, level=pack.proof_level, events=pack.event_count)
    return pack.to_dict()


@router.post("/proof/build/markdown", response_class=PlainTextResponse)
async def proof_build_markdown(
    req: ProofBuildRequest,
    _: None = Depends(_require_admin),
) -> str:
    return ProofBuilder().build(req).markdown_ar_en


# ---------------------------------------------------------------------------
# Payment — hard blocked for the first launch; no tier/amount authority
# ---------------------------------------------------------------------------


@router.post("/payment/link")
async def payment_link(
    payload: dict[str, Any],
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    del payload
    raise HTTPException(
        status_code=409,
        detail={
            "code": "NO_LIVE_CHARGE",
            "message": "Live payment links are blocked by current first-launch authority.",
        },
    )


@router.get("/payment/tiers")
async def payment_tiers(_: None = Depends(_require_admin)) -> dict[str, Any]:
    return {
        "tiers": [],
        "product_count": 1,
        "public_fixed_price": False,
        "quote_only": True,
        "live_checkout": False,
        "live_charge": False,
        "price_authority": _PRICE_AUTHORITY,
    }


# ---------------------------------------------------------------------------
# Expansion — manual review from proof only, never automatic upsell
# ---------------------------------------------------------------------------


@router.get("/upsell/check")
async def upsell_check_current(
    account_id: str,
    events_count: int = 0,
    proof_pack_generated: bool = False,
    days_active: int = 0,
    nps_score: int | None = None,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    del account_id, events_count, proof_pack_generated, days_active, nps_score
    return {
        "decision": "manual_review_required",
        "eligible_for_automatic_expansion": False,
        "offer": None,
        "price_sar": None,
        "next_step": "STOP_OR_EXPAND_OR_REDESIGN_FROM_SOURCE_BACKED_PROOF",
    }


# ---------------------------------------------------------------------------
# Case study — existing consent-aware builder
# ---------------------------------------------------------------------------


@router.post("/case-study/generate")
async def case_study_generate(
    req: CaseStudyRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    return CaseStudyGenerator().generate(req).to_dict()


@router.post("/case-study/generate/markdown", response_class=PlainTextResponse)
async def case_study_markdown(
    req: CaseStudyRequest,
    _: None = Depends(_require_admin),
) -> str:
    return CaseStudyGenerator().generate(req).markdown_ar_en


# ---------------------------------------------------------------------------
# ROI — internal estimate only, never a customer-value or guarantee claim
# ---------------------------------------------------------------------------


@router.post("/roi/estimate")
async def roi_estimate(
    req: ROIInput,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    return {
        "status": "internal_estimate_only",
        "customer_value_claim": False,
        "guarantee": False,
        "result": estimate_roi(req).to_dict(),
    }


# ---------------------------------------------------------------------------
# Revenue runner — dry-run only under current authority
# ---------------------------------------------------------------------------


@router.post("/revenue/run")
async def revenue_run(
    req: RevenueRunRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    if not req.dry_run:
        raise HTTPException(
            status_code=409,
            detail={"code": "NO_LIVE_COMMERCIAL_EXECUTION"},
        )
    return {
        "dry_run": True,
        "trigger": req.trigger,
        "results": [],
        "commercial_authority": _commercial_authority(),
    }


# ---------------------------------------------------------------------------
# Daily command — no synthetic outreach or payment-ready claim
# ---------------------------------------------------------------------------


@router.get("/daily-brief")
async def daily_brief(_: None = Depends(_require_admin)) -> dict[str, Any]:
    now = datetime.now(UTC)
    return {
        "brief_date": now.strftime("%Y-%m-%d"),
        "brief_time_utc": now.isoformat(),
        "status": "governed_internal_only",
        "warm_intro_status": "draft_only_requires_real_warm_context_ref",
        "payment": {"status": "blocked_no_live_charge", "tiers": []},
        "expansion": {"automatic_upsell": False, "decision": "manual_post_proof_review"},
        "reminders": [
            "NO_LIVE_SEND",
            "NO_LIVE_CHARGE",
            "NO_FAKE_PROOF",
            "NO_REVENUE_WITHOUT_PAYMENT_EVIDENCE",
        ],
    }


# ---------------------------------------------------------------------------
# Transformation — planning only after proof; never quote authority
# ---------------------------------------------------------------------------


@router.get("/transformation/modules")
async def transformation_modules(_: None = Depends(_require_admin)) -> dict[str, Any]:
    return {
        "status": "internal_post_proof_planning_only",
        "safe_to_send": False,
        "commercial_quote_authority": False,
        "registry": [
            "company_brain",
            "revenue_command",
            "customer_success",
            "partnerships",
            "operations",
            "executive_command",
        ],
    }


@router.post("/transformation/proposal")
async def transformation_proposal_current(
    req: TransformationReviewRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    return {
        "status": "internal_review_draft_only",
        "customer_id": req.customer_id,
        "selected_modules": req.selected_modules,
        "pilot_proof_ref": req.pilot_proof_ref,
        "approved_scope_ref": req.approved_scope_ref,
        "safe_to_send": False,
        "commercial_quote_authority": False,
    }


# Legacy transformation generator retained for internal compatibility. It is
# still admin-gated and its output remains a draft; it is not launch authority.
@router.post("/transformation-proposal/generate")
async def transformation_proposal_generate(
    req: TransformationProposalRequest,
    _: None = Depends(_require_admin),
) -> dict[str, Any]:
    try:
        proposal = TransformationProposalGenerator().generate(req)
    except TransformationProposalError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    result = proposal.to_dict()
    result["commercial_quote_authority"] = False
    result["safe_to_send"] = False
    return result


@router.post("/transformation-proposal/generate/markdown", response_class=PlainTextResponse)
async def transformation_proposal_markdown(
    req: TransformationProposalRequest,
    _: None = Depends(_require_admin),
) -> str:
    try:
        proposal = TransformationProposalGenerator().generate(req)
    except TransformationProposalError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return proposal.markdown_ar_en
