"""Deliverable lifecycle state machine.

Truth table:
  draft → internal_review → customer_review_required → approved → delivered → archived
                       ↓                          ↓
                    revision_requested ←─────────┘
                       ↓
                     draft
"""

from __future__ import annotations

from datetime import UTC, datetime, timezone

from auto_client_acquisition.deliverables.schemas import (
    Deliverable,
    DeliverableStatus,
)


class InvalidTransitionError(RuntimeError):
    """Raised on invalid Deliverable.status transition."""


# Allowed transitions for Deliverable.status
DELIVERABLE_TRANSITIONS: dict[DeliverableStatus, set[DeliverableStatus]] = {
    "draft": {"internal_review", "customer_review_required", "archived"},
    "internal_review": {"customer_review_required", "draft", "archived"},
    "customer_review_required": {"approved", "revision_requested", "archived"},
    "revision_requested": {"draft", "archived"},
    "approved": {"delivered", "archived"},
    "delivered": {"archived"},
    "archived": set(),  # terminal
}


def is_terminal(status: DeliverableStatus) -> bool:
    return len(DELIVERABLE_TRANSITIONS.get(status, set())) == 0


def is_transition_allowed(*, current: DeliverableStatus, target: DeliverableStatus) -> bool:
    return target in DELIVERABLE_TRANSITIONS.get(current, set())


def advance(
    rec: Deliverable,
    *,
    target: DeliverableStatus,
    reason: str = "",
) -> Deliverable:
    """Advance the deliverable to `target` status (mutates rec, returns same).

    Article 4: blocks invalid transitions; raises InvalidTransitionError.
    Article 8: when target='delivered' and proof_related=True, requires
      proof_event_id non-null (no fake proof).
    """
    if not is_transition_allowed(current=rec.status, target=target):
        raise InvalidTransitionError(
            f"invalid_transition: {rec.status} -> {target} "
            f"(deliverable={rec.deliverable_id}); allowed={DELIVERABLE_TRANSITIONS[rec.status]}"
        )

    if target == "delivered" and rec.proof_related and not rec.proof_event_id:
        raise InvalidTransitionError(
            f"proof_related_deliverable_must_have_proof_event_id: "
            f"deliverable={rec.deliverable_id}"
        )

    rec.status = target
    rec.updated_at = datetime.now(UTC)
    return rec
