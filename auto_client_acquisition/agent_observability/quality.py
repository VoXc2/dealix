"""Quality assessment helpers for agent traces."""
from __future__ import annotations

from typing import Any


def quality_summary(traces: list[Any]) -> dict[str, Any]:
    """Aggregate quality signals across recent traces."""
    if not traces:
        return {"count": 0, "approval_acceptance_rate": None, "degraded_rate": 0.0}
    approved = sum(1 for t in traces if t.approval_status == "approved")
    degraded = sum(1 for t in traces if t.degraded)
    return {
        "count": len(traces),
        "approval_acceptance_rate": round(approved / len(traces), 3),
        "degraded_rate": round(degraded / len(traces), 3),
    }
