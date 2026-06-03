"""Scope change classification — deterministic gates for services margin."""

from __future__ import annotations

from enum import StrEnum


class ChangeRequestClass(StrEnum):
    INCLUDED = "included"
    MINOR_ADJUSTMENT = "minor_adjustment"
    PAID_ADDON = "paid_addon"
    NEW_SPRINT = "new_sprint"
    RETAINER_BACKLOG = "retainer_backlog"
    REJECTED = "rejected"


def classify_change_request(
    *,
    in_written_scope: bool,
    estimated_additional_hours: float,
    minor_adjustment_hour_threshold: float = 2.0,
    introduces_new_capability_outside_scope: bool,
    aligns_with_retainer_backlog_item: bool,
    requests_unapproved_outbound_execution: bool,
) -> ChangeRequestClass:
    """
    Classify a client change. Outbound automation without approval is always rejected
    (Dealix draft/approval-first posture).
    """
    if requests_unapproved_outbound_execution:
        return ChangeRequestClass.REJECTED
    if aligns_with_retainer_backlog_item:
        return ChangeRequestClass.RETAINER_BACKLOG
    if introduces_new_capability_outside_scope:
        return ChangeRequestClass.NEW_SPRINT
    if in_written_scope:
        if estimated_additional_hours <= 0:
            return ChangeRequestClass.INCLUDED
        if estimated_additional_hours <= minor_adjustment_hour_threshold:
            return ChangeRequestClass.MINOR_ADJUSTMENT
        return ChangeRequestClass.PAID_ADDON
    return ChangeRequestClass.NEW_SPRINT
