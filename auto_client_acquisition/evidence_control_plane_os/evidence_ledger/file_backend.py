"""File-backed JSONL implementation of the Evidence Events ledger.

Append-only writes. PII is redacted in ``summary`` before any write.
There is intentionally no update or delete method — the ledger is
immutable by construction.

Path is overridable via ``DEALIX_EVIDENCE_LEDGER_PATH``; default
``var/evidence_ledger.jsonl``.
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.evidence_control_plane_os.evidence_ledger.schemas import (
    EvidenceEvent,
)
from auto_client_acquisition.proof_ledger.hmac_signing import sign_pack_metadata


def _ledger_path() -> Path:
    raw = os.getenv("DEALIX_EVIDENCE_LEDGER_PATH", "var/evidence_ledger.jsonl")
    path = Path(raw)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _signing_secret() -> str | None:
    return os.getenv("DEALIX_EVIDENCE_LEDGER_SECRET") or None


def _signature_payload(event: EvidenceEvent) -> dict[str, object]:
    return {
        "id": event.id,
        "event_type": event.event_type,
        "source": event.source,
        "summary": event.summary,
        "confidence": event.confidence,
        "approval_required": event.approval_required,
        "linked_asset": event.linked_asset,
        "actor": event.actor,
        "created_at": event.created_at.isoformat(),
    }


class FileEvidenceLedger:
    """Thread-safe append-only JSONL evidence ledger."""

    def __init__(self, path: Path | str | None = None) -> None:
        self._lock = threading.Lock()
        self._path = Path(path) if path else None

    def _resolve(self) -> Path:
        return self._path if self._path is not None else _ledger_path()

    def append(self, event: EvidenceEvent) -> EvidenceEvent:
        """Persist one evidence event with redacted summary. Returns the stored event."""
        stored = event.model_copy(update={"summary": redact_text(event.summary or "")})
        signature = sign_pack_metadata(_signature_payload(stored), _signing_secret())
        record = stored.model_dump(mode="json")
        record["signature"] = signature
        path = self._resolve()
        with self._lock:
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False))
                handle.write("\n")
        return stored

    def list_events(
        self,
        *,
        event_type: str | None = None,
        source: str | None = None,
        limit: int = 200,
    ) -> list[EvidenceEvent]:
        """Read recent events, newest first, with optional filters."""
        path = self._resolve()
        if not path.exists():
            return []
        rows: list[EvidenceEvent] = []
        with self._lock:
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        data.pop("signature", None)
                        ev = EvidenceEvent.model_validate(data)
                    except Exception:  # noqa: BLE001
                        continue
                    if event_type and ev.event_type != event_type:
                        continue
                    if source and ev.source != source:
                        continue
                    rows.append(ev)
        rows.sort(key=lambda e: e.created_at, reverse=True)
        return rows[: max(0, limit)]

    def get(self, event_id: str) -> EvidenceEvent | None:
        """Fetch one event by id, or None."""
        for ev in self.list_events(limit=100_000):
            if ev.id == event_id:
                return ev
        return None

    def verify(self, event: EvidenceEvent) -> bool:
        """Recompute the signature and compare against the stored line."""
        path = self._resolve()
        if not path.exists():
            return False
        expected = sign_pack_metadata(_signature_payload(event), _signing_secret())
        with self._lock:
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except Exception:  # noqa: BLE001
                        continue
                    if data.get("id") == event.id:
                        return data.get("signature") == expected
        return False

    def clear_for_test(self) -> None:
        """Test-only: drop the ledger file."""
        path = self._resolve()
        with self._lock:
            if path.exists():
                path.unlink()


__all__ = ["FileEvidenceLedger"]
