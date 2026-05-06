"""Deterministic action policy. No PII stored."""

from __future__ import annotations

from typing import Any


_BLOCKED = frozenset(
    {
        "cold_whatsapp",
        "live_whatsapp_outbound",
        "gmail_live_send",
        "linkedin_automation",
        "web_scraping",
        "purchased_list_outreach",
        "moyasar_live_charge",
    }
)

_APPROVAL_REQUIRED = frozenset(
    {
        "proof_pack_customer_send",
        "warm_intro_message_send",
        "inbound_whatsapp_reply_send",
        "invoice_request",
    }
)


def assess_external_action(action_type: str, *, has_consent: bool = False, founder_approved: bool = False) -> dict[str, Any]:
    """Return decision, action_mode, and reason."""
    key = (action_type or "").strip().lower().replace(" ", "_")
    if not key:
        return {"decision": "blocked", "action_mode": "blocked", "reason": "empty_action_type"}

    if key in _BLOCKED:
        return {"decision": "blocked", "action_mode": "blocked", "reason": f"hard_block:{key}"}

    if key in _APPROVAL_REQUIRED:
        if founder_approved and has_consent:
            return {
                "decision": "allowed_manual",
                "action_mode": "approved_manual",
                "reason": "consent_and_founder_approval_recorded",
            }
        return {"decision": "pending", "action_mode": "approval_required", "reason": f"requires_approval:{key}"}

    # Default: internal analysis only
    return {"decision": "suggest", "action_mode": "suggest_only", "reason": "internal_or_unknown_action"}
