"""Validate + redact incoming trace dicts."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_dict
from auto_client_acquisition.observability_v10.schemas import TraceRecordV10


def validate_trace(record: dict[str, Any]) -> TraceRecordV10:
    """Validate ``record`` and redact PII inside ``redacted_payload``.

    Raises Pydantic ``ValidationError`` for unknown fields, missing
    required fields, or constraint breaches. Redaction happens *before*
    construction so no raw PII reaches the model instance.
    """
    if not isinstance(record, dict):
        raise TypeError("record must be a dict")
    safe = dict(record)
    payload = safe.get("redacted_payload")
    if isinstance(payload, dict):
        safe["redacted_payload"] = redact_dict(payload)
    return TraceRecordV10(**safe)
