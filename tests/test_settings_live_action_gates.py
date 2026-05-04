"""Tests for the live-action gate flags wired into the integrations."""

from __future__ import annotations

import pytest

from core.config.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


# ── Defaults ──────────────────────────────────────────────────────


def test_all_live_action_flags_default_false(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in (
        "WHATSAPP_ALLOW_LIVE_SEND",
        "GMAIL_ALLOW_LIVE_SEND",
        "MOYASAR_ALLOW_LIVE_CHARGE",
        "LINKEDIN_ALLOW_AUTO_DM",
    ):
        monkeypatch.delenv(var, raising=False)
    s = Settings()
    assert s.whatsapp_allow_live_send is False
    assert s.gmail_allow_live_send is False
    assert s.moyasar_allow_live_charge is False
    assert s.linkedin_allow_auto_dm is False


def test_gmail_flag_can_be_enabled_via_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GMAIL_ALLOW_LIVE_SEND", "true")
    s = Settings()
    assert s.gmail_allow_live_send is True


def test_moyasar_flag_can_be_enabled_via_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MOYASAR_ALLOW_LIVE_CHARGE", "true")
    s = Settings()
    assert s.moyasar_allow_live_charge is True


# ── Gmail wiring ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_gmail_send_blocked_when_flag_false(monkeypatch: pytest.MonkeyPatch) -> None:
    from auto_client_acquisition.email import gmail_send

    monkeypatch.delenv("GMAIL_ALLOW_LIVE_SEND", raising=False)
    # Even with all keys configured, the flag must block.
    monkeypatch.setenv("GMAIL_CLIENT_ID", "x")
    monkeypatch.setenv("GMAIL_CLIENT_SECRET", "x")
    monkeypatch.setenv("GMAIL_REFRESH_TOKEN", "x")
    monkeypatch.setenv("GMAIL_SENDER_EMAIL", "x@y.z")

    result = await gmail_send.send_email(
        to_email="test@example.com",
        subject="hi",
        body_plain="hello",
    )
    assert result.status == "blocked"
    assert result.error == "gmail_allow_live_send_false"


# ── Moyasar wiring ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_moyasar_create_invoice_blocked_when_flag_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from dealix.payments.moyasar import MoyasarClient

    monkeypatch.delenv("MOYASAR_ALLOW_LIVE_CHARGE", raising=False)
    client = MoyasarClient(secret_key="sk_test_dummy")

    with pytest.raises(RuntimeError, match="moyasar_allow_live_charge_false"):
        await client.create_invoice(amount_halalas=49900, description="test")


# ── LinkedIn wiring ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_linkedin_auto_dm_always_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    """Even if flag is flipped True, auto-DM stays disabled."""
    from integrations.linkedin import LinkedInClient

    monkeypatch.setenv("LINKEDIN_ALLOW_AUTO_DM", "true")  # try to bypass
    client = LinkedInClient()
    result = await client.send_auto_dm(recipient_urn="urn:li:person:test", text="hi")
    assert result.success is False
    assert result.disabled is True
    assert "forbidden" in result.reason.lower()


@pytest.mark.asyncio
async def test_linkedin_post_text_default_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    from integrations.linkedin import LinkedInClient

    monkeypatch.delenv("LINKEDIN_ALLOW_AUTO_DM", raising=False)
    client = LinkedInClient()
    result = await client.post_text("test")
    assert result.success is False
    assert result.disabled is True
