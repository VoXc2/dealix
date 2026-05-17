"""Founder revenue-machine workflows A–G — draft-only + evidence-logged."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.revenue_pipeline.founder_workflows import (
    APPROVAL_REQUIRED,
    DRAFT_ONLY,
    WORKFLOWS,
    UnknownWorkflow,
    WorkflowInputError,
    run_workflow,
)

client = TestClient(app)

# Minimal valid params per workflow.
_PARAMS: dict[str, dict] = {
    "new_lead": {"is_b2b": True},
    "qualified_a": {"sector": "b2b_services"},
    "meeting_booked": {"sector": "b2b_services"},
    "meeting_done": {"scope_requested": True},
    "scope_requested": {"tier": "governed_diagnostic_standard_9999"},
    "invoice_paid": {
        "tier": "governed_diagnostic_starter_4999",
        "payment_evidence_source": "bank_transfer_ref_001",
    },
    "delivery_done": {"value_confirmed": True},
}


def test_all_seven_workflows_registered():
    assert set(WORKFLOWS) == set(_PARAMS)
    assert len(WORKFLOWS) == 7


@pytest.mark.parametrize("name", sorted(_PARAMS))
def test_workflow_is_draft_only_and_logs_evidence(name: str):
    draft = run_workflow(name, _PARAMS[name])
    assert draft.workflow == name
    assert draft.action_mode in (DRAFT_ONLY, APPROVAL_REQUIRED)
    assert draft.action_mode not in ("live_send", "live_charge", "auto_send")
    assert draft.proof_event_id.startswith("evt_")
    assert draft.next_action
    assert isinstance(draft.draft, dict) and draft.draft


def test_new_lead_classifies_and_drafts_follow_up():
    draft = run_workflow(
        "new_lead",
        {"decision_maker": True, "is_b2b": True, "has_crm_or_revenue_process": True,
         "uses_or_plans_ai": True},
    )
    assert draft.draft["classification"] == "qualified_A"
    assert draft.draft["recommended_offer"] == "governed_diagnostic_starter_4999"
    assert draft.draft["follow_up_draft_ar"]


def test_meeting_done_routes_to_scope_when_requested():
    yes = run_workflow("meeting_done", {"scope_requested": True})
    assert yes.next_action == "run_workflow_scope_requested"
    no = run_workflow("meeting_done", {"scope_requested": False})
    assert no.next_action == "add_to_nurture_sequence"


def test_scope_requested_rejects_unknown_tier():
    with pytest.raises(WorkflowInputError):
        run_workflow("scope_requested", {"tier": "not_a_tier"})


def test_invoice_paid_requires_payment_evidence():
    with pytest.raises(WorkflowInputError):
        run_workflow(
            "invoice_paid",
            {"tier": "governed_diagnostic_starter_4999", "payment_evidence_source": ""},
        )


def test_run_workflow_rejects_unknown_name():
    with pytest.raises(UnknownWorkflow):
        run_workflow("not_a_workflow", {})


def test_run_workflow_ignores_params_outside_signature():
    # meeting_booked does not accept `tier` — it must be silently dropped.
    draft = run_workflow("meeting_booked", {"sector": "agency", "tier": "x"})
    assert draft.workflow == "meeting_booked"


def test_endpoint_runs_workflow():
    resp = client.post(
        "/api/v1/revenue-machine/workflow/scope_requested",
        json={"tier": "governed_diagnostic_executive_15000"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["draft"]["action_mode"] == APPROVAL_REQUIRED
    assert body["draft"]["draft"]["scope_document"]["price_sar"] == 15000.0


def test_endpoint_unknown_workflow_returns_404():
    resp = client.post("/api/v1/revenue-machine/workflow/nope", json={})
    assert resp.status_code == 404


def test_endpoint_workflow_input_error_returns_400():
    resp = client.post(
        "/api/v1/revenue-machine/workflow/invoice_paid",
        json={"tier": "governed_diagnostic_starter_4999"},
    )
    assert resp.status_code == 400


def test_kpi_dashboard_returns_evidence_backed_counters():
    # Seed one of each so the counters are non-trivial.
    client.post(
        "/api/v1/revenue-machine/workflow/invoice_paid",
        json={"tier": "governed_diagnostic_starter_4999",
              "payment_evidence_source": "bank_ref_kpi"},
    )
    resp = client.get("/api/v1/revenue-machine/kpi-dashboard")
    assert resp.status_code == 200
    body = resp.json()
    assert body["north_star"] == "paid_diagnostics"
    assert body["north_star_paid_diagnostics"] >= 1
    assert body["counters"]["payments_confirmed"] >= 1
