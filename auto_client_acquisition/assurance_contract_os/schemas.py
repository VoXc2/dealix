"""Assurance contract schemas."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class AssuranceContract:
    contract_id: str
    tenant_id: str
    contract_type: str
    agent_id: str
    action_type: str
    may_see: list[str] = field(default_factory=list)
    may_propose: list[str] = field(default_factory=list)
    may_execute: list[str] = field(default_factory=list)
    precondition_checks: list[str] = field(default_factory=list)
    rollback_plan: str = ""
    is_external: bool = False
    is_irreversible: bool = False
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
