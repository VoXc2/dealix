"""Agent risk board — autonomy tiers for MVP vs enterprise."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import (
    AUTONOMY_LEVEL_MAX,
    autonomy_allowed,
)


def agent_autonomy_board_allowed(
    autonomy_level: int,
    *,
    enterprise_tier: bool,
    mvp_organization: bool,
) -> tuple[bool, tuple[str, ...]]:
    """
    Board rules: MVP org allows 0–3; 4–5 need enterprise tier; 6 forbidden.
    """
    errors: list[str] = []
    if autonomy_level < 0 or autonomy_level > AUTONOMY_LEVEL_MAX:
        errors.append("autonomy_level_out_of_range")
        return False, tuple(errors)
    if autonomy_level == AUTONOMY_LEVEL_MAX:
        errors.append("autonomy_level_forbidden")
        return False, tuple(errors)
    if mvp_organization and autonomy_level > 3:
        errors.append("mvp_requires_autonomy_lte_3")
        return False, tuple(errors)
    if not autonomy_allowed(autonomy_level, enterprise_tier=enterprise_tier):
        errors.append("enterprise_tier_required_for_autonomy_level")
        return False, tuple(errors)
    return True, ()
