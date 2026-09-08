"""Governed inbound diagnostic intake orchestration.

This module converts a customer-initiated website intake into an internal work
packet for the five canonical Dealix agents and mirrors the intake into the
existing Revenue Ops Autopilot store. It does not send messages, publish,
charge, create a binding quote, or promote an unproven problem to customer
proof.

Truth rules preserved:
- inbound request != qualified problem
- public/contact data != marketing consent
- diagnostic hypothesis != customer proof
- draft/internal work != sent
- quote != invoice != payment
"""
from __future__ import annotations

import json
from typing import Any

_CANONICAL_AGENTS = (
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
)

_DIAGNOSTIC_FIELDS = (
    ("workflow", "ما الـworkflow أو القرار الذي تريد تحسينه الآن؟"),
    ("decision_owner", "من يملك القرار والمتابعة داخل الشركة؟"),
    ("tools_data", "ما الأدوات أو البيانات التي يعتمد عليها العمل اليوم؟"),
    ("business_impact", "ما الأثر التجاري أو التشغيلي للمشكلة اليوم؟"),
    ("proof_metric", "ما المقياس الذي سيُثبت أن الوضع تحسن؟"),
    ("baseline", "ما الـbaseline الحالي لذلك المقياس، إن كان معروفًا؟"),
    ("target_outcome", "ما النتيجة المستهدفة أو الحد الأدنى المقبول؟"),
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

    work_packets = [
        {
            "agent": "dealix-pm",
            "objective": "Own intake priority, WIP, evidence gaps and next-action routing.",
            "authority": "L0-L3_INTERNAL_ONLY",
        },
        {
            "agent": "dealix-sales",
            "objective": "Resolve account context, buying committee and problem evidence without treating contact data as consent.",
            "authority": "L0-L3_INTERNAL_ONLY",
        },
        {
            "agent": "dealix-delivery",
            "objective": "Draft the diagnostic route, measurable baseline and smallest outcome sprint candidate.",
            "authority": "L0-L3_INTERNAL_ONLY",
        },
        {
            "agent": "dealix-engineer",
            "objective": "Assess data, integration, security and implementation dependencies for the stated workflow.",
            "authority": "L0-L3_INTERNAL_ONLY",
        },
        {
            "agent": "dealix-content",
            "objective": "Prepare the customer-facing diagnostic brief structure using only verified evidence and explicit unknowns.",
            "authority": "L0-L2_DRAFT_ONLY",
        },
    ]

    return {
        "schema_version": 1,
        "intake_kind": "free_execution_diagnostic",
        "company": company,
        "sector": sector,
        "problem_state": problem_state,
        "evidence_completeness_pct": completeness,
        "context": context,
        "next_questions": next_questions,
        "canonical_agents": list(_CANONICAL_AGENTS),
        "work_packets": work_packets,
        "truth": {
            "qualified_problem": False,
            "customer_proof": False,
            "marketing_consent": False,
            "binding_quote": False,
            "payment": False,
        },
        "material_authority": {
            "external_send": False,
            "public_publish": False,
            "paid_spend": False,
            "payment_execution": False,
            "production_mutation": False,
            "binding_commercial_commitment": False,
        },
    }


def mirror_to_revenue_autopilot(record: dict[str, Any], handoff: dict[str, Any]) -> dict[str, Any]:
    """Mirror an inbound intake to the ONE Revenue Ops Autopilot store.

    Idempotency is derived from the lead-inbox record ID. The mirror creates an
    internal lead, an intake-stage diagnostic record and one evidence event.
    It never creates an opportunity, quote, invoice, send or payment state.
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
        consent_marketing=False,
        consent_proof_pack=False,
        lead_score=0,
        score_breakdown={},
        stage="new_lead",
        war_room_status="not_contacted",
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
            f"evidence_completeness_pct={handoff.get('evidence_completeness_pct')}."
        ),
        confidence="high",
    )
    store.append_evidence_idempotent(event)

    return {
        "mirrored": True,
        "lead_id": lead_id,
        "diagnostic_id": diagnostic_id,
        "evidence_id": evidence_id,
        "stage": "new_lead",
        "external_action": "none",
    }
