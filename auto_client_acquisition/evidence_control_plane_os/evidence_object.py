"""Evidence object — canonical fields for auditable artifacts.

Two layers live here:

  * :class:`EvidenceObject` / :func:`evidence_object_valid` — schema-stable
    row contract for callers that persist their own evidence records.
  * :func:`create_evidence`, :func:`list_evidence`, :func:`clear_for_test`
    — an append-only JSONL ledger for evidence control-plane records. Path
    comes from ``DEALIX_EVIDENCE_CONTROL_PATH`` (dev fallback below).

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

_DEFAULT_PATH = "var/evidence-control.jsonl"
_lock = threading.Lock()


class EvidenceType(StrEnum):
    SOURCE = "source"
    SOURCE_PASSPORT = "source_passport"
    AI_RUN = "ai_run"
    POLICY_CHECK = "policy_check"
    GOVERNANCE_DECISION = "governance_decision"
    HUMAN_REVIEW = "human_review"
    APPROVAL = "approval"
    OUTPUT = "output"
    PROOF = "proof"
    VALUE = "value"
    RISK = "risk"
    DECISION = "decision"


@dataclass(frozen=True, slots=True)
class EvidenceObject:
    evidence_id: str
    evidence_type: str
    client_id: str
    project_id: str
    actor_type: str
    actor_id: str
    human_owner: str
    source_ids: tuple[str, ...]
    linked_artifacts: tuple[str, ...]
    summary: str
    confidence: str
    timestamp_iso: str


def evidence_object_valid(obj: EvidenceObject) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not obj.evidence_id.strip():
        errors.append("evidence_id_required")
    if not obj.evidence_type.strip():
        errors.append("evidence_type_required")
    if not obj.client_id.strip():
        errors.append("client_id_required")
    if not obj.summary.strip():
        errors.append("summary_required")
    if not obj.timestamp_iso.strip():
        errors.append("timestamp_required")
    return not errors, tuple(errors)


def is_critical_evidence_type(evidence_type: str) -> bool:
    return evidence_type in (
        EvidenceType.GOVERNANCE_DECISION,
        EvidenceType.APPROVAL,
        EvidenceType.AI_RUN,
        EvidenceType.OUTPUT,
    )


def _type_value(evidence_type: str | EvidenceType) -> str:
    return evidence_type.value if isinstance(evidence_type, EvidenceType) else str(evidence_type)


@dataclass(slots=True)
class EvidenceRecord:
    """An append-only evidence control-plane record."""

    customer_id: str
    type: str
    project_id: str = ""
    actor: str = "system"
    source_ids: list[str] = field(default_factory=list)
    linked_artifacts: list[str] = field(default_factory=list)
    summary: str = ""
    evidence_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_EVIDENCE_CONTROL_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def create_evidence(
    *,
    type: str | EvidenceType,
    customer_id: str,
    project_id: str = "",
    actor: str = "system",
    source_ids: list[str] | None = None,
    linked_artifacts: list[str] | None = None,
    summary: str = "",
) -> EvidenceRecord:
    """Append an evidence record to the JSONL ledger.

    Raises :class:`ValueError` if ``customer_id`` is empty. PII in
    ``summary`` is redacted before persistence.
    """
    if not customer_id:
        raise ValueError("customer_id is required")
    record = EvidenceRecord(
        customer_id=customer_id,
        type=_type_value(type),
        project_id=project_id,
        actor=actor,
        source_ids=list(source_ids or []),
        linked_artifacts=list(linked_artifacts or []),
        summary=sanitize_notes(summary),
    )
    path = _path()
    _ensure_dir(path)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    return record


def _parse_record(line: str) -> EvidenceRecord | None:
    try:
        data = json.loads(line)
        return EvidenceRecord(**data)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def list_evidence(
    *,
    customer_id: str,
    project_id: str | None = None,
    type: str | EvidenceType | None = None,
    limit: int = 1000,
) -> list[EvidenceRecord]:
    """Return evidence records for ``customer_id``, insertion order."""
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    type_filter = _type_value(type) if type is not None else None
    out: list[EvidenceRecord] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            record = _parse_record(line)
            if record is None or record.customer_id != customer_id:
                continue
            if project_id and record.project_id != project_id:
                continue
            if type_filter and record.type != type_filter:
                continue
            out.append(record)
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
    "EvidenceObject",
    "EvidenceRecord",
    "EvidenceType",
    "clear_for_test",
    "create_evidence",
    "evidence_object_valid",
    "is_critical_evidence_type",
    "list_evidence",
]
