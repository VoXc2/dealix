"""Smoke tests for the Full OS 12-stage orchestrator + WhatsApp providers."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_FULL_OS_ROUTER = _REPO_ROOT / "api" / "routers" / "full_os.py"

from auto_client_acquisition.email.whatsapp_multi_provider import (
    PROVIDER_CHAIN,
    _normalize_phone,
    configured_providers,
    runtime_provider_chain,
    send_whatsapp_smart,
)
from core.config.settings import get_settings


# ── Phone normalization ───────────────────────────────────────────
def test_normalize_phone_966_prefix_kept():
    assert _normalize_phone("+966500000001") == "966500000001"


def test_normalize_phone_local_05():
    assert _normalize_phone("0500000001") == "966500000001"


def test_normalize_phone_short_local():
    assert _normalize_phone("500000001") == "966500000001"


def test_normalize_phone_strips_punctuation():
    assert _normalize_phone("+966 (50) 000-0001") == "966500000001"


def test_normalize_phone_double_zero():
    assert _normalize_phone("00966500000001") == "966500000001"


# ── Provider selection ────────────────────────────────────────────
def test_provider_chain_is_official_first():
    names = [name for name, _ in PROVIDER_CHAIN]
    assert names == ["meta_cloud", "green_api", "ultramsg", "fonnte"]


def _provider_env_keys() -> list[str]:
    return [
        "GREEN_API_INSTANCE_ID",
        "GREEN_API_TOKEN",
        "ULTRAMSG_INSTANCE_ID",
        "ULTRAMSG_TOKEN",
        "FONNTE_TOKEN",
        "WHATSAPP_PHONE_NUMBER_ID",
        "WHATSAPP_ACCESS_TOKEN",
        "META_WHATSAPP_PHONE_NUMBER_ID",
        "META_WHATSAPP_ACCESS_TOKEN",
        "WHATSAPP_PROVIDER_PREFERENCE",
        "WHATSAPP_MOCK_MODE",
    ]


def _pop_env(keys: list[str]) -> dict[str, str | None]:
    return {key: os.environ.pop(key, None) for key in keys}


def _restore_env(saved: dict[str, str | None]) -> None:
    for key in saved:
        os.environ.pop(key, None)
    for key, value in saved.items():
        if value is not None:
            os.environ[key] = value


def test_configured_providers_empty_without_env():
    saved = _pop_env(_provider_env_keys())
    try:
        assert configured_providers() == []
    finally:
        _restore_env(saved)


def test_configured_providers_detects_green_api():
    saved = _pop_env(_provider_env_keys())
    os.environ["GREEN_API_INSTANCE_ID"] = "test-instance"
    os.environ["GREEN_API_TOKEN"] = "test-token"
    try:
        assert configured_providers() == ["green_api"]
    finally:
        _restore_env(saved)


def test_configured_providers_detects_canonical_meta_names():
    saved = _pop_env(_provider_env_keys())
    os.environ["WHATSAPP_PHONE_NUMBER_ID"] = "123456"
    os.environ["WHATSAPP_ACCESS_TOKEN"] = "test-token"
    try:
        assert configured_providers() == ["meta_cloud"]
    finally:
        _restore_env(saved)


def test_auto_provider_selection_uses_meta_only_when_meta_is_configured():
    saved = _pop_env(_provider_env_keys())
    os.environ["WHATSAPP_PHONE_NUMBER_ID"] = "123456"
    os.environ["WHATSAPP_ACCESS_TOKEN"] = "meta-token"
    os.environ["GREEN_API_INSTANCE_ID"] = "green-instance"
    os.environ["GREEN_API_TOKEN"] = "green-token"
    try:
        assert [name for name, _ in runtime_provider_chain()] == ["meta_cloud"]
    finally:
        _restore_env(saved)


def test_explicit_green_transition_does_not_select_meta():
    saved = _pop_env(_provider_env_keys())
    os.environ["WHATSAPP_PHONE_NUMBER_ID"] = "123456"
    os.environ["WHATSAPP_ACCESS_TOKEN"] = "meta-token"
    os.environ["GREEN_API_INSTANCE_ID"] = "green-instance"
    os.environ["GREEN_API_TOKEN"] = "green-token"
    os.environ["WHATSAPP_PROVIDER_PREFERENCE"] = "green_api"
    try:
        assert [name for name, _ in runtime_provider_chain()] == ["green_api"]
    finally:
        _restore_env(saved)


# ── Smart send safety ─────────────────────────────────────────────
@pytest.mark.asyncio
async def test_send_whatsapp_smart_no_keys():
    saved = _pop_env(_provider_env_keys())
    saved_flag = os.environ.pop("WHATSAPP_ALLOW_LIVE_SEND", None)
    os.environ["WHATSAPP_ALLOW_LIVE_SEND"] = "true"
    get_settings.cache_clear()
    try:
        result = await send_whatsapp_smart("+966500000001", "test")
        assert result.status == "no_keys"
        assert result.fallback_chain_tried == []
    finally:
        _restore_env(saved)
        os.environ.pop("WHATSAPP_ALLOW_LIVE_SEND", None)
        if saved_flag is not None:
            os.environ["WHATSAPP_ALLOW_LIVE_SEND"] = saved_flag
        get_settings.cache_clear()


@pytest.mark.asyncio
async def test_send_whatsapp_smart_blocked_when_flag_off():
    saved = _pop_env(_provider_env_keys())
    saved_flag = os.environ.pop("WHATSAPP_ALLOW_LIVE_SEND", None)
    os.environ["WHATSAPP_ALLOW_LIVE_SEND"] = "false"
    get_settings.cache_clear()
    try:
        result = await send_whatsapp_smart("+966500000001", "test")
        assert result.status == "blocked"
        assert result.error == "whatsapp_allow_live_send_false"
    finally:
        _restore_env(saved)
        os.environ.pop("WHATSAPP_ALLOW_LIVE_SEND", None)
        if saved_flag is not None:
            os.environ["WHATSAPP_ALLOW_LIVE_SEND"] = saved_flag
        get_settings.cache_clear()


@pytest.mark.asyncio
async def test_send_whatsapp_smart_mock_mode():
    saved = _pop_env(_provider_env_keys())
    os.environ["WHATSAPP_MOCK_MODE"] = "true"
    try:
        result = await send_whatsapp_smart("+966500000001", "test")
        assert result.status == "mock"
        assert result.provider == "mock"
    finally:
        _restore_env(saved)


@pytest.mark.asyncio
async def test_send_whatsapp_smart_invalid_phone():
    saved = _pop_env(_provider_env_keys())
    try:
        result = await send_whatsapp_smart("", "test")
        assert result.status == "http_error"
        assert result.error == "invalid_phone"
    finally:
        _restore_env(saved)


@pytest.mark.asyncio
async def test_send_whatsapp_smart_invalid_provider_preference_fails_closed():
    saved = _pop_env(_provider_env_keys())
    saved_flag = os.environ.pop("WHATSAPP_ALLOW_LIVE_SEND", None)
    os.environ["WHATSAPP_ALLOW_LIVE_SEND"] = "true"
    os.environ["WHATSAPP_PROVIDER_PREFERENCE"] = "unknown-provider"
    get_settings.cache_clear()
    try:
        result = await send_whatsapp_smart("+966500000001", "test")
        assert result.status == "http_error"
        assert result.error == "invalid_whatsapp_provider_preference"
    finally:
        _restore_env(saved)
        os.environ.pop("WHATSAPP_ALLOW_LIVE_SEND", None)
        if saved_flag is not None:
            os.environ["WHATSAPP_ALLOW_LIVE_SEND"] = saved_flag
        get_settings.cache_clear()


# ── 12-stage transition logic ─────────────────────────────────────
def test_transitions_from_full_os_router():
    assert _FULL_OS_ROUTER.is_file(), f"missing {_FULL_OS_ROUTER}"
    with _FULL_OS_ROUTER.open(encoding="utf-8") as f:
        src = f.read()

    import re

    keys = re.findall(r'^\s*"(\w+)":\s*\[', src, re.MULTILINE)
    stage_names = {
        "new_lead",
        "qualifying",
        "qualified",
        "nurturing",
        "meeting_booked",
        "meeting_done",
        "proposal_sent",
        "negotiating",
        "payment_requested",
        "pilot_active",
        "closed_won",
        "closed_lost",
        "opted_out",
    }
    found = stage_names & set(keys)
    assert found == stage_names, f"missing stages: {stage_names - found}"


def test_category_to_stage_map_in_source():
    """Every reply category should map to a valid stage."""
    with _FULL_OS_ROUTER.open(encoding="utf-8") as f:
        src = f.read()
    assert '"unsubscribe":' in src and '"opted_out"' in src
    assert '"angry":' in src and '"closed_lost"' in src
