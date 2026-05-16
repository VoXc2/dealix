"""Registry for Dealix final civilizational systems (46-55)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CivilizationalSystem:
    """Canonical definition for a final-layer system."""

    system_id: int
    key: str
    title: str
    required_platform_paths: tuple[str, ...]


FINAL_CIVILIZATIONAL_SYSTEMS: tuple[CivilizationalSystem, ...] = (
    CivilizationalSystem(
        system_id=46,
        key="enterprise_execution_fabric",
        title="Enterprise Execution Fabric",
        required_platform_paths=(
            "platform/execution_fabric",
            "platform/operational_coordination",
            "platform/execution_chains",
            "platform/execution_state",
        ),
    ),
    CivilizationalSystem(
        system_id=47,
        key="organizational_dependency_engine",
        title="Organizational Dependency Engine",
        required_platform_paths=(
            "platform/org_dependency",
            "platform/embedded_workflows",
            "platform/execution_dependencies",
            "platform/operational_lockin",
        ),
    ),
    CivilizationalSystem(
        system_id=48,
        key="multi_org_intelligence_engine",
        title="Multi-Org Intelligence Engine",
        required_platform_paths=(
            "platform/industry_intelligence",
            "platform/benchmarking",
            "platform/cross_org_patterns",
            "platform/market_learning",
        ),
    ),
    CivilizationalSystem(
        system_id=49,
        key="organizational_autonomy_engine",
        title="Organizational Autonomy Engine",
        required_platform_paths=(
            "platform/adaptive_orchestration",
            "platform/self_healing",
            "platform/autonomous_coordination",
            "platform/goal_execution",
        ),
    ),
    CivilizationalSystem(
        system_id=50,
        key="agent_economy_engine",
        title="Agent Economy Engine",
        required_platform_paths=(
            "platform/agent_economy",
            "platform/agent_marketplace",
            "platform/agent_protocols",
            "platform/inter_agent_governance",
        ),
    ),
    CivilizationalSystem(
        system_id=51,
        key="organizational_trust_fabric",
        title="Organizational Trust Fabric",
        required_platform_paths=(
            "platform/trust_fabric",
            "platform/runtime_audits",
            "platform/accountability",
            "platform/reversibility",
            "platform/trust_scoring",
        ),
    ),
    CivilizationalSystem(
        system_id=52,
        key="organizational_memory_core",
        title="Organizational Memory Core",
        required_platform_paths=(
            "platform/memory_core",
            "platform/lineage",
            "platform/context_memory",
            "platform/operational_memory",
        ),
    ),
    CivilizationalSystem(
        system_id=53,
        key="organizational_reasoning_core",
        title="Organizational Reasoning Core",
        required_platform_paths=(
            "platform/org_reasoning",
            "platform/impact_analysis",
            "platform/causal_reasoning",
            "platform/decision_graph",
        ),
    ),
    CivilizationalSystem(
        system_id=54,
        key="self_evolving_operational_fabric",
        title="Self-Evolving Operational Fabric",
        required_platform_paths=(
            "platform/self_evolving_fabric",
            "platform/meta_learning",
            "platform/continuous_optimization",
            "platform/adaptive_governance",
        ),
    ),
    CivilizationalSystem(
        system_id=55,
        key="organizational_operating_core",
        title="Organizational Operating Core",
        required_platform_paths=("platform/organizational_operating_core",),
    ),
)


def all_required_platform_paths() -> tuple[str, ...]:
    """Flatten all required platform paths for systems 46-55."""
    seen: list[str] = []
    for system in FINAL_CIVILIZATIONAL_SYSTEMS:
        for path in system.required_platform_paths:
            if path not in seen:
                seen.append(path)
    return tuple(seen)


def coverage_ratio(existing_paths: set[str]) -> float:
    """Return required path coverage ratio in [0, 1]."""
    required = set(all_required_platform_paths())
    if not required:
        return 0.0
    return len(required.intersection(existing_paths)) / len(required)


def missing_required_paths(existing_paths: set[str]) -> list[str]:
    """Return missing required paths sorted alphabetically."""
    required = set(all_required_platform_paths())
    return sorted(required.difference(existing_paths))
