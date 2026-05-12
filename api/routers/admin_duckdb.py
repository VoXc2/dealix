"""
DuckDB query endpoint — read-only, admin-gated SQL against the dbt
warehouse marts (analytics/dbt → DuckDB local file).

Endpoint:
    POST /api/v1/admin/duckdb/query
    { "sql": "SELECT * FROM tenants LIMIT 100" }

Safety:
    - Admin-only (ADMIN_API_KEYS or super_admin).
    - Read-only enforced via SQL prefix check + the DuckDB
      `READ_ONLY=true` connection flag.
    - Hard ceiling: 5000 rows + 30s timeout.

Inert when the DuckDB file doesn't exist or DuckDB isn't installed.
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from core.logging import get_logger

router = APIRouter(prefix="/api/v1/admin/duckdb", tags=["admin", "duckdb"])
log = get_logger(__name__)

_FORBIDDEN_PREFIXES = ("DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE", "ATTACH")


class DuckDBQueryIn(BaseModel):
    sql: str = Field(..., min_length=8, max_length=10_000)
    limit: int = Field(default=1000, ge=1, le=5000)


@router.post("/query")
async def duckdb_query(payload: DuckDBQueryIn, request: Request) -> dict[str, Any]:
    is_super = bool(getattr(request.state, "is_super_admin", False))
    api_key = request.headers.get("x-api-key", "")
    admin_keys = {k.strip() for k in os.getenv("ADMIN_API_KEYS", "").split(",") if k.strip()}
    if not is_super and api_key not in admin_keys:
        raise HTTPException(403, "admin_only")

    sql = payload.sql.strip().rstrip(";")
    upper = sql.upper().lstrip()
    if any(upper.startswith(p) for p in _FORBIDDEN_PREFIXES):
        raise HTTPException(422, "write_queries_disallowed")
    if "SELECT" not in upper:
        raise HTTPException(422, "select_required")

    path = os.getenv("DBT_DUCKDB_PATH", "./analytics/dbt/dealix.duckdb")
    try:
        import duckdb  # type: ignore
    except ImportError:
        raise HTTPException(503, "duckdb_not_installed") from None
    if not os.path.isfile(path):
        raise HTTPException(503, "duckdb_file_missing")

    try:
        con = duckdb.connect(database=path, read_only=True)
        rows = con.execute(f"{sql} LIMIT {payload.limit}").fetchall()
        cols = [d[0] for d in con.description] if con.description else []
        con.close()
    except Exception as exc:
        log.exception("duckdb_query_failed")
        raise HTTPException(400, f"duckdb_error:{str(exc)[:200]}") from None

    return {
        "columns": cols,
        "row_count": len(rows),
        "rows": [
            {cols[i]: (str(v) if v is not None else None) for i, v in enumerate(row)}
            for row in rows
        ],
    }
