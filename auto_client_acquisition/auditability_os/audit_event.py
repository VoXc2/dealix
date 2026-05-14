"""Audit event store — every decision/action recorded as an immutable event.

Storage: $DEALIX_AUDIT_LOG_PATH (default var/audit-log.jsonl). Append-only.
PII sanitized via existing redact_text.
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
from uuid import uuid4

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text


class AuditEventKind(StrEnum):
    SOURCE_PASSPORT_VALIDATED = "source_passport_validated"
    AI_RUN = "ai_run"
    POLICY_CHECK = "policy_check"
    GOVERNANCE_DECISION = "governance_decision"
    HUMAN_REVIEW = "human_review"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_REJECTED = "approval_rejected"
    OUTPUT_DELIVERED = "output_delivered"
    PROOF_PACK_ASSEMBLED = "proof_pack_assembled"
    VALUE_EVENT_RECORDED = "value_event_recorded"
    CAPITAL_ASSET_REGISTERED = "capital_asset_registered"
    INCIDENT = "incident"
    DELETION_REQUESTED = "deletion_requested"
    DELETION_COMPLETED = "deletion_completed"


_DEFAULT_PATH = "var/audit-log.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_AUDIT_LOG_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class AuditEvent:
    event_id: str = field(default_factory=lambda: f"aud_{uuid4().hex[:12]}")
    customer_id: str = ""
    engagement_id: str = ""
    kind: str = AuditEventKind.AI_RUN.value
    actor: str = ""  # "founder" | "agent:<id>" | "system"
    source_refs: list[str] = field(default_factory=list)  # source_passport ids, evidence ids
    output_refs: list[str] = field(default_factory=list)  # proof_event ids, capital asset ids
    decision: str = ""  # governance decision if applicable
    policy_checked: str = ""  # name of the policy
    summary: str = ""  # short description (will be redacted)
    occurred_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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
) -> AuditEvent:
    """Persist a single audit event. Summary is PII-redacted."""
    if not customer_id:
        raise ValueError("customer_id is required")
    kind_value = kind.value if isinstance(kind, AuditEventKind) else str(kind)
    event = AuditEvent(
        customer_id=customer_id,
        engagement_id=engagement_id,
        kind=kind_value,
        actor=actor,
        source_refs=list(source_refs or []),
        output_refs=list(output_refs or []),
        decision=decision,
        policy_checked=policy_checked,
        summary=redact_text(summary) if summary else "",
    )
    path = _path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(
    *,
    customer_id: str | None = None,
    engagement_id: str | None = None,
    kind: str | None = None,
    limit: int = 500,
) -> list[AuditEvent]:
    path = _path()
    if not path.exists():
        return []
    out: list[AuditEvent] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    ev = AuditEvent(**data)
                except Exception:  # noqa: BLE001
                    continue
                if customer_id and ev.customer_id != customer_id:
                    continue
                if engagement_id and ev.engagement_id != engagement_id:
                    continue
                if kind and ev.kind != kind:
                    continue
                out.append(ev)
                if len(out) >= limit:
                    break
    return out


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = ["AuditEvent", "AuditEventKind", "clear_for_test", "list_events", "record_event"]
