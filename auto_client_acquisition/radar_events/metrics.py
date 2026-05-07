"""Metrics aggregation over radar events."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.radar_events.event_store import summary_metrics


def funnel_health() -> dict[str, Any]:
    """Quick funnel status from event counts."""
    s = summary_metrics()
    by = s.get("by_event_type", {})
    return {
        "lead_to_qualified_ratio": _ratio(by.get("lead_scored", 0), by.get("lead_created", 0)),
        "approval_acceptance_ratio": _ratio(by.get("approval_accepted", 0), by.get("approval_requested", 0)),
        "payment_to_proof_ratio": _ratio(by.get("proof_event_created", 0), by.get("payment_confirmed", 0)),
        "unsafe_action_blocked_count": s.get("unsafe_action_blocked_count", 0),
        "source": "radar_events.event_store",
    }


def _ratio(numerator: int, denominator: int) -> float | None:
    if not denominator:
        return None
    return round(numerator / denominator, 3)
