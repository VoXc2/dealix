"""Auth principal + coarse permissions (RBAC bridge)."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Permission(StrEnum):
    READ_PIPELINE = "read_pipeline"
    WRITE_PIPELINE = "write_pipeline"
    APPROVE_EXTERNAL = "approve_external"
    ADMIN_TENANT = "admin_tenant"


class AuthPrincipal(BaseModel):
    """Who is acting — tie to JWT subject in real deploy."""

    subject: str = Field(..., min_length=1)
    tenant_id: str = Field(..., min_length=1)
    roles: tuple[str, ...] = Field(default=())


def require_permission(principal: AuthPrincipal, need: Permission) -> None:
    """Placeholder: map roles→permissions in a later policy module."""
    if need.value not in principal.roles and "*" not in principal.roles:
        raise PermissionError(f"missing_permission:{need.value}")
