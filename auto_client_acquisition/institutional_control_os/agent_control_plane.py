"""Institutional Agent Control Plane — Agent Card with allowed_tools.

Extends the endgame Agent Card with an explicit ``allowed_tools`` set.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.endgame_os.agent_control import AutonomyLevel
from auto_client_acquisition.global_grade_os.agent_governance import (
    EnterpriseAgentConstraint,
)


@dataclass(frozen=True)
class InstitutionalAgentCard:
    agent_id: str
    name: str
    owner: str
    purpose: str
    allowed_inputs: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    autonomy_level: AutonomyLevel
    approval_required_for: tuple[str, ...]
    audit_required: bool = True

    def __post_init__(self) -> None:
        if self.autonomy_level >= AutonomyLevel.AUTONOMOUS_EXTERNAL_FORBIDDEN:
            raise ValueError("autonomous_external_action_forbidden_by_doctrine")
        if not self.agent_id:
            raise ValueError("agent_id_required")
        if not self.owner:
            raise ValueError("owner_required")
        # The card MUST declare at least one allowed tool; "no tools" agents
        # add no value and only add risk surface.
        if not self.allowed_tools:
            raise ValueError("allowed_tools_required")

    def can_use_tool(self, tool: str) -> bool:
        return tool in self.allowed_tools and tool not in self.forbidden_actions


@dataclass(frozen=True)
class InstitutionalAgentDecision:
    allowed_in_mvp: bool
    constraint: EnterpriseAgentConstraint
    reason: str


def evaluate_institutional_agent(card: InstitutionalAgentCard) -> InstitutionalAgentDecision:
    """MVP gate identical to the sovereignty rule (autonomy 0–3)."""

    level = card.autonomy_level
    if level <= AutonomyLevel.QUEUE_FOR_APPROVAL:
        return InstitutionalAgentDecision(
            allowed_in_mvp=True,
            constraint=EnterpriseAgentConstraint.ALLOWED_STANDARD,
            reason="within_mvp_autonomy_band_0_to_3",
        )
    if level is AutonomyLevel.EXECUTE_INTERNAL_AFTER_APPROVAL:
        return InstitutionalAgentDecision(
            allowed_in_mvp=False,
            constraint=EnterpriseAgentConstraint.RESTRICTED_REQUIRES_CONTRACT,
            reason="level_4_requires_contract_clause",
        )
    return InstitutionalAgentDecision(
        allowed_in_mvp=False,
        constraint=EnterpriseAgentConstraint.ENTERPRISE_ONLY,
        reason="level_5_enterprise_only",
    )
