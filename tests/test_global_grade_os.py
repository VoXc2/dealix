"""Tests for global_grade_os."""

from __future__ import annotations

from auto_client_acquisition.global_grade_os import (
    CapabilityIndexProfile,
    describe_agent_policy,
    governance_runtime_maturity_score,
    highest_satisfied_trust_level,
    transformation_decision,
    trust_level_satisfied,
)


def test_transformation_table() -> None:
    assert transformation_decision(gap_high=True, feasibility_high=True) == "sprint_now"
    assert transformation_decision(gap_high=True, feasibility_high=False) == "diagnostic_first"
    assert transformation_decision(gap_high=False, feasibility_high=True) == "quick_win"
    assert transformation_decision(gap_high=False, feasibility_high=False) == "deprioritize"


def test_capability_gap() -> None:
    cur = CapabilityIndexProfile(1, 1, 1, 1, 1, 1, 1)
    tgt = CapabilityIndexProfile(3, 3, 3, 3, 3, 3, 3)
    assert cur.transformation_gap(tgt) == 14


def test_trust_ladder() -> None:
    impl = frozenset({"data_handling_policy", "ai_usage_policy", "no_unsafe_automation_commitment", "proof_standard"})
    assert trust_level_satisfied(1, impl) is True
    assert highest_satisfied_trust_level(impl) >= 1


def test_governance_maturity_reexport() -> None:
    assert governance_runtime_maturity_score(frozenset()) == 0


def test_agent_policy() -> None:
    mx, ce = describe_agent_policy(enterprise_customer=False)
    assert mx >= ce
