"""Friction log JSONL store. Tenant-scoped via customer_id."""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

from auto_client_acquisition.friction_log.sanitizer import sanitize_notes
from auto_client_acquisition.friction_log.schemas import (
    FrictionEvent,
    FrictionKind,
    FrictionSeverity,
)

_DEFAULT_PATH = "var/friction-log.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_FRICTION_LOG_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _kind_value(k: str | FrictionKind) -> str:
    return k.value if isinstance(k, FrictionKind) else str(k)


def _severity_value(s: str | FrictionSeverity) -> str:
    return s.value if isinstance(s, FrictionSeverity) else str(s)


def emit(
    *,
    customer_id: str,
    kind: str | FrictionKind,
    severity: str | FrictionSeverity = FrictionSeverity.LOW,
    workflow_id: str = "",
    evidence_ref: str = "",
    cost_minutes: int = 0,
    notes: str = "",
) -> FrictionEvent:
    if not customer_id:
        raise ValueError("customer_id is required")
    kind_str = _kind_value(kind)
    sev_str = _severity_value(severity)
    event = FrictionEvent(
        customer_id=customer_id,
        workflow_id=workflow_id,
        kind=kind_str,
        severity=sev_str,
        evidence_ref=evidence_ref,
        cost_minutes=int(cost_minutes),
        notes=sanitize_notes(notes),
    )
    path = _path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    return event


def list_events(
    *,
    customer_id: str,
    limit: int = 200,
    since_days: int = 30,
    kind: str | FrictionKind | None = None,
) -> list[FrictionEvent]:
    if not customer_id:
        return []
    path = _path()
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc).timestamp() - since_days * 86400
    kind_filter = _kind_value(kind) if kind is not None else None
    out: list[FrictionEvent] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    ev = FrictionEvent(**data)
                except Exception:  # noqa: BLE001
                    continue
                if ev.customer_id != customer_id:
                    continue
                if kind_filter and ev.kind != kind_filter:
                    continue
                try:
                    ts = datetime.fromisoformat(ev.occurred_at).timestamp()
                except Exception:  # noqa: BLE001
                    ts = 0.0
                if ts < cutoff:
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


__all__ = ["clear_for_test", "emit", "list_events"]
