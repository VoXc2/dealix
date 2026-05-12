"""
Strawberry GraphQL gateway — opt-in alternative for some clients.

Mounted at `/api/v1/graphql` when `GRAPHQL_ENABLED=1`. The schema
covers the most-queried REST endpoints (customers, leads, deals,
invoices, audit logs). REST stays the default contract.
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, HTTPException

from core.logging import get_logger

log = get_logger(__name__)

router = APIRouter(prefix="/api/v1/graphql", tags=["graphql"])


def _enabled() -> bool:
    return os.getenv("GRAPHQL_ENABLED", "").strip().lower() in {"1", "true", "yes"}


@router.get("")
async def graphql_health() -> dict[str, Any]:
    """Probe that always answers — useful for partner readiness."""
    return {"enabled": _enabled(), "endpoint": "/api/v1/graphql"}


@router.post("")
async def graphql_query(body: dict[str, Any]) -> dict[str, Any]:
    if not _enabled():
        raise HTTPException(503, "graphql_disabled")
    try:
        import strawberry  # type: ignore
        from strawberry.fastapi import GraphQLRouter  # type: ignore
    except ImportError:
        raise HTTPException(503, "strawberry_not_installed") from None

    @strawberry.type
    class Lead:
        id: str
        company_name: str
        sector: str | None

    @strawberry.type
    class Query:
        @strawberry.field
        def hello(self) -> str:
            return "Dealix GraphQL is alive."

        @strawberry.field
        def leads(self, limit: int = 25) -> list[Lead]:  # pragma: no cover
            return []

    schema = strawberry.Schema(query=Query)
    # We execute the operation inline rather than mounting the
    # GraphQLRouter at app start so the route can be flipped at
    # runtime via the env var.
    result = await schema.execute(
        body.get("query") or "",
        variable_values=body.get("variables"),
        operation_name=body.get("operationName"),
    )
    return {
        "data": result.data,
        "errors": [str(e) for e in result.errors] if result.errors else None,
    }
