"""Outbound safety and send endpoints — all blocked by default.

All send endpoints return a safety response with allowed=false when
EXTERNAL_SEND_ENABLED is not explicitly set to true. The default mode
is draft_only, meaning no external sending occurs.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.outbound import policy_gate

router = APIRouter(prefix="/api/outbound", tags=["outbound-safety"])


# ── Models ──────────────────────────────────────────────────────


class SafetyStatus(BaseModel):
    external_send_enabled: bool
    outbound_mode: str
    email_send_enabled: bool
    whatsapp_send_enabled: bool
    whatsapp_allow_live_send: bool
    sms_send_enabled: bool
    persistent_suppression_ready: bool
    safe_to_send: bool
    reason: str


class ChannelReadiness(BaseModel):
    channel: str
    enabled: bool
    mode: str
    ready: bool
    reason: str


class SendRequest(BaseModel):
    channel: str = "email"
    to: str = ""
    subject: str = ""
    body: str = ""
    template_id: str | None = None


class SendResponse(BaseModel):
    allowed: bool
    safe_to_send: bool
    mode: str
    reason: str
    channel: str


# ── Helpers ─────────────────────────────────────────────────────


def _default_safety_status() -> dict[str, Any]:
    """Delegate status truth to the canonical outbound policy gate."""

    return policy_gate.default_safety_status()


def _evaluate_send(channel: str) -> dict[str, Any]:
    """Evaluate configuration readiness without claiming recipient safety."""

    status = _default_safety_status()
    external_ok = status["external_send_enabled"]
    mode_ok = status["outbound_mode"] == "controlled_live"

    channel_key = f"{channel}_send_enabled"
    channel_enabled = status.get(channel_key, False) if channel_key in status else False

    if channel == "whatsapp":
        channel_enabled = status["whatsapp_send_enabled"]
        wa_live = status["whatsapp_allow_live_send"]
        if not (channel_enabled and wa_live):
            return {
                "allowed": False,
                "safe_to_send": False,
                "mode": status["outbound_mode"],
                "reason": "whatsapp_not_enabled_or_not_live",
                "channel": channel,
            }

    if not external_ok:
        return {
            "allowed": False,
            "safe_to_send": False,
            "mode": status["outbound_mode"],
            "reason": "external_send_disabled",
            "channel": channel,
        }

    if not mode_ok:
        return {
            "allowed": False,
            "safe_to_send": False,
            "mode": status["outbound_mode"],
            "reason": "mode_not_controlled_live",
            "channel": channel,
        }

    if not status["persistent_suppression_ready"]:
        return {
            "allowed": False,
            "safe_to_send": False,
            "mode": status["outbound_mode"],
            "reason": "persistent_suppression_not_verified",
            "channel": channel,
        }

    if not channel_enabled:
        return {
            "allowed": False,
            "safe_to_send": False,
            "mode": status["outbound_mode"],
            "reason": f"{channel}_send_disabled",
            "channel": channel,
        }

    return {
        "allowed": True,
        # Channel configuration is ready, but a recipient/message policy
        # evaluation is still required before any safe-to-send decision.
        "safe_to_send": False,
        "mode": status["outbound_mode"],
        "reason": "recipient_policy_evaluation_required",
        "channel": channel,
    }


def _evaluate_request(channel: str, request: SendRequest) -> dict[str, Any]:
    """Route active API attempts through the canonical recipient policy gate.

    This legacy request schema carries no approval, verification, consent, or
    source evidence. The canonical gate therefore fails closed rather than
    letting configuration flags manufacture a safe-to-send decision.
    """

    contact: dict[str, Any]
    if channel == "email":
        contact = {"email": request.to}
    elif channel == "whatsapp":
        contact = {"whatsapp": request.to}
    else:
        contact = {"phone": request.to}
    message = {
        "status": "pending_review",
        "subject": request.subject,
        "body": request.body,
        "template_name": request.template_id,
    }
    return policy_gate.evaluate_channel_send(channel, message, contact).to_dict()


# ── Endpoints ───────────────────────────────────────────────────


@router.get("/safety")
async def outbound_safety() -> dict[str, Any]:
    """Return the current outbound safety status."""
    return _default_safety_status()


@router.get("/channels")
async def outbound_channels() -> dict[str, Any]:
    """Return per-channel status."""
    status = _default_safety_status()
    return {
        "email": {
            "enabled": status["email_send_enabled"],
            "mode": status["outbound_mode"],
        },
        "whatsapp": {
            "enabled": status["whatsapp_send_enabled"],
            "allow_live": status["whatsapp_allow_live_send"],
            "mode": status["outbound_mode"],
        },
        "sms": {
            "enabled": status["sms_send_enabled"],
            "mode": status["outbound_mode"],
        },
    }


@router.get("/readiness/email")
async def email_readiness() -> dict[str, Any]:
    """Email channel readiness."""
    evaluation = _evaluate_send("email")
    status = _default_safety_status()
    ready = evaluation["allowed"]
    return {
        "channel": "email",
        "enabled": status["email_send_enabled"],
        "mode": status["outbound_mode"],
        "ready": ready,
        "reason": evaluation["reason"],
    }


@router.get("/readiness/whatsapp")
async def whatsapp_readiness() -> dict[str, Any]:
    """WhatsApp channel readiness."""
    evaluation = _evaluate_send("whatsapp")
    status = _default_safety_status()
    ready = evaluation["allowed"]
    return {
        "channel": "whatsapp",
        "enabled": status["whatsapp_send_enabled"],
        "allow_live": status["whatsapp_allow_live_send"],
        "mode": status["outbound_mode"],
        "ready": ready,
        "reason": evaluation["reason"],
    }


@router.get("/readiness/sms")
async def sms_readiness() -> dict[str, Any]:
    """SMS channel readiness."""
    evaluation = _evaluate_send("sms")
    status = _default_safety_status()
    ready = evaluation["allowed"]
    return {
        "channel": "sms",
        "enabled": status["sms_send_enabled"],
        "mode": status["outbound_mode"],
        "ready": ready,
        "reason": evaluation["reason"],
    }


@router.post("/send/email")
async def send_email(request: SendRequest) -> dict[str, Any]:
    """Send email — blocked by default."""
    return _evaluate_request("email", request)


@router.post("/send/whatsapp")
async def send_whatsapp(request: SendRequest) -> dict[str, Any]:
    """Send WhatsApp — blocked by default."""
    return _evaluate_request("whatsapp", request)


@router.post("/send/sms")
async def send_sms(request: SendRequest) -> dict[str, Any]:
    """Send SMS — blocked by default."""
    return _evaluate_request("sms", request)
