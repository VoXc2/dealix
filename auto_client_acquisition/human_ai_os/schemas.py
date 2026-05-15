"""Schemas for System 33 — the Human-AI Operating Model."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Delegation(BaseModel):
    """A bounded grant of authority from a human to an agent.

    `expires_at` is mandatory — there is no such thing as an unbounded
    delegation (`no_unbounded_agents`).
    """

    model_config = ConfigDict(extra="forbid")

    delegation_id: str = Field(default_factory=lambda: f"dlg_{uuid4().hex[:12]}")
    from_human: str
    to_agent: str
    scope: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime
    revoked: bool = False


class Escalation(BaseModel):
    """A run escalated to a human for a decision."""

    model_config = ConfigDict(extra="forbid")

    escalation_id: str = Field(default_factory=lambda: f"esc_{uuid4().hex[:12]}")
    run_id: str
    reason: str
    escalated_to: str
    ticket_id: str
    status: str = "open"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Explanation(BaseModel):
    """A human-readable explanation of a control-plane subject's history."""

    model_config = ConfigDict(extra="forbid")

    subject_id: str
    decision: str
    factors: list[dict[str, Any]] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)


class OversightItem(BaseModel):
    """One pending item in the human oversight queue."""

    model_config = ConfigDict(extra="forbid")

    ticket_id: str
    action_type: str
    description: str
    requested_by: str
    source_module: str
    run_id: str | None = None
    created_at: datetime
