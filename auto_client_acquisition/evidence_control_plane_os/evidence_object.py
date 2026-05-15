"""Evidence object — canonical fields for auditable artifacts.

Two surfaces:

* :class:`EvidenceObject` + :func:`evidence_object_valid` — the
  schema-stable validation row.
* :class:`EvidenceItem` + :func:`create_evidence` / :func:`list_evidence`
  — the JSONL-backed evidence store keyed by ``DEALIX_EVIDENCE_CONTROL_PATH``.
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

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text


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


_DEFAULT_PATH = "var/evidence-control.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_EVIDENCE_CONTROL_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _type_value(t: str | EvidenceType) -> str:
    return t.value if isinstance(t, EvidenceType) else str(t)


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    """A persisted, customer-scoped evidence record."""

    evidence_id: str
    type: str
    customer_id: str
    project_id: str = ""
    summary: str = ""
    source_ids: list[str] = field(default_factory=list)
    linked_artifacts: list[str] = field(default_factory=list)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def create_evidence(
    *,
    type: str | EvidenceType,
    customer_id: str,
    project_id: str = "",
    summary: str = "",
    source_ids: list[str] | None = None,
    linked_artifacts: list[str] | None = None,
) -> EvidenceItem:
    """Append a PII-redacted evidence item to the tenant-scoped store."""
    if not customer_id:
        raise ValueError("customer_id is required")
    type_str = _type_value(type)
    if not type_str.strip():
        raise ValueError("evidence type is required")
    item = EvidenceItem(
        evidence_id=f"ev_{uuid.uuid4().hex[:12]}",
        type=type_str,
        customer_id=customer_id,
        project_id=project_id,
        summary=redact_text(summary) if summary else "",
        source_ids=list(source_ids or []),
        linked_artifacts=list(linked_artifacts or []),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")
    return item


def list_evidence(
    *,
    customer_id: str,
    type: str | EvidenceType | None = None,
    project_id: str | None = None,
    limit: int = 500,
) -> list[EvidenceItem]:
    """List evidence items for a customer, optionally filtered by type/project."""
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    type_filter = _type_value(type) if type is not None else None
    out: list[EvidenceItem] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    item = EvidenceItem(**data)
                except Exception:  # noqa: BLE001
                    continue
                if item.customer_id != customer_id:
                    continue
                if type_filter is not None and item.type != type_filter:
                    continue
                if project_id is not None and item.project_id != project_id:
                    continue
                out.append(item)
    return out[-limit:] if limit else out


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "EvidenceItem",
    "EvidenceObject",
    "EvidenceType",
    "clear_for_test",
    "create_evidence",
    "evidence_object_valid",
    "is_critical_evidence_type",
    "list_evidence",
]
