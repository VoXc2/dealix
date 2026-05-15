"""Evidence object — canonical fields for auditable artifacts.

Adds a JSONL-backed evidence store (env ``DEALIX_EVIDENCE_CONTROL_PATH``) so the
Evidence Control Plane can record + list governed AI runs, source passports,
approvals and outputs. Summaries are PII-redacted before persistence.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any

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


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    """A persisted, tenant-scoped evidence row. Summary is PII-redacted."""

    type: str
    customer_id: str
    summary: str
    project_id: str = ""
    source_ids: tuple[str, ...] = ()
    actor_id: str = ""
    evidence_id: str = field(default_factory=lambda: f"EVD-{uuid.uuid4().hex[:12]}")
    recorded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["source_ids"] = list(self.source_ids)
        return d


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_EVIDENCE_CONTROL_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _type_value(t: str | EvidenceType) -> str:
    return t.value if isinstance(t, EvidenceType) else str(t)


def create_evidence(
    *,
    type: str | EvidenceType,
    customer_id: str,
    summary: str,
    project_id: str = "",
    source_ids: list[str] | tuple[str, ...] | None = None,
    actor_id: str = "",
) -> EvidenceRecord:
    """Append one evidence row. Summary is PII-redacted before persistence."""
    if not customer_id:
        raise ValueError("customer_id is required")
    from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text

    record = EvidenceRecord(
        type=_type_value(type),
        customer_id=customer_id,
        summary=redact_text(summary or ""),
        project_id=project_id,
        source_ids=tuple(source_ids or ()),
        actor_id=actor_id,
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    return record


def list_evidence(
    *,
    customer_id: str | None = None,
    type: str | EvidenceType | None = None,
    project_id: str | None = None,
    limit: int = 500,
) -> list[EvidenceRecord]:
    """Return persisted evidence rows, optionally scoped by tenant / type."""
    path = _path()
    if not path.exists():
        return []
    type_filter = _type_value(type) if type is not None else None
    out: list[EvidenceRecord] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    data["source_ids"] = tuple(data.get("source_ids", []))
                    record = EvidenceRecord(**data)
                except Exception:  # noqa: BLE001
                    continue
                if customer_id is not None and record.customer_id != customer_id:
                    continue
                if type_filter is not None and record.type != type_filter:
                    continue
                if project_id is not None and record.project_id != project_id:
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
    "EvidenceObject",
    "EvidenceRecord",
    "EvidenceType",
    "clear_for_test",
    "create_evidence",
    "evidence_object_valid",
    "is_critical_evidence_type",
    "list_evidence",
]
