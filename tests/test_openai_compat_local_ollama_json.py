from __future__ import annotations

import asyncio

from core.llm import openai_compat
from core.llm.base import Message
from core.llm.openai_compat import OpenAICompatClient


class _FakeResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {
            "choices": [
                {
                    "message": {"content": "{}"},
                    "finish_reason": "stop",
                }
            ],
            "model": "qwen3:4b-instruct-2507-q4_K_M",
            "usage": {"prompt_tokens": 10, "completion_tokens": 2},
        }


class _FakeAsyncClient:
    payloads: list[dict] = []

    def __init__(self, timeout: int) -> None:
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    async def post(self, url: str, *, json: dict, headers: dict):
        self.__class__.payloads.append(json)
        return _FakeResponse()


def _local_client() -> OpenAICompatClient:
    return OpenAICompatClient(
        api_key="ollama-local-nonsecret",
        model="qwen3:4b-instruct-2507-q4_K_M",
        base_url="http://127.0.0.1:11434/v1",
    )


def test_local_ollama_json_only_contract_uses_json_mode_and_no_reasoning(monkeypatch) -> None:
    _FakeAsyncClient.payloads.clear()
    monkeypatch.setattr(openai_compat.httpx, "AsyncClient", _FakeAsyncClient)
    client = _local_client()

    response = asyncio.run(
        client.chat(
            [Message(role="user", content="اختبار")],
            system="أخرج JSON صحيحاً فقط بهذه الحقول: facts, unknowns",
            max_tokens=1800,
            temperature=0.0,
        )
    )

    assert response.content == "{}"
    payload = _FakeAsyncClient.payloads[-1]
    assert payload["response_format"] == {"type": "json_object"}
    assert payload["reasoning_effort"] == "none"
    assert payload["max_tokens"] == 1800
    assert payload["temperature"] == 0.0


def test_local_ollama_explicit_json_schema_is_forwarded_exactly(monkeypatch) -> None:
    _FakeAsyncClient.payloads.clear()
    monkeypatch.setattr(openai_compat.httpx, "AsyncClient", _FakeAsyncClient)
    client = _local_client()
    schema_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "dealix_probe",
            "schema": {
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }

    asyncio.run(
        client.chat(
            [Message(role="user", content="اختبار")],
            system="أخرج JSON صحيحاً فقط",
            response_format=schema_format,
            reasoning_effort="none",
            seed=7,
        )
    )

    payload = _FakeAsyncClient.payloads[-1]
    assert payload["response_format"] == schema_format
    assert payload["reasoning_effort"] == "none"
    assert payload["seed"] == 7


def test_remote_openai_compatible_provider_is_not_mutated(monkeypatch) -> None:
    _FakeAsyncClient.payloads.clear()
    monkeypatch.setattr(openai_compat.httpx, "AsyncClient", _FakeAsyncClient)
    client = OpenAICompatClient(
        api_key="test-key",
        model="remote-model",
        base_url="https://example.invalid/v1",
    )

    asyncio.run(
        client.chat(
            [Message(role="user", content="test")],
            system="valid JSON only",
            max_tokens=100,
            temperature=0.2,
            response_format={"type": "json_object"},
            reasoning_effort="none",
            seed=7,
        )
    )

    payload = _FakeAsyncClient.payloads[-1]
    assert "response_format" not in payload
    assert "reasoning_effort" not in payload
    assert "seed" not in payload


def test_non_json_local_request_is_not_forced_to_json_mode(monkeypatch) -> None:
    _FakeAsyncClient.payloads.clear()
    monkeypatch.setattr(openai_compat.httpx, "AsyncClient", _FakeAsyncClient)
    client = OpenAICompatClient(
        api_key="ollama-local-nonsecret",
        model="qwen3:4b-instruct-2507-q4_K_M",
        base_url="http://localhost:11434/v1/",
    )

    asyncio.run(
        client.chat(
            [Message(role="user", content="Say hello")],
            system="Answer concisely.",
        )
    )

    payload = _FakeAsyncClient.payloads[-1]
    assert "response_format" not in payload
    assert "reasoning_effort" not in payload
