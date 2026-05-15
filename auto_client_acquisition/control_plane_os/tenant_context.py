"""Tenant context helpers for enterprise control-plane modules."""

from __future__ import annotations

import os
from dataclasses import dataclass


_PRODUCTION_ENVS = {"production", "prod"}


def current_app_env() -> str:
    return (os.getenv("APP_ENV") or os.getenv("ENVIRONMENT") or "development").strip().lower()


def resolve_tenant_id(tenant_id: str | None, *, app_env: str | None = None) -> str:
    """Resolve tenant id with dev/test fallback and prod hard requirement."""
    env = (app_env or current_app_env()).strip().lower()
    normalized = (tenant_id or "").strip()
    if normalized:
        return normalized
    if env in _PRODUCTION_ENVS:
        raise ValueError("tenant_id is required in production")
    return "default"


@dataclass(frozen=True, slots=True)
class TenantContext:
    tenant_id: str


def context_for(tenant_id: str | None, *, app_env: str | None = None) -> TenantContext:
    return TenantContext(tenant_id=resolve_tenant_id(tenant_id, app_env=app_env))


__all__ = ["TenantContext", "context_for", "current_app_env", "resolve_tenant_id"]
