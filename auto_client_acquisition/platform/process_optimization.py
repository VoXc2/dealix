"""Process optimization planner."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.meta_tools import MetaToolProposal


@dataclass(frozen=True, slots=True)
class ProcessOptimizationResult:
    latency_improvement_ratio: float
    cost_improvement_ratio: float
    recommendations: tuple[str, ...]


def build_process_optimization(
    *, patterns: dict[str, float], meta_tools: tuple[MetaToolProposal, ...]
) -> ProcessOptimizationResult:
    latency_gain = sum(tool.reduces_latency_ratio for tool in meta_tools)
    cost_gain = sum(tool.reduces_cost_ratio for tool in meta_tools)
    recommendations = tuple(f'deploy:{tool.tool_name}' for tool in meta_tools)

    if patterns.get('success_rate', 1.0) < 0.9:
        recommendations = recommendations + ('tighten_workflow_eval_thresholds',)

    return ProcessOptimizationResult(
        latency_improvement_ratio=round(min(latency_gain, 0.9), 4),
        cost_improvement_ratio=round(min(cost_gain, 0.9), 4),
        recommendations=recommendations,
    )


__all__ = ['ProcessOptimizationResult', 'build_process_optimization']
