"""Evidence Ledger — read-only HTTP surface over the append-only evidence store.

There is intentionally no POST/PUT/PATCH/DELETE here: evidence is written
only by the internal ``record_evidence_event`` helper called from service
code. The ``test_no_evidence_mutation`` guard asserts this stays true.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from auto_client_acquisition.evidence_control_plane_os.event_store import (
    get_default_evidence_ledger,
    list_evidence_events,
)

router = APIRouter(prefix="/api/v1/evidence", tags=["evidence"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "evidence_ledger",
        "backend": "file_jsonl",
        "append_only": True,
        "guardrails": {
            "no_update_path": True,
            "no_delete_path": True,
            "pii_redacted_before_persistence": True,
        },
    }


@router.get("")
async def list_events(
    entity_type: str | None = None,
    entity_id: str | None = None,
    event_type: str | None = None,
    tenant_id: str | None = None,
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    """List evidence events, newest-first, filtered by the given criteria."""
    rows = list_evidence_events(
        entity_type=entity_type,
        entity_id=entity_id,
        event_type=event_type,
        tenant_id=tenant_id,
        limit=limit,
    )
    return {"count": len(rows), "events": [r.model_dump(mode="json") for r in rows]}


@router.get("/{event_id}")
async def get_event(event_id: str) -> dict:
    ev = get_default_evidence_ledger().get(event_id)
    if ev is None:
        raise HTTPException(status_code=404, detail="evidence_event_not_found")
    return ev.model_dump(mode="json")
