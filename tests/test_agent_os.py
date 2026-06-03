"""Agent OS — Wave 14F."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    AgentStatus,
    AutonomyLevel,
    clear_for_test,
    get_agent,
    is_tool_allowed,
    kill_agent,
    list_agents,
    new_card,
    register_agent,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_new_card_requires_owner():
    with pytest.raises(ValueError):
        new_card(agent_id="a1", name="A", owner="", purpose="x")


def test_new_card_requires_purpose():
    with pytest.raises(ValueError):
        new_card(agent_id="a1", name="A", owner="founder", purpose="")


def test_l4_requires_kill_switch_owner():
    with pytest.raises(ValueError):
        new_card(
            agent_id="a1", name="A", owner="founder", purpose="x",
            autonomy_level=AutonomyLevel.L4_AUTO_WITH_AUDIT,
            kill_switch_owner="",
        )


def test_l5_blocked_in_mvp():
    with pytest.raises(ValueError):
        new_card(
            agent_id="a1", name="A", owner="founder", purpose="x",
            autonomy_level=AutonomyLevel.L5_FULLY_AUTONOMOUS,
            kill_switch_owner="founder",
        )


def test_allowed_tools_cannot_include_forbidden():
    with pytest.raises(ValueError):
        new_card(
            agent_id="a1", name="A", owner="founder", purpose="x",
            allowed_tools=["read", "send_email"],
        )


def test_register_and_get_roundtrip():
    card = new_card(
        agent_id="agt-001",
        name="Revenue Intel",
        owner="founder",
        purpose="rank Saudi B2B accounts",
        allowed_tools=["read", "analyze", "draft", "queue_for_approval"],
    )
    register_agent(card)
    got = get_agent("agt-001")
    assert got is not None
    assert got.name == "Revenue Intel"
    assert got.kill_switch_owner == "founder"


def test_duplicate_agent_id_rejected():
    card = new_card(agent_id="dup", name="A", owner="o", purpose="p")
    register_agent(card)
    with pytest.raises(ValueError):
        register_agent(card)


def test_kill_agent_sets_status_killed():
    card = new_card(agent_id="k1", name="A", owner="o", purpose="p")
    register_agent(card)
    out = kill_agent("k1", reason="manual override")
    assert out is not None
    assert out.status == AgentStatus.KILLED.value


def test_kill_requires_reason():
    card = new_card(agent_id="k2", name="A", owner="o", purpose="p")
    register_agent(card)
    with pytest.raises(ValueError):
        kill_agent("k2", reason="")


def test_tool_permissions_block_forbidden():
    ok, reason = is_tool_allowed("send_email")
    assert ok is False
    assert "hard-blocked" in reason

    ok, _ = is_tool_allowed("read", allowed_tools=["read", "analyze"])
    assert ok is True


def test_tool_permissions_block_unlisted():
    ok, _ = is_tool_allowed("draft", allowed_tools=["read"])
    assert ok is False


def test_list_agents_by_status():
    register_agent(new_card(agent_id="x1", name="A", owner="o", purpose="p"))
    register_agent(new_card(agent_id="x2", name="B", owner="o", purpose="p"))
    kill_agent("x2", reason="test")
    proposed = list_agents(status="proposed")
    killed = list_agents(status="killed")
    assert any(a.agent_id == "x1" for a in proposed)
    assert any(a.agent_id == "x2" for a in killed)
