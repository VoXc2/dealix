"""Governed inbound diagnostic intake orchestration.

This module converts a customer-initiated website intake into an internal work
packet for the canonical Omega V3 Agentic Holding and mirrors the intake into
the existing Revenue Ops Autopilot store. Historical five executor names remain
compatibility aliases only; they are not architecture or fleet-size authority.
It does not send messages, publish, charge, create a binding quote, or promote
an unproven problem to customer proof.

Truth rules preserved:
- inbound request != qualified problem
- public/contact data != marketing consent
- customer-reported context != independently verified evidence
- diagnostic hypothesis != customer proof
- draft/internal work != sent
- quote != invoice != payment
"""
from __future__ import annotations

import json
from typing import Any

from dealix.agentic_holding.runtime import build_current_registry

_LEGACY_EXECUTOR_ALIASES = (
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
)
_LEGACY_ALIAS_SEMANTICS = "LEGACY_EXECUTOR_ALIASES_ONLY_NOT_ARCHITECTURE_AUTHORITY"

_DIAGNOSTIC_FIELDS = (
    ("workflow", "ما الـworkflow أو القرار الذي تريد تحسينه الآن؟"),
    ("decision_owner", "من يملك القرار والمتابعة داخل الشركة؟"),
    ("tools_data", "ما الأدوات أو البيانات التي يعتمد عليها العمل اليوم؟"),
    ("business_impact", "ما الأثر التجاري أو التشغيلي للمشكلة اليوم؟"),
    ("proof_metric", "ما المقياس الذي سيُثبت أن الوضع تحسن؟"),
    ("baseline", "ما الـbaseline الحالي لذلك المقياس، إن كان معروفًا؟"),
    ("target_outcome", "ما النتيجة المستهدفة أو الحد الأدنى المقبول؟"),
)

_CONTEXT_EVENT_FIELDS = (
    "workflow",
    "decision_owner",
    "tools_data",
    "business_impact",
    "proof_metric",
    "baseline",
    "target_outcome",
    "urgency",
    "website",
    "role",
    "preferred_contact",
)


def _parse_context(record: dict[str, Any]) -> dict[str, str]:
    raw = record.get("diagnostic_context")
    if isinstance(raw, dict):
        return {str(k): str(v or "").strip() for k, v in raw.items()}

    message = record.get("message")
    if isinstance(message, str) and message.strip().startswith("{"):
        try:
            parsed = json.loads(message)
        except Exception:
            parsed = None
        if isinstance(parsed, dict):
            return {str(k): str(v or "").strip() for k, v in parsed.items()}

    return {"workflow": str(message or "").strip()}


def _material_authority_false() -> dict[str, bool]:
    return {
        "external_send": False,
        "public_publish": False,
        "paid_spend": False,
        "payment_execution": False,
        "production_mutation": False,
        "binding_commercial_commitment": False,
    }


def _agentic_holding_receipt() -> dict[str, Any]:
    registry = build_current_registry()
    receipt = registry.receipt()
    return {
        **receipt,
        "registry_source": "dealix.agentic_holding.runtime.build_current_registry",
        "fixed_five_authority": False,
        "legacy_executor_aliases": list(_LEGACY_EXECUTOR_ALIASES),
        "routing_authority": "Company Operator -> Agentic Holding registry -> Session Factory",
    }


