"""The evaluation taxonomy — 4 categories of AI quality.

Without evals you are blind. This module is the machine-readable
catalog of what Dealix measures: retrieval, response, workflow, and
business quality. Pure data — no I/O.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EvalCategory(StrEnum):
    """The 4 categories of evaluation."""

    RETRIEVAL = "retrieval_quality"
    RESPONSE = "response_quality"
    WORKFLOW = "workflow_quality"
    BUSINESS = "business_quality"


class MetricDirection(StrEnum):
    """Whether a higher or lower metric value is better."""

    HIGHER_BETTER = "higher_better"
    LOWER_BETTER = "lower_better"


@dataclass(frozen=True, slots=True)
class EvalMetric:
    """One measurable quality signal."""

    metric_id: str
    category: EvalCategory
    description: str
    direction: MetricDirection
    threshold: float

    def to_dict(self) -> dict[str, object]:
        return {
            "metric_id": self.metric_id,
            "category": str(self.category),
            "description": self.description,
            "direction": str(self.direction),
            "threshold": self.threshold,
        }


_HB = MetricDirection.HIGHER_BETTER
_LB = MetricDirection.LOWER_BETTER

_METRICS: tuple[EvalMetric, ...] = (
    # Retrieval quality.
    EvalMetric("retrieval_relevance", EvalCategory.RETRIEVAL,
               "Share of retrieved sources relevant to the question", _HB, 0.80),
    EvalMetric("retrieval_recall", EvalCategory.RETRIEVAL,
               "Share of relevant sources actually retrieved", _HB, 0.70),
    EvalMetric("retrieval_precision", EvalCategory.RETRIEVAL,
               "Share of retrieved sources that are on-target", _HB, 0.75),
    # Response quality.
    EvalMetric("response_groundedness", EvalCategory.RESPONSE,
               "Share of claims supported by a cited source", _HB, 0.95),
    EvalMetric("response_hallucination_rate", EvalCategory.RESPONSE,
               "Share of claims with no supporting source", _LB, 0.05),
    EvalMetric("response_source_quality", EvalCategory.RESPONSE,
               "Average trust level of cited sources", _HB, 0.70),
    # Workflow quality.
    EvalMetric("workflow_task_success", EvalCategory.WORKFLOW,
               "Share of workflow runs that reach a completed state", _HB, 0.90),
    EvalMetric("workflow_retry_rate", EvalCategory.WORKFLOW,
               "Share of steps that required a retry", _LB, 0.15),
    EvalMetric("workflow_escalation_correctness", EvalCategory.WORKFLOW,
               "Share of escalations that were warranted", _HB, 0.90),
    # Business quality.
    EvalMetric("business_roi_evidence", EvalCategory.BUSINESS,
               "Share of value claims backed by ledger evidence", _HB, 1.00),
    EvalMetric("business_adoption_signal", EvalCategory.BUSINESS,
               "Customer adoption score band coverage", _HB, 0.60),
    EvalMetric("business_resolution_rate", EvalCategory.BUSINESS,
               "Share of support items resolved", _HB, 0.80),
)


METRIC_IDS: frozenset[str] = frozenset(m.metric_id for m in _METRICS)


def list_metrics() -> list[EvalMetric]:
    """Every evaluation metric across all 4 categories."""
    return list(_METRICS)


def get_metric(metric_id: str) -> EvalMetric:
    """Return one metric by id. Raises KeyError if unknown."""
    for m in _METRICS:
        if m.metric_id == metric_id:
            return m
    raise KeyError(f"unknown metric_id: {metric_id}")


def metrics_for_category(category: EvalCategory) -> list[EvalMetric]:
    """All metrics in one category."""
    return [m for m in _METRICS if m.category == category]
