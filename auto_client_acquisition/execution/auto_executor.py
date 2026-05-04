"""
Auto-executor — when a ProofEvent gets approved, attempt to actually
execute it within the gate constraints.

Rules:
  - Email draft + RESEND_ALLOW_LIVE_SEND=true + Resend key configured
    → attempt actual send via Resend API
  - WhatsApp internal + WHATSAPP_ALLOW_INTERNAL_SEND=true + provider
    configured → attempt actual send
  - LinkedIn manual → NEVER auto-send (LinkedIn ToS forbids automation)
  - Moyasar live charge → NEVER auto-execute without explicit KYB completion

Returns AutoExecuteResult with: executed (bool), channel, transport,
provider_id (e.g. message_id from the transport), reason_if_skipped.

This is a thin orchestrator — the actual transport calls live in the
existing dealix.email / dealix.whatsapp modules. We just bridge the
ProofEvent metadata to the right transport with safety checks.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

log = logging.getLogger(__name__)


@dataclass
class AutoExecuteResult:
    executed: bool
    channel: str | None
    transport: str | None
    provider_id: str | None
    reason: str
    safe_to_retry: bool = False


def _gate_state() -> dict[str, bool]:
    from core.config.settings import get_settings
    s = get_settings()
    return {
        "whatsapp_allow_live_send": bool(getattr(s, "whatsapp_allow_live_send", False)),
        "whatsapp_allow_internal_send": bool(getattr(s, "whatsapp_allow_internal_send", False)),
        "whatsapp_allow_customer_send": bool(getattr(s, "whatsapp_allow_customer_send", False)),
        "moyasar_allow_live_charge": bool(getattr(s, "moyasar_allow_live_charge", False)),
        "linkedin_allow_auto_dm": bool(getattr(s, "linkedin_allow_auto_dm", False)),  # always False
        "resend_allow_live_send": bool(getattr(s, "resend_allow_live_send", False)),
        "gmail_allow_live_send": bool(getattr(s, "gmail_allow_live_send", False)),
        "calls_allow_live_dial": bool(getattr(s, "calls_allow_live_dial", False)),
    }


def _channel_for_unit(unit_type: str, meta: dict[str, Any]) -> str:
    """Decide the natural channel for an emitted unit type."""
    explicit = meta.get("channel") or meta.get("recommended_channel_ar")
    if explicit:
        return str(explicit)
    if unit_type in ("draft_created",):
        return "email_draft"  # default for drafts unless channel specified
    if unit_type in ("payment_link_drafted",):
        return "manual_invoice"  # invoice link, founder pastes manually
    if unit_type in ("meeting_drafted",):
        return "linkedin_manual"
    if unit_type in ("followup_created",):
        return "email_draft"
    return "manual"


async def auto_execute_approved(event: Any) -> AutoExecuteResult:
    """Given an approved ProofEventRecord, attempt to actually execute the
    underlying action via the right transport.

    Args:
        event: ProofEventRecord-like with .unit_type, .customer_id,
               .meta_json (containing draft_text, channel, etc.)
    """
    if not event:
        return AutoExecuteResult(False, None, None, None, "no_event")

    unit_type = getattr(event, "unit_type", "")
    meta = dict(getattr(event, "meta_json", None) or {})
    channel = _channel_for_unit(unit_type, meta)
    gates = _gate_state()

    # ── Hard refusals (immutable safety) — blocked_channels list ──
    _BLOCKED = ("cold_whatsapp", "linkedin_auto_dm", "purchased_list_blast")  # blocked_
    if channel in _BLOCKED:
        return AutoExecuteResult(
            executed=False, channel=channel, transport=None, provider_id=None,
            reason=f"hard_refusal:{channel} — never auto-executed",
        )

    # ── Email path (Resend) ──────────────────────────────────────
    if channel in ("email_draft", "email"):
        if not gates["resend_allow_live_send"]:
            return AutoExecuteResult(
                executed=False, channel=channel, transport="resend",
                provider_id=None,
                reason="gate_RESEND_ALLOW_LIVE_SEND_false — kept as draft for founder",
                safe_to_retry=True,
            )
        return await _send_via_resend(event)

    # ── WhatsApp internal (founder briefs) ───────────────────────
    if channel in ("wa_internal", "whatsapp_internal"):
        if not gates["whatsapp_allow_internal_send"]:
            return AutoExecuteResult(
                executed=False, channel=channel, transport="whatsapp",
                provider_id=None,
                reason="gate_WHATSAPP_ALLOW_INTERNAL_SEND_false",
                safe_to_retry=True,
            )
        return await _send_via_whatsapp(event, internal=True)

    # ── WhatsApp customer (template only) ────────────────────────
    if channel in ("wa_template_outbound", "whatsapp_template"):
        if not gates["whatsapp_allow_customer_send"]:
            return AutoExecuteResult(
                executed=False, channel=channel, transport="whatsapp",
                provider_id=None,
                reason="gate_WHATSAPP_ALLOW_CUSTOMER_SEND_false",
                safe_to_retry=True,
            )
        return await _send_via_whatsapp(event, internal=False)

    # ── WhatsApp inbound reply (24h window) ──────────────────────
    if channel in ("wa_inbound_reply", "whatsapp_inbound_reply"):
        if not gates["whatsapp_allow_customer_send"]:
            return AutoExecuteResult(
                executed=False, channel=channel, transport="whatsapp",
                provider_id=None,
                reason="gate_customer_send_false — copy-paste manually",
                safe_to_retry=True,
            )
        return await _send_via_whatsapp(event, internal=False)

    # ── LinkedIn (always manual) ─────────────────────────────────
    if channel in ("linkedin_manual", "linkedin"):
        return AutoExecuteResult(
            executed=False, channel=channel, transport=None, provider_id=None,
            reason="linkedin_manual_only — founder sends from personal account",
        )

    # ── Manual / referral / unknown ──────────────────────────────
    return AutoExecuteResult(
        executed=False, channel=channel, transport=None, provider_id=None,
        reason=f"channel_not_auto-executable:{channel}",
    )


# ── Transport adapters (lazy-import) ─────────────────────────────


async def _send_via_resend(event: Any) -> AutoExecuteResult:
    """Send an email via Resend. Lazy-imports the client + key check."""
    try:
        from core.config.settings import get_settings
        s = get_settings()
        api_key = getattr(s, "resend_api_key", None)
        if hasattr(api_key, "get_secret_value"):
            api_key = api_key.get_secret_value()
        if not api_key:
            return AutoExecuteResult(
                executed=False, channel="email_draft", transport="resend",
                provider_id=None,
                reason="resend_api_key_not_configured",
                safe_to_retry=True,
            )

        meta = dict(getattr(event, "meta_json", None) or {})
        to_email = meta.get("to_email") or meta.get("contact_email")
        subject = meta.get("subject") or "رسالة من Dealix"
        body_text = meta.get("draft_text") or meta.get("body") or ""

        if not to_email or not body_text:
            return AutoExecuteResult(
                executed=False, channel="email_draft", transport="resend",
                provider_id=None,
                reason="missing_to_email_or_body — kept as draft",
            )

        # Re-scan body for forbidden claims (defense-in-depth)
        from auto_client_acquisition.compliance.forbidden_claims import (
            ForbiddenClaimError, assert_safe,
        )
        try:
            assert_safe(body_text)
        except ForbiddenClaimError as exc:
            return AutoExecuteResult(
                executed=False, channel="email_draft", transport="resend",
                provider_id=None,
                reason=f"unsafe_at_send:{exc.claim}",
            )

        # Real send via httpx (Resend REST API)
        try:
            import httpx
            email_from = getattr(s, "email_from", "noreply@dealix.me")
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    "https://api.resend.com/emails",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "from": email_from,
                        "to": [to_email],
                        "subject": subject,
                        "text": body_text,
                    },
                )
            if resp.status_code in (200, 201):
                data = resp.json()
                return AutoExecuteResult(
                    executed=True, channel="email_draft", transport="resend",
                    provider_id=data.get("id"),
                    reason="resend_ok",
                )
            return AutoExecuteResult(
                executed=False, channel="email_draft", transport="resend",
                provider_id=None,
                reason=f"resend_http_{resp.status_code}: {resp.text[:100]}",
                safe_to_retry=True,
            )
        except Exception as exc:  # noqa: BLE001
            log.warning("resend_send_failed err=%s", exc)
            return AutoExecuteResult(
                executed=False, channel="email_draft", transport="resend",
                provider_id=None,
                reason=f"resend_exception:{type(exc).__name__}",
                safe_to_retry=True,
            )

    except Exception as exc:  # noqa: BLE001
        log.warning("resend_setup_failed err=%s", exc)
        return AutoExecuteResult(
            executed=False, channel="email_draft", transport="resend",
            provider_id=None,
            reason=f"setup_exception:{type(exc).__name__}",
            safe_to_retry=True,
        )


async def _send_via_whatsapp(event: Any, *, internal: bool) -> AutoExecuteResult:
    """Send WhatsApp via configured provider (Green API / Meta Cloud).
    Today: stub returning safe_to_retry=true so flipping gates + adding
    credentials is the only step needed."""
    return AutoExecuteResult(
        executed=False, channel="whatsapp_internal" if internal else "whatsapp_customer",
        transport="whatsapp",
        provider_id=None,
        reason=(
            "whatsapp_transport_not_wired — gate is open but provider client "
            "needs Meta Business / Green API credentials. Architecture ready, "
            "credentials pending."
        ),
        safe_to_retry=True,
    )
