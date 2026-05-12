"""Tests for tenant theming endpoints (W7.5).

Focus on input validation (XSS / CSS injection prevention) since the
GET endpoint embeds tenant strings inside a CSS <style>. The DB
integration paths gracefully degrade when DB is absent.
"""
from __future__ import annotations

import pytest


# ── GET /api/v1/tenants/{handle}/theme.css ────────────────────────

@pytest.mark.asyncio
async def test_theme_css_returns_default_for_unknown_handle(async_client):
    """An unknown tenant returns a default :root block, not 404 —
    so tenant-scoped pages degrade gracefully if the slug is misconfigured."""
    res = await async_client.get("/api/v1/tenants/unknown_tenant_xyz/theme.css")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("text/css")
    assert ":root" in res.text
    # No tenant overrides in the default — just empty :root block
    assert "Dealix defaults apply" in res.text or "--dealix-" not in res.text


@pytest.mark.asyncio
async def test_theme_css_rejects_invalid_slug(async_client):
    """Path regex rejects slugs with hyphens or uppercase."""
    res = await async_client.get("/api/v1/tenants/Bad-Slug/theme.css")
    assert res.status_code == 422


# ── POST /api/v1/admin/tenants/{handle}/theme ─────────────────────

@pytest.mark.asyncio
async def test_theme_update_requires_admin_token(async_client):
    """POST without Bearer token → 401 or 503 (if admin not configured)."""
    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={"brand_primary": "#ff0000"},
    )
    # 401 if ADMIN_API_KEYS is set without our key; 503 if not configured
    assert res.status_code in (401, 503)


@pytest.mark.asyncio
async def test_theme_update_rejects_invalid_color(async_client, monkeypatch):
    """Color validation rejects CSS injection attempts."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_token_validation")
    headers = {"Authorization": "Bearer test_admin_token_validation"}

    # Try a CSS injection payload
    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={"brand_primary": "red; } body { display: none; }"},
        headers=headers,
    )
    assert res.status_code == 400
    assert "invalid color" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_theme_update_rejects_data_url_logo(async_client, monkeypatch):
    """Data URLs are blocked — could embed inline scripts/XSS in some browsers."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_url_validation")
    headers = {"Authorization": "Bearer test_admin_url_validation"}

    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={"logo_url": "data:text/html,<script>alert(1)</script>"},
        headers=headers,
    )
    assert res.status_code == 400
    assert "https://" in res.json()["detail"] or "invalid" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_theme_update_rejects_javascript_url(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_js_url")
    headers = {"Authorization": "Bearer test_admin_js_url"}

    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={"favicon_url": "javascript:alert(1)"},
        headers=headers,
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_theme_update_rejects_injection_in_font_name(async_client, monkeypatch):
    """Font name with semicolons would break out of the CSS string."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_font_injection")
    headers = {"Authorization": "Bearer test_admin_font_injection"}

    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={"font_english": "Arial\"; body { display:none; } \""},
        headers=headers,
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_theme_update_accepts_valid_hex_color(async_client, monkeypatch):
    """Valid 6-digit hex passes validation. Reaches DB layer — may 404 if
    tenant doesn't exist, 503 if DB unavailable. Either way, NOT a 400."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_valid_color")
    headers = {"Authorization": "Bearer test_admin_valid_color"}

    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={"brand_primary": "#0066cc"},
        headers=headers,
    )
    # Color valid → past validation → DB layer reached
    assert res.status_code != 400


@pytest.mark.asyncio
async def test_theme_update_accepts_rgb_color(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_rgb")
    headers = {"Authorization": "Bearer test_admin_rgb"}

    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={"brand_accent": "rgb(15, 23, 42)"},
        headers=headers,
    )
    assert res.status_code != 400


@pytest.mark.asyncio
async def test_theme_update_accepts_valid_https_url(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_url")
    headers = {"Authorization": "Bearer test_admin_url"}

    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={"logo_url": "https://cdn.partner.com/logo.png"},
        headers=headers,
    )
    assert res.status_code != 400


@pytest.mark.asyncio
async def test_theme_update_rejects_empty_body(async_client, monkeypatch):
    """No fields set returns no_changes (200), not 400."""
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_noop")
    headers = {"Authorization": "Bearer test_admin_noop"}

    res = await async_client.post(
        "/api/v1/admin/tenants/acme_saas/theme",
        json={},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json().get("status") == "no_changes"
