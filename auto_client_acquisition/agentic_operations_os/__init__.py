"""Agentic operations OS — governed agents under MVP constraints."""

from __future__ import annotations

from auto_client_acquisition.agentic_operations_os.agent_auditability_card import (
    AgentAuditabilityCard,
    agent_auditability_card_valid,
)
from auto_client_acquisition.agentic_operations_os.agent_governance import (
    AgentGovernanceDecision,
    governance_decision_for_proposed_action,
)
from auto_client_acquisition.agentic_operations_os.agent_identity import (
    MVP_MAX_OPERATING_LEVEL,
    MVP_MIN_OPERATING_LEVEL,
    AgentIdentityCard,
    agent_identity_valid,
    agent_operating_level_allowed_in_mvp,
)
from auto_client_acquisition.agentic_operations_os.agent_lifecycle import (
    DECOMMISSION_TRIGGERS,
    DEPLOY_PREREQUISITES,
    LIFECYCLE_STAGES,
    deploy_prerequisites_met,
    should_decommission,
)
from auto_client_acquisition.agentic_operations_os.agent_permissions import (
    FORBIDDEN_TOOL_SLUGS,
    ToolClass,
    agent_tool_forbidden,
    permission_change_requires_audit,
    tool_class_allowed_in_mvp,
)
from auto_client_acquisition.agentic_operations_os.agent_risk_score import (
    AgentRiskDimensions,
    agent_risk_band,
    agent_risk_score,
)
from auto_client_acquisition.agentic_operations_os.agentic_operations_board import (
    board_decision_for_tool_request,
)
from auto_client_acquisition.agentic_operations_os.handoff import (
    HandoffObject,
    handoff_valid,
    pii_output_requires_handoff,
)

__all__ = (
    "DECOMMISSION_TRIGGERS",
    "DEPLOY_PREREQUISITES",
    "FORBIDDEN_TOOL_SLUGS",
    "LIFECYCLE_STAGES",
    "MVP_MAX_OPERATING_LEVEL",
    "MVP_MIN_OPERATING_LEVEL",
    "AgentAuditabilityCard",
    "AgentGovernanceDecision",
    "AgentIdentityCard",
    "AgentRiskDimensions",
    "HandoffObject",
    "ToolClass",
    "agent_auditability_card_valid",
    "agent_identity_valid",
    "agent_operating_level_allowed_in_mvp",
    "agent_risk_band",
    "agent_risk_score",
    "agent_tool_forbidden",
    "board_decision_for_tool_request",
    "deploy_prerequisites_met",
    "governance_decision_for_proposed_action",
    "handoff_valid",
    "permission_change_requires_audit",
    "pii_output_requires_handoff",
    "should_decommission",
    "tool_class_allowed_in_mvp",
)
