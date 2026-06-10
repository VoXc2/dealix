"""Incident response — ordered phases for client and governance incidents."""

from __future__ import annotations

CLIENT_INCIDENT_PHASES: tuple[str, ...] = (
    "detect",
    "contain",
    "notify_owner",
    "correct",
    "log",
    "update_rule_test_checklist",
)


def incident_response_phases_complete(phases_done: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [p for p in CLIENT_INCIDENT_PHASES if p not in phases_done]
    return not missing, tuple(missing)
