"""Agent identity — MVP autonomy and card validation for scaling layer."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import AgentControlCard
from auto_client_acquisition.institutional_control_os.agent_control_plane import (
    agent_control_plane_mvp_valid,
)


def agent_identity_mvp_ok(card: AgentControlCard) -> tuple[bool, tuple[str, ...]]:
    """Institutional scaling: agents behave as governed identities (MVP ceiling 0–3)."""
    return agent_control_plane_mvp_valid(card)
