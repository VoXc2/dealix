"""Agent sovereignty — MVP autonomy + extended card checks."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.endgame_os.agent_control import (
    MVP_AUTONOMY_CEILING,
    AgentControlCard,
    validate_agent_card,
)


@dataclass(frozen=True, slots=True)
class AgentSovereigntyCard:
    base: AgentControlCard
    allowed_tools: frozenset[str]
    forbidden_actions_enumerated: frozenset[str]
    decommission_rule: str

    def __post_init__(self) -> None:
        if not self.decommission_rule.strip():
            msg = "decommission_rule required"
            raise ValueError(msg)


def validate_agent_sovereignty(card: AgentSovereigntyCard) -> tuple[bool, tuple[str, ...]]:
    ok, errs = validate_agent_card(card.base)
    extra: list[str] = []
    if not card.allowed_tools:
        extra.append("allowed_tools_required")
    if card.base.autonomy_level > MVP_AUTONOMY_CEILING:
        extra.append("mvp_autonomy_exceeded")
    return ok and not extra, (*errs, *extra)
