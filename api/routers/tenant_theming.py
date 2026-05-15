"""Tenant theming endpoints (W7.5).

Two public-facing endpoints:

  GET  /api/v1/tenants/{handle}/theme.css
       Returns a <style>:root{...}</style>-style CSS block with the tenant's
       overrides. Designed to be included server-side BEFORE the main
       theme.css link so CSS variable cascade kicks in.

  POST /api/v1/admin/tenants/{handle}/theme
       Admin-only. Updates the tenant's theme record. Validates every
       color and URL to prevent CSS injection / XSS via theme fields.

Security:
  - Colors validated against strict regex (hex 3/4/6/8, rgb(), hsl(),
    or named colors from a closed allowlist).
  - URLs validated to be https:// only (no data:, javascript:, file:).
  - All text fields escaped before embedding in <style>.
  - Admin endpoint requires ADMIN_API_KEYS header.

Wiring to W3.2:
  - landing/assets/css/theme.css defines CSS custom properties with
    Dealix defaults.
  - This router serves a small <style> that overrides those properties
    per tenant. Unset variables fall back to the defaults.

Wiring to W7.1:
  - Tenants must exist (created via scripts/create_tenant.py) before
    a theme can be assigned. 404 returned otherwise.
"""
from __future__ import annotations

import logging
import os
import re
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Path, Response
from pydantic import BaseModel, ConfigDict, Field

log = logging.getLogger(__name__)

router = APIRouter(tags=["tenant-theming"])

# ── Validators ─────────────────────────────────────────────────────

