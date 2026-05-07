"""Unified channel policy entrypoint — dispatches to per-channel module."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.channel_policy_gateway.calls import calls_policy
from auto_client_acquisition.channel_policy_gateway.email import email_policy
from auto_client_acquisition.channel_policy_gateway.linkedin import (
    linkedin_policy,
)
from auto_client_acquisition.channel_policy_gateway.schemas import (
    Channel,
    PolicyDecision,
)
from auto_client_acquisition.channel_policy_gateway.whatsapp import (
    whatsapp_policy,
)


def check_channel_policy(
    *,
    channel: Channel,
    action_kind: str,
    consent_record_exists: bool = False,
    approved_template_or_24h_window: bool = False,
    live_gate_true: bool = False,
    human_approved: bool = False,
    customer_permission: bool = False,
    is_cold: bool = False,
    is_blast: bool = False,
    is_purchased_list: bool = False,
) -> PolicyDecision:
    if channel == "whatsapp":
        return whatsapp_policy(
            action_kind=action_kind,  # type: ignore[arg-type]
            consent_record_exists=consent_record_exists,
            approved_template_or_24h_window=approved_template_or_24h_window,
            live_gate_true=live_gate_true,
            human_approved=human_approved,
            is_cold=is_cold,
            is_blast=is_blast,
            is_purchased_list=is_purchased_list,
        )
    if channel == "email":
        return email_policy(
            action_kind=action_kind,  # type: ignore[arg-type]
            live_gate_true=live_gate_true,
            human_approved=human_approved,
        )
    if channel == "linkedin":
        return linkedin_policy(action_kind=action_kind)  # type: ignore[arg-type]
    if channel == "calls":
        return calls_policy(
            action_kind=action_kind,  # type: ignore[arg-type]
            customer_permission=customer_permission,
            live_gate_true=live_gate_true,
            human_approved=human_approved,
        )
    return PolicyDecision(
        channel=channel,  # type: ignore[arg-type]
        action_kind=action_kind,  # type: ignore[arg-type]
        allowed=False,
        action_mode="blocked",
        reason_ar="قناة غير مدعومة.",
        reason_en="Channel not supported.",
    )
