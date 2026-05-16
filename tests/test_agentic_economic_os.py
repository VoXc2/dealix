"""Tests for the Agentic Economic Operating Layer (systems 46-55)."""

from __future__ import annotations

from auto_client_acquisition.agentic_economic_os import (
    FINAL_CIVILIZATIONAL_SYSTEMS,
    DependencySignals,
    InfrastructureThresholds,
    all_required_platform_paths,
    compute_dependency_scorecard,
    infrastructure_status,
    platform_readiness_snapshot,
)


def test_registry_contains_systems_46_to_55() -> None:
    ids = [system.system_id for system in FINAL_CIVILIZATIONAL_SYSTEMS]
    assert ids == list(range(46, 56))
    assert len(all_required_platform_paths()) >= 35


def test_dependency_scorecard_high_dependency() -> None:
    scorecard = compute_dependency_scorecard(
        DependencySignals(
            core_processes_on_dealix=19,
            core_processes_total=20,
            workflows_total=100,
            traceable_workflows=99,
            pausable_workflows=97,
            rollbackable_workflows=94,
            auditable_workflows=98,
            reroutable_workflows=95,
            governed_external_actions=970,
            external_actions_total=980,
            self_healed_failures=85,
            failures_total=100,
            executive_decisions_via_dealix=72,
            executive_decisions_total=90,
            bypass_attempts_blocked=100,
            bypass_attempts_total=101,
        ),
    )
    assert scorecard.organizational_dependency_index >= 85
    assert scorecard.no_bypass_rate_pct >= 99


def test_infrastructure_status_requires_hard_gates() -> None:
    signals = DependencySignals(
        core_processes_on_dealix=16,
        core_processes_total=20,
        workflows_total=100,
        traceable_workflows=95,
        pausable_workflows=94,
        rollbackable_workflows=91,
        auditable_workflows=96,
        reroutable_workflows=93,
        governed_external_actions=900,
        external_actions_total=920,
        self_healed_failures=74,
        failures_total=90,
        executive_decisions_via_dealix=61,
        executive_decisions_total=90,
        bypass_attempts_blocked=98,
        bypass_attempts_total=100,
    )
    status = infrastructure_status(signals)
    assert status["infrastructure_status"] is True

    strict_status = infrastructure_status(
        signals,
        thresholds=InfrastructureThresholds(no_bypass_min=99.5),
    )
    assert strict_status["infrastructure_status"] is False
    assert strict_status["gate_results"]["no_bypass_gate"] is False


def test_platform_readiness_snapshot_detects_missing_paths(tmp_path) -> None:
    repo_root = tmp_path
    (repo_root / "platform" / "execution_fabric").mkdir(parents=True)
    (repo_root / "platform" / "operational_coordination").mkdir(parents=True)
    (repo_root / "platform" / "trust_fabric").mkdir(parents=True)

    snapshot = platform_readiness_snapshot(repo_root)
    assert snapshot["required_paths_total"] >= 35
    assert snapshot["covered_paths"] == 3
    assert "platform/execution_chains" in snapshot["missing_paths"]
