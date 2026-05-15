"""Adaptive orchestration strategy selection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrchestrationDecision:
    workflow_id: str
    chosen_variant: str
    reason: str
    retry_budget: int


def choose_orchestration_variant(
    *, workflow_id: str, current_load: float, risk_band: str, latency_slo_ms: int
) -> OrchestrationDecision:
    if risk_band in {'high', 'critical'}:
        return OrchestrationDecision(
            workflow_id=workflow_id,
            chosen_variant='safe_path',
            reason='risk_band_elevated',
            retry_budget=1,
        )
    if current_load > 0.8:
        return OrchestrationDecision(
            workflow_id=workflow_id,
            chosen_variant='cost_optimized_path',
            reason='high_load',
            retry_budget=2,
        )
    variant = 'latency_optimized_path' if latency_slo_ms <= 3000 else 'balanced_path'
    return OrchestrationDecision(
        workflow_id=workflow_id,
        chosen_variant=variant,
        reason='default_adaptive',
        retry_budget=3,
    )


__all__ = ['OrchestrationDecision', 'choose_orchestration_variant']
