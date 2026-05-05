"""Evidence summary — counts only, never PII."""
from __future__ import annotations

from typing import Any


def summarize_evidence(limit: int = 10) -> dict[str, Any]:
    """Return counts by event_type + by month. Never includes raw payloads."""
    try:
        from auto_client_acquisition.proof_ledger import get_default_ledger
        ledger = get_default_ledger()
        events = ledger.list_events(limit=limit)
    except Exception:  # noqa: BLE001
        return {
            "total": 0,
            "by_type": {},
            "by_month": {},
            "note": "proof_ledger_unavailable",
        }

    by_type: dict[str, int] = {}
    by_month: dict[str, int] = {}
    for ev in events:
        t = str(getattr(ev, "event_type", "unknown"))
        by_type[t] = by_type.get(t, 0) + 1
        try:
            month = ev.created_at.strftime("%Y-%m")
        except Exception:  # noqa: BLE001
            month = "unknown"
        by_month[month] = by_month.get(month, 0) + 1

    return {
        "total": len(events),
        "by_type": by_type,
        "by_month": by_month,
        "note": "counts_only_no_pii",
    }
