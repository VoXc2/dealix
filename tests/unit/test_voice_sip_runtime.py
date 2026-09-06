from __future__ import annotations

from types import SimpleNamespace

from dealix.voice_ai.front_desk import VoiceAIConfig
from dealix.voice_ai.sip_runtime import (
    VOICE_MODEL,
    VOICE_OUTPUT_VOICE,
    canonical_positioning_overlay,
    handle_openai_realtime_webhook,
    normalized_reasoning_effort,
    realtime_audio_config,
    realtime_truncation_config,
)


def _config(**overrides):
    values = {
        "enabled": True,
        "model": "gpt-realtime-2.1",
        "provider": "openai_realtime_sip",
        "reasoning_effort": "medium",
        "max_output_tokens": 900,
        "recording_enabled": False,
        "outbound_enabled": False,
        "tracing_enabled": True,
        "booking_url": None,
        "handoff_target_uri": None,
        "openai_api_key": "test-key",
        "webhook_secret": "test-secret",
    }
    values.update(overrides)
    return VoiceAIConfig(**values)


class Calls:
    def __init__(self):
        self.accepted = []
        self.rejected = []

    def accept(self, **kwargs):
        self.accepted.append(kwargs)

    def reject(self, **kwargs):
        self.rejected.append(kwargs)


class Client:
    def __init__(self, event):
        self.webhooks = SimpleNamespace(unwrap=lambda body, headers: event)
        self.realtime = SimpleNamespace(calls=Calls())


def test_voice_and_model_are_full_quality_pins():
    assert VOICE_MODEL == "gpt-realtime-2.1"
    assert VOICE_OUTPUT_VOICE == "cedar"
    audio = realtime_audio_config()
    assert audio["output"] == {"voice": "cedar", "speed": 1.0}
    assert audio["input"]["turn_detection"]["type"] == "semantic_vad"
    assert audio["input"]["turn_detection"]["interrupt_response"] is True


def test_invalid_reasoning_effort_falls_back_to_medium():
    assert normalized_reasoning_effort(_config(reasoning_effort="anything")) == "medium"
    assert normalized_reasoning_effort(_config(reasoning_effort="HIGH")) == "high"


def test_context_strategy_is_bounded_and_cache_friendly():
    truncation = realtime_truncation_config()
    assert truncation["type"] == "retention_ratio"
    assert truncation["retention_ratio"] == 0.8
    assert truncation["token_limits"]["post_instructions"] == 16000


def test_positioning_overlay_matches_current_brand_authority():
    overlay = canonical_positioning_overlay()
    assert "Dealix — AI Business Operating System" in overlay
    assert "Signals into Action. Execution with Governance. Measurable Outcomes." in overlay
    assert "From Opportunity to Outcome." in overlay
    assert "NEVER claim Dealix is the first Saudi company" in overlay
    assert "Command, Revenue, Proof, Client, Delivery, Support, Finance" in overlay


def test_accept_uses_cedar_semantic_vad_and_validated_reasoning():
    event = SimpleNamespace(
        type="realtime.call.incoming",
        data=SimpleNamespace(call_id="call_voice_quality"),
    )
    client = Client(event)
    result = handle_openai_realtime_webhook(
        "{}",
        {},
        _config(reasoning_effort="invalid"),
        client=client,
    )
    assert result.action == "accepted"
    accepted = client.realtime.calls.accepted[0]
    assert accepted["model"] == "gpt-realtime-2.1"
    assert accepted["audio"]["output"]["voice"] == "cedar"
    assert accepted["audio"]["input"]["turn_detection"]["type"] == "semantic_vad"
    assert accepted["reasoning"] == {"effort": "medium"}
    assert accepted["truncation"]["type"] == "retention_ratio"
    assert "AI Business Operating System" in accepted["instructions"]


def test_disabled_runtime_rejects_call_before_model_session():
    event = SimpleNamespace(
        type="realtime.call.incoming",
        data=SimpleNamespace(call_id="call_disabled"),
    )
    client = Client(event)
    result = handle_openai_realtime_webhook(
        "{}",
        {},
        _config(enabled=False),
        client=client,
    )
    assert result.action == "rejected_feature_disabled"
    assert client.realtime.calls.rejected == [
        {"call_id": "call_disabled", "status_code": 603}
    ]
    assert client.realtime.calls.accepted == []
