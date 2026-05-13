"""Agent Sovereignty — MVP autonomy gate over endgame Agent Cards.

See ``docs/sovereignty/AGENT_SOVEREIGNTY.md``. Dealix MVP allows
autonomy levels 0–3 only.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.endgame_os.agent_control import (
    AgentCard,
    AutonomyLevel,
)


# Dealix MVP allows autonomy levels 0..3 only. The card-construction
# layer already forbids level 6; this module enforces the MVP rule.
SOVEREIGN_AGENT_MVP_LEVELS: tuple[AutonomyLevel, ...] = (
    AutonomyLevel.READ,
    AutonomyLevel.ANALYZE,
    AutonomyLevel.DRAFT_RECOMMEND,
    AutonomyLevel.QUEUE_FOR_APPROVAL,
)


@dataclass(frozen=True)
class SovereignAgentDecision:
    allowed_under_mvp: bool
    requires_enterprise_uplift: bool
    reason: str


def evaluate_sovereign_agent(card: AgentCard) -> SovereignAgentDecision:
    if card.autonomy_level in SOVEREIGN_AGENT_MVP_LEVELS:
        return SovereignAgentDecision(
            allowed_under_mvp=True,
            requires_enterprise_uplift=False,
            reason="within_mvp_autonomy_band",
        )
    if card.autonomy_level is AutonomyLevel.EXECUTE_INTERNAL_AFTER_APPROVAL:
        return SovereignAgentDecision(
            allowed_under_mvp=False,
            requires_enterprise_uplift=True,
            reason="level_4_requires_contract_clause",
        )
    if card.autonomy_level is AutonomyLevel.EXTERNAL_RESTRICTED:
        return SovereignAgentDecision(
            allowed_under_mvp=False,
            requires_enterprise_uplift=True,
            reason="level_5_enterprise_only",
        )
    # Level 6 is constitutionally forbidden by AgentCard.__post_init__,
    # so reaching here means the card was constructed incorrectly.
    return SovereignAgentDecision(
        allowed_under_mvp=False,
        requires_enterprise_uplift=False,
        reason="autonomy_level_forbidden",
    )
