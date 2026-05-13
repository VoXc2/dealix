"""Access Classes A0..A7 + Access Card."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AccessClass(str, Enum):
    A0_NO_ACCESS = "a0_no_access"
    A1_READ_METADATA = "a1_read_metadata"
    A2_READ_PASSPORTED = "a2_read_passported"
    A3_ANALYZE = "a3_analyze"
    A4_DRAFT = "a4_draft"
    A5_INTERNAL_WRITE = "a5_internal_write"
    A6_EXTERNAL_QUEUE = "a6_external_queue"
    A7_EXTERNAL_EXECUTE = "a7_external_execute"


ACCESS_CLASSES: tuple[AccessClass, ...] = tuple(AccessClass)


def is_access_allowed_in_mvp(c: AccessClass) -> bool:
    return c in {
        AccessClass.A1_READ_METADATA,
        AccessClass.A2_READ_PASSPORTED,
        AccessClass.A3_ANALYZE,
        AccessClass.A4_DRAFT,
    }


@dataclass(frozen=True)
class AccessCard:
    agent_id: str
    allowed_access: frozenset[AccessClass]
    forbidden_access: frozenset[AccessClass]
    allowed_sources: tuple[str, ...]
    forbidden_sources: tuple[str, ...]
    approval_required_for: tuple[str, ...]

    def __post_init__(self) -> None:
        overlap = self.allowed_access & self.forbidden_access
        if overlap:
            raise ValueError(
                "allowed_and_forbidden_overlap:"
                + ",".join(sorted(a.value for a in overlap))
            )
        if AccessClass.A7_EXTERNAL_EXECUTE in self.allowed_access:
            raise ValueError("a7_execute_forbidden_in_mvp")
