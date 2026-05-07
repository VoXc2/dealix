"""Customer Brain snapshot builder.

Composes a CustomerBrainSnapshot for one customer from:
  - leadops_spine.list_records      → past leads / channels / sectors
  - approval_center.list_pending    → open decisions
  - proof_ledger (best-effort)      → proof_history
  - market_intelligence (best-effort) → growth_opportunities

All sources are best-effort; missing modules degrade gracefully
(snapshot is still returned with empty lists for that section).

Persistence: in-memory cache + JSONL backup (per Article 11).
"""
from __future__ import annotations

import json
import os
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import CustomerBrainSnapshot

_JSONL_PATH = os.path.join("data", "customer_brain_snapshots.jsonl")
_CACHE: dict[str, CustomerBrainSnapshot] = {}


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(snap: CustomerBrainSnapshot) -> None:
    _ensure_dir()
    _CACHE[snap.customer_handle] = snap
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(snap.model_dump_json() + "\n")


def _service_history(customer_handle: str) -> list[dict[str, Any]]:
    """Pull past leadops records + journey state for this customer."""
    history: list[dict[str, Any]] = []
    try:
        from auto_client_acquisition.leadops_spine import list_records
        for rec in list_records(limit=100):
            if rec.customer_handle == customer_handle:
                history.append({
                    "type": "lead",
                    "leadops_id": rec.leadops_id,
                    "source": rec.source,
                    "compliance_status": rec.compliance_status,
                    "score": rec.score,
                    "at": rec.created_at.isoformat(),
                })
    except Exception:
        pass
    return history


def _proof_history(customer_handle: str) -> list[dict[str, Any]]:
    """Pull proof events for this customer (best-effort)."""
    try:
        from auto_client_acquisition.proof_ledger.file_backend import list_events  # type: ignore
        events = list_events(customer_handle=customer_handle, limit=50)
        return [{
            "event_type": e.event_type if hasattr(e, "event_type") else e.get("event_type"),
            "summary_ar": e.summary_ar if hasattr(e, "summary_ar") else e.get("summary_ar", ""),
            "at": (
                e.created_at.isoformat() if hasattr(e, "created_at")
                else e.get("created_at", "")
            ),
        } for e in events]
    except Exception:
        return []


def _open_decisions(customer_handle: str) -> list[dict[str, Any]]:
    """Pull pending approvals related to this customer."""
    try:
        from auto_client_acquisition.approval_center import approval_store
        pending = approval_store.list_pending()
        out: list[dict[str, Any]] = []
        for ap in pending:
            # ApprovalRequest doesn't have customer_handle directly — match
            # via proof_impact field which encodes "leadops:<id>" or
            # "session:<id>" pointers, OR via summary text.
            proof_impact = getattr(ap, "proof_impact", "") or ""
            summary_ar = getattr(ap, "summary_ar", "") or ""
            if customer_handle in proof_impact or customer_handle in summary_ar:
                out.append({
                    "approval_id": ap.approval_id,
                    "object_type": ap.object_type,
                    "action_type": ap.action_type,
                    "action_mode": ap.action_mode,
                    "risk_level": ap.risk_level,
                })
        return out[:20]
    except Exception:
        return []


def _support_context(customer_handle: str) -> dict[str, Any]:
    """Pull support tickets summary (best-effort)."""
    return {
        "open_tickets_count": 0,
        "p0_count": 0,
        "last_ticket_at": None,
        "source": "support_os (placeholder until Phase 7 webhook)",
    }


def _growth_opportunities(sector: str | None) -> list[dict[str, Any]]:
    """Pull top-fit opportunities for the customer's sector (best-effort)."""
    if not sector:
        return []
    try:
        from auto_client_acquisition.market_intelligence.signal_detectors import (
            SIGNAL_TYPES,
        )
        # Surface the top 3 signal types as suggested watchlist items
        return [
            {"signal_type": t, "watch": True, "reason": f"sector_default:{sector}"}
            for t in SIGNAL_TYPES[:3]
        ]
    except Exception:
        return []


def build_snapshot(*, customer_handle: str) -> CustomerBrainSnapshot:
    """Build (or rebuild) the snapshot. Persists to JSONL + cache."""
    service_hist = _service_history(customer_handle)
    proof_hist = _proof_history(customer_handle)
    open_dec = _open_decisions(customer_handle)
    support = _support_context(customer_handle)

    # Derive sector + channels from past leadops records
    sector = None
    channels: list[str] = []
    if service_hist:
        for h in service_hist:
            # Score has no sector; we'd need to look up the full record.
            # Fall back to the first record's stored data.
            pass
    # Better: read from JSONL directly if cache empty
    try:
        from auto_client_acquisition.leadops_spine import list_records
        for rec in list_records(limit=100):
            if rec.customer_handle == customer_handle:
                sector = sector or (rec.normalized.get("sector") if rec.normalized else None)
                if rec.offer_route and rec.offer_route.get("channel") not in channels:
                    channels.append(rec.offer_route["channel"])
    except Exception:
        pass

    snap = CustomerBrainSnapshot(
        customer_handle=customer_handle,
        profile={"sector": sector, "tier": "unknown"},
        icp={},
        offers=[],
        channels=channels or [],
        tone_of_voice={"primary_language": "ar", "secondary_language": "en"},
        compliance_constraints=["pdpl_default", "no_live_send", "no_cold_whatsapp"],
        service_history=service_hist,
        proof_history=proof_hist,
        open_decisions=open_dec,
        support_context=support,
        growth_opportunities=_growth_opportunities(sector),
        source_modules=[
            "leadops_spine",
            "approval_center",
            "proof_ledger",
            "support_os",
            "market_intelligence",
        ],
    )
    _persist(snap)
    return snap


def get_snapshot(*, customer_handle: str) -> CustomerBrainSnapshot | None:
    """Cached fetch — returns None if not yet built."""
    return _CACHE.get(customer_handle)


def list_known_customers() -> list[str]:
    return sorted(_CACHE.keys())
