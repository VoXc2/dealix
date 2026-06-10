"""Session scope — prevents cross-tenant / cross-client context bleed."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentSessionScope:
    session_id: str
    tenant_id: str
    client_id: str


def session_allows_context(*, session: AgentSessionScope, context_tenant: str, context_client: str) -> bool:
    return session.tenant_id == context_tenant and session.client_id == context_client


__all__ = ["AgentSessionScope", "session_allows_context"]
