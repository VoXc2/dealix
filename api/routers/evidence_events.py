"""Evidence Events ledger — append-only API.

POST + GET only. There is intentionally no PATCH or DELETE — the
Evidence Events ledger is append-only by construction. ``source`` is
mandatory; ``summary`` is PII-redacted before any write.

Endpoints under /api/v1/evidence-events/:
    GET  /status   — module health + guardrails
    POST /         — append one EvidenceEvent (returns the stored, redacted record)
    GET  /         — list recent events, newest first
    GET  /{id}     — fetch one event by id
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.evidence_control_plane_os.evidence_ledger import (
    EvidenceEvent,
    get_default_evidence_ledger,
)

router = APIRouter(prefix="/api/v1/evidence-events", tags=["evidence-events"])


@router.get("/status")
async def status() -> dict[str, Any]:
    """Module health + active guardrails."""
    return {
        "module": "evidence_ledger",
        "guardrails": {
            "append_only": True,
            "no_update_or_delete": True,
            "source_mandatory": True,
            "pii_redacted_before_persistence": True,
            "hmac_signed": True,
        },
        "governance_decision": "allow",
    }


@router.post("")
async def append_event(payload: dict = Body(...)) -> dict[str, Any]:
    """Append one EvidenceEvent. Returns the stored (redacted) record."""
    try:
        event = EvidenceEvent.model_validate(payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=422, detail=f"invalid evidence event: {exc}") from exc
    stored = get_default_evidence_ledger().append(event)
    body = stored.model_dump(mode="json")
    body["governance_decision"] = "allow"
    return body


@router.get("")
async def list_events(
    event_type: str | None = None,
    source: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """List recent evidence events, newest first."""
    rows = get_default_evidence_ledger().list_events(
        event_type=event_type,
        source=source,
        limit=max(1, min(int(limit), 1000)),
    )
    return {
        "count": len(rows),
        "events": [r.model_dump(mode="json") for r in rows],
        "governance_decision": "allow",
    }


@router.get("/{event_id}")
async def get_event(event_id: str) -> dict[str, Any]:
    """Fetch one evidence event by id."""
    event = get_default_evidence_ledger().get(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"evidence event {event_id!r} not found")
    body = event.model_dump(mode="json")
    body["governance_decision"] = "allow"
    return body
