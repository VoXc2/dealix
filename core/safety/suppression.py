"""
Suppression list management.

A contact on the suppression list can NEVER become send-ready, regardless of
draft quality or approval. Suppression is one-directional: contacts are added,
never silently removed by an agent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set

from .constants import SUPPRESSION_REASONS


def _normalize(contact: str) -> str:
    return (contact or "").strip().lower()


@dataclass
class SuppressionList:
    """In-memory suppression list keyed by normalized contact (email/phone)."""

    _entries: Dict[str, Set[str]] = field(default_factory=dict)

    def add(self, contact: str, reason: str) -> None:
        if reason not in SUPPRESSION_REASONS:
            raise ValueError(f"Unknown suppression reason: {reason}")
        key = _normalize(contact)
        if not key:
            raise ValueError("Cannot suppress an empty contact")
        self._entries.setdefault(key, set()).add(reason)

    def is_suppressed(self, contact: str) -> bool:
        return _normalize(contact) in self._entries

    def reasons(self, contact: str) -> List[str]:
        return sorted(self._entries.get(_normalize(contact), set()))

    def can_send(self, contact: str) -> bool:
        """Suppressed contacts can never be sent to. No exceptions, no bypass."""
        return not self.is_suppressed(contact)

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, contact: str) -> bool:
        return self.is_suppressed(contact)

    @classmethod
    def from_iterable(cls, rows: Iterable[Dict]) -> "SuppressionList":
        """Build from rows like {"contact": ..., "reason": ...}."""
        sl = cls()
        for row in rows:
            sl.add(row["contact"], row["reason"])
        return sl


def is_suppressed(contact: str, suppression: Optional[SuppressionList]) -> bool:
    """Convenience helper used by tests / callers."""
    if suppression is None:
        return False
    return suppression.is_suppressed(contact)
