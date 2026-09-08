"""Policy gate — the single authority for outbound send decisions.

Defaults are fail-closed:
  allowed=False, safe_to_send=False, mode="draft_only",
  reason="external_send_disabled".

Live send is only possible when:
  - EXTERNAL_SEND_ENABLED == "true"
  - OUTBOUND_MODE == "controlled_live"
  - channel-specific flags are enabled
  - message is approved
  - contact is verified and has not opted out
  - an explicit consent purpose is present
  - recipient-level channel-purpose consent is present
  - durable consent evidence is independently proven
  - rate limits are respected
  - the recipient is not on the suppression list
  - suppression persistence is independently proven

This module never performs a real network send. Provider functions are
dry-run stubs (see provider_router.py).
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from app.outbound.consent import has_consent, persistent_consent_ready
from app.outbound.rate_limiter import within_rate_limits
from app.outbound.suppression import is_suppressed, persistent_suppression_ready

BLOCKED_CLAIMS = [
    "guaranteed roi",
    "guaranteed revenue",
    "مضمون",
    "نضمن لك",
    "100%",
    "testimonial",
    "عميل قال",
]

CHANNELS = ("email", "whatsapp", "sms")


@dataclass(frozen=True)
class GateResult:
    allowed: bool
    reasons: list[str]


@dataclass(frozen=True)
class SendEvaluation:
    """Full evaluation of an outbound send attempt.

    ``safe_to_send`` can only become true in controlled-live mode after every
    recipient-level and cross-cutting guard, including durable suppression and
    channel-purpose consent evidence, succeeds.
    """

    allowed: bool
    safe_to_send: bool
    mode: str
    channel: str
    reason: str
    reasons: list[str] = field(default_factory=list)
    contact: dict[str, Any] = field(default_factory=dict)
    message: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _env_true(env: Mapping[str, str], key: str) -> bool:
    return str(env.get(key, "")).lower() == "true"


def _env() -> Mapping[str, str]:
    return os.environ


def is_external_send_enabled(env: Mapping[str, str] | None = None) -> bool:
    e = env if env is not None else _env()
    return _env_true(e, "EXTERNAL_SEND_ENABLED")


def get_outbound_mode(env: Mapping[str, str] | None = None) -> str:
    e = env if env is not None else _env()
    return str(e.get("OUTBOUND_MODE", "draft_only")) or "draft_only"


def default_safety_status(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    e = env if env is not None else _env()
    mode = get_outbound_mode(e)
    external = is_external_send_enabled(e)
    suppression_ready = persistent_suppression_ready()
    consent_ready = persistent_consent_ready()

    if not external:
        reason = "external_send_disabled"
    elif mode != "controlled_live":
        reason = "mode_not_controlled_live"
    elif not suppression_ready:
        reason = "persistent_suppression_not_verified"
    elif not consent_ready:
        reason = "persistent_consent_not_verified"
    else:
        reason = "recipient_policy_evaluation_required"

    return {
        "external_send_enabled": external,
        "outbound_mode": mode,
        "safe_to_send": False,
        "email_send_enabled": _env_true(e, "EMAIL_SEND_ENABLED"),
        "whatsapp_send_enabled": _env_true(e, "WHATSAPP_SEND_ENABLED"),
        "whatsapp_allow_live_send": _env_true(e, "WHATSAPP_ALLOW_LIVE_SEND"),
        "sms_send_enabled": _env_true(e, "SMS_SEND_ENABLED"),
        "persistent_suppression_ready": suppression_ready,
        "persistent_consent_ready": consent_ready,
        "reason": reason,
    }


def _contains_unsubscribe(text: str) -> bool:
    t = text.lower()
    return (
        "unsubscribe" in t
        or "opt out" in t
        or "opt-out" in t
        or "إلغاء الاشتراك" in t
        or "ايقاف" in t
        or "إيقاف" in t
    )


def _has_blocked_claims(text: str) -> bool:
    t = text.lower()
    return any(claim in t for claim in BLOCKED_CLAIMS)


def _check_email(contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str]) -> list[str]:
    reasons: list[str] = []
    if not is_external_send_enabled(env): reasons.append("external_send_disabled")
    if not _env_true(env, "EMAIL_SEND_ENABLED"): reasons.append("EMAIL_SEND_ENABLED is not true")
    if get_outbound_mode(env) != "controlled_live": reasons.append("OUTBOUND_MODE must be controlled_live")
    if message.get("status") != "approved": reasons.append("message.status must be approved")
    if contact.get("verification_status") != "approved_to_send": reasons.append("contact.verification_status must be approved_to_send")
    if not contact.get("source_url"): reasons.append("source_url is required")
    if not contact.get("email"): reasons.append("email is required")
    if contact.get("email_opt_out") is True: reasons.append("contact has opted out from email")
    body = str(message.get("body", ""))
    if not _contains_unsubscribe(body): reasons.append("unsubscribe/opt-out wording is required")
    if _has_blocked_claims(body): reasons.append("blocked claim detected")
    return reasons


def _check_whatsapp(contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str]) -> list[str]:
    reasons: list[str] = []
    if not is_external_send_enabled(env): reasons.append("external_send_disabled")
    if not _env_true(env, "WHATSAPP_SEND_ENABLED"): reasons.append("WHATSAPP_SEND_ENABLED is not true")
    if not _env_true(env, "WHATSAPP_ALLOW_LIVE_SEND"): reasons.append("WHATSAPP_ALLOW_LIVE_SEND is not true")
    if get_outbound_mode(env) != "controlled_live": reasons.append("OUTBOUND_MODE must be controlled_live")
    if env.get("WHATSAPP_SEND_MODE") != "template_only": reasons.append("WHATSAPP_SEND_MODE must be template_only")
    if message.get("status") != "approved": reasons.append("message.status must be approved")
    if not contact.get("whatsapp"): reasons.append("whatsapp is required")
    if contact.get("whatsapp_opt_in") is not True: reasons.append("whatsapp opt-in is required")
    if contact.get("whatsapp_opt_out") is True: reasons.append("contact has opted out from WhatsApp")
    if not message.get("template_name"): reasons.append("approved template_name is required")
    if contact.get("verification_status") != "approved_to_send": reasons.append("contact.verification_status must be approved_to_send")
    if not contact.get("source_url"): reasons.append("source_url is required")
    if _has_blocked_claims(str(message.get("body", ""))): reasons.append("blocked claim detected")
    return reasons


def _check_sms(contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str]) -> list[str]:
    reasons: list[str] = []
    if not is_external_send_enabled(env): reasons.append("external_send_disabled")
    if not _env_true(env, "SMS_SEND_ENABLED"): reasons.append("SMS_SEND_ENABLED is not true")
    if get_outbound_mode(env) != "controlled_live": reasons.append("OUTBOUND_MODE must be controlled_live")
    if message.get("status") != "approved": reasons.append("message.status must be approved")
    if not contact.get("phone"): reasons.append("phone is required")
    if contact.get("sms_opt_out") is True: reasons.append("contact has opted out from SMS")
    if contact.get("verification_status") != "approved_to_send": reasons.append("contact.verification_status must be approved_to_send")
    if not contact.get("source_url"): reasons.append("source_url is required")
    body = str(message.get("body", ""))
    if not _contains_unsubscribe(body): reasons.append("unsubscribe/opt-out wording is required")
    if _has_blocked_claims(body): reasons.append("blocked claim detected")
    return reasons


_CHANNEL_CHECKS = {"email": _check_email, "whatsapp": _check_whatsapp, "sms": _check_sms}


def _contact_identifier(channel: str, contact: Mapping[str, Any]) -> str:
    if channel == "email": return str(contact.get("email", "")).lower().strip()
    if channel == "whatsapp": return str(contact.get("whatsapp", "")).lower().strip()
    if channel == "sms": return str(contact.get("phone", "")).lower().strip()
    return str(contact.get("email") or contact.get("whatsapp") or contact.get("phone") or "").lower().strip()


def _consent_purpose(message: Mapping[str, Any]) -> str:
    return str(message.get("consent_purpose") or message.get("purpose") or "").strip().lower()


def _apply_cross_cutting(channel: str, contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str], reasons: list[str]) -> None:
    """Append durability, suppression, purpose-consent and rate-limit blockers."""

    controlled_live = is_external_send_enabled(env) and get_outbound_mode(env) == "controlled_live"
    if controlled_live and not persistent_suppression_ready():
        reasons.append("persistent suppression backend is not verified")
    if controlled_live and not persistent_consent_ready():
        reasons.append("persistent consent backend is not verified")

    purpose = _consent_purpose(message)
    if controlled_live and not purpose:
        reasons.append("consent purpose is required for controlled live")

    identifier = _contact_identifier(channel, contact)
    if is_suppressed(identifier, channel=channel): reasons.append("recipient is on suppression list")
    if not has_consent(channel, contact, purpose=purpose or None): reasons.append("consent not recorded for channel and purpose")
    if not within_rate_limits(channel, identifier): reasons.append("rate limit exceeded for channel")


def _evaluate(channel: str, message: Mapping[str, Any], contact: Mapping[str, Any], env: Mapping[str, str] | None = None) -> SendEvaluation:
    e = env if env is not None else _env()
    check = _CHANNEL_CHECKS.get(channel)
    if check is None:
        return SendEvaluation(False, False, get_outbound_mode(e), channel, "unknown_channel", ["unknown channel: " + channel], dict(contact), dict(message))
    reasons = list(check(contact, message, e))
    _apply_cross_cutting(channel, contact, message, e, reasons)
    external = is_external_send_enabled(e)
    mode = get_outbound_mode(e)
    allowed = len(reasons) == 0
    safe_to_send = allowed and external and mode == "controlled_live"
    reason = reasons[0] if reasons else ("external_send_disabled" if not external else "mode_not_controlled_live" if mode != "controlled_live" else "ok")
    return SendEvaluation(allowed, safe_to_send, mode, channel, reason, reasons, dict(contact), dict(message))


def evaluate_email_send(message, contact, env=None): return _evaluate("email", message, contact, env)
def evaluate_whatsapp_send(message, contact, env=None): return _evaluate("whatsapp", message, contact, env)
def evaluate_sms_send(message, contact, env=None): return _evaluate("sms", message, contact, env)
def evaluate_channel_send(channel, message, contact, env=None): return _evaluate(channel, message, contact, env)

def can_send_email(contact, message, env):
    reasons = _check_email(contact, message, env); _apply_cross_cutting("email", contact, message, env, reasons); return GateResult(not reasons, reasons)

def can_send_whatsapp(contact, message, env):
    reasons = _check_whatsapp(contact, message, env); _apply_cross_cutting("whatsapp", contact, message, env, reasons); return GateResult(not reasons, reasons)

def can_send_sms(contact, message, env):
    reasons = _check_sms(contact, message, env); _apply_cross_cutting("sms", contact, message, env, reasons); return GateResult(not reasons, reasons)
