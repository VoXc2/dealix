"""Assurance contract schemas for tenant-scoped action governance."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class AssuranceContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(default_factory=lambda: f"ctr_{uuid4().hex[:12]}")
    tenant_id: str = Field(..., min_length=1)
    agent_id: str = Field(..., min_length=1)
    action_type: str = Field(..., min_length=1)
    may_execute: list[str] = Field(default_factory=list)
    precondition_checks: list[str] = Field(default_factory=list)
    is_external: bool = False
    is_irreversible: bool = False
    rollback_plan: str = ""
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


__all__ = ["AssuranceContract"]
