from __future__ import annotations

from auto_client_acquisition.scale_os.scale_dominance_audit import (
    FinalScaleInputs,
    report_as_dict,
    run_final_scale_test,
)


def _golden_inputs() -> FinalScaleInputs:
    return FinalScaleInputs(
        workflows_running=14,
        workflow_chaos_incidents_last_30d=0,
        agents_active=22,
        governed_agent_ratio=1.0,
        isolated_clients=3,
        memory_contamination_incidents_last_30d=0,
        rollback_time_minutes_p95=4.0,
        proactive_failure_detection_rate=0.96,
        dangerous_agent_stop_time_seconds_p95=22.0,
        explainability_coverage_ratio=0.995,
        executive_insights_emitted_last_30d=5,
        workflow_optimization_improvement_ratio=0.08,
        business_impact_accuracy_ratio=0.94,
    )


def test_final_scale_test_passes_when_all_thresholds_met() -> None:
    report = run_final_scale_test(_golden_inputs())
    assert report.verdict == "scale_ready"
    assert report.passed_count == 10
    assert report.failed_count == 0
    assert report.readiness_score == 1.0
    assert report.recommendations == ()


def test_final_scale_test_returns_targeted_recommendations_on_failures() -> None:
    report = run_final_scale_test(
        FinalScaleInputs(
            workflows_running=8,
            workflow_chaos_incidents_last_30d=3,
            agents_active=18,
            governed_agent_ratio=0.9,
            isolated_clients=2,
            memory_contamination_incidents_last_30d=1,
            rollback_time_minutes_p95=7.2,
            proactive_failure_detection_rate=0.71,
            dangerous_agent_stop_time_seconds_p95=120.0,
            explainability_coverage_ratio=0.8,
            executive_insights_emitted_last_30d=2,
            workflow_optimization_improvement_ratio=0.01,
            business_impact_accuracy_ratio=0.65,
        )
    )
    assert report.verdict == "not_scale_ready"
    assert report.failed_count == 10
    assert report.passed_count == 0
    assert len(report.recommendations) == 10


def test_ratio_out_of_bounds_fails_criteria() -> None:
    report = run_final_scale_test(
        FinalScaleInputs(
            workflows_running=14,
            workflow_chaos_incidents_last_30d=0,
            agents_active=24,
            governed_agent_ratio=1.0,
            isolated_clients=3,
            memory_contamination_incidents_last_30d=0,
            rollback_time_minutes_p95=3.5,
            proactive_failure_detection_rate=1.2,
            dangerous_agent_stop_time_seconds_p95=30.0,
            explainability_coverage_ratio=0.99,
            executive_insights_emitted_last_30d=4,
            workflow_optimization_improvement_ratio=0.06,
            business_impact_accuracy_ratio=0.93,
        )
    )
    failed_ids = {criterion.criterion_id for criterion in report.criteria if not criterion.passed}
    assert failed_ids == {"detect_failures_before_customer"}


def test_report_as_dict_is_json_friendly() -> None:
    payload = report_as_dict(run_final_scale_test(_golden_inputs()))
    assert payload["verdict"] == "scale_ready"
    assert isinstance(payload["criteria"], list)
    assert isinstance(payload["recommendations"], list)
