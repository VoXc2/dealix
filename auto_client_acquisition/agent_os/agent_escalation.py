"""Agent → human-supervisor escalation rules — task 6 of the Agent OS.

Decides when an agent must hand control to a human supervisor. Doctrine:
no AI agent runs unsupervised at high risk; forbidden-tool attempts always
escalate.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from auto_client_acquisition.agent_os.agent_card import AgentCard


class EscalationTrigger(StrEnum):
    NONE = "none"
    FORBIDDEN_TOOL = "forbidden_tool_attempt"
    HIGH_RISK = "high_risk"
    REPEATED_FAILURE = "repeated_failure"
    LOW_CONFIDENCE = "low_confidence"


@dataclass(frozen=True, slots=True)
class EscalationDecision:
    escalate: bool
    trigger: str
    supervisor: str
    reason: str


def evaluate_escalation(
    *,
    agent_id: str,
    risk_level: str = "low",
    failure_count: int = 0,
    confidence: float = 1.0,
    forbidden_tool_attempted: bool = False,
    supervisor: str = "",
    failure_threshold: int = 3,
    confidence_floor: float = 0.6,
) -> EscalationDecision:
    """Decide whether ``agent_id`` must escalate to a human supervisor.

    Trigger precedence: forbidden tool > high risk > repeated failure >
    low confidence.
    """
    trigger = EscalationTrigger.NONE
    if forbidden_tool_attempted:
        trigger = EscalationTrigger.FORBIDDEN_TOOL
    elif risk_level == "high":
        trigger = EscalationTrigger.HIGH_RISK
    elif failure_count >= failure_threshold:
        trigger = EscalationTrigger.REPEATED_FAILURE
    elif confidence < confidence_floor:
        trigger = EscalationTrigger.LOW_CONFIDENCE

    if trigger is EscalationTrigger.NONE:
        return EscalationDecision(
            escalate=False,
            trigger=trigger.value,
            supervisor=supervisor,
            reason=f"agent {agent_id} within autonomous limits",
        )

    reason = f"agent {agent_id} escalated: {trigger.value}"
    if not supervisor.strip():
        reason = f"{reason}; no_supervisor_assigned"
    return EscalationDecision(
        escalate=True,
        trigger=trigger.value,
        supervisor=supervisor,
        reason=reason,
    )


def escalation_for_card(
    card: AgentCard,
    *,
    failure_count: int = 0,
    confidence: float = 1.0,
    forbidden_tool_attempted: bool = False,
) -> EscalationDecision:
    """Evaluate escalation using an agent card's risk level + kill-switch owner."""
    return evaluate_escalation(
        agent_id=card.agent_id,
        risk_level=card.risk_level,
        failure_count=failure_count,
        confidence=confidence,
        forbidden_tool_attempted=forbidden_tool_attempted,
        supervisor=card.kill_switch_owner,
    )


__all__ = [
    "EscalationDecision",
    "EscalationTrigger",
    "escalation_for_card",
    "evaluate_escalation",
]
