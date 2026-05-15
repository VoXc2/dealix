"""Auditability OS — append-only audit events for policy / approval trails.

Two surfaces live here:

* :class:`AuditEvent` + :func:`audit_event_valid` — the schema-stable
  enterprise audit row used by ``platform_core`` and observability.
* :class:`AuditEventRecord` + :func:`record_event` / :func:`list_events`
  — the JSONL-backed customer-scoped audit log used by the audit-export
  API and the evidence chain. Summaries are PII-redacted on write.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text


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
    """Kinds of customer-scoped audit events."""

    SOURCE_PASSPORT_VALIDATED = "source_passport_validated"
    AI_RUN = "ai_run"
    GOVERNANCE_DECISION = "governance_decision"
    APPROVAL = "approval"
    OUTPUT_DELIVERED = "output_delivered"
    PROOF_PACK_ASSEMBLED = "proof_pack_assembled"


_DEFAULT_PATH = "var/audit-log.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_AUDIT_LOG_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _kind_value(k: str | AuditEventKind) -> str:
    return k.value if isinstance(k, AuditEventKind) else str(k)


@dataclass(frozen=True, slots=True)
class AuditEventRecord:
    """A single customer-scoped audit log entry."""

    customer_id: str
    kind: str
    actor: str = "system"
    engagement_id: str = ""
    decision: str = ""
    policy_checked: str = ""
    summary: str = ""
    source_refs: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)
    occurred_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def record_event(
    *,
    customer_id: str,
    kind: str | AuditEventKind,
    actor: str = "system",
    engagement_id: str = "",
    decision: str = "",
    policy_checked: str = "",
    summary: str = "",
    source_refs: list[str] | None = None,
    output_refs: list[str] | None = None,
) -> AuditEventRecord:
    """Append a PII-redacted audit event to the tenant-scoped JSONL log."""
    if not customer_id:
        raise ValueError("customer_id is required")
    kind_str = _kind_value(kind)
    if kind_str not in {k.value for k in AuditEventKind}:
        raise ValueError(f"unknown audit event kind: {kind_str!r}")
    event = AuditEventRecord(
        customer_id=customer_id,
        kind=kind_str,
        actor=actor or "system",
        engagement_id=engagement_id,
        decision=decision,
        policy_checked=policy_checked,
        summary=redact_text(summary) if summary else "",
        source_refs=list(source_refs or []),
        output_refs=list(output_refs or []),
        occurred_at=datetime.now(timezone.utc).isoformat(),
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(
    *,
    customer_id: str,
    limit: int = 200,
) -> list[AuditEventRecord]:
    """List audit events for a customer, oldest first."""
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    out: list[AuditEventRecord] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    ev = AuditEventRecord(**data)
                except Exception:  # noqa: BLE001
                    continue
                if ev.customer_id != customer_id:
                    continue
                out.append(ev)
    return out[-limit:] if limit else out


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "AuditEvent",
    "AuditEventKind",
    "AuditEventRecord",
    "audit_event_valid",
    "clear_for_test",
    "list_events",
    "record_event",
]
