"""Organizational reasoning and risk propagation (System 60)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source: str
    target: str
    risk_weight: float


@dataclass(frozen=True, slots=True)
class OrgReasoningInput:
    edges: tuple[DependencyEdge, ...]
    bottlenecks: frozenset[str]
    failed_nodes: frozenset[str]


def propagate_risk(data: OrgReasoningInput) -> dict[str, float]:
    """Deterministic risk propagation from failed nodes to dependencies."""
    risk: dict[str, float] = {node: 1.0 for node in data.failed_nodes}
    for edge in data.edges:
        src_risk = risk.get(edge.source, 0.0)
        weighted = round(src_risk * max(0.0, min(1.0, edge.risk_weight)), 4)
        if weighted > risk.get(edge.target, 0.0):
            risk[edge.target] = weighted
    return risk


def organizational_reasoning_summary(data: OrgReasoningInput) -> dict[str, object]:
    """Explain organizational consequences and suggest mitigations."""
    propagation = propagate_risk(data)
    high_risk_nodes = tuple(
        sorted(node for node, score in propagation.items() if score >= 0.6)
    )
    recommendations: list[str] = []
    if high_risk_nodes:
        recommendations.append("activate_failover_for_high_risk_nodes")
    if data.bottlenecks:
        recommendations.append("reroute_capacity_around_bottlenecks")
    if not recommendations:
        recommendations.append("maintain_current_operating_plan")
    return {
        "risk_map": propagation,
        "high_risk_nodes": high_risk_nodes,
        "bottlenecks": tuple(sorted(data.bottlenecks)),
        "recommendations": tuple(recommendations),
    }
