"""
Sector benchmarks endpoint — Tinybird-backed when configured, otherwise
falls back to the existing `customer_success/benchmarks.py` aggregates.

Endpoint:
    GET /api/v1/benchmarks/sector
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request

from core.logging import get_logger
from dealix.integrations.tinybird_client import is_configured, query_pipe

router = APIRouter(prefix="/api/v1/benchmarks", tags=["benchmarks"])
log = get_logger(__name__)


@router.get("/sector")
async def sector_benchmarks(request: Request) -> dict[str, Any]:
    tenant_id = getattr(request.state, "tenant_id", None)
    if is_configured():
        res = await query_pipe(
            "sector_benchmarks", {"tenant_id": tenant_id or ""}
        )
        if res.ok:
            return {"source": "tinybird", "rows": res.rows}
    # Fallback: existing internal aggregator.
    try:
        from auto_client_acquisition.customer_success.benchmarks import (
            saudi_b2b_pulse,
        )

        pulse = saudi_b2b_pulse(sector_data={})
        rows = []
        for s in getattr(pulse, "sectors", []) or []:
            rows.append(
                {
                    "sector": s.get("sector"),
                    "metric": s.get("metric") or "reply_rate",
                    "customer_value": s.get("customer_value"),
                    "p50": s.get("p50"),
                    "p75": s.get("p75"),
                    "p90": s.get("p90"),
                    "unit": s.get("unit") or "%",
                }
            )
        return {"source": "internal_aggregator", "rows": rows}
    except Exception:
        log.exception("benchmark_fallback_failed")
        return {"source": "empty", "rows": []}
