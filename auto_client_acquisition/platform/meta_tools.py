"""Meta-tool proposals to optimize agentic workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetaToolProposal:
    tool_name: str
    reduces_llm_calls_ratio: float
    reduces_latency_ratio: float
    reduces_cost_ratio: float


def propose_meta_tools(*, llm_calls_per_run: float, failure_rate: float) -> tuple[MetaToolProposal, ...]:
    proposals: list[MetaToolProposal] = []
    if llm_calls_per_run > 8:
        proposals.append(
            MetaToolProposal(
                tool_name='prompt_cache_router',
                reduces_llm_calls_ratio=0.25,
                reduces_latency_ratio=0.18,
                reduces_cost_ratio=0.2,
            )
        )
    if failure_rate > 0.08:
        proposals.append(
            MetaToolProposal(
                tool_name='deterministic_precheck_gate',
                reduces_llm_calls_ratio=0.1,
                reduces_latency_ratio=0.12,
                reduces_cost_ratio=0.08,
            )
        )
    return tuple(proposals)


__all__ = ['MetaToolProposal', 'propose_meta_tools']