def build_agent_handoff(record: dict[str, Any]) -> dict[str, Any]:
    """Build a deterministic, non-material work packet for an inbound intake."""
    context = _parse_context(record)
    answered = sum(1 for key, _ in _DIAGNOSTIC_FIELDS if context.get(key, "").strip())
    total = len(_DIAGNOSTIC_FIELDS)
    completeness = round((answered / total) * 100) if total else 0
    next_questions = [question for key, question in _DIAGNOSTIC_FIELDS if not context.get(key, "").strip()]

    company = str(record.get("company") or "").strip()
    sector = str(record.get("sector") or "").strip() or "unknown"
    workflow = context.get("workflow", "").strip()
    proof_metric = context.get("proof_metric", "").strip()
    baseline = context.get("baseline", "").strip()

    problem_state = "UNPROVEN_NEEDS_EVIDENCE"
    if workflow and proof_metric and baseline:
        problem_state = "HYPOTHESIS_WITH_BASELINE_PENDING_VALIDATION"

    holding = _agentic_holding_receipt()
    work_packets = [
        {
            "agent": "dealix-pm",
            "agent_semantics": _LEGACY_ALIAS_SEMANTICS,
            "objective": "Own intake priority, WIP, evidence gaps and next-action routing.",
            "authority": "L0-L3_INTERNAL_ONLY",
        },
        {
            "agent": "dealix-sales",
            "agent_semantics": _LEGACY_ALIAS_SEMANTICS,
            "objective": "Resolve account context, buying committee and problem evidence without treating contact data as consent.",
            "authority": "L0-L3_INTERNAL_ONLY",
        },
        {
            "agent": "dealix-delivery",
            "agent_semantics": _LEGACY_ALIAS_SEMANTICS,
            "objective": "Draft the diagnostic route, measurable baseline and smallest outcome sprint candidate.",
            "authority": "L0-L3_INTERNAL_ONLY",
        },
        {
            "agent": "dealix-engineer",
            "agent_semantics": _LEGACY_ALIAS_SEMANTICS,
            "objective": "Assess data, integration, security and implementation dependencies for the stated workflow.",
            "authority": "L0-L3_INTERNAL_ONLY",
        },
        {
            "agent": "dealix-content",
            "agent_semantics": _LEGACY_ALIAS_SEMANTICS,
            "objective": "Prepare the customer-facing diagnostic brief structure using only verified evidence and explicit unknowns.",
            "authority": "L0-L2_DRAFT_ONLY",
        },
    ]

    return {
        "schema_version": 2,
        "intake_kind": "free_execution_diagnostic",
        "company": company,
        "sector": sector,
        "problem_state": problem_state,
        "evidence_completeness_pct": completeness,
        "context": context,
        "next_questions": next_questions,
        "agentic_holding": holding,
        "fixed_five_authority": False,
        "routing_authority": holding["routing_authority"],
        # Compatibility only. Do not infer fleet size or runtime authority from this field.
        "canonical_agents": list(_LEGACY_EXECUTOR_ALIASES),
        "canonical_agents_field_semantics": _LEGACY_ALIAS_SEMANTICS,
        "legacy_executor_aliases": list(_LEGACY_EXECUTOR_ALIASES),
        "work_packets": work_packets,
        "truth": {
            "qualified_problem": False,
            "customer_proof": False,
            "marketing_consent": False,
            "binding_quote": False,
            "payment": False,
        },
        "material_authority": _material_authority_false(),
    }


def mirror_to_revenue_autopilot(record: dict[str, Any], handoff: dict[str, Any]) -> dict[str, Any]:
    """Mirror an inbound intake to the ONE Revenue Ops Autopilot store.

    Idempotency is derived from the lead-inbox record ID. The mirror creates an
    internal lead, an intake-stage diagnostic record and attributable evidence
    events for the customer-reported diagnostic context. Customer-reported
    statements remain explicitly unverified. It never creates an opportunity,
    quote, invoice, send or payment state.
    """
    from dealix.revenue_ops_autopilot.schemas import (
        DiagnosticDeliveryRecord,
        EvidenceEvent,
        FunnelLeadRecord,
    )
    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    source_id = str(record.get("id") or "").strip()
    if not source_id:
        return {"mirrored": False, "reason": "missing_source_id"}

    store = get_autopilot_store()
    lead_id = f"inbound_{source_id}"
    diagnostic_id = f"diag_{lead_id}"
    evidence_id = f"ev_{lead_id}_intake"
    context = handoff.get("context") or {}
    followup_requested = bool(record.get("followup_requested", False))

    lead = FunnelLeadRecord(
        id=lead_id,
        name=str(record.get("name") or ""),
        email=str(record.get("email") or ""),
        phone=str(record.get("phone") or ""),
        company=str(record.get("company") or ""),
        role=str(context.get("role") or record.get("role") or ""),
        industry=str(record.get("sector") or ""),
        country="SA",
        source="website_free_execution_diagnostic",
        pain=str(context.get("workflow") or record.get("message") or "")[:1500],
        urgency=str(context.get("urgency") or record.get("urgency") or ""),
        crm_status=(
            "inbound_followup_requested"
            if followup_requested
            else "inbound_no_followup_requested"
        ),
        consent_marketing=False,
        consent_proof_pack=False,
        lead_score=0,
        score_breakdown={},
        stage="new_lead",
        war_room_status="not_contacted",
        segment="inbound_execution_diagnostic",
        pain_hypothesis=str(context.get("business_impact") or "")[:1000],
        offer_id="free_execution_diagnostic",
        next_action="complete_evidence_backed_diagnostic",
        next_action_hint_ar=(
            "أكمل فجوات الـbaseline والـproof metric ثم حضّر Diagnostic draft داخلي؛ "
            "لا إرسال أو عرض ملزم تلقائي."
        ),
    )
    store.upsert_lead(lead)

    if store.get_diagnostic(diagnostic_id) is None:
        store.append_diagnostic(
            DiagnosticDeliveryRecord(
                id=diagnostic_id,
                lead_id=lead_id,
                stage="intake",
                onboarding_checklist=list(handoff.get("next_questions") or []),
                proof_pack_outline_ar=(
                    "Intake → Evidence/Unknown split → Baseline → Problem validation → "
                    "Smallest measurable intervention → Proof plan."
                ),
            )
        )

    event = EvidenceEvent(
        id=evidence_id,
        event_type="inbound_diagnostic_intake_received",
        entity_type="lead",
        entity_id=lead_id,
        source="website_free_execution_diagnostic",
        summary=(
            f"Inbound diagnostic intake received; problem_state={handoff.get('problem_state')}; "
            f"evidence_completeness_pct={handoff.get('evidence_completeness_pct')}; "
            f"followup_requested={str(followup_requested).lower()}."
        ),
        confidence="direct_submission_unverified",
    )
    store.append_evidence_idempotent(event)

    context_event_ids: list[str] = []
    for key in _CONTEXT_EVENT_FIELDS:
        value = str(context.get(key) or "").strip()
        if not value:
            continue
        context_event_id = f"ev_{lead_id}_customer_reported_{key}"
        store.append_evidence_idempotent(
            EvidenceEvent(
                id=context_event_id,
                event_type="customer_reported_diagnostic_context",
                entity_type="lead",
                entity_id=lead_id,
                source="website_free_execution_diagnostic",
                summary=f"{key}: {value[:4000]}",
                confidence="customer_reported_unverified",
            )
        )
        context_event_ids.append(context_event_id)

    return {
        "mirrored": True,
        "lead_id": lead_id,
        "diagnostic_id": diagnostic_id,
        "evidence_id": evidence_id,
        "context_evidence_ids": context_event_ids,
        "stage": "new_lead",
        "external_action": "none",
    }


