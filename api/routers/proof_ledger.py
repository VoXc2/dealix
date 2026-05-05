"""Proof Ledger v5 — file-backed JSONL endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.proof_ledger import (
    ProofEvent,
    ProofEventType,
    RevenueWorkUnit,
    RevenueWorkUnitType,
    export_for_audit,
    export_redacted,
    get_default_ledger,
)

router = APIRouter(prefix="/api/v1/proof-ledger", tags=["proof-ledger"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "proof_ledger",
        "backend": "file_jsonl",
        "guardrails": {
            "pii_redacted_before_persistence": True,
            "customer_handle_anonymized_unless_consent": True,
            "no_raw_pii_in_exports": True,
        },
    }


@router.post("/events")
async def record_event(payload: dict = Body(...)) -> dict:
    """Persist one ProofEvent. Returns the stored (redacted) record."""
    try:
        event = ProofEvent.model_validate(payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"invalid event: {exc}") from exc
    stored = get_default_ledger().record(event)
    return stored.model_dump(mode="json")


@router.get("/events")
async def list_events(
    customer_handle: str | None = None,
    event_type: str | None = None,
    limit: int = 100,
) -> dict:
    rows = get_default_ledger().list_events(
        customer_handle=customer_handle,
        event_type=event_type,
        limit=max(1, min(int(limit), 500)),
    )
    return {"count": len(rows), "events": [r.model_dump(mode="json") for r in rows]}


@router.post("/units")
async def record_unit(payload: dict = Body(...)) -> dict:
    try:
        unit = RevenueWorkUnit.model_validate(payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"invalid unit: {exc}") from exc
    stored = get_default_ledger().record_unit(unit)
    return stored.model_dump(mode="json")


@router.get("/units")
async def list_units(
    customer_handle: str | None = None,
    unit_type: str | None = None,
    limit: int = 100,
) -> dict:
    rows = get_default_ledger().list_units(
        customer_handle=customer_handle,
        unit_type=unit_type,
        limit=max(1, min(int(limit), 500)),
    )
    return {"count": len(rows), "units": [r.model_dump(mode="json") for r in rows]}


@router.post("/export/redacted")
async def export_redacted_endpoint(payload: dict = Body(default_factory=dict)) -> dict:
    customer_handle = payload.get("customer_handle")
    event_type = payload.get("event_type")
    limit = max(1, min(int(payload.get("limit", 200)), 1000))
    return export_redacted(
        customer_handle=customer_handle,
        event_type=event_type,
        limit=limit,
    )


@router.get("/export/audit")
async def export_audit_endpoint() -> dict:
    """SDAIA / DPO-shareable export. PII redacted unconditionally."""
    return export_for_audit()
