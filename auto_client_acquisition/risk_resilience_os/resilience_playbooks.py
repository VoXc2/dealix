"""Resilience playbooks — five shock types and canonical response themes."""

from __future__ import annotations

RESILIENCE_SHOCK_TYPES: tuple[str, ...] = (
    "client_incident",
    "model_provider_change",
    "partner_violation",
    "market_slowdown",
    "governance_failure",
)


def resilience_shock_valid(shock: str) -> bool:
    return shock in RESILIENCE_SHOCK_TYPES


def governance_failure_playbook_steps() -> tuple[str, ...]:
    return (
        "pause_external_actions",
        "incident_review",
        "add_policy_rule",
        "add_regression_test",
        "update_trust_pack",
    )
