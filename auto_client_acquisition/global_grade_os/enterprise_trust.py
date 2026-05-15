"""Enterprise trust architecture — level ladders as checklists."""

from __future__ import annotations

ENTERPRISE_TRUST_LADDER: dict[int, frozenset[str]] = {
    1: frozenset(
        {
            "data_handling_policy",
            "ai_usage_policy",
            "no_unsafe_automation_commitment",
            "proof_standard",
        },
    ),
    2: frozenset(
        {
            "audit_events",
            "ai_run_logs",
            "approval_records",
            "source_passports",
        },
    ),
    3: frozenset(
        {
            "policy_engine",
            "role_based_approvals",
            "risk_index",
            "incident_response",
        },
    ),
    4: frozenset(
        {
            "rbac",
            "sso_ready",
            "data_retention_policy",
            "audit_exports",
            "sla_support",
        },
    ),
    5: frozenset(
        {
            "ai_control_tower",
            "multi_workflow_governance",
            "business_unit_reporting",
            "executive_value_dashboard",
        },
    ),
}


def trust_level_satisfied(level: int, implemented: frozenset[str]) -> bool:
    required = ENTERPRISE_TRUST_LADDER.get(level)
    if required is None:
        msg = f"invalid trust level: {level}"
        raise ValueError(msg)
    return required <= implemented


def highest_satisfied_trust_level(implemented: frozenset[str]) -> int:
    best = 0
    for lvl in sorted(ENTERPRISE_TRUST_LADDER):
        if trust_level_satisfied(lvl, implemented):
            best = lvl
    return best
