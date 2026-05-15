"""Tenant context helpers for enterprise control-plane operations."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TenantContext:
    tenant_id: str
    actor: str = "system"
    correlation_id: str = ""


def ensure_tenant_id(tenant_id: str) -> str:
    """Enforce tenant id for production, allow default in dev/test."""
    normalized = (tenant_id or "").strip()
    if normalized:
        return normalized
    app_env = os.getenv("APP_ENV", "development").strip().lower()
    if app_env in {"development", "dev", "test", "testing"}:
        return "default"
    raise ValueError("tenant_id is required in non-development environments")


__all__ = ["TenantContext", "ensure_tenant_id"]
