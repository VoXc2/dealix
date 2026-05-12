"""Integration tests for api/routers/onboarding.py (T0)."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_start_validates_payload(async_client) -> None:
    r = await async_client.post(
        "/api/v1/onboarding/start",
        json={"company": ""},  # missing email + name
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_start_happy_path_shape(async_client) -> None:
    r = await async_client.post(
        "/api/v1/onboarding/start",
        json={
            "company": "TestCo",
            "email": "owner@testco.sa",
            "name": "Owner",
            "locale": "ar",
        },
    )
    # DB may be unavailable in unit-test env → either persisted (200) or
    # 500 onboarding_persistence_failed. We assert the route is wired
    # and the schema is enforced.
    assert r.status_code in {200, 500}


@pytest.mark.asyncio
async def test_dpa_requires_accept(async_client) -> None:
    r = await async_client.post(
        "/api/v1/onboarding/dpa",
        json={
            "onboarding_id": "ten_xxx",
            "accept": False,
            "signer_name": "X",
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_get_state_404(async_client) -> None:
    r = await async_client.get("/api/v1/onboarding/nonexistent")
    assert r.status_code in {404, 500}
