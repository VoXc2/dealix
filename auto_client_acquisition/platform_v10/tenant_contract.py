"""Tenant boundary contract — PDPL / multi-tenant readiness."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class TenantContext(BaseModel):
    """Resolved tenant for a single request or workflow run."""

    tenant_id: str = Field(..., min_length=1, max_length=128)
    source: str = Field(
        default="header",
        description="How tenant was resolved: jwt, header, api_key_prefix",
    )

    @field_validator("tenant_id")
    @classmethod
    def strip_tenant(cls, v: str) -> str:
        tid = v.strip()
        if not tid:
            raise ValueError("tenant_id cannot be empty")
        return tid


def assert_same_tenant(ctx: TenantContext, resource_tenant_id: str) -> None:
    """Raise if resource row does not belong to request tenant."""
    if resource_tenant_id != ctx.tenant_id:
        raise PermissionError("cross_tenant_access_denied")
