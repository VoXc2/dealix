"""Unified Evaluation Harness — six evaluation dimensions for agentic systems.

منصة تقييم موحَّدة — ستة أبعاد لتقييم الأنظمة الوكيلة.

Agentic systems without evaluations fail silently. This harness aggregates
caller-supplied results across the six dimensions. Article 8 (no fabrication):
a dimension with no samples is reported as a gap, never defaulted to a number.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

EVAL_DIMENSIONS: tuple[str, ...] = (
    "hallucination",
    "grounding",
    "workflow_success",
    "escalation_correctness",
    "policy_compliance",
    "business_impact",
)


@dataclass(frozen=True, slots=True)
class EvalDimensionResult:
    """A measured result for one evaluation dimension."""

    dimension: str
    score_0_100: float
    sample_size: int
    evidence_ref: str = ""


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    """Aggregated evaluation across the six dimensions."""

    dimensions: tuple[EvalDimensionResult, ...]
    overall_score: float | None
    gaps: tuple[str, ...]


def _clamp_pct(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def run_evaluation_harness(results: Sequence[EvalDimensionResult]) -> EvaluationReport:
    """Aggregate caller-supplied evaluation results into a report.

    A dimension is only scored when it has at least one sample. Dimensions with
    no samples (or absent entirely) are listed in ``gaps`` and excluded from
    ``overall_score``. Empty input yields ``overall_score=None`` and all six
    dimensions as gaps.
    """
    by_dimension = {r.dimension: r for r in results if r.dimension in EVAL_DIMENSIONS}
    scored: list[EvalDimensionResult] = []
    gaps: list[str] = []
    for dimension in EVAL_DIMENSIONS:
        result = by_dimension.get(dimension)
        if result is None or result.sample_size <= 0:
            gaps.append(dimension)
            continue
        scored.append(
            EvalDimensionResult(
                dimension=dimension,
                score_0_100=_clamp_pct(result.score_0_100),
                sample_size=result.sample_size,
                evidence_ref=result.evidence_ref,
            )
        )
    overall = (
        sum(r.score_0_100 for r in scored) / len(scored) if scored else None
    )
    return EvaluationReport(
        dimensions=tuple(scored),
        overall_score=round(overall, 1) if overall is not None else None,
        gaps=tuple(gaps),
    )


__all__ = [
    "EVAL_DIMENSIONS",
    "EvalDimensionResult",
    "EvaluationReport",
    "run_evaluation_harness",
]
