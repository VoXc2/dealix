"""Tests for the smallest governed workflow runtime foundation."""
from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.workflow_engine.governed_runtime import (
    WorkflowStepDefinition,
    execute_governed_workflow,
    load_workflow_definition,
)


WORKFLOW_PATH = Path("workflows/sales/lead_qualification.workflow.yaml")


def _tool_registry() -> dict:
    return {
        "leads.normalize": lambda ctx, step: {
            "step": step.step_id,
            "normalized": True,
            "source": ctx["trigger"]["source_id"],
        },
        "leads.enrich": lambda ctx, step: {
            "step": step.step_id,
            "domain": "example.sa",
        },
        "lead.score": lambda ctx, step: {
            "step": step.step_id,
            "score": 84,
        },
        "crm.create_lead": lambda ctx, step: {
            "step": step.step_id,
            "crm_id": "crm_123",
        },
        "metrics.publish": lambda ctx, step: {
            "step": step.step_id,
            "kpi": "lead_qualification_cycle",
        },
    }


def test_load_workflow_definition_from_yaml() -> None:
    definition = load_workflow_definition(WORKFLOW_PATH)
    assert definition.name == "lead_qualification"
    assert definition.trigger_type == "lead_created"
    assert len(definition.steps) == 5
    assert definition.steps[-1].step_id == "executive_metrics"


def test_execute_governed_workflow_happy_path() -> None:
    definition = load_workflow_definition(WORKFLOW_PATH)
    report = execute_governed_workflow(
        definition=definition,
        trigger_payload={"source_id": "lead_001", "auto_approve": True},
        tool_registry=_tool_registry(),
    )
    assert report.status == "completed"
    assert report.metrics.steps_total == 5
    assert report.metrics.steps_completed == 5
    assert report.metrics.approvals_required == 1
    assert report.metrics.approvals_granted == 1
    assert report.metrics.approvals_denied == 0
    assert any(item.stage == "execution" for item in report.audit_log)


def test_execute_governed_workflow_blocks_on_policy() -> None:
    definition = load_workflow_definition(WORKFLOW_PATH)

    def policy_checker(context: dict, step: WorkflowStepDefinition, risk_score: float) -> GovernanceDecision:
        del context, risk_score
        if step.step_id == "external_commit":
            return GovernanceDecision.BLOCK
        return GovernanceDecision.ALLOW

    report = execute_governed_workflow(
        definition=definition,
        trigger_payload={"source_id": "lead_002", "auto_approve": True},
        tool_registry=_tool_registry(),
        policy_checker=policy_checker,
    )
    assert report.status == "blocked"
    assert report.executed_steps[-1].status == "blocked"
    assert report.executed_steps[-1].step_id == "external_commit"


def test_execute_governed_workflow_pauses_when_approval_denied() -> None:
    definition = load_workflow_definition(WORKFLOW_PATH)

    def approval_checker(context: dict, step: WorkflowStepDefinition, decision: GovernanceDecision) -> bool:
        del context, decision
        return step.step_id != "external_commit"

    report = execute_governed_workflow(
        definition=definition,
        trigger_payload={"source_id": "lead_003", "auto_approve": True},
        tool_registry=_tool_registry(),
        approval_checker=approval_checker,
    )
    assert report.status == "paused_for_approval"
    assert report.metrics.approvals_required == 1
    assert report.metrics.approvals_denied == 1
    assert report.executed_steps[-1].status == "awaiting_approval"


def test_execute_governed_workflow_retries_then_succeeds() -> None:
    definition = load_workflow_definition(WORKFLOW_PATH)
    attempts = {"score": 0}

    registry = _tool_registry()

    def flaky_score_tool(ctx: dict, step: WorkflowStepDefinition) -> dict:
        del ctx, step
        attempts["score"] += 1
        if attempts["score"] == 1:
            raise RuntimeError("transient scorer failure")
        return {"score": 89}

    registry["lead.score"] = flaky_score_tool

    report = execute_governed_workflow(
        definition=definition,
        trigger_payload={"source_id": "lead_004", "auto_approve": True},
        tool_registry=registry,
    )
    assert report.status == "completed"
    assert report.metrics.retries_total == 1
    score_step = next(item for item in report.executed_steps if item.step_id == "qualification_scoring")
    assert score_step.retries_used == 1


def test_execute_governed_workflow_fails_when_retries_exhausted() -> None:
    definition = load_workflow_definition(WORKFLOW_PATH)
    registry = _tool_registry()

    def always_fail(ctx: dict, step: WorkflowStepDefinition) -> dict:
        del ctx, step
        raise RuntimeError("persistent failure")

    registry["lead.score"] = always_fail

    report = execute_governed_workflow(
        definition=definition,
        trigger_payload={"source_id": "lead_005", "auto_approve": True},
        tool_registry=registry,
    )
    assert report.status == "failed"
    assert report.metrics.steps_failed == 1
    failed_step = next(item for item in report.executed_steps if item.status == "failed")
    assert failed_step.step_id == "qualification_scoring"
