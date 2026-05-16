"""System 16–25 capability registry for the Agentic Enterprise vision.

This module is intentionally deterministic and import-safe:
- No runtime I/O
- No external service calls
- No side effects at import time
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class AgenticDominanceSystem:
    """One dominance system contract with required capability paths."""

    system_id: int
    code: str
    thesis: str
    required_paths: tuple[str, ...]
    success_signals: tuple[str, ...]


SYSTEMS_16_25: tuple[AgenticDominanceSystem, ...] = (
    AgenticDominanceSystem(
        system_id=16,
        code="ENTERPRISE_REALITY_ENGINE",
        thesis="Real-time operational consciousness for organizational reality.",
        required_paths=(
            "/platform/reality_engine",
            "/platform/operational_health",
            "/platform/org_pressure_detection",
            "/platform/workflow_congestion",
            "/platform/execution_monitoring",
        ),
        success_signals=(
            "Knows bottlenecks now",
            "Surfaces overload hotspots",
            "Predicts near-term workflow collapse risk",
        ),
    ),
    AgenticDominanceSystem(
        system_id=17,
        code="ORGANIZATIONAL_REASONING_ENGINE",
        thesis="Reasons over organizational dependencies and tradeoffs.",
        required_paths=(
            "/platform/org_reasoning",
            "/platform/causal_analysis",
            "/platform/impact_modeling",
            "/platform/strategic_reasoning",
            "/platform/decision_graph",
        ),
        success_signals=(
            "Explains downstream consequences before execution",
            "Evaluates tradeoffs and dependency impact",
            "Prioritizes actions with strategic context",
        ),
    ),
    AgenticDominanceSystem(
        system_id=18,
        code="AUTONOMOUS_BUSINESS_MODEL_ENGINE",
        thesis="Continuously optimizes business model levers.",
        required_paths=(
            "/platform/business_optimization",
            "/platform/revenue_optimization",
            "/platform/cost_optimization",
            "/platform/process_optimization",
            "/platform/operational_ai",
        ),
        success_signals=(
            "Improves pricing and margin decisions",
            "Optimizes staffing and process design",
            "Compounds revenue-system efficiency",
        ),
    ),
    AgenticDominanceSystem(
        system_id=19,
        code="AGENT_SUPERVISION_ENGINE",
        thesis="Supervises large-scale agent ecosystems safely.",
        required_paths=(
            "/platform/agent_supervision",
            "/platform/agent_coordination",
            "/platform/agent_conflict_resolution",
            "/platform/agent_lifecycle",
            "/platform/agent_monitoring",
        ),
        success_signals=(
            "Has AI escalation paths",
            "Coordinates multi-agent execution reliably",
            "Runs lifecycle and performance governance",
        ),
    ),
    AgenticDominanceSystem(
        system_id=20,
        code="TRUST_AND_SAFETY_DOMINANCE_ENGINE",
        thesis="Permission-bound autonomy with reversible execution.",
        required_paths=(
            "/platform/runtime_safety",
            "/platform/reversibility",
            "/platform/explainability",
            "/platform/accountability",
            "/platform/trust_engine",
        ),
        success_signals=(
            "Every action is explainable and auditable",
            "Every action has explicit authority context",
            "Rollback path exists for critical operations",
        ),
    ),
    AgenticDominanceSystem(
        system_id=21,
        code="ORGANIZATIONAL_LEARNING_ENGINE",
        thesis="Compounds organizational intelligence from outcomes.",
        required_paths=(
            "/platform/org_learning",
            "/platform/pattern_detection",
            "/platform/feedback_loops",
            "/platform/outcome_analysis",
            "/platform/adaptive_optimization",
        ),
        success_signals=(
            "Reduces repeated failure classes over time",
            "Improves workflow reliability continuously",
            "Feeds governance and orchestration improvements",
        ),
    ),
    AgenticDominanceSystem(
        system_id=22,
        code="STRATEGIC_INTELLIGENCE_ENGINE",
        thesis="Converts market and operating signals into executive foresight.",
        required_paths=(
            "/platform/market_intelligence",
            "/platform/risk_forecasting",
            "/platform/competitive_analysis",
            "/platform/opportunity_detection",
            "/platform/strategic_reasoning",
        ),
        success_signals=(
            "Forecasts risk and detects opportunities",
            "Supports executive planning with evidence",
            "Guides prioritization with market context",
        ),
    ),
    AgenticDominanceSystem(
        system_id=23,
        code="SELF_EVOLVING_WORKFLOW_ENGINE",
        thesis="Self-improves orchestration and execution paths.",
        required_paths=(
            "/platform/workflow_optimization",
            "/platform/adaptive_orchestration",
            "/platform/process_learning",
            "/platform/execution_optimization",
        ),
        success_signals=(
            "Workflows improve cycle-by-cycle",
            "Bottlenecks are corrected automatically",
            "Orchestration adapts from observed outcomes",
        ),
    ),
    AgenticDominanceSystem(
        system_id=24,
        code="CIVILIZATIONAL_SCALING_ENGINE",
        thesis="Learns patterns across organizations and industries.",
        required_paths=(
            "/platform/industry_intelligence",
            "/platform/cross_org_learning",
            "/platform/benchmarking",
            "/platform/pattern_library",
        ),
        success_signals=(
            "Finds cross-org operational patterns",
            "Benchmarks performance across sectors",
            "Turns market patterns into reusable intelligence",
        ),
    ),
    AgenticDominanceSystem(
        system_id=25,
        code="SELF_EVOLVING_ENTERPRISE_CORE",
        thesis="Continuous meta-governance and optimization core.",
        required_paths=(
            "/platform/self_evolving_core",
            "/platform/meta_orchestration",
            "/platform/meta_governance",
            "/platform/org_intelligence_core",
            "/platform/continuous_optimization",
        ),
        success_signals=(
            "Continuously monitors and coordinates execution",
            "Prevents chaos through governance runtime",
            "Compounds strategic and operational intelligence",
        ),
    ),
)


def _normalize_path(path: str) -> str:
    cleaned = path.strip()
    if not cleaned:
        return cleaned
    if not cleaned.startswith("/"):
        cleaned = f"/{cleaned}"
    while "//" in cleaned:
        cleaned = cleaned.replace("//", "/")
    return cleaned


def all_required_paths(
    systems: Iterable[AgenticDominanceSystem] = SYSTEMS_16_25,
) -> tuple[str, ...]:
    """Return all unique required capability paths, stable-sorted."""
    unique = {_normalize_path(path) for s in systems for path in s.required_paths}
    return tuple(sorted(p for p in unique if p))


def missing_capabilities(
    available_paths: Iterable[str],
    systems: Iterable[AgenticDominanceSystem] = SYSTEMS_16_25,
) -> tuple[str, ...]:
    """Compute missing capability paths for systems 16–25."""
    available = {_normalize_path(path) for path in available_paths}
    missing = set(all_required_paths(systems)).difference(available)
    return tuple(sorted(missing))


def dominance_coverage_percent(
    available_paths: Iterable[str],
    systems: Iterable[AgenticDominanceSystem] = SYSTEMS_16_25,
) -> float:
    """Coverage of required paths across systems 16–25, clamped to 0–100."""
    required = all_required_paths(systems)
    if not required:
        return 100.0
    missing = set(missing_capabilities(available_paths, systems))
    covered = len(required) - len(missing)
    ratio = (covered / len(required)) * 100.0
    return round(max(0.0, min(100.0, ratio)), 2)


def system_completion_ratio(
    system_id: int,
    available_paths: Iterable[str],
    systems: Iterable[AgenticDominanceSystem] = SYSTEMS_16_25,
) -> float:
    """Return the completion ratio (0–1) for one dominance system."""
    available = {_normalize_path(path) for path in available_paths}
    target = next((s for s in systems if s.system_id == system_id), None)
    if target is None:
        raise ValueError(f"Unknown system_id: {system_id}")
    if not target.required_paths:
        return 1.0
    have = sum(1 for path in target.required_paths if _normalize_path(path) in available)
    return round(max(0.0, min(1.0, have / len(target.required_paths))), 4)


def readiness_by_system(
    available_paths: Iterable[str],
    *,
    threshold: float = 0.8,
    systems: Iterable[AgenticDominanceSystem] = SYSTEMS_16_25,
) -> dict[int, bool]:
    """Return pass/fail readiness by system using per-system completion threshold."""
    t = max(0.0, min(1.0, float(threshold)))
    return {s.system_id: system_completion_ratio(s.system_id, available_paths, systems) >= t for s in systems}


def most_critical_gaps(
    available_paths: Iterable[str],
    *,
    top_n: int = 5,
    systems: Iterable[AgenticDominanceSystem] = SYSTEMS_16_25,
) -> tuple[tuple[str, int], ...]:
    """
    Rank missing paths by number of systems that depend on them.

    This naturally prioritizes cross-cutting paths (for example,
    ``/platform/strategic_reasoning`` appears in both systems 17 and 22).
    """
    available = {_normalize_path(path) for path in available_paths}
    impact: dict[str, int] = {}
    for system in systems:
        for raw in system.required_paths:
            path = _normalize_path(raw)
            if path in available:
                continue
            impact[path] = impact.get(path, 0) + 1
    ranked = sorted(impact.items(), key=lambda item: (-item[1], item[0]))
    return tuple(ranked[: max(0, top_n)])


def systems_by_id(
    systems: Iterable[AgenticDominanceSystem] = SYSTEMS_16_25,
) -> Mapping[int, AgenticDominanceSystem]:
    """Return an immutable-like mapping (plain dict) keyed by system id."""
    return {system.system_id: system for system in systems}
