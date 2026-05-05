"""Schemas for the Approval Command Center.

Every "approval_required" action across the platform — outbound draft
messages, invoice drafts, proof packs, partner intros, etc. — funnels
through these schemas. The store is in-memory / file-backed for now;
the Pydantic surface is what stays stable when we swap to Redis later.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    BLOCKED = "blocked"


class ApprovalRequest(BaseModel):
    """A single approvable action awaiting human review.

    ``action_mode`` mirrors the platform-wide gate vocabulary:
      - ``draft_only``        → never sent live, kept as draft
      - ``approval_required`` → human must approve before any send
      - ``approved_execute``  → already approved upstream; recorded for audit
      - ``blocked``           → hard-stopped by policy; cannot be approved
    """

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    approval_id: str = Field(default_factory=lambda: f"apr_{uuid4().hex[:12]}")
    object_type: str
    object_id: str
    action_type: str
    action_mode: str = "approval_required"
    channel: str | None = None
    summary_ar: str = ""
    summary_en: str = ""
    risk_level: str = "low"
    proof_impact: str = ""
    expires_at: datetime | None = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    edit_history: list[dict[str, Any]] = Field(default_factory=list)
    reject_reason: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
