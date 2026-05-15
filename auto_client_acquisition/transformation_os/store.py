"""JSONL store for transformation engagement records.

Append-only ledger of transformation state snapshots, mirroring the
friction_log store pattern. Tenant-scoped via client_id.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path

from auto_client_acquisition.transformation_os.schemas import TransformationRecord

_DEFAULT_PATH = "var/transformation-log.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_TRANSFORMATION_LOG_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def emit(record: TransformationRecord) -> TransformationRecord:
    """Append a transformation record snapshot to the JSONL ledger."""
    if not record.engagement_id:
        raise ValueError("engagement_id is required")
    if not record.client_id:
        raise ValueError("client_id is required")
    path = _path()
    _ensure_dir(path)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    return record


def list_records(*, client_id: str, limit: int = 200) -> list[TransformationRecord]:
    """All record snapshots for one client, newest last."""
    if not client_id:
        return []
    path = _path()
    if not path.exists():
        return []
    out: list[TransformationRecord] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                record = TransformationRecord.from_dict(data)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
            if record.client_id != client_id:
                continue
            out.append(record)
    return out[-limit:]


def clear_for_test() -> None:
    """Truncate the ledger. For tests and CI only."""
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = ["clear_for_test", "emit", "list_records"]
