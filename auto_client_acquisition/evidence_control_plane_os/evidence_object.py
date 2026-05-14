"""Canonical EvidenceObject — append-only JSONL store.

A typed object that links a source artifact → an operation → its outputs.
Compatible with the existing auditability_os.audit_event but coarser-
grained: one EvidenceObject may span many audit events.
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


class EvidenceType(StrEnum):
    SOURCE_PASSPORT = "source_passport"
    AI_RUN = "ai_run"
    POLICY_CHECK = "policy_check"
    GOVERNANCE_DECISION = "governance_decision"
    APPROVAL = "approval"
    OUTPUT = "output"
    PROOF_PACK = "proof_pack"
    VALUE_EVENT = "value_event"
    CAPITAL_ASSET = "capital_asset"
    INCIDENT = "incident"


_DEFAULT_PATH = "var/evidence-control-plane.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_EVIDENCE_CONTROL_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class EvidenceObject:
    evidence_id: str = field(default_factory=lambda: f"ev_{uuid4().hex[:12]}")
    type: str = EvidenceType.AI_RUN.value
    customer_id: str = ""
    project_id: str = ""
    source_ids: list[str] = field(default_factory=list)
    linked_artifacts: list[str] = field(default_factory=list)
    summary: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def create_evidence(
    *,
    type: str | EvidenceType,
    customer_id: str,
    project_id: str = "",
    source_ids: list[str] | None = None,
    linked_artifacts: list[str] | None = None,
    summary: str = "",
) -> EvidenceObject:
    if not customer_id:
        raise ValueError("customer_id is required")
    from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
    type_value = type.value if isinstance(type, EvidenceType) else str(type)
    ev = EvidenceObject(
        type=type_value,
        customer_id=customer_id,
        project_id=project_id,
        source_ids=list(source_ids or []),
        linked_artifacts=list(linked_artifacts or []),
        summary=redact_text(summary) if summary else "",
    )
    path = _path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")
    return ev


def list_evidence(
    *,
    customer_id: str | None = None,
    project_id: str | None = None,
    type: str | None = None,
    limit: int = 500,
) -> list[EvidenceObject]:
    path = _path()
    if not path.exists():
        return []
    out: list[EvidenceObject] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = EvidenceObject(**json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
                if customer_id and ev.customer_id != customer_id:
                    continue
                if project_id and ev.project_id != project_id:
                    continue
                if type and ev.type != type:
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


__all__ = ["EvidenceObject", "EvidenceType", "clear_for_test", "create_evidence", "list_evidence"]
