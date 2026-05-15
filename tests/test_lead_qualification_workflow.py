"""End-to-end tests for the lead_qualification governed workflow."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_observability.trace import _reset_traces, list_recent_traces
from auto_client_acquisition.agent_os.agent_registry import clear_agent_registry_for_tests
from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.sales_os.lead_qualification import (
    LeadInput,
    WorkflowDeps,
    build_definition,
    resume_lead_qualification,
    run_lead_qualification,
)
from auto_client_acquisition.sales_os.lead_qualification.orchestrator import load_workflow_spec
from auto_client_acquisition.workflow_os_v10.state_machine import (
    _reset_workflow_buffer,
    advance_workflow,
    get_run,
)

EXPECTED_STEPS = [
    "lq_lead_intake",
    "lq_tenant_detection",
    "lq_rbac_check",
    "lq_knowledge_retrieval",
    "lq_qualification",
    "lq_lead_scoring",
    "lq_draft_response",
    "lq_risk_check",
    "lq_approval",
    "lq_crm_update",
    "lq_metrics_emission",
    "lq_eval_report",
    "lq_executive_dashboard",
]


@pytest.fixture
def deps() -> WorkflowDeps:
    _reset_workflow_buffer()
    _reset_traces()
    clear_agent_registry_for_tests()
    return WorkflowDeps(approval_store=ApprovalStore())


def _lead(**overrides: object) -> LeadInput:
    base: dict[str, object] = {
        "lead_id": "lead_001",
        "tenant_slug": "acme",
        "actor_role": "sales_rep",
        "source": "inbound_form",
        "company_name": "Acme Co",
        "sector": "b2b_services",
        "region": "riyadh",
        "icp_b2b_service_fit": 80,
        "icp_data_maturity": 75,
        "icp_governance_posture": 80,
        "icp_budget_signal": 75,
        "icp_decision_velocity": 75,
    }
    base.update(overrides)
    return LeadInput(**base)  # type: ignore[arg-type]


def test_yaml_declaration_has_13_steps() -> None:
    spec = load_workflow_spec()
    assert spec["name"] == "lead_qualification"
    assert [s["step_id"] for s in spec["steps"]] == EXPECTED_STEPS


def test_workflow_definition_matches_yaml() -> None:
    definition = build_definition()
    assert definition.workflow_id == "lead_qualification"
    assert definition.steps == EXPECTED_STEPS


def test_end_to_end_happy_path(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    assert out.state == "completed"
    assert out.completed
    assert len(out.steps) == 13
    assert out.dashboard_card["signal"]
    assert out.eval_report["overall_pass"] is True


def test_every_step_output_has_governance_decision(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    assert all(s["governance_decision"] for s in out.steps)
    assert out.governance_decision  # worst-case roll-up is set


def test_governance_decision_is_worst_case(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    # The approval step requires approval — that is the strictest step.
    assert out.governance_decision == "REQUIRE_APPROVAL"


def test_approval_gate_pauses_run(deps: WorkflowDeps) -> None:
    out = run_lead_qualification(_lead(), deps)
    assert out.state == "paused_for_approval"
    assert out.paused_for_approval
    assert len(out.steps) == 9
    assert out.approval_id
    # No CRM write happened before approval.
    run = get_run(out.run_id)
    assert "crm" not in run.checkpoint
    pending = deps.approval_store.list_pending()
    assert len(pending) == 1
    assert pending[0].action_mode == "approval_required"


def test_resume_completes_run(deps: WorkflowDeps) -> None:
    out = run_lead_qualification(_lead(), deps)
    resumed = resume_lead_qualification(out.run_id, deps)
    assert resumed.state == "completed"
    assert len(resumed.steps) == 13
    assert not deps.approval_store.list_pending()


def test_resume_on_completed_run_is_safe(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    again = resume_lead_qualification(out.run_id, deps)
    assert again.state == "completed"
    assert len(again.steps) == 13


def test_rbac_denied_blocks_run(deps: WorkflowDeps) -> None:
    out = run_lead_qualification(_lead(actor_role="viewer"), deps)
    assert out.state == "blocked"
    assert out.governance_decision == "BLOCK"
    assert out.blocked_reason.startswith("rbac_denied")
    assert len(out.steps) == 3


def test_qualification_reject_blocks_run(deps: WorkflowDeps) -> None:
    out = run_lead_qualification(_lead(wants_scraping_or_spam=True), deps)
    assert out.state == "blocked"
    assert out.blocked_reason.startswith("qualification_rejected")


def test_blocked_source_blocks_run(deps: WorkflowDeps) -> None:
    out = run_lead_qualification(_lead(source="scraping"), deps)
    assert out.state == "blocked"
    assert out.blocked_reason.startswith("blocked_source")


def test_tenant_not_found_blocks_run(deps: WorkflowDeps) -> None:
    out = run_lead_qualification(_lead(tenant_slug=""), deps)
    assert out.state == "blocked"
    assert out.blocked_reason.startswith("tenant_not_found")


def test_risk_check_blocks_forbidden_draft(deps: WorkflowDeps) -> None:
    deps.llm = lambda lead, verdict, ctx: "We offer guaranteed sales for your team"
    out = run_lead_qualification(_lead(), deps)
    assert out.state == "blocked"
    assert out.blocked_reason.startswith("risk_blocked")
    # The forbidden draft never reached the approval center.
    assert not deps.approval_store.list_pending()


def test_rollback_restores_checkpoint(deps: WorkflowDeps) -> None:
    deps.llm = lambda lead, verdict, ctx: "guaranteed sales pitch"
    out = run_lead_qualification(_lead(), deps)
    assert out.state == "blocked"
    run = get_run(out.run_id)
    # The risk step wrote checkpoint['risk'] then blocked — rollback removed it.
    assert "risk" not in run.checkpoint
    # State from earlier successful steps survives the rollback.
    assert "draft" in run.checkpoint


def test_traces_recorded_for_each_step(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    run_lead_qualification(_lead(), deps)
    traces = [t for t in list_recent_traces(limit=200) if t.workflow == "lead_qualification"]
    assert len(traces) == 13
    assert {t.input_kind for t in traces} == set(EXPECTED_STEPS)


def test_eval_report_overall_pass(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    report = out.eval_report
    assert report["eval_id"] == "lead_qualification"
    assert report["overall_pass"] is True
    assert {c["id"] for c in report["checks"]} == {
        "governance_present",
        "draft_labeled",
        "no_forbidden_language",
        "approval_gated",
        "score_justified",
    }


def test_idempotent_replay(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    run = get_run(out.run_id)
    before = len(run.step_history)
    # Replaying a step with an already-seen idempotency key is a no-op.
    advance_workflow(run, "lq_lead_intake", idempotency_key=f"{run.run_id}:lq_lead_intake")
    assert len(run.step_history) == before


def test_audit_trail_covers_every_step(deps: WorkflowDeps) -> None:
    deps.auto_approve = True
    out = run_lead_qualification(_lead(), deps)
    audited_steps = {a["step_id"] for a in out.audit}
    assert set(EXPECTED_STEPS).issubset(audited_steps)
    assert "approval_granted" in audited_steps
