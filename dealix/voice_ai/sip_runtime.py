"""Hardened SIP admission configuration for Dealix Voice AI.

This module is a narrow provider adapter around the shared front-desk prompt/tools.
It pins the production-grade voice/audio/VAD/truncation configuration while the
business behavior remains owned by ``front_desk``.
"""

from __future__ import annotations

from typing import Any, Mapping

from .front_desk import (
    VoiceAIConfig,
    VoiceWebhookResult,
    build_realtime_tools,
    build_voice_instructions,
)

VOICE_MODEL = "gpt-realtime-2.1"
VOICE_OUTPUT_VOICE = "cedar"
_ALLOWED_REASONING = {"minimal", "low", "medium", "high", "xhigh"}


def normalized_reasoning_effort(config: VoiceAIConfig) -> str:
    value = (config.reasoning_effort or "medium").strip().lower()
    return value if value in _ALLOWED_REASONING else "medium"


def realtime_audio_config() -> dict[str, Any]:
    """Return a phone-call tuned audio configuration.

    Cedar is one of OpenAI's recommended highest-quality Realtime voices. Semantic
    VAD avoids cutting callers off on natural hesitations while still allowing
    interruption of the assistant.
    """

    return {
        "input": {
            "noise_reduction": {"type": "near_field"},
            "turn_detection": {
                "type": "semantic_vad",
                "eagerness": "auto",
                "create_response": True,
                "interrupt_response": True,
            },
        },
        "output": {
            "voice": VOICE_OUTPUT_VOICE,
            "speed": 1.0,
        },
    }


def realtime_truncation_config() -> dict[str, Any]:
    # Keep enough context for a serious discovery call while bounding repeated
    # long-history cost and reducing frequent cache-busting truncations.
    return {
        "type": "retention_ratio",
        "retention_ratio": 0.8,
        "token_limits": {"post_instructions": 16000},
    }


def handle_openai_realtime_webhook(
    raw_body: str,
    headers: Mapping[str, str],
    config: VoiceAIConfig,
    client: Any,
) -> VoiceWebhookResult:
    """Verify and admit one OpenAI SIP call with the hardened Dealix session."""

    event = client.webhooks.unwrap(raw_body, headers)
    event_type = str(getattr(event, "type", "unknown"))
    if event_type != "realtime.call.incoming":
        return VoiceWebhookResult(event_type=event_type, action="ignored")

    data = getattr(event, "data", None)
    call_id = str(getattr(data, "call_id", "") or "").strip()[:200]
    if not call_id:
        raise RuntimeError("verified_realtime_call_missing_call_id")

    if not config.enabled:
        client.realtime.calls.reject(call_id=call_id, status_code=603)
        return VoiceWebhookResult(
            event_type=event_type,
            action="rejected_feature_disabled",
            call_id=call_id,
        )

    client.realtime.calls.accept(
        call_id=call_id,
        type="realtime",
        model=VOICE_MODEL,
        audio=realtime_audio_config(),
        instructions=build_voice_instructions(config),
        output_modalities=["audio"],
        max_output_tokens=config.max_output_tokens,
        parallel_tool_calls=False,
        reasoning={"effort": normalized_reasoning_effort(config)},
        tool_choice="auto",
        tools=build_realtime_tools(config),
        tracing="auto" if config.tracing_enabled else None,
        truncation=realtime_truncation_config(),
    )
    return VoiceWebhookResult(
        event_type=event_type,
        action="accepted",
        call_id=call_id,
        start_sideband=True,
    )
