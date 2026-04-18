"""
Tests: Authentication
"""
from __future__ import annotations

import pytest
from conftest import auth


@pytest.mark.asyncio
async def test_health_no_auth(client):
    """Health endpoint requires no auth."""
    r = await client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["service"] == "dealix-dashboard-api"


@pytest.mark.asyncio
async def test_login_success(client):
    """Valid credentials return JWT."""
    r = await client.post("/api/v1/auth/login", json={
        "email": "user_a@test.com",
        "password": "testpass123"
    })
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "user_a@test.com"
    assert "tenant_id" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Wrong password returns 401."""
    r = await client.post("/api/v1/auth/login", json={
        "email": "user_a@test.com",
        "password": "wrong_password"
    })
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_user(client):
    """Unknown email returns 401."""
    r = await client.post("/api/v1/auth/login", json={
        "email": "nobody@test.com",
        "password": "anything"
    })
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_no_token(client):
    """Protected endpoint without token returns 401."""
    r = await client.get("/api/v1/leads")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_bad_token(client):
    """Protected endpoint with invalid token returns 401."""
    r = await client.get("/api/v1/leads", headers={"Authorization": "Bearer bad.token.here"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_trace_id_header(client):
    """Every response includes X-Trace-ID header."""
    r = await client.get("/api/v1/health")
    assert "x-trace-id" in r.headers
    assert len(r.headers["x-trace-id"]) > 0
