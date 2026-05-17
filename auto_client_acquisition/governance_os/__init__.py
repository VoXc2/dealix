"""Governance OS — lightweight checks on draft content and intake posture."""

from auto_client_acquisition.governance_os.approval_matrix import approval_for_action
from auto_client_acquisition.governance_os.draft_gate import (
    audit_draft_text,
    intake_violations_for_source,
)
from auto_client_acquisition.governance_os.approval_policy import ApprovalRequirement, approval_for_external_channel
from auto_client_acquisition.governance_os.channel_policy import (
    CHANNEL_POLICY_AR,
    draft_text_has_forbidden_channel_language,
    forbidden_channel_markers,
)
from auto_client_acquisition.governance_os.claim_safety import ClaimSafetyResult, audit_claim_safety
from auto_client_acquisition.governance_os.policy_check import (
    PolicyCheckResult,
    PolicyVerdict,
    policy_check_draft,
    policy_check_intake_source,
    run_policy_check,
)
from auto_client_acquisition.governance_os.runtime_decision import (
    GovernanceDecision,
    governance_decision_from_passport_ai_gate,
    governance_decision_from_policy_check,
)
from auto_client_acquisition.governance_os.workflow_control_registry import (
    ControlRule,
    control_classes_for,
    workflow_controls,
    workflow_domain_is_governed,
)
from auto_client_acquisition.governance_os.forbidden_actions import (
    FORBIDDEN_CHANNEL_MARKERS,
    is_channel_forbidden,
)
from auto_client_acquisition.governance_os.lawful_basis import LawfulBasis, describe_basis
from auto_client_acquisition.governance_os.revenue_factory_policy import (
    ACTION_POLICY,
    AutomationLevel,
    DecisionStatus,
    PolicyDecision,
    PolicyRisk,
    evaluate_governed_action,
    founder_approval_action_keys,
)

__all__ = [
    "CHANNEL_POLICY_AR",
    "ClaimSafetyResult",
    "FORBIDDEN_CHANNEL_MARKERS",
    "GovernanceDecision",
    "LawfulBasis",
    "ApprovalRequirement",
    "PolicyCheckResult",
    "PolicyVerdict",
    "approval_for_action",
    "approval_for_external_channel",
    "audit_claim_safety",
    "audit_draft_text",
    "describe_basis",
    "draft_text_has_forbidden_channel_language",
    "ACTION_POLICY",
    "AutomationLevel",
    "DecisionStatus",
    "PolicyDecision",
    "PolicyRisk",
    "evaluate_governed_action",
    "founder_approval_action_keys",
    "forbidden_channel_markers",
    "governance_decision_from_passport_ai_gate",
    "governance_decision_from_policy_check",
    "intake_violations_for_source",
    "is_channel_forbidden",
    "policy_check_draft",
    "policy_check_intake_source",
    "run_policy_check",
    "ControlRule",
    "control_classes_for",
    "workflow_controls",
    "workflow_domain_is_governed",
]
