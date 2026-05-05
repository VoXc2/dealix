"""Build a chronological, PII-free event timeline for an account."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

from auto_client_acquisition.crm_v10.schemas import (
    Deal, Lead, ProofEventRef, ServiceSession,
)


def _ts(dt: datetime | None) -> str:
    return dt.isoformat() if dt is not None else ""


def build_timeline(
    account_id: str,
    leads: Iterable[Lead],
    deals: Iterable[Deal],
    service_sessions: Iterable[ServiceSession],
    proof_events: Iterable[ProofEventRef],
) -> list[dict[str, Any]]:
    """Return chronologically ordered events for ``account_id``.

    Each entry is a small typed dict with no PII — only id, type, stage
    (where applicable), and an ISO timestamp.
    """
    events: list[dict[str, Any]] = []

    for lead in leads:
        if lead.account_id != account_id:
            continue
        events.append({
            "kind": "lead_created", "id": lead.id, "stage": lead.stage,
            "source": lead.source, "at": _ts(lead.created_at),
            "_sort": lead.created_at,
        })

    for deal in deals:
        if deal.account_id != account_id:
            continue
        sort_key = (
            datetime.combine(deal.expected_close_date, datetime.min.time())
            if deal.expected_close_date is not None else datetime.min
        )
        events.append({
            "kind": "deal", "id": deal.id, "stage": deal.stage,
            "amount_sar": deal.amount_sar,
            "at": _ts(sort_key) if deal.expected_close_date else "",
            "_sort": sort_key,
        })

    for s in service_sessions:
        if s.account_id != account_id:
            continue
        sort_key = s.started_at or s.completed_at or datetime.min
        events.append({
            "kind": "service_session", "id": s.id, "service_id": s.service_id,
            "status": s.status, "at": _ts(s.started_at or s.completed_at),
            "_sort": sort_key,
        })

    for p in proof_events:
        if p.account_id != account_id:
            continue
        events.append({
            "kind": "proof_event", "id": p.id, "event_type": p.event_type,
            "at": _ts(p.created_at), "_sort": p.created_at,
        })

    def _key(ev: dict[str, Any]) -> tuple[int, str]:
        v = ev["_sort"]
        return (0, v.isoformat()) if isinstance(v, datetime) else (1, str(v))

    events.sort(key=_key)
    for ev in events:
        ev.pop("_sort", None)
    return events


__all__ = ["build_timeline"]
