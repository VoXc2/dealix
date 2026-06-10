"""Approval-gated outreach queue — drafts wait for founder approval before any send."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class OutreachDraft:
    """A single pending outreach draft awaiting founder approval."""
    draft_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8].upper())
    lead_id: str = ""
    company_name: str = ""
    contact_name: str = ""
    channel: str = "email"  # email | whatsapp
    subject_ar: str = ""
    subject_en: str = ""
    body_ar: str = ""
    body_en: str = ""
    score: float = 0.0
    sector: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    status: str = "pending_approval"  # pending_approval | approved | rejected | sent
    approved_by: str = ""
    approved_at: str = ""
    rejection_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__.items())


class OutreachQueue:
    """In-memory approval queue for outreach drafts.

    Doctrine: items can only move to 'approved' via explicit founder action.
    The queue NEVER auto-approves or auto-sends.
    """
    _instance: OutreachQueue | None = None

    def __init__(self) -> None:
        self._drafts: dict[str, OutreachDraft] = {}

    @classmethod
    def instance(cls) -> OutreachQueue:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def enqueue(self, draft: OutreachDraft) -> str:
        """Add a draft to the queue. Returns draft_id."""
        self._drafts[draft.draft_id] = draft
        logger.info("outreach_draft_queued", draft_id=draft.draft_id, company=draft.company_name, channel=draft.channel)
        return draft.draft_id

    def approve(self, draft_id: str, approved_by: str = "founder") -> OutreachDraft:
        """Mark a draft as approved. Does NOT send — caller must handle send."""
        draft = self._get_or_raise(draft_id)
        draft.status = "approved"
        draft.approved_by = approved_by
        draft.approved_at = datetime.now(UTC).isoformat()
        logger.info("outreach_draft_approved", draft_id=draft_id, by=approved_by)
        return draft

    def reject(self, draft_id: str, reason: str = "") -> OutreachDraft:
        """Reject a draft."""
        draft = self._get_or_raise(draft_id)
        draft.status = "rejected"
        draft.rejection_reason = reason
        logger.info("outreach_draft_rejected", draft_id=draft_id)
        return draft

    def pending(self) -> list[OutreachDraft]:
        return [d for d in self._drafts.values() if d.status == "pending_approval"]

    def approved(self) -> list[OutreachDraft]:
        return [d for d in self._drafts.values() if d.status == "approved"]

    def all_drafts(self) -> list[OutreachDraft]:
        return list(self._drafts.values())

    def stats(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for d in self._drafts.values():
            counts[d.status] = counts.get(d.status, 0) + 1
        return counts

    def _get_or_raise(self, draft_id: str) -> OutreachDraft:
        if draft_id not in self._drafts:
            raise KeyError(f"Draft {draft_id!r} not found")
        return self._drafts[draft_id]


__all__ = ["OutreachDraft", "OutreachQueue"]
