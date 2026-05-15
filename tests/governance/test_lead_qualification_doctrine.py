"""Doctrine guards for the lead_qualification workflow.

These assert the non-negotiables hold for the workflow: drafts are
labeled, nothing is sent without approval, every output carries a
governance decision, and the agent has a registered identity.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_observability.trace import _reset_traces
from auto_client_acquisition.agent_os.agent_card import agent_card_valid
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    get_agent,
)
from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.sales_os.lead_qualification import (
    LeadInput,
    WorkflowDeps,
    run_lead_qualification,
)
from auto_client_acquisition.sales_os.lead_qualification.sales_agent import (
    DRAFT_LABEL,
    SALES_AGENT_ID,
)
from auto_client_acquisition.workflow_os_v10.state_machine import _reset_workflow_buffer, get_run


@pytest.fixture
def deps() -> WorkflowDeps:
    _reset_workflow_buffer()
    _reset_traces()
    clear_agent_registry_for_tests()
    return WorkflowDeps(approval_store=ApprovalStore())


def _lead() -> LeadInput:
    return LeadInput(
        lead_id="lead_doctrine",
        tenant_slug="acme",
        actor_role="sales_rep",
        source="inbound_form",
        company_name="Acme Co",
        sector="b2b_services",
        region="riyadh",
        icp_b2b_service_fit=80,
        icp_data_maturity=75,
        icp_governance_posture=80,
        icp_budget_signal=75,
        icp_decision_velocity=75,
    )


def test_draft_is_labeled_as_draft(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    draft = get_run(out.run_id).checkpoint["draft"]
    assert draft.startswith(DRAFT_LABEL)


def test_no_send_without_approval(deps: WorkflowDeps) -> None:
    # Default run pauses for approval — nothing proceeds past the gate.
    out = run_lead_qualification(_lead(), deps)
    assert out.state == "paused_for_approval"
    pending = deps.approval_store.list_pending()
    assert len(pending) == 1
    assert pending[0].action_mode == "approval_required"
    # No CRM update / dashboard card was produced before approval.
    assert out.dashboard_card == {}


def test_output_carries_governance_decision(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    assert out.governance_decision
    for step in out.steps:
        assert step["governance_decision"], step["step_id"]


def test_agent_has_identity(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    run_lead_qualification(_lead(), deps)
    card = get_agent(SALES_AGENT_ID)
    assert card is not None
    assert agent_card_valid(card)
    assert card.autonomy_level == 1  # draft-only — never auto-sends


def test_forbidden_draft_blocked_before_approval(deps: WorkflowDeps) -> None:
    deps.llm = lambda lead, verdict, ctx: "guaranteed results, scraping included"
    out = run_lead_qualification(_lead(), deps)
    assert out.state == "blocked"
    assert not deps.approval_store.list_pending()
