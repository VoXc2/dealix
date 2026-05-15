"""Human-AI oversight schemas."""

from __future__ import annotations

from datetime import UTC, datetime
from pydantic import BaseModel, ConfigDict, Field
from uuid import uuid4


class Delegation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    delegation_id: str = Field(default_factory=lambda: f"dlg_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    delegated_by: str = Field(..., min_length=1)
    delegated_to: str = Field(..., min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Escalation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    escalation_id: str = Field(default_factory=lambda: f"esc_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)
    escalated_by: str = Field(..., min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


__all__ = ["Delegation", "Escalation"]