# Hex color: #RGB, #RGBA, #RRGGBB, #RRGGBBAA
_HEX_COLOR = re.compile(r"^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
# rgb(r, g, b) or rgba(r, g, b, a) — strict whitespace allowed
_RGB_COLOR = re.compile(
    r"^rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}(?:\s*,\s*(?:0|1|0?\.\d+))?\s*\)$"
)
# hsl(h, s%, l%) or hsla(h, s%, l%, a)
_HSL_COLOR = re.compile(
    r"^hsla?\(\s*\d{1,3}(?:\.\d+)?\s*,\s*\d{1,3}(?:\.\d+)?%\s*,\s*\d{1,3}(?:\.\d+)?%"
    r"(?:\s*,\s*(?:0|1|0?\.\d+))?\s*\)$"
)
# Font family name: letters, digits, spaces, hyphens, underscores only.
# Prevents CSS injection like "Arial; }; body { display:none"
_FONT_FAMILY = re.compile(r"^[A-Za-z][A-Za-z0-9 _\-]{0,126}$")
# Display name: same restrictions + Arabic Unicode block + parentheses/dot
_DISPLAY_NAME = re.compile(r"^[A-Za-z0-9 _\-.()؀-ۿ]{1,127}$")
# Custom domain: standard host pattern
_DOMAIN = re.compile(
    r"^(?=.{1,253}$)(?!-)(?:[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,63}$"
)


def _valid_color(value: str) -> bool:
    if not isinstance(value, str) or len(value) > 32:
        return False
    return bool(
        _HEX_COLOR.match(value) or _RGB_COLOR.match(value) or _HSL_COLOR.match(value)
    )


def _valid_https_url(value: str) -> bool:
    """Reject any URL that isn't https://. Blocks data:, javascript:, file:."""
    if not isinstance(value, str) or len(value) > 512:
        return False
    if not value.startswith("https://"):
        return False
    # No control chars or whitespace in URL
    return not bool(re.search(r"[\s<>\"\\'`]", value))


def _css_escape(value: str) -> str:
    """Escape a string for safe embedding inside a CSS string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "")


# ── Request schema (admin update) ─────────────────────────────────

class TenantThemeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    brand_primary: str | None = Field(default=None, max_length=32)
    brand_accent: str | None = Field(default=None, max_length=32)
    brand_muted: str | None = Field(default=None, max_length=32)
    brand_surface: str | None = Field(default=None, max_length=32)
    brand_bg: str | None = Field(default=None, max_length=32)
    font_arabic: str | None = Field(default=None, max_length=128)
    font_english: str | None = Field(default=None, max_length=128)
    logo_url: str | None = Field(default=None, max_length=512)
    favicon_url: str | None = Field(default=None, max_length=512)
    display_name: str | None = Field(default=None, max_length=128)
    custom_domain: str | None = Field(default=None, max_length=255)


# ── Admin: write theme ────────────────────────────────────────────

def _require_admin(authorization: str | None) -> None:
    """Reject if Authorization Bearer doesn't match one of ADMIN_API_KEYS."""
    allowed_keys = (os.environ.get("ADMIN_API_KEYS") or "").split(",")
    allowed_keys = [k.strip() for k in allowed_keys if k.strip()]
    if not allowed_keys:
        # Misconfigured prod = always reject; never allow open admin
        raise HTTPException(status_code=503, detail="admin not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing Bearer token")
    token = authorization[len("Bearer "):].strip()
    if token not in allowed_keys:
        raise HTTPException(status_code=403, detail="invalid admin key")


@router.post("/api/v1/admin/tenants/{handle}/theme")
async def update_tenant_theme(
    update: TenantThemeUpdate,
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    """Update or create a tenant's theme overrides.

    Color fields must be valid CSS color values (hex/rgb/hsl).
    URL fields must be https:// only.
    Font names use a strict regex preventing CSS injection.
    """
    _require_admin(authorization)

    fields_to_set: dict[str, Any] = {}

    # Validate colors
    for color_field in ("brand_primary", "brand_accent", "brand_muted", "brand_surface", "brand_bg"):
        value = getattr(update, color_field)
        if value is not None:
            if not _valid_color(value):
                raise HTTPException(
                    status_code=400,
                    detail=f"invalid color for {color_field}: must be hex/rgb/hsl",
                )
            fields_to_set[color_field] = value

    # Validate fonts
    for font_field in ("font_arabic", "font_english"):
        value = getattr(update, font_field)
        if value is not None:
            if not _FONT_FAMILY.match(value):
                raise HTTPException(
                    status_code=400,
                    detail=f"invalid {font_field}: letters/digits/spaces/hyphens only",
                )
            fields_to_set[font_field] = value

    # Validate URLs
    for url_field in ("logo_url", "favicon_url"):
        value = getattr(update, url_field)
        if value is not None:
            if value == "":  # explicit clear
                fields_to_set[url_field] = None
            elif not _valid_https_url(value):
                raise HTTPException(
                    status_code=400,
                    detail=f"invalid {url_field}: https:// only, no control chars",
                )
            else:
                fields_to_set[url_field] = value

    if update.display_name is not None:
        if not _DISPLAY_NAME.match(update.display_name):
            raise HTTPException(status_code=400, detail="invalid display_name")
        fields_to_set["display_name"] = update.display_name

    if update.custom_domain is not None:
        if update.custom_domain == "":
            fields_to_set["custom_domain"] = None
        elif not _DOMAIN.match(update.custom_domain):
            raise HTTPException(status_code=400, detail="invalid custom_domain")
        else:
            fields_to_set["custom_domain"] = update.custom_domain

    if not fields_to_set:
        return {"status": "no_changes", "handle": handle}

    # Persist (best-effort: gracefully degrade if DB unavailable)
    try:
        from sqlalchemy import select

        from db.models import TenantRecord, TenantThemeRecord
        from db.session import async_session_factory
    except Exception as exc:
        log.warning("tenant_theme_update_skipped_imports error=%s", exc)
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    try:
        async with async_session_factory()() as session:
            tenant = (
                await session.execute(select(TenantRecord).where(TenantRecord.slug == handle))
            ).scalar_one_or_none()
            if tenant is None:
                raise HTTPException(status_code=404, detail=f"tenant {handle!r} not found")

            existing = (
                await session.execute(
                    select(TenantThemeRecord).where(TenantThemeRecord.tenant_id == tenant.id)
                )
            ).scalar_one_or_none()

            if existing is None:
                new_theme = TenantThemeRecord(tenant_id=tenant.id, **fields_to_set)
                session.add(new_theme)
            else:
                for k, v in fields_to_set.items():
                    setattr(existing, k, v)

            await session.commit()
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001 — DB unreachable / not migrated
        log.warning("tenant_theme_update_db_unavailable error=%s", exc)
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    return {
        "status": "updated" if existing else "created",
        "handle": handle,
        "fields_set": list(fields_to_set.keys()),
    }


# ── Public: read theme.css ────────────────────────────────────────

@router.get("/api/v1/tenants/{handle}/theme.css")
async def get_tenant_theme_css(
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
) -> Response:
    """Return the tenant's CSS variable overrides as a `:root{...}` block.

    Cacheable at the CDN/edge for ~5 minutes — themes change rarely.

    Designed to be loaded BEFORE the global theme.css:
      <link rel="stylesheet" href="/api/v1/tenants/{handle}/theme.css">
      <link rel="stylesheet" href="/assets/css/theme.css">

    Unset variables fall through to Dealix defaults in theme.css.
    """
    css_default = (
        ":root {\n"
        "  /* No tenant theme configured — Dealix defaults apply. */\n"
        "}\n"
    )

    try:
        from sqlalchemy import select

        from db.models import TenantRecord, TenantThemeRecord
        from db.session import async_session_factory
    except Exception:
        return Response(content=css_default, media_type="text/css")

    try:
        async with async_session_factory()() as session:
            tenant = (
                await session.execute(
                    select(TenantRecord).where(TenantRecord.slug == handle)
                )
            ).scalar_one_or_none()
            if tenant is None:
                # 404 silently — return empty :root so tenant URLs degrade gracefully.
                return Response(content=css_default, media_type="text/css")

            theme = (
                await session.execute(
                    select(TenantThemeRecord).where(TenantThemeRecord.tenant_id == tenant.id)
                )
            ).scalar_one_or_none()
    except Exception as exc:
        log.debug("tenant_theme_read_skipped reason=%s", exc)
        return Response(content=css_default, media_type="text/css")

    if theme is None:
        return Response(content=css_default, media_type="text/css")

    # Build :root block — all values already validated on write
    lines = [":root {"]
    var_map = {
        "--dealix-brand-primary": theme.brand_primary,
        "--dealix-brand-accent": theme.brand_accent,
        "--dealix-brand-muted": theme.brand_muted,
        "--dealix-brand-surface": theme.brand_surface,
        "--dealix-brand-bg": theme.brand_bg,
        "--dealix-font-ar": f'"{_css_escape(theme.font_arabic)}", system-ui, sans-serif',
        "--dealix-font-en": f'"{_css_escape(theme.font_english)}", system-ui, sans-serif',
        "--dealix-tenant-name": f'"{_css_escape(theme.display_name)}"',
    }
    if theme.logo_url:
        var_map["--dealix-tenant-logo-url"] = f'url("{_css_escape(theme.logo_url)}")'
    if theme.favicon_url:
        var_map["--dealix-tenant-favicon-url"] = f'url("{_css_escape(theme.favicon_url)}")'

    for var, val in var_map.items():
        lines.append(f"  {var}: {val};")
    lines.append("}")

    headers = {"Cache-Control": "public, max-age=300"}  # 5-minute edge cache
    return Response(
        content="\n".join(lines) + "\n",
        media_type="text/css",
        headers=headers,
    )
