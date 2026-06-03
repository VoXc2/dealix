"""Contract: MVP autonomy levels are capped at 3."""

from __future__ import annotations

from auto_client_acquisition.standards_os.agent_control_standard import (
    MVP_AUTONOMY_LEVEL_MAX,
    agent_autonomy_allowed_in_mvp,
)


def test_agent_autonomy_mvp_limit() -> None:
    assert MVP_AUTONOMY_LEVEL_MAX == 3
    assert agent_autonomy_allowed_in_mvp(3) is True
    assert agent_autonomy_allowed_in_mvp(4) is False
