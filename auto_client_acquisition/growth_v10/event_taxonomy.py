"""Event taxonomy — list + Pydantic-backed validation with PII redaction."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import (
    redact_dict,
    redact_text,
)
from auto_client_acquisition.growth_v10.schemas import EventName, EventRecord


def list_event_names() -> list[str]:
    """Return the canonical list of all 17 event names (string values)."""
    return [e.value for e in EventName]


def validate_event(record: dict[str, Any] | EventRecord) -> EventRecord:
    """Validate an event payload and auto-redact PII in payload.

    Accepts either a raw dict or an existing EventRecord instance.
    Returns a fresh EventRecord with redacted=True if redaction was
    applied to any string in the payload.
    """
    data = (
        record.model_dump(mode="json")
        if isinstance(record, EventRecord)
        else dict(record)
    )

    raw_handle = data.get("customer_handle", "")
    handle_redacted = redact_text(raw_handle) if isinstance(raw_handle, str) else raw_handle
    data["customer_handle"] = handle_redacted

    raw_payload = data.get("payload") or {}
    redacted_payload = redact_dict(dict(raw_payload))
    data["payload"] = redacted_payload

    redacted_flag = (handle_redacted != raw_handle) or (redacted_payload != raw_payload)
    data["redacted"] = bool(redacted_flag)

    return EventRecord.model_validate(data)
