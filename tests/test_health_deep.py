"""Tests for /health/deep + /healthz?deep=1 enrichment (W5.1).

Verifies the deep health endpoint surfaces:
  - postgres status (skip when no DATABASE_URL)
  - redis status + DLQ depths for the 4 production queues
  - sentry config validation (mirrors preflight R8 logic)
  - llm_providers list
"""
from __future__ import annotations

import pytest

from api.routers.health import _normalize_postgres_dsn_for_psycopg2


@pytest.mark.asyncio
async def test_health_deep_returns_status_and_checks(async_client):
    res = await async_client.get("/health/deep")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] in ("ok", "degraded", "down")
    assert "checks" in body
    # All five dependency categories represented (some may be skip)
    for key in ("postgres", "redis", "sentry", "llm_providers"):
        assert key in body["checks"], f"missing check: {key}"


@pytest.mark.asyncio
async def test_healthz_default_is_simple(async_client):
    res = await async_client.get("/healthz")
    assert res.status_code == 200
    body = res.json()
    assert body == {"status": "ok", "service": "dealix"}


@pytest.mark.asyncio
async def test_healthz_deep_query_returns_deep_payload(async_client):
    res = await async_client.get("/healthz?deep=1")
    assert res.status_code == 200
    body = res.json()
    # When ?deep=1, payload matches /health/deep shape
    assert "checks" in body
    assert "postgres" in body["checks"]
    assert "redis" in body["checks"]


@pytest.mark.asyncio
async def test_health_deep_sentry_check_with_no_dsn(async_client, monkeypatch):
    """If SENTRY_DSN is unset, sentry check should be 'skip' not 'fail'."""
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    res = await async_client.get("/health/deep")
    body = res.json()
    sentry = body["checks"]["sentry"]
    # skip when DSN unset, or skip when sentry_sdk not installed
    assert sentry["status"] in ("skip", "ok", "misconfigured")


def test_normalize_postgres_asyncpg_dsn_for_psycopg2():
    """Convert SQLAlchemy-style driver DSN to psycopg2-compatible DSN."""
    assert (
        _normalize_postgres_dsn_for_psycopg2(
            "postgresql+asyncpg://user:password@localhost:5432/ai_company"
        )
        == "postgresql://user:password@localhost:5432/ai_company"
    )
    assert (
        _normalize_postgres_dsn_for_psycopg2("postgresql://user:password@localhost:5432/ai_company")
        == "postgresql://user:password@localhost:5432/ai_company"
    )


@pytest.mark.asyncio
async def test_health_deep_dlq_only_when_redis_ok(async_client):
    """DLQ check appears only when Redis was reachable. Otherwise the key is
    absent (not failed-looking)."""
    res = await async_client.get("/health/deep")
    body = res.json()
    if body["checks"]["redis"]["status"] == "ok":
        assert "dlq" in body["checks"], "DLQ check expected when Redis is up"
        if body["checks"]["dlq"]["status"] in ("ok", "degraded"):
            depths = body["checks"]["dlq"]["depths"]
            for queue in ("webhooks", "outbound", "enrichment", "crm_sync"):
                assert queue in depths, f"missing DLQ queue: {queue}"
