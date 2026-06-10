"""Change requests — classify client asks to protect margin and delivery."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ChangeRequestType(StrEnum):
    """Commercial classification for any post-signature ask."""

    INCLUDED = "included"
    MINOR_ADJUSTMENT = "minor_adjustment"
    PAID_ADD_ON = "paid_add_on"
    NEW_SPRINT = "new_sprint"
    RETAINER_BACKLOG = "retainer_backlog"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class ChangeRequest:
    request_id: str
    engagement_id: str
    summary: str
    classification: ChangeRequestType
    rationale: str


def change_request_valid(cr: ChangeRequest) -> bool:
    return all((cr.request_id.strip(), cr.engagement_id.strip(), cr.summary.strip(), cr.rationale.strip()))


__all__ = ["ChangeRequest", "ChangeRequestType", "change_request_valid"]
