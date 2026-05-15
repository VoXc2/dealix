"""Agent transparency card — no invisible or unowned agents on client outputs."""

from __future__ import annotations

from dataclasses import dataclass

_AUTONOMY_MAX = 6


@dataclass(frozen=True, slots=True)
class AgentTransparencyCard:
    agent: str
    task: str
    autonomy_level: int
    human_owner: str
    external_action_allowed: bool
    approval_required: bool
    audit_event: str


def agent_transparency_card_valid(card: AgentTransparencyCard) -> bool:
    if not (
        card.agent.strip()
        and card.task.strip()
        and card.human_owner.strip()
        and card.audit_event.strip()
    ):
        return False
    if not 0 <= card.autonomy_level <= _AUTONOMY_MAX:
        return False
    if card.external_action_allowed and not card.approval_required:
        return False
    return True
