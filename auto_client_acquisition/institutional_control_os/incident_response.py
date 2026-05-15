"""Incident response — every incident must harden controls."""

from __future__ import annotations

from enum import StrEnum


class IncidentType(StrEnum):
    PII_EXPOSURE = "pii_exposure"
    SOURCE_MISUSE = "source_misuse"
    UNAPPROVED_EXTERNAL_ACTION = "unapproved_external_action"
    UNSUPPORTED_CLAIM = "unsupported_claim"
    HALLUCINATED_ANSWER = "hallucinated_answer"
    WRONG_CLIENT_DATA = "wrong_client_data"
    PARTNER_VIOLATION = "partner_violation"


INCIDENT_RESPONSE_STEPS: tuple[str, ...] = (
    "detect",
    "contain",
    "notify_internal_owner",
    "assess_severity",
    "correct_output",
    "log_incident",
    "update_rule",
    "add_test",
    "update_playbook",
)


def incident_control_closure_ok(
    *,
    rule_updated: bool,
    test_added: bool,
    playbook_updated: bool,
) -> tuple[bool, tuple[str, ...]]:
    """Institutional anti-fragility: closure requires at least one durable control artifact."""
    if rule_updated or test_added or playbook_updated:
        return True, ()
    return False, ("control_update_required",)
