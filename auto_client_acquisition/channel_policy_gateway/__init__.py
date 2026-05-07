"""Channel Policy Gateway (Phase 8).

One unified policy check for every external channel attempt:
WhatsApp · Email · LinkedIn · Calls.

Returns: { allowed, action_mode, reason_ar, reason_en,
            safe_alternative_ar, safe_alternative_en,
            required_conditions, missing_conditions }

Reuses designops/safety_gate forbidden-token logic and
whatsapp_safe_send 6-gate concept (decision-only).
"""
from auto_client_acquisition.channel_policy_gateway.policy import (
    check_channel_policy,
)

__all__ = ["check_channel_policy"]
