"""AI control plane vocabulary, policy gates, and deterministic state flow."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping, Sequence

CONTROL_PLANE_COMPONENTS: tuple[str, ...] = (
    "Agent Registry",
    "LLM Gateway",
    "Prompt Registry",
    "Model Router",
    "Cost Guard",
    "Eval Runner",
    "AI Run Ledger",
    "Policy Engine",
    "Approval Engine",
    "Kill Switch",
)

AI_OS_LAYERS: tuple[str, ...] = (
    "identity_layer",
    "policy_engine",
    "workflow_runtime",
    "tool_execution_engine",
    "memory_system",
    "observability",
    "evaluation_engine",
    "human_oversight",
)

PHASE_0_FOUNDATION: tuple[str, ...] = (
    "postgres",
    "redis",
    "otel",
    "auth",
    "rbac",
    "audit_logs",
)
PHASE_1_EXECUTION_CORE: tuple[str, ...] = (
    "workflow_engine",
    "tool_registry",
    "state_machine",
    "queue_system",
    "retry_system",
)
PHASE_2_AI_LAYER: tuple[str, ...] = (
    "prompt_runtime",
    "context_retrieval",
    "memory",
    "evals",
)
PHASE_3_GOVERNANCE: tuple[str, ...] = (
    "policies",
    "approvals",
    "risk_engine",
    "compliance_layer",
)


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ApprovalMode(StrEnum):
    NONE = "none"
    REQUIRED = "required"
    ALWAYS_REQUIRED = "always_required"
    BLOCKED = "blocked"


class AuditMode(StrEnum):
    MINIMAL = "minimal"
    FULL_TRACE = "full_trace"


class WorkflowStepState(StrEnum):
    RETRIEVE_CONTEXT = "retrieve_context"
    EVALUATE_REQUEST = "evaluate_request"
    RISK_ANALYSIS = "risk_analysis"
    APPROVAL = "approval"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    LOGGING = "logging"


@dataclass(frozen=True, slots=True)
class AgentIdentityCard:
    """Bounded agent identity card (no generic super-agent)."""

    agent_id: str
    owner: str
    permissions: tuple[str, ...]
    memory_scope: tuple[str, ...]
    policies: tuple[str, ...] = ()
    risk_level: RiskLevel = RiskLevel.MEDIUM


@dataclass(frozen=True, slots=True)
class ToolContract:
    """Governed tool contract for enterprise-safe execution."""

    tool_id: str
    schema_version: str
    risk_level: RiskLevel
    timeout_seconds: int = 30
    max_retries: int = 2
    approval_mode: ApprovalMode = ApprovalMode.REQUIRED
    audit_mode: AuditMode = AuditMode.FULL_TRACE
    rollback_supported: bool = False


@dataclass(frozen=True, slots=True)
class ZeroTrustPolicyRule:
    """Deterministic rule with explicit match + explicit effects."""

    rule_id: str
    tool_equals: str | None = None
    customer_region_equals: str | None = None
    tool_risk_equals: RiskLevel | None = None
    min_transaction_value: float | None = None
    require_approval: bool = False
    disable_external_memory: bool = False
    log_full_trace: bool = False
    block_execution: bool = False


@dataclass(frozen=True, slots=True)
class PolicyEvaluationResult:
    decision: str
    require_approval: bool
    disable_external_memory: bool
    log_full_trace: bool
    matched_rules: tuple[str, ...]


DEFAULT_ZERO_TRUST_RULES: tuple[ZeroTrustPolicyRule, ...] = (
    ZeroTrustPolicyRule(
        rule_id="crm_deal_large_value_requires_approval",
        tool_equals="crm.update_deal",
        min_transaction_value=10_000,
        require_approval=True,
    ),
    ZeroTrustPolicyRule(
        rule_id="eu_region_disable_external_memory",
        customer_region_equals="EU",
        disable_external_memory=True,
    ),
    ZeroTrustPolicyRule(
        rule_id="high_risk_tool_full_trace",
        tool_risk_equals=RiskLevel.HIGH,
        log_full_trace=True,
    ),
)

WORKFLOW_STATE_MACHINE: dict[WorkflowStepState, tuple[WorkflowStepState, ...]] = {
    WorkflowStepState.RETRIEVE_CONTEXT: (WorkflowStepState.EVALUATE_REQUEST,),
    WorkflowStepState.EVALUATE_REQUEST: (WorkflowStepState.RISK_ANALYSIS,),
    WorkflowStepState.RISK_ANALYSIS: (WorkflowStepState.APPROVAL,),
    WorkflowStepState.APPROVAL: (
        WorkflowStepState.EXECUTION,
        WorkflowStepState.LOGGING,
    ),
    WorkflowStepState.EXECUTION: (WorkflowStepState.VERIFICATION,),
    WorkflowStepState.VERIFICATION: (WorkflowStepState.LOGGING,),
    WorkflowStepState.LOGGING: (),
}


def validate_agent_identity(card: AgentIdentityCard) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not card.agent_id.strip():
        errors.append("agent_id_required")
    if not card.owner.strip():
        errors.append("owner_required")
    if not card.permissions:
        errors.append("permissions_required")
    if not card.memory_scope:
        errors.append("memory_scope_required")
    return (not errors, tuple(errors))


def validate_tool_contract(contract: ToolContract) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not contract.tool_id.strip():
        errors.append("tool_id_required")
    if contract.timeout_seconds <= 0:
        errors.append("timeout_seconds_must_be_positive")
    if contract.max_retries < 0:
        errors.append("max_retries_must_be_non_negative")
    if contract.approval_mode == ApprovalMode.BLOCKED and contract.rollback_supported:
        errors.append("blocked_tool_cannot_have_rollback")
    return (not errors, tuple(errors))


def _rule_matches(rule: ZeroTrustPolicyRule, request: Mapping[str, Any]) -> bool:
    if rule.tool_equals is not None:
        if str(request.get("tool", "")).lower() != rule.tool_equals.lower():
            return False
    if rule.customer_region_equals is not None:
        if str(request.get("customer_region", "")).lower() != rule.customer_region_equals.lower():
            return False
    if rule.tool_risk_equals is not None:
        if str(request.get("tool_risk", "")).lower() != rule.tool_risk_equals.value:
            return False
    if rule.min_transaction_value is not None:
        try:
            tx_value = float(request.get("value", 0))
        except (TypeError, ValueError):
            tx_value = 0.0
        if tx_value < rule.min_transaction_value:
            return False
    return True


def evaluate_zero_trust_policy(
    request: Mapping[str, Any],
    *,
    rules: Sequence[ZeroTrustPolicyRule] = DEFAULT_ZERO_TRUST_RULES,
) -> PolicyEvaluationResult:
    """Evaluate request against deterministic zero-trust rules."""
    require_approval = False
    disable_external_memory = False
    log_full_trace = False
    block_execution = False
    matched: list[str] = []
    for rule in rules:
        if not _rule_matches(rule, request):
            continue
        matched.append(rule.rule_id)
        require_approval = require_approval or rule.require_approval
        disable_external_memory = disable_external_memory or rule.disable_external_memory
        log_full_trace = log_full_trace or rule.log_full_trace
        block_execution = block_execution or rule.block_execution

    decision = "block" if block_execution else "require_approval" if require_approval else "allow"
    return PolicyEvaluationResult(
        decision=decision,
        require_approval=require_approval,
        disable_external_memory=disable_external_memory,
        log_full_trace=log_full_trace,
        matched_rules=tuple(matched),
    )


def is_valid_workflow_transition(
    from_state: WorkflowStepState,
    to_state: WorkflowStepState,
) -> bool:
    return to_state in WORKFLOW_STATE_MACHINE[from_state]


def validate_workflow_path(
    path: Sequence[WorkflowStepState],
) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not path:
        return False, ("workflow_path_required",)
    if path[0] != WorkflowStepState.RETRIEVE_CONTEXT:
        errors.append("workflow_must_start_with_retrieve_context")
    if path[-1] != WorkflowStepState.LOGGING:
        errors.append("workflow_must_end_with_logging")
    for idx in range(len(path) - 1):
        current_state = path[idx]
        next_state = path[idx + 1]
        if not is_valid_workflow_transition(current_state, next_state):
            errors.append(
                f"invalid_transition:{current_state.value}->{next_state.value}",
            )
    return (not errors, tuple(errors))


def example_ai_run_record() -> dict[str, Any]:
    return {
        "ai_run_id": "AIR-001",
        "agent": "RevenueAgent",
        "task": "score_accounts",
        "model_tier": "balanced",
        "prompt_version": "lead_scoring_v1",
        "inputs_redacted": True,
        "output_schema": "AccountScore",
        "governance_status": "approved_with_review",
        "qa_score": 91,
        "risk_level": "medium",
        "cost": 0.42,
        "workflow_state": WorkflowStepState.LOGGING.value,
    }


__all__ = [
    "AI_OS_LAYERS",
    "ApprovalMode",
    "AuditMode",
    "AgentIdentityCard",
    "CONTROL_PLANE_COMPONENTS",
    "DEFAULT_ZERO_TRUST_RULES",
    "PHASE_0_FOUNDATION",
    "PHASE_1_EXECUTION_CORE",
    "PHASE_2_AI_LAYER",
    "PHASE_3_GOVERNANCE",
    "PolicyEvaluationResult",
    "RiskLevel",
    "ToolContract",
    "WORKFLOW_STATE_MACHINE",
    "WorkflowStepState",
    "ZeroTrustPolicyRule",
    "evaluate_zero_trust_policy",
    "example_ai_run_record",
    "is_valid_workflow_transition",
    "validate_agent_identity",
    "validate_tool_contract",
    "validate_workflow_path",
]
