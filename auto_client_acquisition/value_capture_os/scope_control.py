"""Scope Control — classify change requests."""

from __future__ import annotations

from enum import Enum


class ChangeRequestClass(str, Enum):
    INCLUDED = "included"
    MINOR_ADJUSTMENT = "minor_adjustment"
    PAID_ADD_ON = "paid_add_on"
    NEW_SPRINT = "new_sprint"
    RETAINER_BACKLOG = "retainer_backlog"
    REJECTED = "rejected"


def classify_change_request(
    *,
    is_in_original_scope: bool,
    is_minor: bool,
    is_in_retainer_scope: bool,
    is_unsafe_or_forbidden: bool,
    is_recurring_capability: bool,
) -> ChangeRequestClass:
    if is_unsafe_or_forbidden:
        return ChangeRequestClass.REJECTED
    if is_in_original_scope:
        return ChangeRequestClass.INCLUDED
    if is_in_retainer_scope:
        return ChangeRequestClass.RETAINER_BACKLOG
    if is_minor:
        return ChangeRequestClass.MINOR_ADJUSTMENT
    if is_recurring_capability:
        return ChangeRequestClass.NEW_SPRINT
    return ChangeRequestClass.PAID_ADD_ON
