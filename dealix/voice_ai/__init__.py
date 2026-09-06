"""Dealix Voice AI channel adapter.

The voice layer is an inbound-first adapter into the existing Company Machine.
It does not create a parallel CRM, proof ledger, scheduler, or sales authority.
"""

from .front_desk import (
    VoiceAIConfig,
    VoiceWebhookResult,
    build_voice_instructions,
    get_voice_readiness,
    handle_openai_realtime_webhook,
)

__all__ = [
    "VoiceAIConfig",
    "VoiceWebhookResult",
    "build_voice_instructions",
    "get_voice_readiness",
    "handle_openai_realtime_webhook",
]
