"""Validate + redact incoming trace dicts.

Fail-closed redaction rule: ``redacted_payload`` must never carry raw
prompts, tool args/results, PII, or secrets. Denied keys are replaced
with ``HOLD`` (unknown sensitivity => omit/HOLD, never store raw).
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_dict
from auto_client_acquisition.observability_v10.schemas import TraceRecordV10

# Keys that must never hold raw execution content. Values are
# replaced with HOLD unless already an explicit safe summary label.
_DENIED_PAYLOAD_KEYS = frozenset(
    {
        "prompt",
        "raw_prompt",
        "system_prompt",
        "tool_args",
        "tool_arguments",
        "arguments",
        "raw_result",
        "raw_response",
        "full_transcript",
        "transcript",
        "completion",
        "secret",
        "api_key",
        "token",
        "password",
    }
)

_HOLD = "HOLD"


def coerce_denied_payload_keys(payload: dict[str, Any]) -> dict[str, Any]:
    """Replace denied raw-content keys with HOLD (recursive, depth-bounded)."""
    def _walk(value: Any, depth: int = 0) -> Any:
        if depth > 5:
            return {"_redacted": "max_depth_exceeded"}
        if isinstance(value, dict):
            out: dict[str, Any] = {}
            for k, v in value.items():
                if str(k).lower() in _DENIED_PAYLOAD_KEYS:
                    out[k] = _HOLD
                else:
                    out[k] = _walk(v, depth + 1)
            return out
        if isinstance(value, list):
            return [_walk(v, depth + 1) for v in value]
        return value

    result = _walk(dict(payload or {}))
    return result if isinstance(result, dict) else {}


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
        coerced = coerce_denied_payload_keys(payload)
        safe["redacted_payload"] = redact_dict(coerced)
    return TraceRecordV10(**safe)
