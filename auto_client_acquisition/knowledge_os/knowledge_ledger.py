"""Knowledge ledger — append-only JSONL log of ingest + query activity.

Same pattern as ``friction_log.store``: tenant-scoped, PII-safe (snippets
are redacted before they ever reach a KnowledgeEvent), env-overridable
path, test-clearable.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

from auto_client_acquisition.knowledge_os.schemas import KnowledgeEvent, knowledge_event_valid

__all__ = ["emit_knowledge_event", "list_knowledge_events", "clear_for_test"]

_DEFAULT_PATH = "var/knowledge-ledger.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_KNOWLEDGE_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def emit_knowledge_event(event: KnowledgeEvent) -> KnowledgeEvent:
    if not knowledge_event_valid(event):
        raise ValueError("invalid knowledge event")
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_knowledge_events(
    *,
    customer_handle: str,
    limit: int = 200,
    since_days: int = 90,
) -> list[KnowledgeEvent]:
    if not customer_handle:
        return []
    path = _path()
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc).timestamp() - since_days * 86400
    out: list[KnowledgeEvent] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            data["source_types"] = tuple(data.get("source_types", ()))
            ev = KnowledgeEvent(**data)
        except Exception:  # noqa: BLE001
            continue
        if ev.customer_handle != customer_handle:
            continue
        try:
            ts = datetime.fromisoformat(ev.occurred_at).timestamp()
        except Exception:  # noqa: BLE001
            ts = 0.0
        if ts < cutoff:
            continue
        out.append(ev)
    return out[-limit:]


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")
