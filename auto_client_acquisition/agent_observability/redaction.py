"""PII + secret redaction for agent traces."""
from __future__ import annotations

import re
from typing import Any

from auto_client_acquisition.radar_events.redaction import redact_payload

# Common secret patterns we always strip
_SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9_-]{8,}"),
    re.compile(r"sk_test_[A-Za-z0-9_-]{8,}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9_\-.]{20,}", re.IGNORECASE),
]


def redact_trace(payload: dict[str, Any]) -> dict[str, Any]:
    """Redact PII first (via radar_events), then strip secret patterns."""
    safe = redact_payload(payload)
    return _strip_secrets(safe)


def _strip_secrets(obj: Any) -> Any:
    if isinstance(obj, str):
        s = obj
        for p in _SECRET_PATTERNS:
            s = p.sub("[SECRET]", s)
        return s
    if isinstance(obj, list):
        return [_strip_secrets(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _strip_secrets(v) for k, v in obj.items()}
    return obj
