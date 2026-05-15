"""Tenant-aware schemas for Agent Mesh routing."""

from __future__ import annotations

from datetime import UTC, datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


AgentStatus = Literal["active", "inactive", "isolated"]


class AgentDescriptor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str = Field(..., min_length=1)
    tenant_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    trust_tier: str = Field(default="standard", min_length=1)
    autonomy_level: int = Field(default=1, ge=0, le=4)
    status: AgentStatus = "active"
    capabilities: list[str] = Field(default_factory=list)
    tool_permissions: list[str] = Field(default_factory=list)
    composite_score: float = 0.0
    registered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TrustBoundary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    boundary_id: str = Field(..., min_length=1)
    allowed_data_classes: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)


__all__ = ["AgentDescriptor", "TrustBoundary"]
