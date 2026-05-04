"""Small structured-event recorder.

This is the seed of a future ProofEvent ledger. Today it's an
in-process append-only buffer (per-process, no DB). When the
real Postgres ledger ships (Phase E of the strategic plan), the
public API of this module stays the same — only the storage
backend changes.

Never logs PII. Never sends anything externally.
"""
from __future__ import annotations

import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.self_growth_os.schemas import (
    ApprovalStatus,
    EvidenceRecord,
    Language,
    RiskLevel,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG_DIR = REPO_ROOT / "docs" / "proof-events"

_lock = threading.Lock()
_buffer: list[EvidenceRecord] = []


def record(
    event_type: str,
    summary: str,
    *,
    payload: dict[str, Any] | None = None,
    artifact_path: str | None = None,
    risk_level: RiskLevel = RiskLevel.LOW,
) -> EvidenceRecord:
    """Append an event to the in-process buffer + return it."""
    rec = EvidenceRecord.new(
        source="self_growth_os.evidence_collector",
        confidence=1.0,
        risk_level=risk_level,
        target_persona="founder",
        approval_status=ApprovalStatus.APPROVED,
        recommended_action="archive",
        event_type=event_type,
        summary=summary,
        artifact_path=artifact_path,
        payload=payload or {},
    )
    with _lock:
        _buffer.append(rec)
    return rec


def all_events() -> list[EvidenceRecord]:
    """Return a snapshot copy of the in-process buffer."""
    with _lock:
        return list(_buffer)


def clear() -> None:
    """Test-only helper to reset the buffer."""
    with _lock:
        _buffer.clear()


def write_jsonl(out_path: Path | None = None) -> Path:
    """Serialize the buffer as JSON Lines to disk for archiving.

    No PII filter is applied automatically — callers are responsible
    for ensuring the events they record do not contain personal data.
    """
    out_path = out_path or DEFAULT_LOG_DIR / f"events-{datetime.now(UTC):%Y%m%dT%H%M%SZ}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        with _lock:
            snapshot = list(_buffer)
        for rec in snapshot:
            f.write(rec.model_dump_json() + "\n")
    return out_path


def language_breakdown() -> dict[str, int]:
    counts: dict[str, int] = {}
    for rec in all_events():
        lang = str(rec.language)
        counts[lang] = counts.get(lang, 0) + 1
    return counts


__all__ = [
    "DEFAULT_LOG_DIR",
    "all_events",
    "clear",
    "language_breakdown",
    "record",
    "write_jsonl",
    "Language",  # re-export for convenience
]