def load_company_os_inbound_diagnostics(limit: int = 50) -> list[dict[str, Any]]:
    """Expose website diagnostics to the canonical Company OS internal cycle.

    This is a read-only bridge over the existing Revenue Ops store. It does not
    create a second queue/store. Cases without an explicit follow-up request are
    still visible for internal evidence analysis but are marked ineligible for
    external follow-up.
    """
    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    store = get_autopilot_store()
    leads = [
        lead
        for lead in store.list_leads(limit=max(100, limit * 4))
        if lead.source == "website_free_execution_diagnostic"
    ][:limit]
    evidence = store.list_evidence(limit=max(500, limit * 20))

    cases: list[dict[str, Any]] = []
    for lead in leads:
        followup_requested = lead.crm_status == "inbound_followup_requested"
        diagnostic = store.get_diagnostic(f"diag_{lead.id}")
        case_events = [event for event in evidence if event.entity_id == lead.id]
        evidence_refs = [f"revenue_autopilot:{event.id}" for event in case_events]
        context: dict[str, str] = {}
        for event in case_events:
            if event.event_type != "customer_reported_diagnostic_context":
                continue
            key, sep, value = event.summary.partition(": ")
            if sep and key in _CONTEXT_EVENT_FIELDS:
                context[key] = value

        record = {
            "id": lead.id,
            "company": lead.company,
            "sector": lead.industry or "unknown",
            "diagnostic_context": context,
        }
        handoff = build_agent_handoff(record)
        cases.append(
            {
                "lead_id": lead.id,
                "company_name": lead.company,
                "sector": lead.industry or "unknown",
                "source": lead.source,
                "relationship_state": "INBOUND" if followup_requested else "INBOUND_NO_FOLLOWUP",
                "consent_state": "INBOUND_REQUEST" if followup_requested else "NONE",
                "followup_requested": followup_requested,
                "commercial_stage": "REAL_INTERACTION",
                "problem_state": handoff["problem_state"],
                "evidence_completeness_pct": handoff["evidence_completeness_pct"],
                "evidence_refs": evidence_refs,
                "next_questions": (
                    list(diagnostic.onboarding_checklist)
                    if diagnostic is not None
                    else list(handoff["next_questions"])
                ),
                "agentic_holding": handoff["agentic_holding"],
                "routing_authority": handoff["routing_authority"],
                "legacy_executor_aliases": handoff["legacy_executor_aliases"],
                "work_packets": handoff["work_packets"],
                "next_action": "complete_evidence_backed_diagnostic_internal",
                "external_followup_eligible": followup_requested,
                "material_authority": _material_authority_false(),
            }
        )
    return cases