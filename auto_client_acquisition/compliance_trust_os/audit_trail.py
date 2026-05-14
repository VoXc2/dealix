"""Audit trail — required metadata for governed AI runs."""

from __future__ import annotations

AUDIT_EVENT_REQUIRED_FIELDS: tuple[str, ...] = (
    "audit_event_id",
    "actor",
    "action",
    "resource",
    "governance_decision",
    "timestamp_iso",
)


def audit_event_metadata_complete(fields_present: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [f for f in AUDIT_EVENT_REQUIRED_FIELDS if f not in fields_present]
    return not missing, tuple(missing)
