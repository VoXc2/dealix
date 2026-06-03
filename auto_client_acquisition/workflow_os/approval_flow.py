"""Approval flow markers for workflow OS."""

from __future__ import annotations

APPROVAL_FLOW_STEPS: tuple[str, ...] = (
    "draft_created",
    "internal_review",
    "client_approval",
    "release_to_send_queue",
)


def approval_flow_complete(done: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = tuple(s for s in APPROVAL_FLOW_STEPS if s not in done)
    return not missing, missing


__all__ = ["APPROVAL_FLOW_STEPS", "approval_flow_complete"]
