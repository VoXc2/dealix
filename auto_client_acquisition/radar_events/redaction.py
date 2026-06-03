"""PII redaction for radar events — wraps customer_data_plane.pii_redactor
if present, else falls back to local regex (defence-in-depth)."""
from __future__ import annotations

import re
from typing import Any

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+", re.IGNORECASE)
_PHONE_RE = re.compile(r"\+?9665\d{8}|\b05\d{8}\b")
_SAUDI_ID_RE = re.compile(r"\b[12]\d{9}\b")


def redact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Redact PII from any string values in a dict, recursively.

    Tries customer_data_plane.pii_redactor first; falls back to local
    regex if not present.
    """
    try:
        from auto_client_acquisition.customer_data_plane.pii_redactor import (
            redact_dict,
        )
        return redact_dict(payload)
    except Exception:
        return _local_redact(payload)


def _local_redact(obj: Any) -> Any:
    if isinstance(obj, str):
        s = _EMAIL_RE.sub("[EMAIL]", obj)
        s = _PHONE_RE.sub("[PHONE]", s)
        s = _SAUDI_ID_RE.sub("[ID]", s)
        return s
    if isinstance(obj, list):
        return [_local_redact(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _local_redact(v) for k, v in obj.items()}
    return obj
