"""Radar event store — thread-safe in-memory + JSONL append.

Always redacts PII on insert (defence-in-depth — even if caller
already redacted, we redact again).
"""
from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.radar_events.redaction import redact_payload
from auto_client_acquisition.radar_events.taxonomy import is_known_event_type

_JSONL_PATH = os.path.join("data", "radar_events.jsonl")
_LOCK = threading.Lock()
_BUFFER: list[dict[str, Any]] = []


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def record_event(
    *,
    event_type: str,
    customer_handle: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Append-only event recording with PII redaction.

    Returns the persisted (redacted) event dict.
    Unknown event_type still recorded (best-effort) but flagged.
    """
    safe_payload = redact_payload(payload or {})
    event = {
        "event_id": f"rev_{uuid.uuid4().hex[:10]}",
        "event_type": event_type,
        "is_known_type": is_known_event_type(event_type),
        "customer_handle": customer_handle,
        "payload": safe_payload,
        "recorded_at": datetime.now(UTC).isoformat(),
        "safety_summary": "pii_redacted_on_insert",
    }
    _ensure_dir()
    with _LOCK:
        _BUFFER.append(event)
        with open(_JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def list_recent(*, limit: int = 100) -> list[dict[str, Any]]:
    with _LOCK:
        return list(_BUFFER[-limit:])


def summary_metrics() -> dict[str, Any]:
    with _LOCK:
        events = list(_BUFFER)
    counts: dict[str, int] = {}
    for e in events:
        counts[e["event_type"]] = counts.get(e["event_type"], 0) + 1
    return {
        "total_events": len(events),
        "by_event_type": counts,
        "unsafe_action_blocked_count": counts.get("unsafe_action_blocked", 0),
    }


def _reset_buffer() -> None:
    """Test helper — never use in production."""
    with _LOCK:
        _BUFFER.clear()
