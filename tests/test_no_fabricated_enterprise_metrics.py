"""Contract: the Agentic Enterprise OS never fabricates metrics (Article 8).

عقد: نظام تشغيل المؤسسة الوكيلة لا يختلق أرقامًا عند غياب المصدر.
"""

from __future__ import annotations

from auto_client_acquisition.agentic_enterprise_os.evaluation_harness import (
    EVAL_DIMENSIONS,
    EvalDimensionResult,
    run_evaluation_harness,
)
from auto_client_acquisition.agentic_enterprise_os.evolution_loop import run_evolution_loop


def test_empty_evaluation_has_no_overall_score() -> None:
    report = run_evaluation_harness(())
    assert report.overall_score is None
    assert set(report.gaps) == set(EVAL_DIMENSIONS)
    assert report.dimensions == ()


def test_zero_sample_dimension_excluded_from_overall_score() -> None:
    results = (
        EvalDimensionResult("grounding", 90.0, sample_size=0),
        EvalDimensionResult("workflow_success", 80.0, sample_size=4),
    )
    report = run_evaluation_harness(results)
    scored = {d.dimension for d in report.dimensions}
    # The zero-sample dimension is a gap, not a 0/100 default.
    assert "grounding" in report.gaps
    assert "grounding" not in scored
    assert report.overall_score == 80.0


def test_empty_evolution_loop_yields_no_recommendations() -> None:
    result = run_evolution_loop()
    assert result.recommendations == ()
    assert not any(result.sources_present.values())
