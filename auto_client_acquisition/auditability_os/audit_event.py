"""Auditability OS — append-only audit events for policy / approval trails.

Two layers live here:

* ``AuditEvent`` — the schema-stable enterprise-audit row plus
  ``audit_event_valid`` (unchanged; used by existing callers).
* ``AuditRecord`` + a JSONL-backed recording API (``record_event`` /
  ``list_events`` / ``clear_for_test``) that mirrors ``friction_log/store.py``:
  env-var path override, ``threading.Lock``, ``_path()`` helper, append-only.

All persisted text is PII-redacted; no raw contact data ever lands in the log.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
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


class AuditEventKind(str, Enum):
    """Kinds of auditable events recorded on an engagement."""

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


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _kind_value(k: str | AuditEventKind) -> str:
    return k.value if isinstance(k, AuditEventKind) else str(k)


@dataclass(frozen=True, slots=True)
class AuditRecord:
    """A single append-only audit row, tenant-scoped via customer_id."""

    event_id: str
    customer_id: str
    engagement_id: str
    kind: str
    actor: str
    decision: str
    policy_checked: str
    summary: str
    source_refs: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)
    occurred_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def record_event(
    *,
    customer_id: str,
    kind: str | AuditEventKind,
    engagement_id: str = "",
    actor: str = "system",
    decision: str = "",
    policy_checked: str = "",
    summary: str = "",
    source_refs: list[str] | None = None,
    output_refs: list[str] | None = None,
) -> AuditRecord:
    """Append one audit event to the JSONL store.

    The ``summary`` is PII-redacted before persistence so no raw contact
    data (email, phone, national ID) ever reaches the log.
    """
    if not customer_id:
        raise ValueError("customer_id is required")
    record = AuditRecord(
        event_id=uuid.uuid4().hex,
        customer_id=customer_id,
        engagement_id=engagement_id,
        kind=_kind_value(kind),
        actor=actor,
        decision=decision,
        policy_checked=policy_checked,
        summary=redact_text(summary) if summary else "",
        source_refs=list(source_refs or []),
        output_refs=list(output_refs or []),
        occurred_at=datetime.now(timezone.utc).isoformat(),
    )
    path = _path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    return record


def list_events(
    *,
    customer_id: str,
    engagement_id: str = "",
    kind: str | AuditEventKind | None = None,
    limit: int = 500,
) -> list[AuditRecord]:
    """Return audit records for a tenant, oldest first."""
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    kind_filter = _kind_value(kind) if kind is not None else None
    out: list[AuditRecord] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    record = AuditRecord(**data)
                except Exception:  # noqa: BLE001
                    continue
                if record.customer_id != customer_id:
                    continue
                if engagement_id and record.engagement_id != engagement_id:
                    continue
                if kind_filter and record.kind != kind_filter:
                    continue
                out.append(record)
                if len(out) >= limit:
                    break
    return out


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "AuditEvent",
    "AuditEventKind",
    "AuditRecord",
    "audit_event_valid",
    "clear_for_test",
    "list_events",
    "record_event",
]
