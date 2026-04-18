"""
Tests for LLMGateway — fallback, prompt loading, tool calling.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_chat_groq_primary(llm):
    """chat() uses Groq when API key is set."""
    llm.settings.groq_api_key = "test_key"

    with patch.object(llm, "_call", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = "مرحبا من Groq"
        result = await llm.chat([{"role": "user", "content": "مرحبا"}])

    assert result == "مرحبا من Groq"
    mock_call.assert_called_once()
    call_url = mock_call.call_args[1]["url"] if mock_call.call_args[1] else mock_call.call_args[0][0]
    assert "groq.com" in call_url


@pytest.mark.asyncio
async def test_chat_falls_back_to_openai(llm):
    """chat() falls back to OpenAI when Groq fails."""
    llm.settings.groq_api_key = "test_groq_key"
    llm.settings.openai_api_key = "test_openai_key"

    call_count = {"groq": 0, "openai": 0}

    async def mock_call(url, api_key, payload):
        if "groq.com" in url:
            call_count["groq"] += 1
            raise RuntimeError("Groq unavailable")
        call_count["openai"] += 1
        return "fallback from OpenAI"

    with patch.object(llm, "_call", side_effect=mock_call):
        result = await llm.chat([{"role": "user", "content": "test"}])

    assert result == "fallback from OpenAI"
    assert call_count["groq"] == 1
    assert call_count["openai"] == 1


@pytest.mark.asyncio
async def test_chat_static_fallback_when_no_keys(llm):
    """chat() returns static Arabic fallback when both providers have no keys."""
    llm.settings.groq_api_key = ""
    llm.settings.openai_api_key = ""

    result = await llm.chat([{"role": "user", "content": "test"}])
    assert "Dealix" in result or "شكراً" in result  # static fallback message


def test_get_system_prompt_loads_file(llm):
    """get_system_prompt() loads a prompt .md file by key."""
    # This test requires the actual prompts directory to exist
    prompt = llm.get_system_prompt("system_base_ar")
    assert "Dealix" in prompt
    assert "ديلكس" in prompt or "Dealix" in prompt


def test_get_system_prompt_caches(llm):
    """Prompt files are cached after first load."""
    llm._prompt_cache.clear()
    prompt1 = llm.get_system_prompt("system_base_ar")
    prompt2 = llm.get_system_prompt("system_base_ar")
    assert prompt1 is prompt2  # exact same object from cache


def test_get_system_prompt_missing_key(llm):
    """Missing prompt key returns empty string."""
    result = llm.get_system_prompt("nonexistent_prompt_xyz")
    assert result == ""


def test_compose_prompt(llm):
    """compose_prompt() combines multiple prompts with separator."""
    result = llm.compose_prompt("system_base_ar", "qualifier_ar")
    assert "Dealix" in result
    assert "BANT" in result


def test_list_available_prompts(llm):
    """list_available_prompts() returns all .md file stems."""
    prompts = llm.list_available_prompts()
    assert "system_base_ar" in prompts
    assert "whatsapp_outbound_ar" in prompts
    assert "qualifier_ar" in prompts
    assert len(prompts) >= 9  # at least the 9 required prompts


@pytest.mark.asyncio
async def test_chat_with_tools_returns_tool_calls(llm):
    """chat_with_tools() returns raw response with tool_calls."""
    llm.settings.groq_api_key = "test_key"

    mock_response = {
        "choices": [{
            "message": {
                "content": None,
                "tool_calls": [{
                    "id": "call_abc",
                    "type": "function",
                    "function": {
                        "name": "book_meeting",
                        "arguments": '{"datetime_iso": "2025-05-01T10:00:00Z"}'
                    }
                }]
            }
        }]
    }

    with patch.object(llm, "_call_raw", new_callable=AsyncMock) as mock_raw:
        mock_raw.return_value = mock_response
        result = await llm.chat_with_tools(
            messages=[{"role": "user", "content": "أريد حجز موعد"}],
            tools=[{"type": "function", "function": {"name": "book_meeting"}}],
        )

    tool_calls = result["choices"][0]["message"]["tool_calls"]
    assert len(tool_calls) == 1
    assert tool_calls[0]["function"]["name"] == "book_meeting"
