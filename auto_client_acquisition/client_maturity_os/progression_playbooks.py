"""Progression playbooks — deliverables between adjacent maturity levels."""

from __future__ import annotations

PROGRESSION_DELIVERABLES: dict[str, tuple[str, ...]] = {
    "0_1": ("ai_inventory", "risk_map", "governance_boundary", "executive_brief"),
    "1_2": (
        "capability_diagnostic",
        "first_use_case_selection",
        "source_passport",
        "sprint_scope",
    ),
    "2_3": (
        "productized_sprint",
        "ai_assisted_output",
        "human_review",
        "proof_pack",
    ),
    "3_4": (
        "governance_runtime",
        "approval_matrix",
        "ai_run_ledger",
        "qa_rubric",
    ),
    "4_5": (
        "monthly_retainer",
        "value_report",
        "proof_timeline",
        "operating_cadence",
    ),
    "5_6": (
        "client_workspace",
        "multi_workflow_dashboard",
        "cross_functional_review",
    ),
    "6_7": (
        "ai_control_plane",
        "audit_exports",
        "policy_registry",
        "agent_registry",
        "enterprise_trust_program",
    ),
}


def transition_key(from_level: int, to_level: int) -> str:
    return f"{from_level}_{to_level}"


def progression_deliverables(from_level: int, to_level: int) -> tuple[str, ...]:
    if to_level != from_level + 1:
        return ()
    return PROGRESSION_DELIVERABLES.get(transition_key(from_level, to_level), ())
