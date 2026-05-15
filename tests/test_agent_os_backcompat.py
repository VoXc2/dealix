"""Agent OS — backward-compat contract for pre-Wave-14F importers."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    AgentCard,
    AgentLifecycleState,
    AutonomyLevel,
    agent_card_valid,
    clear_agent_registry_for_tests,
    clear_for_test,
    lifecycle_allows_production_tools,
    register_agent,
    tool_allowed_mvp,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_old_exports_still_importable():
    assert callable(agent_card_valid)
    assert callable(lifecycle_allows_production_tools)
    assert AgentLifecycleState.PRODUCTION.value == "production"
    assert lifecycle_allows_production_tools(AgentLifecycleState.PRODUCTION) is True
    assert lifecycle_allows_production_tools(AgentLifecycleState.DRAFT) is False


def test_agent_card_legacy_constructor_positional_kwargs():
    card = AgentCard(
        agent_id="legacy-1",
        name="Legacy",
        owner="owner",
        purpose="p",
        autonomy_level=2,
        status="active",
    )
    assert card.agent_id == "legacy-1"
    assert agent_card_valid(card) is True
    assert card.kill_switch_owner == ""  # new field defaults safely


def test_register_agent_legacy_invalid_card_raises():
    bad = AgentCard(agent_id="", name="x", owner="o", purpose="p", autonomy_level=1, status="draft")
    with pytest.raises(ValueError):
        register_agent(bad)


def test_tool_allowed_mvp_still_boolean():
    assert tool_allowed_mvp("draft") is True
    assert tool_allowed_mvp("send_email") is False
    assert isinstance(tool_allowed_mvp("web_scrape"), bool)


def test_clear_agent_registry_for_tests_alias():
    assert clear_agent_registry_for_tests is clear_for_test


def test_autonomy_level_full_ladder_l0_to_l5():
    assert int(AutonomyLevel.L0_READ_ONLY) == 0
    assert int(AutonomyLevel.L4_AUTO_WITH_AUDIT) == 4
    assert int(AutonomyLevel.L5_FULLY_AUTONOMOUS) == 5
    assert [int(level) for level in AutonomyLevel] == [0, 1, 2, 3, 4, 5]
