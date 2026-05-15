"""Cost summary — composes from llm_gateway_v10 if shipped."""
from __future__ import annotations

from typing import Any


def summarize_cost(period_days: int = 7) -> dict[str, Any]:
    """Return a USD cost summary for the last ``period_days`` days.

    Defensive: if ``llm_gateway_v10`` is not yet shipped, returns zeros
    plus a note. Never crashes.
    """
    period_days = max(1, int(period_days or 1))
    try:
        # Optional import — module ships in §S5 / Phase A.
        from auto_client_acquisition import llm_gateway_v10  # type: ignore[attr-defined]
    except Exception:
        return {
            "period_days": period_days,
            "total_usd": 0.0,
            "by_provider": {},
            "note": "no cost data yet",
        }

    try:
        if hasattr(llm_gateway_v10, "summarize_cost"):
            payload = llm_gateway_v10.summarize_cost(period_days=period_days)
            if isinstance(payload, dict):
                payload.setdefault("period_days", period_days)
                return payload
    except Exception:
        pass

    return {
        "period_days": period_days,
        "total_usd": 0.0,
        "by_provider": {},
        "note": "llm_gateway_v10 wired but summarize_cost not exposed",
    }
