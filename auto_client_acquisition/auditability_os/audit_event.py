"""Auditability OS — append-only audit events for policy / approval trails.

Two layers live here:

  * :class:`AuditEvent` / :func:`audit_event_valid` — schema-stable row
    contract used by callers that persist their own audit records.
  * :class:`AuditEventKind`, :func:`record_event`, :func:`list_events`,
    :func:`clear_for_test` — an append-only JSONL ledger for runtime audit
    events. Path comes from ``DEALIX_AUDIT_LOG_PATH`` (dev fallback below).

PII in ``summary`` is redacted before persistence (PDPL — no PII in logs).
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from auto_client_acquisition.friction_log.sanitizer import sanitize_notes

_DEFAULT_PATH = "var/audit-log.jsonl"
_lock = threading.Lock()


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Minimal enterprise-audit row (persisted by callers; schema-stable)."""

    event_id: str
    actor: str
    source: str
    policy_checked: str
    matched_rule: str
    decision: str
    approval_status: str
    output_id: str
    timestamp_iso: str


def audit_event_valid(e: AuditEvent) -> bool:
    return all(
        (
            e.event_id.strip(),
            e.actor.strip(),
            e.source.strip(),
            e.policy_checked.strip(),
            e.decision.strip(),
            e.timestamp_iso.strip(),
        ),
    )


class AuditEventKind(StrEnum):
    """Kinds of runtime audit events recorded in the JSONL ledger."""

    GOVERNANCE_DECISION = "governance_decision"
    AI_RUN = "ai_run"
    SOURCE_PASSPORT_VALIDATED = "source_passport_validated"
    HUMAN_REVIEW = "human_review"
    APPROVAL = "approval"
    EXTERNAL_SEND = "external_send"
    OUTPUT_PUBLISHED = "output_published"


@dataclass(slots=True)
class AuditLogEntry:
    """An append-only runtime audit event."""

    customer_id: str
    kind: str
    engagement_id: str = ""
    actor: str = "system"
    source_refs: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)
    decision: str = ""
    policy_checked: str = ""
    summary: str = ""
    event_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    occurred_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_AUDIT_LOG_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _kind_value(kind: str | AuditEventKind) -> str:
    return kind.value if isinstance(kind, AuditEventKind) else str(kind)


def record_event(
    *,
    customer_id: str,
    kind: str | AuditEventKind,
    engagement_id: str = "",
    actor: str = "system",
    source_refs: list[str] | None = None,
    output_refs: list[str] | None = None,
    decision: str = "",
    policy_checked: str = "",
    summary: str = "",
) -> AuditLogEntry:
    """Append a runtime audit event to the JSONL ledger.

    Raises :class:`ValueError` if ``customer_id`` is empty. PII in
    ``summary`` is redacted before persistence.
    """
    if not customer_id:
        raise ValueError("customer_id is required")
    entry = AuditLogEntry(
        customer_id=customer_id,
        kind=_kind_value(kind),
        engagement_id=engagement_id,
        actor=actor,
        source_refs=list(source_refs or []),
        output_refs=list(output_refs or []),
        decision=decision,
        policy_checked=policy_checked,
        summary=sanitize_notes(summary),
    )
    path = _path()
    _ensure_dir(path)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")
    return entry


def _parse_entry(line: str) -> AuditLogEntry | None:
    try:
        data = json.loads(line)
        return AuditLogEntry(**data)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def list_events(
    *,
    customer_id: str,
    engagement_id: str | None = None,
    kind: str | AuditEventKind | None = None,
    limit: int = 1000,
) -> list[AuditLogEntry]:
    """Return audit events for ``customer_id``, newest last (insertion order)."""
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    kind_filter = _kind_value(kind) if kind is not None else None
    out: list[AuditLogEntry] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            entry = _parse_entry(line)
            if entry is None or entry.customer_id != customer_id:
                continue
            if engagement_id and entry.engagement_id != engagement_id:
                continue
            if kind_filter and entry.kind != kind_filter:
                continue
            out.append(entry)
            if len(out) >= limit:
                break
    return out


def clear_for_test() -> None:
    """Dev/test helper — truncates the JSONL ledger file."""
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "AuditEvent",
    "AuditEventKind",
    "AuditLogEntry",
    "audit_event_valid",
    "clear_for_test",
    "list_events",
    "record_event",
]
