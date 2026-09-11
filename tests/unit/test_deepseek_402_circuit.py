from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest

from core.config.models import Provider, Task
from core.config.settings import Settings
from core.llm.base import LLMResponse, Message
from core.llm.openai_compat import (
    DeepSeekClient,
    OllamaCompatClient,
    _record_retry_attempt,
    openai_compat_retry_count,
    reset_openai_compat_retry_count,
)
from core.llm.router import ModelRouter


def settings(**overrides: object) -> Settings:
    values: dict[str, object] = {"deepseek_api_key": "sk-test-deepseek", "deepseek_model": "deepseek-chat"}
    values.update(overrides)
    return Settings(_env_file=None, **values)


def payment_required() -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://api.deepseek.com/v1/chat/completions")
    response = httpx.Response(402, request=request)
    return httpx.HTTPStatusError("payment required", request=request, response=response)


def response(model: str, provider: str = "deepseek") -> LLMResponse:
    return LLMResponse(content="OK", provider=provider, model=model, input_tokens=1000, output_tokens=100,
        cached_tokens=700 if provider == "deepseek" else 0,
        raw={"usage": {"prompt_cache_hit_tokens": 700, "prompt_cache_miss_tokens": 0}})


@pytest.mark.asyncio
async def test_402_opens_circuit_and_second_call_skips_deepseek() -> None:
    router = ModelRouter(settings=settings(deepseek_402_ollama_fallback_enabled=True))
    deepseek = router.get_client(Provider.DEEPSEEK); local = router._deepseek_local_fallback
    assert isinstance(deepseek, DeepSeekClient); assert isinstance(local, OllamaCompatClient)
    deepseek.chat = AsyncMock(side_effect=payment_required())
    local.chat = AsyncMock(return_value=response("qwen3:4b-instruct-2507-q4_K_M", "ollama_local"))
    first = await router.run(Task.CODE, [Message(role="user", content="x")])
    second = await router.run(Task.CODE, [Message(role="user", content="y")])
    assert first.provider == second.provider == "ollama_local"
    assert router.circuit_status() == {"deepseek": "billing_402"}
    assert deepseek.chat.await_count == 1; assert local.chat.await_count == 2


@pytest.mark.asyncio
async def test_explicit_reset_allows_deepseek_again() -> None:
    router = ModelRouter(settings=settings(deepseek_402_ollama_fallback_enabled=True))
    deepseek = router.get_client(Provider.DEEPSEEK); local = router._deepseek_local_fallback
    assert isinstance(deepseek, DeepSeekClient); assert isinstance(local, OllamaCompatClient)
    deepseek.chat = AsyncMock(side_effect=payment_required())
    local.chat = AsyncMock(return_value=response("qwen3:4b-instruct-2507-q4_K_M", "ollama_local"))
    await router.run(Task.CODE, "one"); router.reset_provider_circuit(Provider.DEEPSEEK); await router.run(Task.CODE, "two")
    assert deepseek.chat.await_count == 2


@pytest.mark.asyncio
async def test_402_circuit_without_local_fallback_fails_closed() -> None:
    router = ModelRouter(settings=settings()); deepseek = router.get_client(Provider.DEEPSEEK)
    assert isinstance(deepseek, DeepSeekClient); deepseek.chat = AsyncMock(side_effect=payment_required())
    with pytest.raises(RuntimeError): await router.run(Task.CODE, "one")
    with pytest.raises(RuntimeError): await router.run(Task.CODE, "two")
    assert deepseek.chat.await_count == 1; assert router.circuit_status() == {"deepseek": "billing_402"}


@pytest.mark.asyncio
async def test_local_fallback_failure_does_not_loop() -> None:
    router = ModelRouter(settings=settings(deepseek_402_ollama_fallback_enabled=True))
    deepseek = router.get_client(Provider.DEEPSEEK); local = router._deepseek_local_fallback
    assert isinstance(deepseek, DeepSeekClient); assert isinstance(local, OllamaCompatClient)
    deepseek.chat = AsyncMock(side_effect=payment_required()); local.chat = AsyncMock(side_effect=RuntimeError("local unavailable"))
    with pytest.raises(RuntimeError): await router.run(Task.CODE, "one")
    with pytest.raises(RuntimeError): await router.run(Task.CODE, "two")
    assert deepseek.chat.await_count == 1; assert local.chat.await_count == 2


def test_non_loopback_ollama_configuration_is_rejected() -> None:
    router = ModelRouter(settings=settings(deepseek_402_ollama_fallback_enabled=True, deepseek_ollama_base_url="https://example.com/v1"))
    assert router._deepseek_local_fallback is None


@pytest.mark.asyncio
async def test_usage_event_separates_requested_effective_model_and_cache() -> None:
    router = ModelRouter(settings=settings(deepseek_model="deepseek-chat")); deepseek = router.get_client(Provider.DEEPSEEK)
    assert isinstance(deepseek, DeepSeekClient); deepseek.chat = AsyncMock(return_value=response("deepseek-v4-flash"))
    await router.run(Task.CODE, "telemetry"); event = router.recent_usage_events(1)[0]
    assert event["logical_route"] == "code"; assert event["requested_model"] == "deepseek-chat"
    assert event["effective_model"] == "deepseek-v4-flash"; assert event["cache_status"] == "hit"
    assert event["retries"] == 0; assert event["accepted"] is True; assert event["budget_cost_usd"] is not None
    assert event["cost_per_accepted_result_usd"] == event["budget_cost_usd"]; assert router.recent_usage_events(0) == []


@pytest.mark.asyncio
async def test_402_logs_do_not_include_api_key(caplog: pytest.LogCaptureFixture) -> None:
    router = ModelRouter(settings=settings()); deepseek = router.get_client(Provider.DEEPSEEK)
    assert isinstance(deepseek, DeepSeekClient); deepseek.chat = AsyncMock(side_effect=payment_required())
    with pytest.raises(RuntimeError): await router.run(Task.CODE, "secret-safe")
    assert "sk-test-deepseek" not in caplog.text


def test_retry_counter_is_resettable_and_counts_attempts() -> None:
    reset_openai_compat_retry_count(); assert openai_compat_retry_count() == 0
    _record_retry_attempt(SimpleNamespace(attempt_number=3)); assert openai_compat_retry_count() == 2
    reset_openai_compat_retry_count(); assert openai_compat_retry_count() == 0
