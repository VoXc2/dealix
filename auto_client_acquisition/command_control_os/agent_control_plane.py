"""Agent Control Plane — live registry + autonomy decision.

See ``docs/command_control/AGENT_CONTROL_PLANE.md``. Builds on the
``endgame_os.agent_control`` Agent Card and the ``global_grade_os``
enterprise constraints.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.endgame_os.agent_control import (
    AgentCard,
    AgentRegistry,
)
from auto_client_acquisition.global_grade_os.agent_governance import (
    AgentOperationDecision,
    EnterpriseAgentConstraint,
    evaluate_card,
)


@dataclass(frozen=True)
class AutonomyDecision:
    """Result of asking the control plane whether an agent may operate."""

    allowed: bool
    constraint: EnterpriseAgentConstraint
    reason: str
    requires_contract: bool
    enterprise_only: bool


class AgentControlPlane:
    """Live wrapper around the Agent Registry.

    Adds enterprise-constraint evaluation, pause/resume, and a query
    surface used by the Command Center.
    """

    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self._registry = registry or AgentRegistry()

    @property
    def registry(self) -> AgentRegistry:
        return self._registry

    def register(self, card: AgentCard) -> AgentCard:
        return self._registry.register(card)

    def evaluate(self, agent_id: str) -> AutonomyDecision:
        card = self._registry.get(agent_id)
        decision: AgentOperationDecision = evaluate_card(card)
        allowed = decision.constraint in {
            EnterpriseAgentConstraint.ALLOWED_STANDARD,
            EnterpriseAgentConstraint.RESTRICTED_REQUIRES_CONTRACT,
            EnterpriseAgentConstraint.ENTERPRISE_ONLY,
        }
        return AutonomyDecision(
            allowed=allowed,
            constraint=decision.constraint,
            reason=decision.reason,
            requires_contract=decision.constraint
            is EnterpriseAgentConstraint.RESTRICTED_REQUIRES_CONTRACT,
            enterprise_only=decision.constraint
            is EnterpriseAgentConstraint.ENTERPRISE_ONLY,
        )

    def pause(self, agent_id: str) -> None:
        self._registry.pause(agent_id)

    def retire(self, agent_id: str) -> None:
        self._registry.retire(agent_id)

    def list_active(self) -> tuple[AgentCard, ...]:
        return self._registry.list_active()
