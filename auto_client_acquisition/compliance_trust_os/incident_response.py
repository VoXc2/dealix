"""Compliance incident response — types and closure rule (artifact required)."""

from __future__ import annotations

COMPLIANCE_INCIDENT_TYPES: tuple[str, ...] = (
    "pii_exposure",
    "unsupported_claim",
    "source_misuse",
    "wrong_client_data",
    "unapproved_external_action",
    "hallucinated_answer",
    "partner_violation",
    "agent_tool_misuse",
)

COMPLIANCE_INCIDENT_FLOW: tuple[str, ...] = (
    "detect",
    "contain",
    "assign_owner",
    "assess_severity",
    "notify_stakeholders",
    "correct_output",
    "log_incident",
    "add_rule",
    "add_test",
    "update_checklist_or_trust_pack",
)


def compliance_incident_type_valid(kind: str) -> bool:
    return kind in COMPLIANCE_INCIDENT_TYPES


def incident_closure_requires_artifact(*, rule_added: bool, test_added: bool, checklist_updated: bool) -> bool:
    """Every incident must produce a rule, test, or checklist update."""
    return rule_added or test_added or checklist_updated
