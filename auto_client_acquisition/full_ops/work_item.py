"""V12 — unified ``WorkItem`` schema for the Daily Command Center."""
from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

OSType = Literal[
    "growth",
    "sales",
    "support",
    "customer_success",
    "delivery",
    "partnership",
    "compliance",
    "executive",
    "self_improvement",
]

Priority = Literal["p0", "p1", "p2", "p3"]

WorkItemStatus = Literal[
    "new",
    "triaged",
    "in_progress",
    "needs_approval",
    "waiting_customer",
    "done",
    "blocked",
    "escalated",
]

ActionMode = Literal[
    "suggest_only",
    "draft_only",
    "approval_required",
    "approved_manual",
    "blocked",
]


def _deterministic_id(*parts: str) -> str:
    """Stable 16-char id derived from the given parts."""
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return f"wi_{digest[:16]}"


class WorkItem(BaseModel):
    """A single thing the founder (or an agent) should look at.

    Holds NO PII directly — ``customer_id`` + ``evidence_ids`` are
    references, not free-text. Bilingual fields stay short (≤ 140
    chars) so the daily command center renders cleanly.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    tenant_id: str = "dealix"
    customer_id: str | None = None
    os_type: OSType
    title_ar: str = Field(min_length=1, max_length=140)
    title_en: str = Field(min_length=1, max_length=140)
    description_ar: str = ""
    description_en: str = ""
    priority: Priority = "p2"
    status: WorkItemStatus = "new"
    action_mode: ActionMode = "draft_only"
    owner_role: str = "founder"
    due_at: datetime | None = None
    source: str = "unknown"
    evidence_ids: list[str] = Field(default_factory=list)
    proof_event_ids: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    next_action_ar: str = ""
    next_action_en: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def make(
        cls,
        *,
        os_type: OSType,
        title_ar: str,
        title_en: str,
        source: str,
        priority: Priority = "p2",
        status: WorkItemStatus = "new",
        action_mode: ActionMode = "draft_only",
        customer_id: str | None = None,
        **extra: Any,
    ) -> WorkItem:
        """Construct with a deterministic id derived from os/source/title."""
        wid = _deterministic_id(os_type, source, title_en, customer_id or "")
        return cls(
            id=wid,
            os_type=os_type,
            title_ar=title_ar,
            title_en=title_en,
            source=source,
            priority=priority,
            status=status,
            action_mode=action_mode,
            customer_id=customer_id,
            **extra,
        )
