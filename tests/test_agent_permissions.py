"""Agent OS — role & permission matrix (task 2)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    AutonomyLevel,
    OperationType,
    card_permission,
    clear_for_test,
    evaluate_permission,
    new_card,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_unknown_role_denied():
    result = evaluate_permission("ghost", OperationType.READ)
    assert result.decision == "deny"
    assert result.allowed is False


def test_analyst_can_read_and_analyze():
    assert evaluate_permission("analyst", OperationType.READ).allowed is True
    assert evaluate_permission("analyst", OperationType.ANALYZE).allowed is True
    assert evaluate_permission("analyst", OperationType.EXECUTE).decision == "deny"


def test_execute_needs_approval_below_l4():
    low = evaluate_permission(
        "executor", OperationType.EXECUTE, autonomy_level=AutonomyLevel.L2_DRAFT,
    )
    assert low.decision == "needs_approval"
    high = evaluate_permission(
        "executor", OperationType.EXECUTE, autonomy_level=AutonomyLevel.L4_AUTO_WITH_AUDIT,
    )
    assert high.decision == "allow"


def test_forbidden_tool_overrides_role_allow():
    result = evaluate_permission("admin", OperationType.READ, tool="web_scrape")
    assert result.decision == "deny"
    assert "hard-blocked" in result.reason


def test_card_permission_uses_card_role_and_tools():
    card = new_card(
        agent_id="agt-perm",
        name="Perm Agent",
        owner="founder",
        purpose="evaluate permissions",
        role="executor",
        allowed_tools=["read", "draft"],
    )
    assert card_permission(card, OperationType.READ, tool="read").allowed is True
    blocked = card_permission(card, OperationType.READ, tool="analyze")
    assert blocked.decision == "deny"  # analyze not in the card's allowed_tools


def test_admin_role_broad_allow():
    # APPROVE is not autonomy-gated — admin gets a straight ALLOW.
    assert evaluate_permission("admin", OperationType.APPROVE).allowed is True
    # DELETE is autonomy-gated: needs approval below L4, allowed at L4+.
    assert evaluate_permission("admin", OperationType.DELETE).decision == "needs_approval"
    assert evaluate_permission(
        "admin", OperationType.DELETE, autonomy_level=AutonomyLevel.L4_AUTO_WITH_AUDIT,
    ).allowed is True
