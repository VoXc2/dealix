"""Tests for enterprise_rollout_os."""

from __future__ import annotations

from auto_client_acquisition.enterprise_rollout_os import (
    ENTERPRISE_ADOPTION_GATES,
    ENTERPRISE_ROLLOUT_CONTROLS,
    ENTERPRISE_ROLLOUT_RISK_IDS,
    ENTERPRISE_ROLLOUT_ROLES,
    PLATFORM_PULL_SIGNALS,
    ROLLOUT_DASHBOARD_SIGNALS,
    ROLLOUT_KIT_ITEMS,
    ROLLOUT_STAGES,
    enterprise_gate_passes,
    platform_pull_coverage_score,
    rollout_dashboard_coverage_score,
    rollout_kit_coverage_score,
    rollout_next_stage,
    rollout_stage_index,
)


def test_rollout_stages() -> None:
    assert rollout_stage_index("land") == 0
    assert rollout_next_stage("prove") == "adopt"
    assert rollout_next_stage("institutionalize") is None


def test_enterprise_gates() -> None:
    sponsor_ok = frozenset(ENTERPRISE_ADOPTION_GATES["sponsor"])
    assert enterprise_gate_passes("sponsor", sponsor_ok) == (True, ())
    assert not enterprise_gate_passes("sponsor", frozenset())[0]


def test_rollout_kit() -> None:
    assert rollout_kit_coverage_score(frozenset(ROLLOUT_KIT_ITEMS)) == 100


def test_platform_pull() -> None:
    assert platform_pull_coverage_score(frozenset(PLATFORM_PULL_SIGNALS)) == 100


def test_rollout_dashboard() -> None:
    assert rollout_dashboard_coverage_score(frozenset(ROLLOUT_DASHBOARD_SIGNALS)) == 100


def test_registry_counts() -> None:
    assert len(ROLLOUT_STAGES) == 7
    assert len(ENTERPRISE_ADOPTION_GATES) == 7
    assert len(ENTERPRISE_ROLLOUT_ROLES) == 6
    assert len(ENTERPRISE_ROLLOUT_RISK_IDS) == 10
    assert len(ENTERPRISE_ROLLOUT_CONTROLS) == 10
