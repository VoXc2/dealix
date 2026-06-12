"""Tests for the MiniMax provider in mock mode (no network, no API key).

These tests do not require openai or any external dep. They cover:
- Constructor behavior with no key (mock fallback).
- Constructor behavior with a fake key (env path).
- The chat() response shape in mock mode.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _import_provider():
    return importlib.import_module("dealix.hermes.providers.minimax_provider")


def test_provider_module_imports():
    mod = _import_provider()
    assert hasattr(mod, "MiniMaxProvider"), "MiniMaxProvider class must exist"


def test_provider_no_key_falls_back_to_mock(monkeypatch):
    """With no API key in env, the provider must stay in mock mode.

    We strip both the explicit arg and the env var so we are testing the
    real mock fallback, not the env-resolved path.
    """
    monkeypatch.delenv("MINIMAX_API_KEY", raising=False)
    mod = _import_provider()
    provider = mod.MiniMaxProvider(api_key="")
    assert provider._api_key == "", "With key cleared, _api_key must be empty"
    assert provider._client is None, "Without a key, _client must remain None (mock mode)"


def test_provider_with_fake_key_constructs(monkeypatch):
    monkeypatch.setenv("MINIMAX_API_KEY", "test-fake-key-not-real")
    mod = _import_provider()
    provider = mod.MiniMaxProvider()
    # The provider either constructed an openai client (if openai is installed)
    # or stayed in mock mode (if openai is not installed). Both are valid.
    assert provider._api_key == "test-fake-key-not-real"


def test_chat_returns_expected_shape():
    import asyncio

    mod = _import_provider()
    provider = mod.MiniMaxProvider(api_key="")
    out = asyncio.run(
        provider.chat(
            system="You are MiniMax.",
            messages=[{"role": "user", "content": "hello"}],
        )
    )
    assert isinstance(out, dict)
    assert "text" in out
    assert "tool_calls" in out
    assert "usage" in out
    assert isinstance(out["tool_calls"], list)
    assert out["text"] is not None


def test_chat_handles_tools_argument():
    import asyncio

    mod = _import_provider()
    provider = mod.MiniMaxProvider(api_key="")
    tools = [
        {
            "name": "noop",
            "description": "does nothing",
            "input_schema": {"type": "object", "properties": {}},
        }
    ]
    out = asyncio.run(
        provider.chat(
            system="x",
            messages=[{"role": "user", "content": "x"}],
            tools=tools,
        )
    )
    assert "text" in out
