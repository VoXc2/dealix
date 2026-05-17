"""Support ticket store — in-memory with JSONL persistence.

Tickets are mutable (status transitions, drafted replies), so this
mirrors the knowledge ArticleStore pattern: a live dict with a JSONL
append log replayed last-write-wins on load.
"""

from __future__ import annotations

import os
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = REPO_ROOT / "data" / "support"

VALID_STATUSES: frozenset[str] = frozenset(
    {"open", "in_progress", "waiting_customer", "escalated", "resolved", "closed"}
)


def _now() -> datetime:
    return datetime.now(UTC)


class SupportTicket(BaseModel):
    """A persisted support ticket.

    ``message_redacted`` is PII-redacted on creation by the lifecycle layer.
    """

    model_config = ConfigDict(extra="forbid")

    ticket_id: str = Field(default_factory=lambda: f"tkt_{uuid4().hex[:12]}")
    tenant_id: str | None = None
    customer_id: str | None = None
    channel: str = "unknown"
    subject: str = ""
    message_redacted: str = ""
    category: str = "unknown"
    priority: str = "p2"
    sentiment: str = "neutral"
    status: str = "open"
    risk_level: str = "low"
    intent: str = ""
    suggested_reply: str = ""
    kb_article_ids: list[str] = Field(default_factory=list)
    escalation_needed: bool = False
    escalation_reason: str = ""
    sla_due_at: datetime | None = None
    resolved_at: datetime | None = None
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    deleted_at: datetime | None = None


class TicketStore:
    """Thread-safe support ticket store with JSONL persistence."""

    def __init__(self, base_dir: Path | str | None = None) -> None:
        self._lock = threading.Lock()
        self._items: dict[str, SupportTicket] = {}
        self._base = Path(base_dir) if base_dir else DEFAULT_DIR
        self._base.mkdir(parents=True, exist_ok=True)
        self._log = self._base / "tickets.jsonl"
        self._load()

    def _load(self) -> None:
        if not self._log.exists():
            return
        try:
            with self._log.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        tkt = SupportTicket.model_validate_json(line)
                    except Exception:  # noqa: BLE001
                        continue
                    self._items[tkt.ticket_id] = tkt
        except OSError:
            pass

    def _persist(self, tkt: SupportTicket) -> None:
        try:
            with self._log.open("a", encoding="utf-8") as fh:
                fh.write(tkt.model_dump_json() + "\n")
        except OSError:
            pass

    def create(self, tkt: SupportTicket) -> SupportTicket:
        tkt.created_at = _now()
        tkt.updated_at = tkt.created_at
        with self._lock:
            self._items[tkt.ticket_id] = tkt
            self._persist(tkt)
        return tkt

    def update(self, ticket_id: str, patch: dict[str, Any]) -> SupportTicket:
        """Apply a field patch. ``status`` must be a valid value if present."""
        if "status" in patch and patch["status"] not in VALID_STATUSES:
            raise ValueError(f"invalid status: {patch['status']}")
        with self._lock:
            tkt = self._require(ticket_id)
            for key, value in patch.items():
                if hasattr(tkt, key) and key not in {"ticket_id", "created_at"}:
                    setattr(tkt, key, value)
            tkt.updated_at = _now()
            self._persist(tkt)
        return tkt

    def get(self, ticket_id: str) -> SupportTicket | None:
        with self._lock:
            tkt = self._items.get(ticket_id)
        if tkt is None or tkt.deleted_at is not None:
            return None
        return tkt

    def list(
        self,
        *,
        status: str | None = None,
        category: str | None = None,
        risk_level: str | None = None,
        tenant_id: str | None = None,
    ) -> list[SupportTicket]:
        with self._lock:
            rows = list(self._items.values())
        out = []
        for tkt in rows:
            if tkt.deleted_at is not None:
                continue
            if status and tkt.status != status:
                continue
            if category and tkt.category != category:
                continue
            if risk_level and tkt.risk_level != risk_level:
                continue
            if tenant_id and tkt.tenant_id != tenant_id:
                continue
            out.append(tkt)
        out.sort(key=lambda t: t.updated_at, reverse=True)
        return out

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
            try:
                if self._log.exists():
                    self._log.unlink()
            except OSError:
                pass

    def _require(self, ticket_id: str) -> SupportTicket:
        tkt = self._items.get(ticket_id)
        if tkt is None or tkt.deleted_at is not None:
            raise ValueError(f"support ticket {ticket_id} not found")
        return tkt


_DEFAULT: TicketStore | None = None


def get_default_ticket_store() -> TicketStore:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = TicketStore(os.getenv("DEALIX_SUPPORT_DIR"))
    return _DEFAULT


def reset_default_ticket_store() -> None:
    """Test helper: drop the cached singleton."""
    global _DEFAULT
    _DEFAULT = None
