"""Institutional Dependency Index — does the institution depend on Dealix to operate?

The honest test of "institutional intelligence layer" status is not the number
of agents or features. It is dependency: ten 0–100 signals, one per system
56–65 (Layers 37–46), weighted into a single 0–100 index.
"""

from __future__ import annotations

from dataclasses import dataclass

# One weight per system 56–65; sums to 100.
_WEIGHTS: tuple[int, ...] = (10, 10, 10, 10, 10, 10, 10, 10, 10, 10)

# A dimension below this is too thin to support the "operating core" claim.
_BLOCKER_THRESHOLD: int = 70

_BLOCKER_LABELS: tuple[str, ...] = (
    "control_plane_dependency_thin",
    "agent_society_not_fully_governed",
    "assurance_contract_coverage_thin",
    "memory_fabric_traceability_thin",
    "org_reasoning_depth_thin",
    "resilience_recovery_thin",
    "meta_governance_not_self_improving",
    "value_not_measurable",
    "learning_loop_inactive",
    "operating_core_reliance_thin",
)


@dataclass(frozen=True, slots=True)
class InstitutionalDependencyDimensions:
    """Each field is a 0–100 signal for one institutional system (56–65)."""

    control_plane_coverage: int
    agent_society_governed: int
    assurance_contract_coverage: int
    memory_fabric_traceability: int
    org_reasoning_depth: int
    resilience_recovery: int
    meta_governance_improvement: int
    value_measurability: int
    learning_loop_active: int
    operating_core_reliance: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def _ordered_values(dimensions: InstitutionalDependencyDimensions) -> tuple[int, ...]:
    d = dimensions
    return (
        _clamp_pct(d.control_plane_coverage),
        _clamp_pct(d.agent_society_governed),
        _clamp_pct(d.assurance_contract_coverage),
        _clamp_pct(d.memory_fabric_traceability),
        _clamp_pct(d.org_reasoning_depth),
        _clamp_pct(d.resilience_recovery),
        _clamp_pct(d.meta_governance_improvement),
        _clamp_pct(d.value_measurability),
        _clamp_pct(d.learning_loop_active),
        _clamp_pct(d.operating_core_reliance),
    )


def institutional_dependency_index(dimensions: InstitutionalDependencyDimensions) -> int:
    """Weighted 0–100 dependency index. Higher = harder to remove Dealix."""
    values = _ordered_values(dimensions)
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def dependency_band(score: int) -> str:
    """Maturity band — institutional dependency, not feature count."""
    if score >= 85:
        return "institutional_operating_core"
    if score >= 70:
        return "infrastructure"
    if score >= 50:
        return "platform"
    return "tool"


def dependency_blockers(
    dimensions: InstitutionalDependencyDimensions,
) -> tuple[str, ...]:
    """Directional gates — any thin dimension blocks the operating-core claim."""
    values = _ordered_values(dimensions)
    return tuple(
        label
        for label, value in zip(_BLOCKER_LABELS, values, strict=True)
        if value < _BLOCKER_THRESHOLD
    )
