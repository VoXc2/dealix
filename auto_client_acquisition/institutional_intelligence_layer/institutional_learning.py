"""Institutional learning loop primitives (System 64)."""

from __future__ import annotations

from dataclasses import dataclass

FAILURE_OUTCOMES: frozenset[str] = frozenset({"failure", "rollback", "incident"})


@dataclass(frozen=True, slots=True)
class LearningSignal:
    workflow_id: str
    category: str
    outcome: str
    severity: str


def learning_error_rate(signals: tuple[LearningSignal, ...]) -> float:
    """Share of execution signals marked as failure outcomes."""
    if not signals:
        return 0.0
    failures = sum(1 for s in signals if s.outcome in FAILURE_OUTCOMES)
    return round((failures / len(signals)) * 100.0, 2)


def learning_improvement(
    *,
    previous_error_rate: float,
    current_error_rate: float,
) -> dict[str, float | bool]:
    """Error-rate improvement tracker."""
    delta = round(previous_error_rate - current_error_rate, 2)
    return {
        "improved": delta > 0,
        "delta": delta,
    }


def learning_actions(signals: tuple[LearningSignal, ...]) -> tuple[str, ...]:
    """Suggest deterministic learning actions from failure patterns."""
    failing_categories = sorted(
        {s.category for s in signals if s.outcome in FAILURE_OUTCOMES},
    )
    if not failing_categories:
        return ("continue_current_policies",)
    return tuple(f"improve:{cat}" for cat in failing_categories)
