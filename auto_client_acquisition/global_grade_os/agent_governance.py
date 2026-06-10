"""Agent governance — MVP vs enterprise autonomy ceilings."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import (
    AUTONOMY_LEVEL_MAX,
    ENTERPRISE_EXTENDED_MAX,
    MVP_AUTONOMY_CEILING,
    autonomy_allowed,
)

AGENT_MVP_RULE = "Allowed autonomy levels: 0–3 internal MVP; 4 enterprise; 5 restricted external; 6 forbidden."


def describe_agent_policy(*, enterprise_customer: bool) -> tuple[int, int]:
    """Return (max_allowed_level, mvp_ceiling)."""
    ceiling = ENTERPRISE_EXTENDED_MAX if enterprise_customer else MVP_AUTONOMY_CEILING
    return AUTONOMY_LEVEL_MAX, ceiling


__all__ = [
    "AGENT_MVP_RULE",
    "AUTONOMY_LEVEL_MAX",
    "ENTERPRISE_EXTENDED_MAX",
    "MVP_AUTONOMY_CEILING",
    "autonomy_allowed",
    "describe_agent_policy",
]
