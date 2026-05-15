"""Wave 8 §10 — PII & Secret Redaction Filter.

Scrubs sensitive patterns from log strings and metadata dicts before
any external emission. Used by all observability adapters.

Policy:
- Phone numbers → REDACTED_PHONE
- Email addresses → REDACTED_EMAIL
- API key patterns → REDACTED_KEY
- Saudi CR/ID numbers → REDACTED_ID
- Portal tokens → REDACTED_TOKEN
- IBAN → REDACTED_IBAN
"""
from __future__ import annotations

import re
from typing import Any

# ── Redaction patterns ─────────────────────────────────────────────────────
_PATTERNS = [
    (re.compile(r"\+966[5][0-9]{8}"),               "REDACTED_PHONE"),
    (re.compile(r"\+[0-9]{7,15}"),                   "REDACTED_PHONE"),
    (re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"), "REDACTED_EMAIL"),
    (re.compile(r"sk_live_[A-Za-z0-9]{10,}"),        "REDACTED_KEY"),
    (re.compile(r"sk-ant-api[A-Za-z0-9\-]{10,}"),    "REDACTED_KEY"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"),             "REDACTED_KEY"),
    (re.compile(r"eyJ[A-Za-z0-9\-_]{20,}"),          "REDACTED_JWT"),
    (re.compile(r"dealix-cust-[A-Za-z0-9\-_]{10,}"), "REDACTED_TOKEN"),
    (re.compile(r"Bearer [A-Za-z0-9\-_.]{10,}"),     "REDACTED_BEARER"),
    (re.compile(r"[0-9]{10}"),                        "REDACTED_ID"),   # Saudi CR / national ID
    (re.compile(r"SA[0-9]{22}"),                      "REDACTED_IBAN"),
    (re.compile(r"phc_[A-Za-z0-9]{20,}"),            "REDACTED_KEY"),  # PostHog
]

_SENSITIVE_KEYS = {
    "password", "token", "secret", "api_key", "phone", "email",
    "name", "address", "cr_number", "iban", "card_number",
    "access_token", "refresh_token", "webhook_secret",
}


class RedactionFilter:
    """Scrubs PII and secrets from strings and dicts."""

    @staticmethod
    def scrub_string(text: str) -> str:
        """Replace all sensitive patterns in a string."""
        for pattern, replacement in _PATTERNS:
            text = pattern.sub(replacement, text)
        return text

    @staticmethod
    def scrub_dict(data: dict[str, Any], *, depth: int = 0) -> dict[str, Any]:
        """Recursively scrub sensitive keys and values from a dict."""
        if depth > 5:
            return {"_redacted": "max_depth_exceeded"}

        result = {}
        for key, value in data.items():
            key_lower = str(key).lower()
            if any(s in key_lower for s in _SENSITIVE_KEYS):
                result[key] = "REDACTED"
            elif isinstance(value, dict):
                result[key] = RedactionFilter.scrub_dict(value, depth=depth + 1)
            elif isinstance(value, list):
                result[key] = [
                    RedactionFilter.scrub_dict(item, depth=depth + 1)
                    if isinstance(item, dict)
                    else (RedactionFilter.scrub_string(str(item)) if isinstance(item, str) else item)
                    for item in value
                ]
            elif isinstance(value, str):
                result[key] = RedactionFilter.scrub_string(value)
            else:
                result[key] = value
        return result

    @staticmethod
    def is_safe_for_external_log(text: str) -> bool:
        """Quick check: return False if text contains any sensitive pattern."""
        return all(not pattern.search(text) for pattern, _ in _PATTERNS)
