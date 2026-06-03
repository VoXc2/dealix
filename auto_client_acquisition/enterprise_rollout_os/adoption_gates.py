"""Enterprise adoption gates — stage transitions require explicit criteria."""

from __future__ import annotations

ENTERPRISE_ADOPTION_GATES: dict[str, tuple[str, ...]] = {
    "sponsor": (
        "executive_sponsor",
        "business_owner",
        "clear_problem",
    ),
    "data": (
        "data_sources_known",
        "source_passport_ready",
        "pii_status_clear",
        "allowed_use_clear",
    ),
    "workflow": (
        "workflow_owner",
        "approval_owner_clear",
        "success_metric_defined",
    ),
    "governance": (
        "external_actions_defined",
        "draft_only_boundaries_clear",
        "blocked_actions_agreed",
    ),
    "proof": (
        "proof_pack_complete",
        "proof_score_gte_70",
        "limitations_written",
        "next_action_clear",
    ),
    "adoption": (
        "users_reviewed_outputs",
        "approvals_completed",
        "workflow_used_twice",
    ),
    "retainer": (
        "proof_score_gte_80",
        "adoption_score_gte_70",
        "monthly_value_clear",
        "owner_committed",
    ),
}


def enterprise_gate_passes(gate: str, criteria_met: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    required = ENTERPRISE_ADOPTION_GATES.get(gate)
    if not required:
        return False, ("unknown_gate",)
    missing = [c for c in required if c not in criteria_met]
    return not missing, tuple(missing)
