"""Admin endpoints — cost dashboard, cache stats."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Query

from dealix.caching.cache_stats import get_global_stats
from dealix.observability.cost_tracker import CostTracker

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

_tracker = CostTracker()


@router.get("/costs")
async def costs(
    window_hours: int = Query(24, ge=1, le=720),
    group_by: str = Query("model", regex="^(model|provider|task)$"),
) -> dict[str, Any]:
    """Aggregate LLM spend over the last N hours."""
    since = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    entries = _tracker.query_window(since=since)

    total_usd = sum(e.cost_usd for e in entries)
    total_in = sum(e.input_tokens for e in entries)
    total_out = sum(e.output_tokens for e in entries)
    total_cached = sum(getattr(e, "cached_tokens", 0) for e in entries)

    groups: dict[str, dict[str, float]] = {}
    for e in entries:
        key = getattr(e, group_by, "unknown") or "unknown"
        g = groups.setdefault(str(key), {"usd": 0.0, "calls": 0, "in": 0, "out": 0})
        g["usd"] += e.cost_usd
        g["calls"] += 1
        g["in"] += e.input_tokens
        g["out"] += e.output_tokens

    return {
        "window_hours": window_hours,
        "group_by": group_by,
        "totals": {
            "usd": round(total_usd, 4),
            "calls": len(entries),
            "input_tokens": total_in,
            "output_tokens": total_out,
            "cached_tokens": total_cached,
            "cache_hit_ratio": round(total_cached / total_in, 3) if total_in else 0.0,
        },
        "by_group": {k: {**v, "usd": round(v["usd"], 4)} for k, v in groups.items()},
    }


@router.get("/cache/stats")
async def cache_stats() -> dict[str, Any]:
    """Semantic cache hit/miss stats."""
    return get_global_stats()
