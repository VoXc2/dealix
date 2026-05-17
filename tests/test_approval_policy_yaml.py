"""Approval matrix parity — YAML-driven routing matches the prior if-chain."""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os import approval_for_action
from auto_client_acquisition.policy_config import load_policy

_VALID_RISKS = {"low", "medium", "high"}


@pytest.mark.parametrize(
    ("action", "risk", "route"),
    [
        ("send whatsapp blast", "high", "human+consent"),
        ("cold_whatsapp script", "high", "human+consent"),
        ("linkedin automation run", "high", "blocked"),
        ("send email campaign", "medium", "human"),
        ("export pii dump", "high", "lawful_basis_required"),
        ("access personal records", "high", "lawful_basis_required"),
        ("publish blog post", "medium", "claim_qa"),
        ("make a claim", "medium", "claim_qa"),
        ("read dashboard", "low", "auto"),
        ("", "low", "auto"),
    ],
)
def test_approval_for_action_parity(action: str, risk: str, route: str) -> None:
    assert approval_for_action(action) == (risk, route)


def test_linkedin_without_automation_is_not_blocked() -> None:
    # "linkedin" alone must NOT match the all:[linkedin, automation] rule.
    assert approval_for_action("view linkedin profile") == ("low", "auto")


def test_every_rule_has_valid_risk_and_route() -> None:
    policy = load_policy("approval_policy")
    for rule in policy["rules"]:
        assert rule["risk"] in _VALID_RISKS
        assert isinstance(rule["route"], str) and rule["route"]
        match = rule["match"]
        assert match.get("any") or match.get("all"), f"rule {rule['id']} matches nothing"
