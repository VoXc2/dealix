"""Agent Governance — enterprise constraints on Agent Card autonomy.

See ``docs/global_grade/AGENT_GOVERNANCE.md`` and the endgame doctrine
in ``auto_client_acquisition.endgame_os.agent_control``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from auto_client_acquisition.endgame_os.agent_control import (
    AgentCard,
    AutonomyLevel,
)


class EnterpriseAgentConstraint(str, Enum):
    ALLOWED_STANDARD = "allowed_standard"
    RESTRICTED_REQUIRES_CONTRACT = "restricted_requires_contract"
    ENTERPRISE_ONLY = "enterprise_only"
    FORBIDDEN = "forbidden"


@dataclass(frozen=True)
class AgentOperationDecision:
    constraint: EnterpriseAgentConstraint
    reason: str


# Doctrine MVP rule: 0–3 standard, 4 restricted, 5 enterprise-only, 6 forbidden.
_LEVEL_CONSTRAINTS: dict[AutonomyLevel, EnterpriseAgentConstraint] = {
    AutonomyLevel.READ: EnterpriseAgentConstraint.ALLOWED_STANDARD,
    AutonomyLevel.ANALYZE: EnterpriseAgentConstraint.ALLOWED_STANDARD,
    AutonomyLevel.DRAFT_RECOMMEND: EnterpriseAgentConstraint.ALLOWED_STANDARD,
    AutonomyLevel.QUEUE_FOR_APPROVAL: EnterpriseAgentConstraint.ALLOWED_STANDARD,
    AutonomyLevel.EXECUTE_INTERNAL_AFTER_APPROVAL: EnterpriseAgentConstraint.RESTRICTED_REQUIRES_CONTRACT,
    AutonomyLevel.EXTERNAL_RESTRICTED: EnterpriseAgentConstraint.ENTERPRISE_ONLY,
    AutonomyLevel.AUTONOMOUS_EXTERNAL_FORBIDDEN: EnterpriseAgentConstraint.FORBIDDEN,
}


def enterprise_allowed_levels() -> tuple[AutonomyLevel, ...]:
    """Levels allowed for standard engagements (no extra contract terms)."""

    return tuple(
        level
        for level, constraint in _LEVEL_CONSTRAINTS.items()
        if constraint is EnterpriseAgentConstraint.ALLOWED_STANDARD
    )


def evaluate_card(card: AgentCard) -> AgentOperationDecision:
    constraint = _LEVEL_CONSTRAINTS[card.autonomy_level]
    if constraint is EnterpriseAgentConstraint.FORBIDDEN:
        reason = "autonomy_level_forbidden_by_doctrine"
    elif constraint is EnterpriseAgentConstraint.RESTRICTED_REQUIRES_CONTRACT:
        reason = "level_4_requires_explicit_contract_clause"
    elif constraint is EnterpriseAgentConstraint.ENTERPRISE_ONLY:
        reason = "level_5_requires_enterprise_runtime_controls"
    else:
        reason = "within_standard_engagement_envelope"
    return AgentOperationDecision(constraint=constraint, reason=reason)
