"""Self-evolving proposal schemas."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class ImprovementProposal:
    proposal_id: str
    tenant_id: str
    title: str
    summary: str
    proposed_by: str
    state: str = "proposed"  # proposed | approved | applied | rejected
    approval_ticket_id: str = ""
    approved_by: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
