from __future__ import annotations

from auto_client_acquisition.diagnostic_intake_orchestrator import (
    build_agent_handoff,
    mirror_to_revenue_autopilot,
)
from dealix.revenue_ops_autopilot.store import reset_autopilot_store_for_tests


CANONICAL_AGENTS = [
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
]


def _record() -> dict:
    return {
        "id": "webdiag_test_001",
        "name": "Example Buyer",
        "email": "buyer@example.com",
        "phone": "+966500000000",
        "company": "Example Co",
        "role": "COO",
        "sector": "manufacturing",
        "message": "",
        "diagnostic_context": {
            "role": "COO",
            "workflow": "Reduce manual order-to-delivery handoffs across the operations team.",
            "decision_owner": "COO with Finance and Operations",
            "tools_data": "ERP, spreadsheets and email",
            "business_impact": "Delayed decisions and rework",
            "proof_metric": "order cycle time",
            "baseline": "9 days",
            "target_outcome": "6 days or less",
            "urgency": "this quarter",
            "preferred_contact": "email",
            "followup_requested": "true",
        },
    }


def test_handoff_uses_exactly_five_canonical_agents_and_no_material_authority():
    handoff = build_agent_handoff(_record())

    assert handoff["canonical_agents"] == CANONICAL_AGENTS
    assert [row["agent"] for row in handoff["work_packets"]] == CANONICAL_AGENTS
    assert handoff["evidence_completeness_pct"] == 100
    assert handoff["problem_state"] == "HYPOTHESIS_WITH_BASELINE_PENDING_VALIDATION"

    assert handoff["truth"] == {
        "qualified_problem": False,
        "customer_proof": False,
        "marketing_consent": False,
        "binding_quote": False,
        "payment": False,
    }
    assert all(value is False for value in handoff["material_authority"].values())


def test_missing_evidence_returns_questions_instead_of_fake_qualification():
    record = _record()
    record["diagnostic_context"] = {
        "workflow": "Improve the customer support workflow with a measurable response-time outcome."
    }
    handoff = build_agent_handoff(record)

    assert handoff["problem_state"] == "UNPROVEN_NEEDS_EVIDENCE"
    assert handoff["evidence_completeness_pct"] < 100
    assert handoff["next_questions"]
    assert handoff["truth"]["qualified_problem"] is False
    assert handoff["truth"]["customer_proof"] is False


def test_mirror_is_idempotent_and_never_grants_marketing_consent(tmp_path):
    store = reset_autopilot_store_for_tests(tmp_path / "autopilot.json")
    record = _record()
    handoff = build_agent_handoff(record)

    first = mirror_to_revenue_autopilot(record, handoff)
    second = mirror_to_revenue_autopilot(record, handoff)

    assert first["mirrored"] is True
    assert second["mirrored"] is True
    assert first["lead_id"] == second["lead_id"]

    leads = store.list_leads(limit=20)
    assert len(leads) == 1
    lead = leads[0]
    assert lead.source == "website_free_execution_diagnostic"
    assert lead.stage == "new_lead"
    assert lead.war_room_status == "not_contacted"
    assert lead.consent_marketing is False
    assert lead.consent_proof_pack is False
    assert lead.offer_id == "free_execution_diagnostic"

    diagnostic = store.get_diagnostic(first["diagnostic_id"])
    assert diagnostic is not None
    assert diagnostic.stage == "intake"

    evidence = store.list_evidence(limit=20)
    assert len([row for row in evidence if row.id == first["evidence_id"]]) == 1
    assert store.list_invoice_drafts(limit=20) == []
