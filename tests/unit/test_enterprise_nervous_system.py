"""Unit tests for Enterprise Nervous System capability scoring."""

from __future__ import annotations

from auto_client_acquisition.agentic_operations_os.enterprise_nervous_system import (
    ASSESSMENT_SYSTEMS_COUNT,
    CORE_SYSTEMS,
    assess_enterprise_nervous_system,
)


def test_assessment_defaults_missing_scores_to_zero() -> None:
    out = assess_enterprise_nervous_system(system_scores={})
    assert out.overall_score == 0.0
    assert out.maturity_band == "feature_led"
    assert out.governed_autonomy_ready is False
    assert len(out.systems) == ASSESSMENT_SYSTEMS_COUNT


def test_assessment_marks_governed_autonomy_ready_on_high_control_scores() -> None:
    scores = {item.system_id: 80.0 for item in CORE_SYSTEMS}
    out = assess_enterprise_nervous_system(system_scores=scores)
    assert out.overall_score == 80.0
    assert out.maturity_band == "agentic_operator"
    assert out.governed_autonomy_ready is True


def test_assessment_returns_top_five_weakest_systems_and_moves() -> None:
    scores = {item.system_id: 90.0 for item in CORE_SYSTEMS}
    scores["observability_system"] = 20.0
    scores["evaluation_system"] = 25.0
    scores["governance_operating_system"] = 30.0
    scores["execution_system"] = 35.0
    scores["workflow_orchestration_system"] = 40.0
    out = assess_enterprise_nervous_system(system_scores=scores)
    assert out.weakest_systems[0] == "observability_system"
    assert len(out.weakest_systems) == 5
    assert len(out.prioritized_next_moves_ar) == 5


def test_architecture_coverage_uses_target_system_count() -> None:
    scores = {item.system_id: 60.0 for item in CORE_SYSTEMS}
    out = assess_enterprise_nervous_system(system_scores=scores, target_systems_count=24)
    assert out.architecture_coverage_percent == 50.0
