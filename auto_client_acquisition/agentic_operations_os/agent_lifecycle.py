"""Agent lifecycle — deploy gates and decommission triggers."""

from __future__ import annotations

LIFECYCLE_STAGES: tuple[str, ...] = (
    "proposed",
    "reviewed",
    "approved",
    "registered",
    "tested",
    "deployed",
    "monitored",
    "reviewed_monthly",
    "restricted_or_expanded",
    "decommissioned",
)

DEPLOY_PREREQUISITES: tuple[str, ...] = (
    "agent_identity_card",
    "permission_card",
    "auditability_card",
    "governance_tests",
    "owner_assigned",
    "decommission_rule",
)

DECOMMISSION_TRIGGERS: tuple[str, ...] = (
    "owner_removed",
    "policy_violation",
    "unused_for_90_days",
    "repeated_low_qa_score",
    "permission_boundary_violation",
)


def deploy_prerequisites_met(present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [p for p in DEPLOY_PREREQUISITES if p not in present]
    return not missing, tuple(missing)


def should_decommission(*, owner_present: bool, policy_violation: bool) -> bool:
    if policy_violation:
        return True
    return not owner_present
