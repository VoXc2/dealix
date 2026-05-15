"""Agent loop ledger — append-only JSONL log of completed loop traces.

Same pattern as ``friction_log.store``. Stores the full ``LoopTrace`` dict
so every agent run is replayable and auditable.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.agent_loop_os.trace import LoopTrace

__all__ = ["emit_loop", "list_loops", "clear_for_test"]

_DEFAULT_PATH = "var/agent-loop-ledger.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_AGENT_LOOP_LEDGER_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def emit_loop(trace: LoopTrace) -> LoopTrace:
    if not trace.customer_id.strip():
        raise ValueError("trace.customer_id is required")
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(trace.to_dict(), ensure_ascii=False) + "\n")
    return trace


def list_loops(
    *,
    customer_id: str,
    limit: int = 100,
    since_days: int = 90,
) -> list[dict[str, Any]]:
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc).timestamp() - since_days * 86400
    out: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except Exception:  # noqa: BLE001
            continue
        if data.get("customer_id") != customer_id:
            continue
        try:
            ts = datetime.fromisoformat(data.get("occurred_at", "")).timestamp()
        except Exception:  # noqa: BLE001
            ts = 0.0
        if ts < cutoff:
            continue
        out.append(data)
    return out[-limit:]


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")
