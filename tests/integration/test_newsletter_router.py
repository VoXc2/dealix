"""Integration tests for api/routers/newsletter.py."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_subscribe_requires_consent(async_client) -> None:
    r = await async_client.post(
        "/api/v1/newsletter/subscribe",
        json={"email": "test@example.com", "consent": False, "locale": "en"},
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "consent_required"


@pytest.mark.asyncio
async def test_subscribe_rejects_invalid_email(async_client) -> None:
    r = await async_client.post(
        "/api/v1/newsletter/subscribe",
        json={"email": "not-an-email", "consent": True, "locale": "en"},
    )
    # Pydantic EmailStr validation runs first → 422.
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_subscribe_no_loops_returns_202_shaped(
    async_client, monkeypatch
) -> None:
    monkeypatch.delenv("LOOPS_API_KEY", raising=False)
    # Reset the cached singleton so the env change takes effect.
    from dealix.marketing import loops_client as lc

    lc._singleton = None
    r = await async_client.post(
        "/api/v1/newsletter/subscribe",
        json={
            "email": "lead@dealix.sa",
            "consent": True,
            "locale": "ar",
            "source": "landing-pricing-calc",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["loops_configured"] is False
    assert body["delivered"] is False
