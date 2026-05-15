"""Schemas for self-evolving proposals (never auto-apply)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ImprovementProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    proposal_id: str = Field(default_factory=lambda: f"imp_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    summary: str = ""
    status: str = "proposed"
    approval_ticket_id: str = ""
    approved: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


__all__ = ["ImprovementProposal"]
