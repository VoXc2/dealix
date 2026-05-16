"""Optimization suggestions driven by intelligence signals."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OptimizationSuggestion:
    area: str
    expected_impact: str
    action: str


def propose_optimizations(*, bottlenecks: tuple[str, ...], risk_band: str) -> tuple[OptimizationSuggestion, ...]:
    suggestions: list[OptimizationSuggestion] = []
    if any('sla_breach' in item for item in bottlenecks):
        suggestions.append(
            OptimizationSuggestion(
                area='workflow_latency',
                expected_impact='reduce_p95_latency',
                action='split_workflow_into_modular_steps',
            )
        )
    if any('retry_churn' in item for item in bottlenecks):
        suggestions.append(
            OptimizationSuggestion(
                area='reliability',
                expected_impact='reduce_retry_waste',
                action='tighten_retry_guardrails_and_idempotency',
            )
        )
    if risk_band in {'high', 'critical'}:
        suggestions.append(
            OptimizationSuggestion(
                area='governance',
                expected_impact='reduce_policy_violations',
                action='increase_runtime_policy_sampling',
            )
        )
    return tuple(suggestions)


__all__ = ['OptimizationSuggestion', 'propose_optimizations']
