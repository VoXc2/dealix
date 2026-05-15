"""Institutional dominance blueprint surfaces for systems 56-65."""

from __future__ import annotations

REQUIRED_PLATFORM_SURFACES: dict[str, tuple[str, ...]] = {
    "56_control_plane": (
        "/platform/control_plane",
        "/platform/operational_routing",
        "/platform/global_coordination",
        "/platform/policy_coordination",
        "/platform/runtime_control",
    ),
    "57_agent_society_engine": (
        "/platform/agent_society",
        "/platform/agent_coordination",
        "/platform/agent_arbitration",
        "/platform/agent_hierarchy",
        "/platform/collective_reasoning",
    ),
    "58_assurance_and_safety_contracts": (
        "/platform/assurance_contracts",
        "/platform/execution_contracts",
        "/platform/rollback_contracts",
        "/platform/evaluation_contracts",
    ),
    "59_institutional_memory_fabric": (
        "/platform/memory_fabric",
        "/platform/lineage",
        "/platform/context_memory",
        "/platform/decision_memory",
        "/platform/operational_memory",
    ),
    "60_organizational_reasoning_engine": (
        "/platform/org_reasoning",
        "/platform/impact_analysis",
        "/platform/causal_reasoning",
        "/platform/risk_propagation",
    ),
    "61_resilience_and_chaos_engine": (
        "/platform/resilience",
        "/platform/chaos_testing",
        "/platform/replay_engine",
        "/platform/canary_trials",
        "/platform/recovery_engine",
    ),
    "62_meta_governance_engine": (
        "/platform/meta_governance",
        "/platform/policy_analysis",
        "/platform/governance_optimization",
        "/platform/escalation_optimization",
    ),
    "63_institutional_value_engine": (
        "/platform/value_engine",
        "/platform/roi_tracking",
        "/platform/impact_analysis",
        "/platform/execution_metrics",
    ),
    "64_institutional_learning_engine": (
        "/platform/institutional_learning",
        "/platform/pattern_detection",
        "/platform/feedback_loops",
        "/platform/outcome_learning",
    ),
    "65_institutional_operating_core": (
        "/platform/operating_core",
    ),
}
