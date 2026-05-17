"""Pydantic schema for the append-only Evidence Events ledger.

An Evidence Event is one immutable record that an action, observation or
proof artifact occurred. The ledger is append-only: events are never
updated or deleted. ``source`` is mandatory — no source-less evidence.
"""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class EvidenceEvent(BaseModel):
    """One immutable evidence record."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: f"evd_{uuid4().hex[:16]}")
    event_type: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    summary: str = ""
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    approval_required: bool = False
    linked_asset: str | None = None
    actor: str = Field(..., min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


__all__ = ["EvidenceEvent"]
