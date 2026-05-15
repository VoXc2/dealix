"""Control-event ledger with JSONL fallback for local development."""

from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock

from auto_client_acquisition.control_plane_os.schemas import ControlEvent

_LOCK = Lock()


def _path() -> Path:
    configured = os.getenv("DEALIX_CONTROL_LEDGER_PATH", "").strip()
    if configured:
        return Path(configured)
    return Path("data/control_events.jsonl")


class JsonlControlLedger:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or _path()

    def append(self, event: ControlEvent) -> ControlEvent:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with _LOCK:
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
        return event

    def list_events(self, *, tenant_id: str, run_id: str = "", limit: int = 500) -> list[ControlEvent]:
        if not self._path.exists():
            return []
        rows: list[ControlEvent] = []
        with _LOCK:
            for line in self._path.read_text(encoding="utf-8").splitlines():
                payload = line.strip()
                if not payload:
                    continue
                try:
                    raw = json.loads(payload)
                    row = ControlEvent(**raw)
                except Exception:  # noqa: BLE001
                    continue
                if row.tenant_id != tenant_id:
                    continue
                if run_id and row.run_id != run_id:
                    continue
                rows.append(row)
        rows.sort(key=lambda r: r.occurred_at)
        if limit <= 0:
            return rows
        return rows[-limit:]
