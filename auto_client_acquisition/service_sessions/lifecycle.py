"""Service session state-machine validation.

Reuses SESSION_TRANSITIONS truth table from full_ops_contracts.schemas.
"""
from __future__ import annotations

from auto_client_acquisition.full_ops_contracts.schemas import (
    SESSION_TRANSITIONS,
    SessionStatus,
)


def is_transition_allowed(*, current: SessionStatus, target: SessionStatus) -> bool:
    return target in SESSION_TRANSITIONS.get(current, set())


def advance_session(
    *,
    current: SessionStatus,
    target: SessionStatus,
    approval_id: str | None,
) -> tuple[bool, str]:
    """Validate a transition. Returns (allowed, reason).

    Hard rule: any transition INTO `active` requires an approval_id
    (the founder's go-ahead via approval_center).
    """
    if not is_transition_allowed(current=current, target=target):
        return (
            False,
            f"transition_not_allowed: {current} -> {target}",
        )

    if target == "active" and not approval_id:
        return (
            False,
            "approval_id_required_to_activate_session",
        )

    return (True, f"transition_allowed: {current} -> {target}")
