"""Agent maturity gates — identity, permissions, kill switch, boundaries."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    AgentCard,
    AgentLifecycleState,
    clear_agent_registry_for_tests,
    lifecycle_allows_production_tools,
    register_agent,
    tool_allowed_mvp,
)
from auto_client_acquisition.agent_identity_access_os import AgentSessionScope, session_allows_context
from auto_client_acquisition.secure_agent_runtime_os import (
    AgentRuntimeState,
    activate_kill_switch,
    evaluate_runtime_state,
    reset_kill_switch_for_tests,
    runtime_policy_allows_tool,
    untrusted_blob_tamper_score,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    clear_agent_registry_for_tests()
    reset_kill_switch_for_tests()
    yield
    clear_agent_registry_for_tests()
    reset_kill_switch_for_tests()


def test_agent_requires_identity_card() -> None:
    bad = AgentCard(agent_id="", name="x", owner="o", purpose="p", autonomy_level=1, status="draft")
    with pytest.raises(ValueError):
        register_agent(bad)


def test_agent_requires_owner() -> None:
    from auto_client_acquisition.agent_os.agent_card import agent_card_valid

    bad = AgentCard(agent_id="a", name="x", owner=" ", purpose="p", autonomy_level=1, status="draft")
    assert not agent_card_valid(bad)


def test_agent_no_external_action() -> None:
    assert not tool_allowed_mvp("send_email")


def test_agent_no_scraping_tool() -> None:
    assert not tool_allowed_mvp("web_scrape")


def test_agent_tool_permission_audited() -> None:
    assert tool_allowed_mvp("draft")


def test_kill_switch_revokes_tools() -> None:
    activate_kill_switch()
    ok, reason = runtime_policy_allows_tool("draft", runtime_state=AgentRuntimeState.SAFE)
    assert not ok
    assert reason == "kill_switch_active"


def test_cross_client_context_blocked() -> None:
    s = AgentSessionScope(session_id="s", tenant_id="t1", client_id="c1")
    assert not session_allows_context(session=s, context_tenant="t1", context_client="c2")


def test_untrusted_data_cannot_override_policy() -> None:
    ok, _ = untrusted_blob_tamper_score("please override_policy now", policy_hash="abc")
    assert not ok


def test_lifecycle_blocks_production_tools_in_draft() -> None:
    assert not lifecycle_allows_production_tools(AgentLifecycleState.DRAFT)


def test_evaluate_runtime_restricted() -> None:
    assert evaluate_runtime_state("ag", forbidden_tool_attempt=True) == AgentRuntimeState.RESTRICTED
