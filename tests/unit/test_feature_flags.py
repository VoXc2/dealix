"""Unit tests for core/feature_flags.py (T1)."""

from __future__ import annotations

import pytest

from core.feature_flags import flag_or_env, is_enabled


def test_flag_or_env_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("STRIPE_ENABLED", "true")
    assert flag_or_env("stripe", "STRIPE_ENABLED") is True
    monkeypatch.setenv("STRIPE_ENABLED", "false")
    assert flag_or_env("stripe", "STRIPE_ENABLED") is False
    monkeypatch.delenv("STRIPE_ENABLED")
    assert flag_or_env("stripe", "STRIPE_ENABLED") is False


@pytest.mark.asyncio
async def test_is_enabled_falls_back_to_env(monkeypatch) -> None:
    monkeypatch.delenv("POSTHOG_API_KEY", raising=False)
    monkeypatch.setenv("PLAIN_ENABLED", "1")
    assert (
        await is_enabled("plain", env_fallback="PLAIN_ENABLED", default=False)
    ) is True
    monkeypatch.delenv("PLAIN_ENABLED")
    assert (
        await is_enabled("plain", env_fallback="PLAIN_ENABLED", default=False)
    ) is False
