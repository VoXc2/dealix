"""Append-only Evidence Ledger — file-backed JSONL stopgap.

Every state transition and external action across the Sales + Customer Ops
Autopilot records one :class:`EvidenceEvent` here. The ledger is
APPEND-ONLY: there is no update or delete path — corrections are new
events. PII in summaries is redacted before anything hits disk.

Backend: file-backed JSONL (one file per UTC day under ``data/evidence_events``).
The public API (``record``, ``list_events``, ``get``) stays stable so a
Postgres backend can drop in later without touching call sites.
"""

from __future__ import annotations

import os
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = REPO_ROOT / "data" / "evidence_events"


class EvidenceEvent(BaseModel):
    """One auditable event in the evidence ledger.

    ``is_estimate`` + ``source`` honour the estimate doctrine: any value in
    ``payload`` not derived from a persisted record must set ``is_estimate``
    True and name its ``source``.
    """

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=lambda: f"ev_{uuid4().hex[:12]}")
    tenant_id: str | None = None
    event_type: str
    entity_type: str
    entity_id: str
    actor: str = "system"
    action: str = ""
    summary_ar: str = ""
    summary_en: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    is_estimate: bool = False
    source: str = ""
    approval_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def _date_file(base: Path, when: datetime | None = None) -> Path:
    when = when or datetime.now(UTC)
    return base / f"{when.strftime('%Y-%m-%d')}.jsonl"


class EvidenceLedger:
    """Thread-safe, append-only JSONL evidence ledger.

    Deliberately exposes no ``update``/``delete``/``edit`` method — the
    ``test_no_evidence_mutation`` guard asserts this stays true.
    """

    def __init__(self, base_dir: Path | str | None = None) -> None:
        self._lock = threading.Lock()
        self._base = Path(base_dir) if base_dir else DEFAULT_DIR
        self._base.mkdir(parents=True, exist_ok=True)

    def record(self, event: EvidenceEvent) -> EvidenceEvent:
        """Append one event. Summaries are redacted before persistence."""
        stored = event.model_copy(
            update={
                "summary_ar": redact_text(event.summary_ar) if event.summary_ar else "",
                "summary_en": redact_text(event.summary_en) if event.summary_en else "",
            }
        )
        line = stored.model_dump_json() + "\n"
        path = _date_file(self._base)
        with self._lock:
            with path.open("a", encoding="utf-8") as f:
                f.write(line)
        return stored

    def list_events(
        self,
        *,
        entity_type: str | None = None,
        entity_id: str | None = None,
        event_type: str | None = None,
        tenant_id: str | None = None,
        limit: int = 100,
    ) -> list[EvidenceEvent]:
        """Read recent events (newest-first), filtered by the given criteria."""
        out: list[EvidenceEvent] = []
        with self._lock:
            files = sorted(self._base.glob("*.jsonl"), reverse=True)[:30]
        for f in files:
            try:
                with f.open("r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            ev = EvidenceEvent.model_validate_json(line)
                        except Exception:  # noqa: BLE001 — skip corrupt lines
                            continue
                        if entity_type and ev.entity_type != entity_type:
                            continue
                        if entity_id and ev.entity_id != entity_id:
                            continue
                        if event_type and ev.event_type != event_type:
                            continue
                        if tenant_id and ev.tenant_id != tenant_id:
                            continue
                        out.append(ev)
            except OSError:
                continue
        out.sort(key=lambda e: e.created_at, reverse=True)
        return out[: max(1, min(int(limit), 500))]

    def get(self, event_id: str) -> EvidenceEvent | None:
        for ev in self.list_events(limit=500):
            if ev.event_id == event_id:
                return ev
        return None

    def count(self) -> int:
        return len(self.list_events(limit=500))

    def clear_dir(self) -> None:
        """Test-only: remove the JSONL files in the ledger directory."""
        with self._lock:
            for f in list(self._base.glob("*.jsonl")):
                try:
                    f.unlink()
                except OSError:
                    pass


# Module-level default ledger (process-scoped).
_DEFAULT: EvidenceLedger | None = None


def get_default_evidence_ledger() -> EvidenceLedger:
    """Return the process-wide evidence ledger singleton."""
    global _DEFAULT
    if _DEFAULT is None:
        env_dir = os.getenv("DEALIX_EVIDENCE_LEDGER_DIR")
        _DEFAULT = EvidenceLedger(env_dir)
    return _DEFAULT


def reset_default_evidence_ledger() -> None:
    """Test helper: drop the cached singleton so the next call re-evaluates env."""
    global _DEFAULT
    _DEFAULT = None


def record_evidence_event(
    *,
    event_type: str,
    entity_type: str,
    entity_id: str,
    actor: str = "system",
    action: str = "",
    summary_ar: str = "",
    summary_en: str = "",
    payload: dict[str, Any] | None = None,
    is_estimate: bool = False,
    source: str = "",
    approval_id: str | None = None,
    tenant_id: str | None = None,
) -> EvidenceEvent:
    """Build and append one evidence event to the default ledger.

    This is the single primitive every later module calls to log a state
    transition or external action.
    """
    event = EvidenceEvent(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        actor=actor,
        action=action,
        summary_ar=summary_ar,
        summary_en=summary_en,
        payload=payload or {},
        is_estimate=is_estimate,
        source=source,
        approval_id=approval_id,
        tenant_id=tenant_id,
    )
    return get_default_evidence_ledger().record(event)


def list_evidence_events(**kwargs: Any) -> list[EvidenceEvent]:
    """Convenience wrapper over the default ledger's ``list_events``."""
    return get_default_evidence_ledger().list_events(**kwargs)


__all__ = [
    "EvidenceEvent",
    "EvidenceLedger",
    "get_default_evidence_ledger",
    "list_evidence_events",
    "record_evidence_event",
    "reset_default_evidence_ledger",
]
