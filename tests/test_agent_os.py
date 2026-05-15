"""Agent OS — governed agent identity + tool-boundary contracts."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    ALLOWED_TOOLS_MVP,
    FORBIDDEN_TOOLS_MVP,
    AgentCard,
    AgentLifecycleState,
    AutonomyLevel,
    agent_card_valid,
    clear_agent_registry_for_tests,
    get_agent,
    lifecycle_allows_production_tools,
    list_agents,
    register_agent,
    tool_allowed_mvp,
)


@pytest.fixture(autouse=True)
def _isolated():
    clear_agent_registry_for_tests()
    yield
    clear_agent_registry_for_tests()


def _card(agent_id: str = "agt-001", **over) -> AgentCard:
    base = dict(
        agent_id=agent_id,
        name="Revenue Intel",
        owner="founder",
        purpose="rank Saudi B2B accounts",
        autonomy_level=int(AutonomyLevel.ANALYZE),
        status="proposed",
    )
    base.update(over)
    return AgentCard(**base)


def test_autonomy_levels_are_a_0_to_4_ladder():
    assert int(AutonomyLevel.READ_ONLY) == 0
    assert int(AutonomyLevel.QUEUE_FOR_APPROVAL) == 4


def test_valid_card_passes_validation():
    assert agent_card_valid(_card()) is True


def test_card_missing_owner_is_invalid():
    assert agent_card_valid(_card(owner="")) is False


def test_card_missing_purpose_is_invalid():
    assert agent_card_valid(_card(purpose="")) is False


def test_card_autonomy_out_of_range_is_invalid():
    assert agent_card_valid(_card(autonomy_level=9)) is False


def test_register_and_get_roundtrip():
    register_agent(_card("agt-100"))
    got = get_agent("agt-100")
    assert got is not None
    assert got.name == "Revenue Intel"


def test_register_invalid_card_raises():
    with pytest.raises(ValueError):
        register_agent(_card("agt-x", owner=""))


def test_list_agents_returns_registered():
    register_agent(_card("a1"))
    register_agent(_card("a2"))
    agents = list_agents()
    assert set(agents) == {"a1", "a2"}


def test_forbidden_tools_are_blocked():
    assert tool_allowed_mvp("send_whatsapp") is False
    assert tool_allowed_mvp("web_scrape") is False
    assert "send_email" in FORBIDDEN_TOOLS_MVP


def test_allowed_tools_pass():
    assert tool_allowed_mvp("read") is True
    assert tool_allowed_mvp("queue_for_approval") is True
    assert "draft" in ALLOWED_TOOLS_MVP


def test_unknown_tool_is_not_allowed():
    assert tool_allowed_mvp("teleport") is False


def test_only_production_lifecycle_allows_production_tools():
    assert lifecycle_allows_production_tools(AgentLifecycleState.PRODUCTION) is True
    assert lifecycle_allows_production_tools(AgentLifecycleState.DRAFT) is False
    assert lifecycle_allows_production_tools(AgentLifecycleState.SUSPENDED) is False
