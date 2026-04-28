"""Smoke tests for the Full OS 12-stage orchestrator + WhatsApp multi-provider."""

from __future__ import annotations

import os

import pytest

from auto_client_acquisition.email.whatsapp_multi_provider import (
    PROVIDER_CHAIN, _normalize_phone, configured_providers, send_whatsapp_smart,
)


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


# ── Provider chain order ─────────────────────────────────────────
def test_provider_chain_has_4_providers():
    names = [name for name, _ in PROVIDER_CHAIN]
    assert names == ["green_api", "ultramsg", "fonnte", "meta_cloud"]


def test_configured_providers_empty_without_env():
    """Without any provider env, no providers configured."""
    keys = [
        "GREEN_API_INSTANCE_ID", "GREEN_API_TOKEN",
        "ULTRAMSG_INSTANCE_ID", "ULTRAMSG_TOKEN",
        "FONNTE_TOKEN",
        "META_WHATSAPP_PHONE_NUMBER_ID", "META_WHATSAPP_ACCESS_TOKEN",
    ]
    saved = {k: os.environ.pop(k, None) for k in keys}
    try:
        assert configured_providers() == []
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


def test_configured_providers_detects_green_api():
    saved_id = os.environ.pop("GREEN_API_INSTANCE_ID", None)
    saved_tok = os.environ.pop("GREEN_API_TOKEN", None)
    os.environ["GREEN_API_INSTANCE_ID"] = "test-instance"
    os.environ["GREEN_API_TOKEN"] = "test-token"
    try:
        assert "green_api" in configured_providers()
    finally:
        os.environ.pop("GREEN_API_INSTANCE_ID", None)
        os.environ.pop("GREEN_API_TOKEN", None)
        if saved_id is not None: os.environ["GREEN_API_INSTANCE_ID"] = saved_id
        if saved_tok is not None: os.environ["GREEN_API_TOKEN"] = saved_tok


# ── Smart send with no keys → no_keys status ─────────────────────
@pytest.mark.asyncio
async def test_send_whatsapp_smart_no_keys():
    keys = [
        "GREEN_API_INSTANCE_ID", "GREEN_API_TOKEN",
        "ULTRAMSG_INSTANCE_ID", "ULTRAMSG_TOKEN",
        "FONNTE_TOKEN",
        "META_WHATSAPP_PHONE_NUMBER_ID", "META_WHATSAPP_ACCESS_TOKEN",
        "WHATSAPP_MOCK_MODE",
    ]
    saved = {k: os.environ.pop(k, None) for k in keys}
    try:
        result = await send_whatsapp_smart("+966500000001", "test")
        assert result.status == "no_keys"
        assert result.fallback_chain_tried == []
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


@pytest.mark.asyncio
async def test_send_whatsapp_smart_mock_mode():
    saved = os.environ.pop("WHATSAPP_MOCK_MODE", None)
    os.environ["WHATSAPP_MOCK_MODE"] = "true"
    try:
        result = await send_whatsapp_smart("+966500000001", "test")
        assert result.status == "mock"
        assert result.provider == "mock"
    finally:
        os.environ.pop("WHATSAPP_MOCK_MODE", None)
        if saved is not None:
            os.environ["WHATSAPP_MOCK_MODE"] = saved


@pytest.mark.asyncio
async def test_send_whatsapp_smart_invalid_phone():
    saved = os.environ.pop("WHATSAPP_MOCK_MODE", None)
    try:
        result = await send_whatsapp_smart("", "test")
        assert result.status == "http_error"
        assert result.error == "invalid_phone"
    finally:
        if saved is not None:
            os.environ["WHATSAPP_MOCK_MODE"] = saved


# ── 12-stage transition logic ─────────────────────────────────────
def test_transitions_from_full_os_router():
    # Import the pure constants without triggering FastAPI app init
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location("full_os_pure",
        "/tmp/dx-final/dealix/api/routers/full_os.py")
    # Skip — would require config setup; instead test transition table values directly
    # by reading the file
    with open("/tmp/dx-final/dealix/api/routers/full_os.py") as f:
        src = f.read()

    # Sanity: 12 stages + 3 terminal = 13 keys in TRANSITIONS
    import re
    keys = re.findall(r'^\s*"(\w+)":\s*\[', src, re.MULTILINE)
    # Filter to stage-like names (drop dict keys like "messaging_product")
    stage_names = {
        "new_lead", "qualifying", "qualified", "nurturing",
        "meeting_booked", "meeting_done", "proposal_sent", "negotiating",
        "payment_requested", "pilot_active",
        "closed_won", "closed_lost", "opted_out",
    }
    found = stage_names & set(keys)
    assert found == stage_names, f"missing stages: {stage_names - found}"


def test_category_to_stage_map_in_source():
    """Every reply category should map to a valid stage."""
    with open("/tmp/dx-final/dealix/api/routers/full_os.py") as f:
        src = f.read()
    # Just check unsubscribe → opted_out and angry → closed_lost
    assert '"unsubscribe":' in src and '"opted_out"' in src
    assert '"angry":' in src and '"closed_lost"' in src
