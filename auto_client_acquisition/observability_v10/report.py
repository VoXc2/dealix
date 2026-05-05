"""Roll-up report over collected traces."""
from __future__ import annotations

from auto_client_acquisition.observability_v10.schemas import TraceRecordV10


def summarize_traces(traces: list[TraceRecordV10]) -> dict:
    """Return counts by ``action_mode`` + total cost + average latency."""
    try:
        n = len(traces or [])
        if n == 0:
            return {
                "trace_count": 0,
                "total_cost_usd": 0.0,
                "avg_latency_ms": 0.0,
                "by_action_mode": {},
                "by_risk_level": {},
            }
        total_cost = 0.0
        total_latency = 0.0
        by_mode: dict[str, int] = {}
        by_risk: dict[str, int] = {}
        for t in traces:
            total_cost += float(t.estimated_cost_usd or 0.0)
            total_latency += float(t.latency_ms or 0.0)
            mode = str(t.action_mode or "unknown")
            risk = str(t.risk_level or "unknown")
            by_mode[mode] = by_mode.get(mode, 0) + 1
            by_risk[risk] = by_risk.get(risk, 0) + 1
        return {
            "trace_count": n,
            "total_cost_usd": round(total_cost, 6),
            "avg_latency_ms": round(total_latency / n, 3),
            "by_action_mode": by_mode,
            "by_risk_level": by_risk,
        }
    except Exception:  # noqa: BLE001 - defensive default
        return {
            "trace_count": 0,
            "total_cost_usd": 0.0,
            "avg_latency_ms": 0.0,
            "by_action_mode": {},
            "by_risk_level": {},
        }
