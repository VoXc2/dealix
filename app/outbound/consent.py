"""Consent registry — tracks explicit opt-in consent per channel.

Consent is required for WhatsApp (opt_in must be True) and SMS. Legacy draft
flows may still derive an email eligibility signal from
``verification_status=approved_to_send``; that signal is **not** durable consent
proof and must never by itself unlock controlled-live execution.

The current registry is process memory. Production controlled-live activation
therefore remains fail-closed until a durable, auditable consent backend stores
channel/purpose, timestamp, source/evidence, and withdrawal state. The public
interface is intentionally stable so that migration can replace storage without
creating a second consent authority.
"""

from __future__ import annotations

import time
from threading import Lock
from typing import Any, Mapping

_LOCK = Lock()
# _CONSENT[identifier] = {channel: {"ts": float, "source": str}}
_CONSENT: dict[str, dict[str, dict[str, Any]]] = {}


def consent_backend_kind() -> str:
    """Return the active consent authority kind.

    Only the in-memory backend exists today. This explicit API prevents a future
    deployment from treating contact flags as durable consent evidence.
    """

    return "memory"


def persistent_consent_ready() -> bool:
    """Whether durable consent evidence is independently proven.

    Current answer is deliberately False. A later Postgres implementation must
    prove a migrated schema and required privileges before changing this.
    """

    return False


def consent_backend_status() -> dict[str, Any]:
    return {
        "backend": consent_backend_kind(),
        "persistent": persistent_consent_ready(),
        "live_send_eligible": False,
        "reason": "in_memory_consent_is_not_durable",
    }


def _norm(identifier: str) -> str:
    return (identifier or "").strip().lower()


def _identifier_for(channel: str, contact: Mapping[str, Any]) -> str:
    if channel == "email":
        return str(contact.get("email", ""))
    if channel == "whatsapp":
        return str(contact.get("whatsapp", ""))
    if channel == "sms":
        return str(contact.get("phone", ""))
    return str(contact.get("email") or contact.get("whatsapp") or contact.get("phone") or "")


def has_consent(channel: str, contact: Mapping[str, Any]) -> bool:
    """True if channel-level consent/eligibility exists for draft policy checks.

    This function answers recipient-level policy only. Controlled-live execution
    has an additional independent ``persistent_consent_ready`` gate.

    Rules:
      - email: explicit in-process consent OR legacy eligibility
        (verification_status == "approved_to_send" AND not email_opt_out)
      - whatsapp: explicit in-process consent OR contact.whatsapp_opt_in is True
      - sms: explicit in-process consent OR contact.sms_opt_in is True
    """

    ident = _norm(_identifier_for(channel, contact))
    with _LOCK:
        entry = _CONSENT.get(ident, {})
        if channel in entry:
            return True

    if channel == "email":
        if contact.get("email_opt_out") is True:
            return False
        return contact.get("verification_status") == "approved_to_send"
    if channel == "whatsapp":
        return contact.get("whatsapp_opt_in") is True
    if channel == "sms":
        return contact.get("sms_opt_in") is True
    return False


def record_consent(channel: str, contact: Mapping[str, Any], source: str = "manual") -> None:
    """Record process-local explicit consent for draft/testing workflows."""

    ident = _norm(_identifier_for(channel, contact))
    if not ident:
        return
    with _LOCK:
        _CONSENT.setdefault(ident, {})[channel] = {
            "ts": time.time(),
            "source": source,
        }


def withdraw_consent(channel: str, contact: Mapping[str, Any]) -> None:
    """Withdraw process-local consent.

    Durable withdrawal is not claimed by this backend. Production live-send
    remains blocked until the durable consent authority exists.
    """

    ident = _norm(_identifier_for(channel, contact))
    with _LOCK:
        entry = _CONSENT.get(ident)
        if entry:
            entry.pop(channel, None)
            if not entry:
                _CONSENT.pop(ident, None)


def clear_consent() -> None:
    """Clear process-local consent state (tests only)."""

    with _LOCK:
        _CONSENT.clear()


def consent_record(channel: str, contact: Mapping[str, Any]) -> dict[str, Any] | None:
    """Return a process-local consent record for inspection."""

    ident = _norm(_identifier_for(channel, contact))
    with _LOCK:
        record = _CONSENT.get(ident, {}).get(channel)
        return dict(record) if record else None
