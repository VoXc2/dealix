"""Channel safety: web + email are live-safe (draft-first); WhatsApp is
inbound/opt-in only with no cold outbound and no auto-send authority.
"""

from __future__ import annotations

from typing import Any, Literal

OpsChannel = Literal["web", "email", "whatsapp", "phone_requested", "partner_intro"]

_WEB_EMAIL_SAFE = {"web", "email"}


def enforce_whatsapp_inbound_only(
    *,
    consent_granted: bool,
    is_cold: bool = False,
    is_blast: bool = False,
    is_purchased_list: bool = False,
    action_kind: str = "send_live",
) -> dict[str, Any]:
    """WhatsApp guard: inbound/opt-in only. live gate is never flipped here."""
    from auto_client_acquisition.channel_policy_gateway.policy import check_channel_policy

    if is_cold or is_blast or is_purchased_list:
        return {
            "allowed": False,
            "action_mode": "blocked",
            "reason": "cold/blast/purchased lists are always blocked",
        }
    decision = check_channel_policy(
        channel="whatsapp",
        action_kind=action_kind,  # type: ignore[arg-type]
        consent_record_exists=bool(consent_granted),
        approved_template_or_24h_window=False,
        live_gate_true=False,  # kernel never flips the live gate
        human_approved=False,
    )
    return {
        "allowed": False if action_kind == "send_live" else decision.allowed,
        "action_mode": "blocked" if action_kind == "send_live" else decision.action_mode,
        "reason": decision.reason_en,
        "missing_conditions": list(decision.missing_conditions),
    }


def enforce_channel_policy(
    *,
    channel: str,
    action_kind: str,
    consent_granted: bool = False,
    human_approved: bool = False,
) -> dict[str, Any]:
    """Route web/email through canonical policy (draft-first); WhatsApp locked."""
    ch = (channel or "").strip().lower()
    if ch == "whatsapp":
        return enforce_whatsapp_inbound_only(
            consent_granted=consent_granted, action_kind=action_kind
        )
    if ch in _WEB_EMAIL_SAFE:
        if action_kind in ("draft", "internal_brief", "manual_outreach"):
            return {"allowed": True, "action_mode": "draft_only", "reason": "draft-first"}
        # send_live on web/email still needs explicit human approval; kernel
        # itself never sends — it returns approval_required for the founder.
        if human_approved:
            return {
                "allowed": True,
                "action_mode": "approved_manual",
                "reason": "human-approved manual send only",
            }
        return {
            "allowed": False,
            "action_mode": "approval_required",
            "reason": "live send requires human approval",
        }
    return {"allowed": False, "action_mode": "blocked", "reason": f"unsupported: {ch}"}
