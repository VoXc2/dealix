"""Data boundary — tenant/client scoping for reads."""

from __future__ import annotations


def data_boundary_ok(*, resource_tenant: str, session_tenant: str, resource_client: str, session_client: str) -> bool:
    return resource_tenant == session_tenant and resource_client == session_client


__all__ = ["data_boundary_ok"]
