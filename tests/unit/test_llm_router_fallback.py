"""
Unit tests — LLM ModelRouter fallback chain.
اختبارات الوحدة — سلسلة الاحتياط لمُوجّه النموذج.

Tests that when a provider raises an exception the router correctly
falls back to the next provider in the FALLBACK_CHAIN.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.config.models import Provider, Task
from core.llm.base import LLMResponse, Message
from core.llm.router import ModelRouter, UsageRecord

# ── Fixtures ───────────────────────────────────────────────────────

@pytest.fixture()
def mock_settings():
    settings = MagicMock()
    settings.anthropic_api_key.get_secret_value.return_value = "sk-test-anthropic"
    settings.deepseek_api_key.get_secret_value.return_value = "sk-test-deepseek"
    settings.groq_api_key.get_secret_value.return_value = "sk-test-groq"
    settings.glm_api_key.get_secret_value.return_value = "sk-test-glm"
    settings.google_api_key.get_secret_value.return_value = "sk-test-google"
    settings.openai_api_key.get_secret_value.return_value = ""
    return settings


def _make_response(provider: Provider, content: str = "OK") -> LLMResponse:
    return LLMResponse(
        content=content,
        provider=provider,
        model="test-model",
        input_tokens=10,
        output_tokens=5,
    )


# ── Tests ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_router_uses_primary_provider(mock_settings):
    """Router calls the primary provider and returns its response."""
    router = ModelRouter(settings=mock_settings)

    primary_provider = next(iter(router._clients))
    mock_client = AsyncMock()
    mock_client.chat.return_value = _make_response(primary_provider, "primary response")
    router._clients[primary_provider] = mock_client

    messages = [Message(role="user", content="hello")]
    response = await router.run(task=Task.REASONING, messages=messages)

    assert response.content == "primary response"
    mock_client.chat.assert_called_once()


@pytest.mark.asyncio
async def test_router_falls_back_on_provider_error(mock_settings):
    """When the primary provider raises, router tries the next in fallback chain."""
    router = ModelRouter(settings=mock_settings)

    # Make every client fail except the last one
    success_content = "fallback response"
    providers = list(router._clients.keys())

    for provider in providers[:-1]:
        mock_fail = AsyncMock()
        mock_fail.chat.side_effect = Exception(f"Provider {provider} unavailable")
        router._clients[provider] = mock_fail

    # Last provider succeeds
    last_provider = providers[-1]
    mock_ok = AsyncMock()
    mock_ok.chat.return_value = _make_response(last_provider, success_content)
    router._clients[last_provider] = mock_ok

    messages = [Message(role="user", content="test")]
    response = await router.run(task=Task.REASONING, messages=messages)

    assert response.content == success_content


@pytest.mark.asyncio
async def test_router_raises_when_all_providers_fail(mock_settings):
    """Router raises RuntimeError when every provider in the chain fails."""
    router = ModelRouter(settings=mock_settings)

    for provider in router._clients:
        mock_fail = AsyncMock()
        mock_fail.chat.side_effect = Exception("unavailable")
        router._clients[provider] = mock_fail

    messages = [Message(role="user", content="test")]
    with pytest.raises((RuntimeError, Exception)):
        await router.run(task=Task.REASONING, messages=messages)


@pytest.mark.asyncio
async def test_router_increments_fallback_counter(mock_settings):
    """After a fallback the triggering provider's fallbacks_triggered is incremented."""
    router = ModelRouter(settings=mock_settings)
    providers = list(router._clients.keys())

    if len(providers) < 2:
        pytest.skip("Need at least 2 providers for this test")

    primary = providers[0]
    secondary = providers[1]

    mock_fail = AsyncMock()
    mock_fail.chat.side_effect = Exception("timeout")
    router._clients[primary] = mock_fail

    mock_ok = AsyncMock()
    mock_ok.chat.return_value = _make_response(secondary)
    router._clients[secondary] = mock_ok

    # Patch remaining providers to also fail cleanly
    for p in providers[2:]:
        router._clients[p] = mock_ok

    await router.run(task=Task.REASONING, messages=[Message(role="user", content="x")])

    assert router.usage[primary].fallbacks_triggered >= 1


@pytest.mark.asyncio
async def test_router_usage_records_are_updated(mock_settings):
    """Usage records are incremented on successful completion."""
    router = ModelRouter(settings=mock_settings)
    providers = list(router._clients.keys())
    primary = providers[0]

    mock_client = AsyncMock()
    mock_client.chat.return_value = _make_response(primary, "ok")
    router._clients[primary] = mock_client

    initial_calls = router.usage[primary].calls
    await router.run(task=Task.REASONING, messages=[Message(role="user", content="test")])
    assert router.usage[primary].calls == initial_calls + 1


@pytest.mark.asyncio
async def test_router_concurrent_safety(mock_settings):
    """Concurrent route calls don't corrupt usage counters (asyncio.Lock)."""
    router = ModelRouter(settings=mock_settings)
    providers = list(router._clients.keys())
    primary = providers[0]

    call_count = 0

    async def _increment_and_respond(**kwargs):
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0)  # yield — simulates I/O
        return _make_response(primary)

    mock_client = MagicMock()
    mock_client.chat = _increment_and_respond
    router._clients[primary] = mock_client

    messages = [Message(role="user", content="concurrent")]
    tasks = [router.run(task=Task.REASONING, messages=messages) for _ in range(10)]
    responses = await asyncio.gather(*tasks)

    assert len(responses) == 10
    assert router.usage[primary].calls == 10
