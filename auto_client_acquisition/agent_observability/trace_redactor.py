"""
Trace Redactor — strips PII / secrets from text & dicts before logging.

Pure function. NEVER lets the following leak into traces / cost ledger /
metrics:
  - Saudi mobile numbers (+966 5XXXXXXXX, 05XXXXXXXX)
  - International phone numbers (E.164 + common formats)
  - Email addresses
  - Bearer / API keys (sk-..., secret_*, gho_*, gha_*, glpat-*)
  - Common JWT / hex-secret patterns (32+ hex chars)
  - Moyasar / Stripe-style payment ids (pay_*, invoice_*, sub_*)

Output uses fixed redaction tokens so downstream tooling can group events
without seeing the underlying values.
"""

from __future__ import annotations

import re
from typing import Any


_PII_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # Saudi + international phone numbers (very permissive on purpose)
    (re.compile(r"\+9665\d{8}"), "<phone:sa>"),
    (re.compile(r"\b05\d{8}\b"), "<phone:sa>"),
    (re.compile(r"\+\d{8,15}\b"), "<phone:intl>"),
    # Emails
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "<email>"),
    # Provider keys
    (re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"), "<api_key>"),
    (re.compile(r"\bsk_live_[A-Za-z0-9_-]{12,}\b"), "<api_key>"),
    (re.compile(r"\bsecret_[A-Za-z0-9_-]{12,}\b"), "<api_key>"),
    (re.compile(r"\bgh[opst]_[A-Za-z0-9_]{20,}\b"), "<api_key>"),
    (re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"), "<api_key>"),
    # Long hex secrets / JWT-ish tokens (32+ hex chars)
    (re.compile(r"\b[a-f0-9]{32,}\b"), "<hex_secret>"),
    # Payment ids (stripe / moyasar style)
    (re.compile(r"\b(pay|inv|invoice|sub|subscription|cus|customer)_[A-Za-z0-9]{8,}\b"),
     "<payment_id>"),
)


# Keys whose values are scrubbed regardless of content.
_SENSITIVE_KEYS: frozenset[str] = frozenset({
    "password", "passcode", "secret", "api_key", "apikey", "access_token",
    "refresh_token", "authorization", "auth", "set-cookie", "cookie",
    "phone", "mobile", "whatsapp_number", "card_number", "cvv",
    "iban", "swift", "national_id", "iqama",
    "moyasar_token", "moyasar_api_key", "resend_api_key", "anthropic_api_key",
})


def redact_text(text: str | None) -> str:
    if not text:
        return ""
    out = str(text)
    for pat, token in _PII_PATTERNS:
        out = pat.sub(token, out)
    return out


def redact_dict(data: dict[str, Any] | None, *, max_str_len: int = 1024) -> dict[str, Any]:
    """Recursive redact: scrub sensitive keys + redact text inside string values.

    Strings longer than `max_str_len` get truncated to keep traces small.
    """
    if not isinstance(data, dict):
        return {}
    out: dict[str, Any] = {}
    for k, v in data.items():
        key_l = str(k).lower()
        if key_l in _SENSITIVE_KEYS or any(s in key_l for s in ("token", "secret", "password")):
            out[k] = "<redacted>"
            continue
        out[k] = _redact_value(v, max_str_len=max_str_len)
    return out


def _redact_value(v: Any, *, max_str_len: int) -> Any:
    if isinstance(v, str):
        s = redact_text(v)
        if len(s) > max_str_len:
            s = s[:max_str_len] + "…(truncated)"
        return s
    if isinstance(v, dict):
        return redact_dict(v, max_str_len=max_str_len)
    if isinstance(v, (list, tuple)):
        return [_redact_value(i, max_str_len=max_str_len) for i in v]
    return v
