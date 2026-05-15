"""Schemas for System 27 — Agent Mesh Infrastructure."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TrustTier(StrEnum):
    INTERNAL = "internal"
    PARTNER = "partner"
    VENDOR = "vendor"
    THIRD_PARTY = "third_party"
    UNTRUSTED = "untrusted"


class AgentStatus(StrEnum):
    ACTIVE = "active"
    MONITORED = "monitored"
    ISOLATED = "isolated"
    RETIRED = "retired"


class AgentDescriptor(BaseModel):
    """A mesh-level record for one agent — identity + capabilities + trust."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    agent_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)
    capabilities: list[str] = Field(default_factory=list)
    trust_tier: TrustTier = TrustTier.INTERNAL
    status: AgentStatus = AgentStatus.ACTIVE
    autonomy_level: int = Field(default=2, ge=0, le=4)
    endpoint: str = ""
    composite_score: float | None = None
    registered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TrustBoundary(BaseModel):
    """Capability + autonomy limits for one agent."""

    model_config = ConfigDict(extra="forbid")

    agent_id: str
    allowed_capabilities: list[str] = Field(default_factory=list)
    denied_capabilities: list[str] = Field(default_factory=list)
    max_autonomy_level: int = Field(default=4, ge=0, le=4)


class RoutingDecision(BaseModel):
    """Which agent a capability request was routed to."""

    model_config = ConfigDict(extra="forbid")

    requested_capability: str
    chosen_agent_id: str | None
    trust_tier: str | None
    reason: str


class AgentScore(BaseModel):
    """Reliability / safety / latency score for an agent."""

    model_config = ConfigDict(extra="forbid")

    agent_id: str
    reliability: float = Field(ge=0.0, le=1.0)
    safety: float = Field(ge=0.0, le=1.0)
    latency_ms: float = Field(ge=0.0)
    composite: float = Field(ge=0.0, le=1.0)
