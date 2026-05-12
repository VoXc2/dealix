"""Integration tests for api/routers/saudi_gov.py."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_tenders_503_without_key(async_client, monkeypatch) -> None:
    monkeypatch.delenv("ETIMAD_API_KEY", raising=False)
    r = await async_client.get("/api/v1/saudi-gov/tenders")
    assert r.status_code == 503
    assert r.json()["detail"] == "etimad_not_configured"


@pytest.mark.asyncio
async def test_maroof_503_without_key(async_client, monkeypatch) -> None:
    monkeypatch.delenv("MAROOF_API_KEY", raising=False)
    r = await async_client.get("/api/v1/saudi-gov/maroof/1010101010")
    assert r.status_code == 503
    assert r.json()["detail"] == "maroof_not_configured"


@pytest.mark.asyncio
async def test_judicial_503_without_key(async_client, monkeypatch) -> None:
    monkeypatch.delenv("NAJIZ_API_KEY", raising=False)
    r = await async_client.get("/api/v1/saudi-gov/judicial/1010101010")
    assert r.status_code == 503
    assert r.json()["detail"] == "najiz_not_configured"


@pytest.mark.asyncio
async def test_najm_503_without_key(async_client, monkeypatch) -> None:
    monkeypatch.delenv("NAJM_API_KEY", raising=False)
    r = await async_client.get("/api/v1/saudi-gov/najm/VIN12345")
    assert r.status_code == 503
    assert r.json()["detail"] == "najm_not_configured"


@pytest.mark.asyncio
async def test_tadawul_503_without_key(async_client, monkeypatch) -> None:
    monkeypatch.delenv("TADAWUL_API_KEY", raising=False)
    r = await async_client.get("/api/v1/saudi-gov/tadawul/2222")
    assert r.status_code == 503
    assert r.json()["detail"] == "tadawul_not_configured"


@pytest.mark.asyncio
async def test_misa_503_without_key(async_client, monkeypatch) -> None:
    monkeypatch.delenv("MISA_API_KEY", raising=False)
    r = await async_client.get("/api/v1/saudi-gov/misa/MISA123456")
    assert r.status_code == 503
    assert r.json()["detail"] == "misa_not_configured"


@pytest.mark.asyncio
async def test_tenders_filter_params_accepted(async_client, monkeypatch) -> None:
    """Param validation must run before the 503 check so we know the
    filter contract is enforced — but lacking a key, still 503."""
    monkeypatch.delenv("ETIMAD_API_KEY", raising=False)
    r = await async_client.get(
        "/api/v1/saudi-gov/tenders?sector=construction&region=Riyadh&page=1&page_size=10"
    )
    assert r.status_code == 503


@pytest.mark.asyncio
async def test_tenders_rejects_oversize_page(async_client, monkeypatch) -> None:
    monkeypatch.delenv("ETIMAD_API_KEY", raising=False)
    r = await async_client.get("/api/v1/saudi-gov/tenders?page_size=999")
    # FastAPI validates ge/le before the route body runs.
    assert r.status_code == 422
