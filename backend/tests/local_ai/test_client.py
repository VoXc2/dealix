"""Unit tests for the Ollama client — network mocked with respx."""
from __future__ import annotations

import json

import httpx
import pytest
import respx

from app.services.local_ai.client import OllamaChatResult, OllamaClient


BASE = "http://localhost:11434"


@pytest.mark.asyncio
@respx.mock
async def test_health_returns_true_on_200():
    respx.get(f"{BASE}/api/tags").mock(return_value=httpx.Response(200, json={"models": []}))
    client = OllamaClient(base_url=BASE)
    assert await client.health(force=True) is True


@pytest.mark.asyncio
@respx.mock
async def test_health_returns_false_on_connection_error():
    respx.get(f"{BASE}/api/tags").mock(side_effect=httpx.ConnectError("nope"))
    client = OllamaClient(base_url=BASE)
    assert await client.health(force=True) is False


@pytest.mark.asyncio
@respx.mock
async def test_list_models_parses_tags():
    respx.get(f"{BASE}/api/tags").mock(
        return_value=httpx.Response(200, json={"models": [{"name": "qwen2.5:3b-instruct"}]})
    )
    client = OllamaClient(base_url=BASE)
    tags = await client.list_models()
    assert tags and tags[0]["name"] == "qwen2.5:3b-instruct"


@pytest.mark.asyncio
@respx.mock
async def test_chat_success_returns_result():
    respx.post(f"{BASE}/api/chat").mock(
        return_value=httpx.Response(200, json={
            "model": "qwen2.5:3b-instruct",
            "message": {"role": "assistant", "content": "مرحبا"},
            "prompt_eval_count": 5,
            "eval_count": 3,
            "done": True,
        })
    )
    client = OllamaClient(base_url=BASE, retries=0)
    res = await client.chat(
        model="qwen2.5:3b-instruct",
        messages=[{"role": "user", "content": "hi"}],
    )
    assert isinstance(res, OllamaChatResult)
    assert res.success is True
    assert res.content == "مرحبا"
    assert res.total_tokens == 8


@pytest.mark.asyncio
@respx.mock
async def test_chat_404_does_not_retry_and_returns_error():
    route = respx.post(f"{BASE}/api/chat").mock(
        return_value=httpx.Response(404, text="model not found")
    )
    client = OllamaClient(base_url=BASE, retries=3)
    res = await client.chat(model="missing", messages=[{"role": "user", "content": "x"}])
    assert res.success is False
    assert "404" in (res.error or "")
    # 4xx should NOT retry
    assert route.call_count == 1


@pytest.mark.asyncio
@respx.mock
async def test_chat_5xx_retries_then_gives_up():
    route = respx.post(f"{BASE}/api/chat").mock(
        return_value=httpx.Response(503, text="busy")
    )
    client = OllamaClient(base_url=BASE, retries=2)
    res = await client.chat(model="m", messages=[{"role": "user", "content": "x"}])
    assert res.success is False
    # original + 2 retries
    assert route.call_count == 3


@pytest.mark.asyncio
@respx.mock
async def test_chat_json_mode_sets_format():
    captured = {}

    def responder(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content.decode())
        return httpx.Response(200, json={"message": {"content": "{}"}, "done": True})

    respx.post(f"{BASE}/api/chat").mock(side_effect=responder)
    client = OllamaClient(base_url=BASE, retries=0)
    await client.chat(model="m", messages=[{"role": "user", "content": "x"}], json_mode=True)
    assert captured["body"]["format"] == "json"
