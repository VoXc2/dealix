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
