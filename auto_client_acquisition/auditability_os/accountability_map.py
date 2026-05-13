"""Accountability Map — owners per action."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AccountabilityMap:
    action: str
    performed_by: str
    responsibility_owner: str
    dealix_owner: str
    audit_event_id: str | None = None

    def __post_init__(self) -> None:
        if not self.action:
            raise ValueError("action_required")
        if not self.responsibility_owner:
            raise ValueError("responsibility_owner_required")
        if not self.dealix_owner:
            raise ValueError("dealix_owner_required")
