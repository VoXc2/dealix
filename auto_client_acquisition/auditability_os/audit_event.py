"""Auditability OS — append-only audit events for policy / approval trails.

Provides:
- Legacy immutable ``AuditEvent`` + ``audit_event_valid`` contract.
- Runtime JSONL store APIs used by routers/tests:
  ``AuditEventKind``, ``record_event``, ``list_events``, ``clear_for_test``.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from uuid import uuid4

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text

_DEFAULT_PATH = "var/audit-log.jsonl"
_lock = threading.Lock()


class AuditEventKind(StrEnum):
    AI_RUN = "ai_run"
    GOVERNANCE_DECISION = "governance_decision"
    SOURCE_PASSPORT_VALIDATED = "source_passport_validated"
    APPROVAL_DECISION = "approval_decision"
    OUTPUT_GENERATED = "output_generated"


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Legacy schema contract used by foundational governance tests."""

    event_id: str
    actor: str
    source: str
    policy_checked: str
    matched_rule: str
    decision: str
    approval_status: str
    output_id: str
    timestamp_iso: str


@dataclass(frozen=True, slots=True)
class AuditLogEvent:
    """Runtime audit log row used by API + evidence chain."""

    event_id: str
    customer_id: str
    engagement_id: str
    kind: str
    actor: str
    source_refs: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)
    decision: str = ""
    policy_checked: str = ""
    summary: str = ""
    tenant_id: str = "default"
    occurred_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_AUDIT_LOG_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _normalize_kind(kind: str | AuditEventKind) -> str:
    if isinstance(kind, AuditEventKind):
        return kind.value
    return str(kind).strip().lower()


def _coerce_event(data: dict[str, object]) -> AuditLogEvent | None:
    try:
        return AuditLogEvent(
            event_id=str(data.get("event_id", "")),
            customer_id=str(data.get("customer_id", "")),
            engagement_id=str(data.get("engagement_id", "")),
            kind=str(data.get("kind", "")),
            actor=str(data.get("actor", "system")),
            source_refs=[str(x) for x in data.get("source_refs", []) or []],
            output_refs=[str(x) for x in data.get("output_refs", []) or []],
            decision=str(data.get("decision", "")),
            policy_checked=str(data.get("policy_checked", "")),
            summary=str(data.get("summary", "")),
            tenant_id=str(data.get("tenant_id", "default") or "default"),
            occurred_at=str(data.get("occurred_at", "")) or datetime.now(UTC).isoformat(),
        )
    except (TypeError, ValueError):
        return None


def record_event(
    *,
    customer_id: str,
    engagement_id: str = "",
    kind: str | AuditEventKind = AuditEventKind.AI_RUN,
    actor: str = "system",
    source_refs: list[str] | None = None,
    output_refs: list[str] | None = None,
    decision: str = "",
    policy_checked: str = "",
    summary: str = "",
    tenant_id: str = "default",
) -> AuditLogEvent:
    """Append one audit event with PII-redacted summary."""
    cid = customer_id.strip()
    if not cid:
        raise ValueError("customer_id is required")
    event = AuditLogEvent(
        event_id=f"aud_{uuid4().hex[:16]}",
        customer_id=cid,
        engagement_id=engagement_id.strip(),
        kind=_normalize_kind(kind),
        actor=actor.strip() or "system",
        source_refs=[str(x) for x in (source_refs or [])],
        output_refs=[str(x) for x in (output_refs or [])],
        decision=decision.strip(),
        policy_checked=policy_checked.strip(),
        summary=redact_text(summary or ""),
        tenant_id=tenant_id.strip() or "default",
    )
    path = _path()
    _ensure_parent(path)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(
    *,
    customer_id: str = "",
    engagement_id: str = "",
    limit: int = 200,
    since_days: int = 3650,
) -> list[AuditLogEvent]:
    """List audit events with optional customer/engagement filters."""
    path = _path()
    if not path.exists():
        return []
    customer_filter = customer_id.strip()
    engagement_filter = engagement_id.strip()
    cutoff = datetime.now(UTC) - timedelta(days=max(int(since_days), 0))
    rows: list[AuditLogEvent] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            ev = _coerce_event(payload if isinstance(payload, dict) else {})
            if ev is None:
                continue
            if customer_filter and ev.customer_id != customer_filter:
                continue
            if engagement_filter and ev.engagement_id != engagement_filter:
                continue
            try:
                ts = datetime.fromisoformat(ev.occurred_at)
            except ValueError:
                ts = datetime.min.replace(tzinfo=UTC)
            if ts < cutoff:
                continue
            rows.append(ev)
    rows.sort(key=lambda e: e.occurred_at, reverse=True)
    return rows[: max(int(limit), 0)]


def clear_for_test() -> None:
    path = _path()
    if not path.exists():
        return
    with _lock:
        path.write_text("", encoding="utf-8")


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


__all__ = [
    "AuditEvent",
    "AuditEventKind",
    "AuditLogEvent",
    "audit_event_valid",
    "clear_for_test",
    "list_events",
    "record_event",
]
