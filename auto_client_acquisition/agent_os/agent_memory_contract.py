"""Agent memory contract — task 5 of the Agent Operating System.

Declares what an agent may store, why, and for how long. Doctrine: no PII in
logs without a lawful basis; sensitive PII needs explicit consent.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from enum import StrEnum
from typing import Any

_PII_KEY_HINTS: tuple[str, ...] = (
    "email", "phone", "mobile", "national", "iqama", "passport", "iban",
)


def _key_looks_like_pii(name: str) -> bool:
    n = name.lower()
    return any(hint in n for hint in _PII_KEY_HINTS)


class DataClass(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    PII = "pii"
    SENSITIVE_PII = "sensitive_pii"


class LawfulBasis(StrEnum):
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGITIMATE_INTEREST = "legitimate_interest"
    LEGAL_OBLIGATION = "legal_obligation"
    NONE = "none"


_PII_CLASSES: frozenset[DataClass] = frozenset({DataClass.PII, DataClass.SENSITIVE_PII})


@dataclass(frozen=True, slots=True)
class MemoryItem:
    key: str
    data_class: str
    purpose: str
    retention_days: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AgentMemoryContract:
    agent_id: str
    lawful_basis: str
    max_retention_days: int
    items: tuple[MemoryItem, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["items"] = [i.to_dict() for i in self.items]
        return d


@dataclass(frozen=True, slots=True)
class MemoryValidation:
    ok: bool
    issues: tuple[str, ...]


def new_memory_contract(
    *,
    agent_id: str,
    lawful_basis: LawfulBasis | str = LawfulBasis.NONE,
    max_retention_days: int = 90,
    items: list[MemoryItem] | None = None,
) -> AgentMemoryContract:
    """Build a memory contract. Raises on a blank id or bad retention cap."""
    if not agent_id.strip():
        raise ValueError("agent_id is required")
    if max_retention_days <= 0:
        raise ValueError("max_retention_days must be positive")
    basis = LawfulBasis(lawful_basis)
    return AgentMemoryContract(
        agent_id=agent_id.strip(),
        lawful_basis=basis.value,
        max_retention_days=int(max_retention_days),
        items=tuple(items or ()),
    )


def validate_memory_contract(contract: AgentMemoryContract) -> MemoryValidation:
    """Non-raising validation against the PII / retention doctrine rules."""
    issues: list[str] = []
    basis = LawfulBasis(contract.lawful_basis)
    for item in contract.items:
        dc = DataClass(item.data_class)
        if dc in _PII_CLASSES and basis is LawfulBasis.NONE:
            issues.append(f"pii_without_lawful_basis:{item.key}")
        if dc is DataClass.SENSITIVE_PII and basis is not LawfulBasis.CONSENT:
            issues.append(f"sensitive_pii_requires_consent:{item.key}")
        if item.retention_days > contract.max_retention_days:
            issues.append(f"retention_exceeds_max:{item.key}")
        if item.retention_days > 0 and not item.purpose.strip():
            issues.append(f"retention_without_purpose:{item.key}")
        if dc in {DataClass.PUBLIC, DataClass.INTERNAL} and _key_looks_like_pii(item.key):
            issues.append(f"key_looks_like_pii_but_classified_nonpii:{item.key}")
    return MemoryValidation(ok=not issues, issues=tuple(issues))


def is_expired(
    item: MemoryItem,
    *,
    stored_at_iso: str,
    now_iso: str | None = None,
) -> bool:
    """True when an item has passed its retention window."""
    stored = datetime.fromisoformat(stored_at_iso)
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(UTC)
    return now - stored > timedelta(days=item.retention_days)


__all__ = [
    "AgentMemoryContract",
    "DataClass",
    "LawfulBasis",
    "MemoryItem",
    "MemoryValidation",
    "is_expired",
    "new_memory_contract",
    "validate_memory_contract",
]
