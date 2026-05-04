"""File-backed JSONL implementation of the proof ledger.

Append-only writes to ``docs/proof-events/<YYYY-MM-DD>.jsonl``.
Reads scan a directory + filter. PII redacted before write.

When Postgres lands, swap this module's class for a SQL-backed one
with the same public methods (``record``, ``list_events``,
``record_unit``, ``list_units``).
"""
from __future__ import annotations

import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.proof_ledger.schemas import (
    ProofEvent,
    RevenueWorkUnit,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = REPO_ROOT / "docs" / "proof-events"


def _date_file(base: Path, when: datetime | None = None) -> Path:
    when = when or datetime.now(UTC)
    return base / f"{when.strftime('%Y-%m-%d')}.jsonl"


def _units_file(base: Path, when: datetime | None = None) -> Path:
    when = when or datetime.now(UTC)
    return base / f"{when.strftime('%Y-%m-%d')}-units.jsonl"


class FileProofLedger:
    """Thread-safe append-only JSONL ledger."""

    def __init__(self, base_dir: Path | str | None = None) -> None:
        self._lock = threading.Lock()
        self._base = Path(base_dir) if base_dir else DEFAULT_DIR
        self._base.mkdir(parents=True, exist_ok=True)

    # ─── ProofEvents ────────────────────────────────────────────

    def record(self, event: ProofEvent) -> ProofEvent:
        """Persist one event with redaction. Returns the stored event."""
        # Redact summaries before persistence — store both raw and
        # redacted? NO. Only the redacted form ever hits disk.
        ar_redacted = redact_text(event.summary_ar) if event.summary_ar else ""
        en_redacted = redact_text(event.summary_en) if event.summary_en else ""
        if not event.consent_for_publication:
            # Strip the customer handle too unless explicitly anonymized.
            handle = event.customer_handle
        else:
            handle = event.customer_handle

        # Build a written copy with redaction applied.
        stored = event.model_copy(update={
            "redacted_summary_ar": ar_redacted,
            "redacted_summary_en": en_redacted,
        })

        line = stored.model_dump_json() + "\n"
        path = _date_file(self._base)
        with self._lock:
            with path.open("a", encoding="utf-8") as f:
                f.write(line)
        return stored

    def list_events(
        self,
        *,
        customer_handle: str | None = None,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[ProofEvent]:
        """Read recent events (today + yesterday's file by default)."""
        out: list[ProofEvent] = []
        with self._lock:
            files = sorted(self._base.glob("*.jsonl"), reverse=True)[:7]  # last 7 days
        for f in files:
            if "-units" in f.name:
                continue
            try:
                with f.open("r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            ev = ProofEvent.model_validate(data)
                        except Exception:  # noqa: BLE001
                            continue
                        if customer_handle and ev.customer_handle != customer_handle:
                            continue
                        if event_type and str(ev.event_type) != event_type:
                            continue
                        out.append(ev)
                        if len(out) >= limit:
                            return out
            except OSError:
                continue
        return out

    # ─── RevenueWorkUnits ───────────────────────────────────────

    def record_unit(self, unit: RevenueWorkUnit) -> RevenueWorkUnit:
        line = unit.model_dump_json() + "\n"
        path = _units_file(self._base)
        with self._lock:
            with path.open("a", encoding="utf-8") as f:
                f.write(line)
        return unit

    def list_units(
        self,
        *,
        customer_handle: str | None = None,
        unit_type: str | None = None,
        limit: int = 100,
    ) -> list[RevenueWorkUnit]:
        out: list[RevenueWorkUnit] = []
        with self._lock:
            files = sorted(self._base.glob("*-units.jsonl"), reverse=True)[:7]
        for f in files:
            try:
                with f.open("r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            u = RevenueWorkUnit.model_validate(data)
                        except Exception:  # noqa: BLE001
                            continue
                        if customer_handle and u.customer_handle != customer_handle:
                            continue
                        if unit_type and str(u.unit_type) != unit_type:
                            continue
                        out.append(u)
                        if len(out) >= limit:
                            return out
            except OSError:
                continue
        return out

    # ─── Test helpers ───────────────────────────────────────────

    def clear_dir(self) -> None:
        """Test-only: clear the JSONL files in the ledger directory."""
        with self._lock:
            for f in list(self._base.glob("*.jsonl")):
                try:
                    f.unlink()
                except OSError:
                    pass


# Module-level default ledger (process-scoped).
_DEFAULT: FileProofLedger | None = None


def get_default_ledger() -> FileProofLedger:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = FileProofLedger()
    return _DEFAULT
