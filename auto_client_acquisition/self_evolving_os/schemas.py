"""Schemas for System 35 — the Self-Evolving Enterprise Fabric."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ImprovementTarget(StrEnum):
    WORKFLOW = "workflow"
    GOVERNANCE = "governance"
    ORCHESTRATION = "orchestration"


class ProposalStatus(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"


class ImprovementProposal(BaseModel):
    """A proposed improvement — never applied without an approved ticket."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    proposal_id: str = Field(default_factory=lambda: f"imp_{uuid4().hex[:12]}")
    target: ImprovementTarget
    target_id: str
    current_state: dict[str, Any] = Field(default_factory=dict)
    proposed_change: dict[str, Any] = Field(default_factory=dict)
    rationale: str = ""
    expected_gain: dict[str, Any] = Field(default_factory=dict)
    status: ProposalStatus = ProposalStatus.PROPOSED
    approval_ticket_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MetaLearningInsight(BaseModel):
    """A pattern mined from control-plane history."""

    model_config = ConfigDict(extra="forbid")

    insight_id: str = Field(default_factory=lambda: f"ins_{uuid4().hex[:12]}")
    pattern: str
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
