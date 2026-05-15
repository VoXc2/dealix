"""Friction Log schemas."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4


class FrictionKind(StrEnum):
    GOVERNANCE_BLOCK = "governance_block"
    APPROVAL_DELAY = "approval_delay"
    SCHEMA_FAILURE = "schema_failure"
    MANUAL_OVERRIDE = "manual_override"
    RETRY = "retry"
    SUPPORT_TICKET = "support_ticket"
    MISSING_SOURCE_PASSPORT = "missing_source_passport"
    MISSING_PROOF_PACK = "missing_proof_pack"
    AI_REGRESSION = "ai_regression"


class FrictionSeverity(StrEnum):
    LOW = "low"
    MED = "med"
    HIGH = "high"


@dataclass
class FrictionEvent:
    event_id: str = field(default_factory=lambda: f"frc_{uuid4().hex[:12]}")
    customer_id: str = ""
    workflow_id: str = ""
    kind: str = FrictionKind.MANUAL_OVERRIDE.value
    severity: str = FrictionSeverity.LOW.value
    evidence_ref: str = ""
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved_at: str = ""
    cost_minutes: int = 0
    notes: str = ""  # already-sanitized by store.emit before persistence

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


__all__ = ["FrictionEvent", "FrictionKind", "FrictionSeverity"]
