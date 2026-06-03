"""Row-level security policy contract (Postgres RLS pattern reference)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RLSPolicy(BaseModel):
    """Declarative RLS expectation — enforcement lives in DB migration later."""

    table_name: str = Field(..., min_length=1)
    tenant_column: str = Field(default="tenant_id")
    enforce_in_app_layer: bool = Field(
        default=True,
        description="Until DB RLS exists, app must filter by tenant_column",
    )


def row_tenant_matches(
    policy: RLSPolicy,
    row_tenant_id: str | None,
    ctx_tenant_id: str,
) -> bool:
    """App-layer check mirroring future USING (tenant_id = current_tenant)."""
    if not policy.enforce_in_app_layer:
        return True
    if row_tenant_id is None:
        return False
    return row_tenant_id == ctx_tenant_id
