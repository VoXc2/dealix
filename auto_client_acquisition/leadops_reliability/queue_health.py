"""Queue depth + age distribution."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.integration_upgrade import safe_call


def queue_health() -> dict[str, Any]:
    """Returns queue depth + age buckets."""
    return safe_call(
        name="queue_health",
        fn=_compute,
        fallback={
            "total": 0, "by_compliance_status": {}, "by_source": {},
            "oldest_at": None, "newest_at": None,
        },
    )


def _compute() -> dict[str, Any]:
    from auto_client_acquisition.leadops_spine import list_records
    records = list_records(limit=1000)

    by_compliance: dict[str, int] = {}
    by_source: dict[str, int] = {}
    timestamps: list[datetime] = []
    for r in records:
        by_compliance[r.compliance_status] = by_compliance.get(r.compliance_status, 0) + 1
        by_source[r.source] = by_source.get(r.source, 0) + 1
        timestamps.append(r.created_at)

    timestamps.sort()
    return {
        "total": len(records),
        "by_compliance_status": by_compliance,
        "by_source": by_source,
        "oldest_at": timestamps[0].isoformat() if timestamps else None,
        "newest_at": timestamps[-1].isoformat() if timestamps else None,
    }
