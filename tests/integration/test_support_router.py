"""Integration tests for api/routers/support.py."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_support_health(async_client) -> None:
    r = await async_client.get("/api/v1/support/health")
    assert r.status_code == 200
    body = r.json()
    assert "plain_configured" in body


@pytest.mark.asyncio
async def test_support_ticket_validation(async_client) -> None:
    r = await async_client.post(
        "/api/v1/support/tickets",
        json={"email": "not-email", "name": "X", "subject": "a", "body": "b"},
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_support_ticket_happy_shape(async_client, monkeypatch) -> None:
    # Plain unset → falls back to Resend. Resend may also be unset → noop.
    monkeypatch.delenv("PLAIN_API_KEY", raising=False)
    r = await async_client.post(
        "/api/v1/support/tickets",
        json={
            "email": "user@example.sa",
            "name": "Test User",
            "subject": "Hello",
            "body": "Please help with onboarding.",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "transport" in body
    assert body["transport"] in {"plain", "resend", "noop"}
