"""Dealix scale dominance audit.

Transforms strategic scale principles into deterministic pass/fail gates.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class FinalScaleInputs:
    """Observable metrics for the 10-point final scale test."""

    workflows_running: int
    workflow_chaos_incidents_last_30d: int
    agents_active: int
    governed_agent_ratio: float
    isolated_clients: int
    memory_contamination_incidents_last_30d: int
    rollback_time_minutes_p95: float
    proactive_failure_detection_rate: float
    dangerous_agent_stop_time_seconds_p95: float
    explainability_coverage_ratio: float
    executive_insights_emitted_last_30d: int
    workflow_optimization_improvement_ratio: float
    business_impact_accuracy_ratio: float


@dataclass(frozen=True, slots=True)
class ScaleCriterionResult:
    """Result for one scale criterion."""

    criterion_id: str
    passed: bool
    observed_value: float | int
    threshold: str
    rationale: str


@dataclass(frozen=True, slots=True)
class ScaleAuditReport:
    """Structured output for operational + executive review."""

    verdict: str
    readiness_score: float
    passed_count: int
    failed_count: int
    criteria: tuple[ScaleCriterionResult, ...]
    recommendations: tuple[str, ...]


def _ratio_in_bounds(value: float) -> bool:
    return 0.0 <= value <= 1.0


def _recommendation_map(criterion_id: str) -> str:
    mapping = {
        "workflows_10_plus_no_chaos": "Harden workflow templates, owners, and retry isolation.",
        "agents_20_plus_fully_governed": "Block non-registered agents and enforce permission mirroring.",
        "clients_3_plus_without_memory_contamination": (
            "Enforce tenant-scoped memory retrieval and lineage checks."
        ),
        "rollback_within_minutes": "Pre-build rollback bundles and automate release reversibility drills.",
        "detect_failures_before_customer": "Raise proactive alert coverage and synthetic failure probes.",
        "stop_dangerous_agents_immediately": "Wire kill-switch hooks to runtime policy and supervision mesh.",
        "explain_all_decisions": "Require audit + rationale envelope for every external-impact action.",
        "weekly_executive_insights": "Schedule weekly executive packet generation with delivery SLO.",
        "improve_workflows_over_time": "Activate workflow learning loop and meta-tool optimization cycle.",
        "measure_business_impact_accurately": "Backfill impact labels and calibrate forecasting confidence.",
    }
    return mapping[criterion_id]


def run_final_scale_test(inputs: FinalScaleInputs) -> ScaleAuditReport:
    """Evaluate Dealix against the final 10 scale-dominance gates."""

    criteria: list[ScaleCriterionResult] = [
        ScaleCriterionResult(
            criterion_id="workflows_10_plus_no_chaos",
            passed=inputs.workflows_running >= 10 and inputs.workflow_chaos_incidents_last_30d == 0,
            observed_value=inputs.workflows_running,
            threshold="workflows >= 10 and chaos incidents == 0",
            rationale=(
                "Workflow count must scale without orchestration collisions over a 30-day window."
            ),
        ),
        ScaleCriterionResult(
            criterion_id="agents_20_plus_fully_governed",
            passed=inputs.agents_active >= 20 and inputs.governed_agent_ratio >= 1.0,
            observed_value=inputs.agents_active,
            threshold="agents >= 20 and governed ratio == 1.0",
            rationale="Every active agent must be registered, observable, and rollbackable.",
        ),
        ScaleCriterionResult(
            criterion_id="clients_3_plus_without_memory_contamination",
            passed=inputs.isolated_clients >= 3
            and inputs.memory_contamination_incidents_last_30d == 0,
            observed_value=inputs.isolated_clients,
            threshold="isolated clients >= 3 and contamination incidents == 0",
            rationale="Tenant isolation must hold under concurrent multi-client execution.",
        ),
        ScaleCriterionResult(
            criterion_id="rollback_within_minutes",
            passed=inputs.rollback_time_minutes_p95 <= 5.0,
            observed_value=inputs.rollback_time_minutes_p95,
            threshold="rollback p95 <= 5 minutes",
            rationale="Release failures must be reversible before business impact compounds.",
        ),
        ScaleCriterionResult(
            criterion_id="detect_failures_before_customer",
            passed=inputs.proactive_failure_detection_rate >= 0.95
            and _ratio_in_bounds(inputs.proactive_failure_detection_rate),
            observed_value=inputs.proactive_failure_detection_rate,
            threshold="proactive detection rate >= 0.95",
            rationale="Incidents should be detected internally before customer reports.",
        ),
        ScaleCriterionResult(
            criterion_id="stop_dangerous_agents_immediately",
            passed=inputs.dangerous_agent_stop_time_seconds_p95 <= 60.0,
            observed_value=inputs.dangerous_agent_stop_time_seconds_p95,
            threshold="kill-switch stop p95 <= 60 seconds",
            rationale="Unsafe agents require deterministic emergency stop guarantees.",
        ),
        ScaleCriterionResult(
            criterion_id="explain_all_decisions",
            passed=inputs.explainability_coverage_ratio >= 0.99
            and _ratio_in_bounds(inputs.explainability_coverage_ratio),
            observed_value=inputs.explainability_coverage_ratio,
            threshold="explainability coverage >= 0.99",
            rationale="Every material action must be auditable and explainable.",
        ),
        ScaleCriterionResult(
            criterion_id="weekly_executive_insights",
            passed=inputs.executive_insights_emitted_last_30d >= 4,
            observed_value=inputs.executive_insights_emitted_last_30d,
            threshold="executive insights emitted >= 4 per 30 days",
            rationale="Executive operating cadence must be continuous and automatic.",
        ),
        ScaleCriterionResult(
            criterion_id="improve_workflows_over_time",
            passed=inputs.workflow_optimization_improvement_ratio >= 0.05
            and _ratio_in_bounds(inputs.workflow_optimization_improvement_ratio),
            observed_value=inputs.workflow_optimization_improvement_ratio,
            threshold="workflow improvement ratio >= 0.05",
            rationale="Self-evolving orchestration must produce measurable improvement.",
        ),
        ScaleCriterionResult(
            criterion_id="measure_business_impact_accurately",
            passed=inputs.business_impact_accuracy_ratio >= 0.9
            and _ratio_in_bounds(inputs.business_impact_accuracy_ratio),
            observed_value=inputs.business_impact_accuracy_ratio,
            threshold="business impact accuracy >= 0.9",
            rationale="Operational intelligence needs calibrated impact measurement.",
        ),
    ]

    passed_count = sum(1 for criterion in criteria if criterion.passed)
    failed = [criterion for criterion in criteria if not criterion.passed]
    readiness_score = round(passed_count / len(criteria), 4)
    verdict = "scale_ready" if passed_count == len(criteria) else "not_scale_ready"
    recommendations = tuple(_recommendation_map(criterion.criterion_id) for criterion in failed)

    return ScaleAuditReport(
        verdict=verdict,
        readiness_score=readiness_score,
        passed_count=passed_count,
        failed_count=len(failed),
        criteria=tuple(criteria),
        recommendations=recommendations,
    )


def report_as_dict(report: ScaleAuditReport) -> dict[str, object]:
    """Convert report dataclasses to plain dictionaries for JSON logging."""

    payload = asdict(report)
    payload["criteria"] = [asdict(c) for c in report.criteria]
    payload["recommendations"] = list(report.recommendations)
    return payload


__all__ = [
    "FinalScaleInputs",
    "ScaleAuditReport",
    "ScaleCriterionResult",
    "report_as_dict",
    "run_final_scale_test",
]
