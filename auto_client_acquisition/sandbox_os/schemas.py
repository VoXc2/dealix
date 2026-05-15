"""Sandbox runtime schemas."""

from __future__ import annotations

from datetime import UTC, datetime
from pydantic import BaseModel, ConfigDict, Field
from uuid import uuid4


class SandboxRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sandbox_run_id: str = Field(default_factory=lambda: f"sbx_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    scenario: str = ""
    status: str = "queued"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


__all__ = ["SandboxRun"]
