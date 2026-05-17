"""Revenue Machine — founder-led funnel surface.

Endpoints that feed the Governed Revenue & AI Ops Diagnostic (the hero
offer). Every external-facing action is draft-only or approval-gated; no
endpoint here sends a message or charges a card.

Endpoints:
  POST /api/v1/revenue-machine/risk-score       → AI & Revenue Ops Risk Score
  GET  /api/v1/revenue-machine/diagnostic-offer → the 3 hero tiers
  GET  /api/v1/revenue-machine/pipeline-view    → the 16-label funnel read-model
  POST /api/v1/revenue-machine/classify-lead    → founder lead scoring
  POST /api/v1/revenue-machine/workflow/{name}  → run a draft-only workflow A–G
  GET  /api/v1/revenue-machine/kpi-dashboard    → funnel counters from the ledger
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.business_ops.stage_definitions import JourneyStage
from auto_client_acquisition.crm_v10.founder_lead_scoring import score_founder_lead
from auto_client_acquisition.crm_v10.pipeline_view import (
    LeadClassification,
    all_pipeline_states,
    to_pipeline_view,
)
from auto_client_acquisition.proof_ledger.factory import get_default_ledger
from auto_client_acquisition.proof_ledger.schemas import ProofEvent, ProofEventType
from auto_client_acquisition.revenue_pipeline.founder_workflows import (
    WORKFLOWS,
    WorkflowInputError,
    run_workflow,
)
from auto_client_acquisition.sales_os.risk_score import score_risk
from auto_client_acquisition.service_catalog.registry import get_offering

router = APIRouter(prefix="/api/v1/revenue-machine", tags=["revenue-machine"])

_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_unconsented_data": True,
    "no_hidden_pricing": True,
    "no_fake_proof": True,
}

_DIAGNOSTIC_TIER_IDS = (
    "governed_diagnostic_starter_4999",
    "governed_diagnostic_standard_9999",
    "governed_diagnostic_executive_15000",
)


class _RiskScoreRequest(BaseModel):
    """The 7-question AI & Revenue Ops Risk Score questionnaire.

    Each boolean is the team's answer (``True`` = yes). ``consent`` is the
    lawful basis under PDPL — without it the submission is rejected and
    nothing is stored.
    """

    model_config = ConfigDict(extra="forbid")

    has_crm: bool = False
    uses_ai_in_sales_or_ops: bool = False
    approval_before_external_messages: bool = False
    can_link_ai_to_financial_outcome: bool = False
    followup_documented: bool = False
    knows_source_of_every_decision: bool = False
    has_ai_evidence_pack: bool = False
    context_text: str = Field(default="", max_length=2000)
    company_handle: str = Field(default="Saudi B2B lead", max_length=120)
    consent: bool = False


class _ClassifyLeadRequest(BaseModel):
    """Boolean intake signals for the founder lead scorer."""

    model_config = ConfigDict(extra="forbid")

    decision_maker: bool = False
    is_b2b: bool = False
    has_crm_or_revenue_process: bool = False
    uses_or_plans_ai: bool = False
    in_gcc: bool = False
    urgent_within_30_days: bool = False
    budget_5k_plus_sar: bool = False
    no_company: bool = False
    student_or_jobseeker: bool = False
    vague_curiosity: bool = False
    is_partner: bool = False
    company_handle: str = Field(default="Saudi B2B lead", max_length=120)


class _WorkflowRequest(BaseModel):
    """Union of inputs for workflows A–G; each workflow reads only its own."""

    model_config = ConfigDict(extra="forbid")

    company_handle: str = Field(default="Saudi B2B lead", max_length=120)
    # Workflow A — new lead signals
    decision_maker: bool = False
    is_b2b: bool = False
    has_crm_or_revenue_process: bool = False
    uses_or_plans_ai: bool = False
    in_gcc: bool = False
    urgent_within_30_days: bool = False
    budget_5k_plus_sar: bool = False
    no_company: bool = False
    student_or_jobseeker: bool = False
    vague_curiosity: bool = False
    is_partner: bool = False
    # Workflows B / C
    contact_role: str = Field(default="decision maker", max_length=80)
    sector: str = Field(default="b2b_services", max_length=80)
    # Workflow D — meeting outcome
    pain_confirmed: bool = False
    budget_range: str = Field(default="", max_length=80)
    timeline: str = Field(default="", max_length=80)
    decision_maker_present: bool = False
    scope_requested: bool = False
    # Workflows E / F — diagnostic tier
    tier: str = Field(default="governed_diagnostic_starter_4999", max_length=64)
    payment_evidence_source: str = Field(default="", max_length=200)
    # Workflow G
    value_confirmed: bool = False


def _governance_envelope() -> dict[str, Any]:
    return {"hard_gates": _HARD_GATES, "governance_decision": "allow"}


@router.get("/status")
async def revenue_machine_status() -> dict[str, Any]:
    return {
        "service": "revenue_machine",
        "hero_offer": "governed_revenue_ai_ops_diagnostic",
        "tiers": list(_DIAGNOSTIC_TIER_IDS),
        **_governance_envelope(),
    }


@router.post("/risk-score")
async def submit_risk_score(req: _RiskScoreRequest) -> dict[str, Any]:
    """Score the AI & Revenue Ops Risk questionnaire.

    Returns a Low/Medium/High band + recommended next step. Requires
    explicit ``consent`` — the lawful basis is recorded on the proof event.
    """
    if not req.consent:
        raise HTTPException(
            status_code=400,
            detail="consent_required: explicit consent is the lawful basis "
            "for processing this submission (PDPL).",
        )

    result = score_risk(
        has_crm=req.has_crm,
        uses_ai_in_sales_or_ops=req.uses_ai_in_sales_or_ops,
        approval_before_external_messages=req.approval_before_external_messages,
        can_link_ai_to_financial_outcome=req.can_link_ai_to_financial_outcome,
        followup_documented=req.followup_documented,
        knows_source_of_every_decision=req.knows_source_of_every_decision,
        has_ai_evidence_pack=req.has_ai_evidence_pack,
        context_text=req.context_text,
    )

    event = ProofEvent(
        event_type=ProofEventType.LEAD_INTAKE,
        customer_handle=req.company_handle,
        service_id=result.recommended_offer,
        summary_en=(
            f"AI & Revenue Ops Risk Score submitted — band={result.risk_level}, "
            f"score={result.score}"
        ),
        summary_ar=(
            f"تم إرسال مؤشر مخاطر الذكاء الاصطناعي والإيراد — "
            f"المستوى={result.risk_level}، النتيجة={result.score}"
        ),
        evidence_source="ai_revenue_ops_risk_score_form",
        risk_level=result.risk_level.lower(),
        approval_status="approval_required",
        payload={
            "score": result.score,
            "risk_signals": result.risk_signals,
            "doctrine_flags": result.doctrine_flags,
            "cta": result.cta,
            "lawful_basis": "explicit_consent",
            "consent": True,
        },
    )
    get_default_ledger().record(event)

    return {
        "result": result.to_dict(),
        "proof_event_id": event.id,
        **_governance_envelope(),
    }


@router.get("/diagnostic-offer")
async def diagnostic_offer() -> dict[str, Any]:
    """The 3 tiers of the Governed Revenue & AI Ops Diagnostic hero offer."""
    tiers: list[dict[str, Any]] = []
    for tier_id in _DIAGNOSTIC_TIER_IDS:
        offering = get_offering(tier_id)
        if offering is None:  # pragma: no cover — registry guarantees presence
            raise HTTPException(status_code=500, detail=f"missing offering {tier_id}")
        tiers.append(
            {
                "service_id": offering.id,
                "name_ar": offering.name_ar,
                "name_en": offering.name_en,
                "price_sar": offering.price_sar,
                "price_unit": offering.price_unit,
                "duration_days": offering.duration_days,
                "deliverables": list(offering.deliverables),
                "kpi_commitment_ar": offering.kpi_commitment_ar,
                "kpi_commitment_en": offering.kpi_commitment_en,
                "refund_policy_ar": offering.refund_policy_ar,
                "refund_policy_en": offering.refund_policy_en,
                "is_estimate": offering.is_estimate,
            }
        )
    return {
        "hero_offer": "governed_revenue_ai_ops_diagnostic",
        "landing_url": "/dealix-diagnostic.html",
        "tiers": tiers,
        **_governance_envelope(),
    }


@router.get("/pipeline-view")
async def pipeline_view() -> dict[str, Any]:
    """The 16-label founder funnel as a read-model over the canonical journey.

    No transition logic — advancing a lead/deal stays the job of the
    existing journey + CRM state machines. This is the projection only.
    """
    return {
        "pipeline_states": [s.value for s in all_pipeline_states()],
        "journey_stage_map": {
            stage.value: to_pipeline_view(stage).value for stage in JourneyStage
        },
        "lead_classifications": [c.value for c in LeadClassification],
        **_governance_envelope(),
    }


@router.post("/classify-lead")
async def classify_lead(req: _ClassifyLeadRequest) -> dict[str, Any]:
    """Score a captured lead and project it onto the founder pipeline.

    A fresh lead is pre-meeting, so the pipeline state is driven by the
    classification (qualified_A/B, nurture, partner_candidate, or
    closed_lost for a drop).
    """
    result = score_founder_lead(
        decision_maker=req.decision_maker,
        is_b2b=req.is_b2b,
        has_crm_or_revenue_process=req.has_crm_or_revenue_process,
        uses_or_plans_ai=req.uses_or_plans_ai,
        in_gcc=req.in_gcc,
        urgent_within_30_days=req.urgent_within_30_days,
        budget_5k_plus_sar=req.budget_5k_plus_sar,
        no_company=req.no_company,
        student_or_jobseeker=req.student_or_jobseeker,
        vague_curiosity=req.vague_curiosity,
        is_partner=req.is_partner,
    )
    state = to_pipeline_view(
        JourneyStage.TARGET_IDENTIFIED,
        lead_classification=LeadClassification(result.classification),
    )

    event = ProofEvent(
        event_type=ProofEventType.LEAD_INTAKE,
        customer_handle=req.company_handle,
        summary_en=(
            f"Founder lead classified — score={result.score}, "
            f"classification={result.classification}"
        ),
        summary_ar=(
            f"تم تصنيف العميل المحتمل — النتيجة={result.score}، "
            f"التصنيف={result.classification}"
        ),
        evidence_source="founder_lead_scoring",
        approval_status="approval_required",
        payload={
            "score": result.score,
            "classification": result.classification,
            "reasons": result.reasons,
            "pipeline_state": state.value,
        },
    )
    get_default_ledger().record(event)

    return {
        "result": result.to_dict(),
        "pipeline_state": state.value,
        "proof_event_id": event.id,
        **_governance_envelope(),
    }


@router.post("/workflow/{name}")
async def run_revenue_workflow(name: str, req: _WorkflowRequest) -> dict[str, Any]:
    """Run one of the draft-only revenue workflows A–G.

    Every workflow returns a draft for founder review and records one
    evidence event — none sends a message, issues an invoice, or charges.
    """
    if name not in WORKFLOWS:
        raise HTTPException(
            status_code=404,
            detail=f"unknown workflow {name!r}; known: {sorted(WORKFLOWS)}",
        )
    try:
        draft = run_workflow(name, req.model_dump())
    except WorkflowInputError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"draft": draft.to_dict(), **_governance_envelope()}


@router.get("/kpi-dashboard")
async def kpi_dashboard() -> dict[str, Any]:
    """Funnel counters derived strictly from recorded proof-ledger events.

    North Star = Paid Diagnostics. Every counter is evidence-backed — a
    number here exists only because an event was recorded (no_fake_proof).
    """
    events = get_default_ledger().list_events(limit=2000)
    counters = {
        "risk_scores_submitted": 0,
        "leads_classified": 0,
        "qualified_a": 0,
        "meetings_booked": 0,
        "meetings_done": 0,
        "scopes_drafted": 0,
        "payments_confirmed": 0,
        "proof_packs_sent": 0,
        "workflow_runs": 0,
    }
    north_star_paid_diagnostics = 0

    for ev in events:
        event_type = str(getattr(ev, "event_type", ""))
        source = str(getattr(ev, "evidence_source", ""))
        payload = getattr(ev, "payload", {}) or {}
        workflow = payload.get("workflow")

        if source == "ai_revenue_ops_risk_score_form":
            counters["risk_scores_submitted"] += 1
        if source == "founder_lead_scoring" or workflow == "new_lead":
            counters["leads_classified"] += 1
        if payload.get("classification") == "qualified_A":
            counters["qualified_a"] += 1
        if event_type == ProofEventType.MEETING_BOOKED.value:
            counters["meetings_booked"] += 1
        if event_type == ProofEventType.MEETING_COMPLETED.value:
            counters["meetings_done"] += 1
        if workflow == "scope_requested":
            counters["scopes_drafted"] += 1
        if event_type == ProofEventType.PAYMENT_CONFIRMED.value:
            counters["payments_confirmed"] += 1
            if str(payload.get("tier", "")).startswith("governed_diagnostic_"):
                north_star_paid_diagnostics += 1
        if event_type == ProofEventType.PROOF_PACK_SENT.value:
            counters["proof_packs_sent"] += 1
        if workflow is not None:
            counters["workflow_runs"] += 1

    return {
        "north_star": "paid_diagnostics",
        "north_star_paid_diagnostics": north_star_paid_diagnostics,
        "counters": counters,
        "events_scanned": len(events),
        **_governance_envelope(),
    }

