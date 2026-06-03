"""Agent control plane — MVP autonomy ceiling and card validation."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import (
    MVP_AUTONOMY_CEILING,
    AgentControlCard,
    validate_agent_card,
)


def agent_control_plane_mvp_valid(
    card: AgentControlCard,
) -> tuple[bool, tuple[str, ...]]:
    """Dealix MVP: autonomy levels 0–3 only."""
    ok, errs = validate_agent_card(card)
    if not ok:
        return False, errs
    if card.autonomy_level > MVP_AUTONOMY_CEILING:
        return False, ("mvp_autonomy_ceiling_exceeded",)
    return True, ()
