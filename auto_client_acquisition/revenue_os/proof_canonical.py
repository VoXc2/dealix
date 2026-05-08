"""
Canonical Proof Event shape (product contract) ↔ maps into ProofLedger.payload.

Ledger rows use `ProofEvent` in proof_ledger/schemas.py; rich metrics live in payload.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProofEventCanonical(BaseModel):
    """Fields the Portal / Proof Studio expect — persist inside ProofEvent.payload."""

    model_config = ConfigDict(extra="forbid")

    what_happened_ar: str = ""
    what_happened_en: str = ""
    action_id: str | None = None
    customer_id: str | None = None
    source: str = ""
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metric: str | None = None
    metric_before: float | None = None
    metric_after: float | None = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    evidence_level: int = Field(default=0, ge=0, le=5)
    consent_status: str = "unknown"
    public_allowed: bool = False

    def as_ledger_payload(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
