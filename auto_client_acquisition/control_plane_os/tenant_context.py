"""Tenant resolution helpers for control-plane endpoints and services."""

from __future__ import annotations

import os

DEFAULT_DEV_TENANT_ID = "default"


def require_tenant_id(tenant_id: str | None) -> str:
    """Resolve tenant context.

    Development/test accepts an implicit tenant to simplify local loops.
    Production requires explicit tenant_id.
    """
    normalized = (tenant_id or "").strip()
    app_env = os.getenv("APP_ENV", os.getenv("ENVIRONMENT", "development")).lower()
    if normalized:
        return normalized
    if app_env in {"development", "dev", "test", "testing"}:
        return DEFAULT_DEV_TENANT_ID
    raise ValueError("tenant_id is required in production")
