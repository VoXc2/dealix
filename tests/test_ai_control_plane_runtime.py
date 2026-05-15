"""Tests for trust_os AI control plane runtime primitives."""

from __future__ import annotations

from auto_client_acquisition.trust_os.ai_control_plane import (
    AI_OS_LAYERS,
    ApprovalMode,
    AgentIdentityCard,
    RiskLevel,
    ToolContract,
    WorkflowStepState,
    evaluate_zero_trust_policy,
    validate_agent_identity,
    validate_tool_contract,
    validate_workflow_path,
)


def test_ai_os_layers_cover_eight_foundations() -> None:
    assert len(AI_OS_LAYERS) == 8
    assert AI_OS_LAYERS[0] == "identity_layer"
    assert AI_OS_LAYERS[-1] == "human_oversight"


def test_agent_identity_requires_scope_and_permissions() -> None:
    bounded = AgentIdentityCard(
        agent_id="sales_qualifier_agent",
        owner="revenue_team",
        permissions=("crm.read", "draft.email"),
        memory_scope=("customer_history",),
        risk_level=RiskLevel.MEDIUM,
    )
    assert validate_agent_identity(bounded) == (True, ())

    invalid = AgentIdentityCard(
        agent_id="sales_qualifier_agent",
        owner="revenue_team",
        permissions=(),
        memory_scope=(),
        risk_level=RiskLevel.MEDIUM,
    )
    ok, errors = validate_agent_identity(invalid)
    assert ok is False
    assert "permissions_required" in errors
    assert "memory_scope_required" in errors


def test_tool_contract_requires_valid_runtime_limits() -> None:
    valid = ToolContract(
        tool_id="gmail.send_email",
        schema_version="v1",
        risk_level=RiskLevel.HIGH,
        timeout_seconds=20,
        max_retries=1,
        approval_mode=ApprovalMode.ALWAYS_REQUIRED,
    )
    assert validate_tool_contract(valid) == (True, ())

    invalid = ToolContract(
        tool_id="",
        schema_version="v1",
        risk_level=RiskLevel.HIGH,
        timeout_seconds=0,
        max_retries=-1,
        approval_mode=ApprovalMode.BLOCKED,
        rollback_supported=True,
    )
    ok, errors = validate_tool_contract(invalid)
    assert ok is False
    assert "tool_id_required" in errors
    assert "timeout_seconds_must_be_positive" in errors
    assert "max_retries_must_be_non_negative" in errors
    assert "blocked_tool_cannot_have_rollback" in errors


def test_zero_trust_rules_require_approval_for_large_crm_updates() -> None:
    result = evaluate_zero_trust_policy(
        {
            "tool": "crm.update_deal",
            "value": 25_000,
            "customer_region": "KSA",
            "tool_risk": "medium",
        },
    )
    assert result.decision == "require_approval"
    assert result.require_approval is True
    assert "crm_deal_large_value_requires_approval" in result.matched_rules


def test_zero_trust_rules_disable_external_memory_for_eu() -> None:
    result = evaluate_zero_trust_policy(
        {
            "tool": "crm.update_deal",
            "value": 500,
            "customer_region": "EU",
            "tool_risk": "low",
        },
    )
    assert result.disable_external_memory is True
    assert "eu_region_disable_external_memory" in result.matched_rules


def test_zero_trust_rules_enable_full_trace_for_high_risk_tool() -> None:
    result = evaluate_zero_trust_policy(
        {
            "tool": "knowledge.search",
            "value": 100,
            "customer_region": "KSA",
            "tool_risk": "high",
        },
    )
    assert result.log_full_trace is True
    assert "high_risk_tool_full_trace" in result.matched_rules


def test_workflow_path_is_deterministic_and_enforced() -> None:
    happy_path = [
        WorkflowStepState.RETRIEVE_CONTEXT,
        WorkflowStepState.EVALUATE_REQUEST,
        WorkflowStepState.RISK_ANALYSIS,
        WorkflowStepState.APPROVAL,
        WorkflowStepState.EXECUTION,
        WorkflowStepState.VERIFICATION,
        WorkflowStepState.LOGGING,
    ]
    assert validate_workflow_path(happy_path) == (True, ())

    invalid_path = [
        WorkflowStepState.RETRIEVE_CONTEXT,
        WorkflowStepState.RISK_ANALYSIS,
        WorkflowStepState.APPROVAL,
        WorkflowStepState.EXECUTION,
        WorkflowStepState.VERIFICATION,
        WorkflowStepState.LOGGING,
    ]
    ok, errors = validate_workflow_path(invalid_path)
    assert ok is False
    assert "invalid_transition:retrieve_context->risk_analysis" in errors
