from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from dealix.voice_ai.front_desk import (
    VOICE_MODEL,
    VoiceAIConfig,
    build_realtime_tools,
    build_voice_instructions,
    dispatch_voice_tool,
    get_voice_readiness,
    handle_openai_realtime_webhook,
)


def _config(**overrides):
    values = {
        "enabled": True,
        "model": VOICE_MODEL,
        "provider": "openai_realtime_sip",
        "reasoning_effort": "medium",
        "max_output_tokens": 900,
        "recording_enabled": False,
        "outbound_enabled": False,
        "tracing_enabled": True,
        "booking_url": "https://calendly.example/dealix",
        "handoff_target_uri": None,
        "openai_api_key": "test-key",
        "webhook_secret": "test-webhook-secret",
    }
    values.update(overrides)
    return VoiceAIConfig(**values)


class _FakeCalls:
    def __init__(self):
        self.accepted = []
        self.rejected = []

    def accept(self, **kwargs):
        self.accepted.append(kwargs)

    def reject(self, **kwargs):
        self.rejected.append(kwargs)


class _FakeClient:
    def __init__(self, event):
        self.event = event
        self.calls = _FakeCalls()
        self.realtime = SimpleNamespace(calls=self.calls)
        self.webhooks = SimpleNamespace(unwrap=self._unwrap)
        self.unwrap_args = None

    def _unwrap(self, body, headers):
        self.unwrap_args = (body, headers)
        return self.event


def test_model_is_locked_to_full_realtime_2_1(monkeypatch):
    monkeypatch.setenv("VOICE_AI_MODEL", "gpt-realtime-2.1-mini")
    cfg = VoiceAIConfig.from_env()
    assert cfg.model == "gpt-realtime-2.1"


def test_readiness_never_returns_secret_values():
    state = get_voice_readiness(_config())
    assert state["model"] == "gpt-realtime-2.1"
    assert state["openai_api_key_configured"] is True
    assert state["webhook_secret_configured"] is True
    assert "test-key" not in json.dumps(state)
    assert "test-webhook-secret" not in json.dumps(state)


def test_voice_instructions_ground_identity_truth_and_commercial_boundaries():
    instructions = build_voice_instructions(_config())
    assert "official Dealix AI Voice Front Desk" in instructions
    assert "Revenue + Proof + Command" in instructions
    assert "not Sami" in instructions
    assert "Never invent customers" in instructions
    assert "customer-specific quote" in instructions
    assert "Recording is OFF" in instructions


def test_tools_include_grounding_booking_qualification_and_handoff():
    names = {tool["name"] for tool in build_realtime_tools(_config())}
    assert names == {
        "lookup_dealix_capabilities",
        "get_booking_link",
        "save_qualification",
        "request_human_handoff",
    }


def test_verified_incoming_call_is_accepted_with_realtime_2_1_and_tools():
    event = SimpleNamespace(
        type="realtime.call.incoming",
        data=SimpleNamespace(call_id="call_test_123"),
    )
    client = _FakeClient(event)
    result = handle_openai_realtime_webhook(
        "{}",
        {"webhook-id": "evt"},
        config=_config(),
        client=client,
    )

    assert result.action == "accepted"
    assert result.start_sideband is True
    assert len(client.calls.accepted) == 1
    accepted = client.calls.accepted[0]
    assert accepted["call_id"] == "call_test_123"
    assert accepted["model"] == "gpt-realtime-2.1"
    assert accepted["output_modalities"] == ["audio"]
    assert accepted["reasoning"] == {"effort": "medium"}
    assert accepted["parallel_tool_calls"] is False
    assert {tool["name"] for tool in accepted["tools"]} >= {
        "lookup_dealix_capabilities",
        "save_qualification",
    }


def test_disabled_voice_rejects_verified_call_fail_closed():
    event = SimpleNamespace(
        type="realtime.call.incoming",
        data=SimpleNamespace(call_id="call_disabled"),
    )
    client = _FakeClient(event)
    result = handle_openai_realtime_webhook(
        "{}",
        {},
        config=_config(enabled=False),
        client=client,
    )
    assert result.action == "rejected_feature_disabled"
    assert client.calls.rejected == [{"call_id": "call_disabled", "status_code": 603}]
    assert client.calls.accepted == []


def test_non_call_event_is_ignored():
    event = SimpleNamespace(type="response.completed", data=SimpleNamespace())
    client = _FakeClient(event)
    result = handle_openai_realtime_webhook("{}", {}, config=_config(), client=client)
    assert result.action == "ignored"
    assert client.calls.accepted == []


@pytest.mark.asyncio
async def test_capability_tool_is_grounded():
    output = await dispatch_voice_tool(
        call_id="call_1",
        name="lookup_dealix_capabilities",
        arguments='{"topic":"overview"}',
        config=_config(),
        client=SimpleNamespace(),
    )
    assert output["ok"] is True
    assert "Governed AI Execution" in output["grounded_answer"]


@pytest.mark.asyncio
async def test_booking_tool_fails_cleanly_when_no_url():
    output = await dispatch_voice_tool(
        call_id="call_1",
        name="get_booking_link",
        arguments="{}",
        config=_config(booking_url=None),
        client=SimpleNamespace(),
    )
    assert output == {
        "ok": False,
        "configured": False,
        "next_step": "offer_human_follow_up",
    }


@pytest.mark.asyncio
async def test_handoff_does_not_fake_transfer_without_target():
    output = await dispatch_voice_tool(
        call_id="call_1",
        name="request_human_handoff",
        arguments='{"reason":"caller requested human"}',
        config=_config(handoff_target_uri=None),
        client=SimpleNamespace(),
    )
    assert output["ok"] is False
    assert output["transferred"] is False


@pytest.mark.asyncio
async def test_handoff_uses_refer_when_target_exists():
    calls = SimpleNamespace(refer=AsyncMock())
    client = SimpleNamespace(realtime=SimpleNamespace(calls=calls))
    output = await dispatch_voice_tool(
        call_id="call_1",
        name="request_human_handoff",
        arguments='{"reason":"enterprise security escalation"}',
        config=_config(handoff_target_uri="tel:+966500000000"),
        client=client,
    )
    assert output == {"ok": True, "transferred": True}
    calls.refer.assert_awaited_once_with(
        call_id="call_1",
        target_uri="tel:+966500000000",
    )


@pytest.mark.asyncio
async def test_invalid_tool_json_fails_closed():
    output = await dispatch_voice_tool(
        call_id="call_1",
        name="save_qualification",
        arguments="{not-json",
        config=_config(),
        client=SimpleNamespace(),
    )
    assert output == {"ok": False, "error": "invalid_tool_arguments"}
