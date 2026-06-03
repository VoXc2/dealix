"""Aggregate proof events into anonymized counts."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.proof_ledger import export_redacted


def proof_summary(
    *,
    ledger: Any | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Return anonymized counts per event_type and per customer_handle.

    PII is removed via ``export_redacted`` — customer_handle becomes
    ``<anonymized>`` whenever the event lacks consent_for_publication.
    Pure aggregation: never persists, never sends.
    """
    try:
        export = export_redacted(limit=limit, ledger=ledger)
    except Exception:
        return {
            "total": 0,
            "by_type": {},
            "by_customer": {},
            "error": "ledger_unavailable",
        }

    events = export.get("events") or []
    by_type: dict[str, int] = {}
    by_customer: dict[str, int] = {}
    for ev in events:
        if not isinstance(ev, dict):
            continue
        ev_type = str(ev.get("event_type") or "unknown")
        by_type[ev_type] = by_type.get(ev_type, 0) + 1
        handle = str(ev.get("customer_handle") or "<anonymized>")
        by_customer[handle] = by_customer.get(handle, 0) + 1

    return {
        "total": len(events),
        "by_type": by_type,
        "by_customer": by_customer,
    }
