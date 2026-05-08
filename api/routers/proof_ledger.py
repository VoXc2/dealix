"""Proof Ledger v5 — file-backed JSONL endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException

from api.security.auth_deps import get_optional_user
from auto_client_acquisition.proof_ledger import (
    ProofEvent,
    ProofEventType,
    RevenueWorkUnit,
    RevenueWorkUnitType,
    export_for_audit,
    export_redacted,
    get_default_ledger,
)
from db.models import UserRecord

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
async def record_event(
    payload: dict = Body(...),
    auth_user: UserRecord | None = Depends(get_optional_user),
) -> dict:
    """Persist one ProofEvent. Returns the stored (redacted) record."""
    body = dict(payload)
    inner = dict(body.get("payload") or {})
    if auth_user is not None and getattr(auth_user, "tenant_id", None):
        inner["dealix_tenant_id"] = auth_user.tenant_id
    body["payload"] = inner
    try:
        event = ProofEvent.model_validate(body)
    except Exception as exc:
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
    except Exception as exc:
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


# ── Phase 6 extensions ────────────────────────────────────────

@router.post("/attachments")
async def attachments_endpoint(payload: dict = Body(default_factory=dict)) -> dict:
    """Store an evidence attachment for one proof event.

    Body: {
      'customer_handle': 'acme',
      'event_id': 'pe_abc',
      'filename': 'report.pdf',
      'mime_type': 'application/pdf',
      'data_base64': '...'
    }
    """
    import base64

    from auto_client_acquisition.proof_ledger.file_storage import store_attachment

    required = ["customer_handle", "event_id", "filename", "mime_type", "data_base64"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise HTTPException(status_code=422, detail=f"missing: {missing}")
    try:
        data = base64.b64decode(payload["data_base64"])
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"invalid base64: {e}")
    try:
        result = store_attachment(
            customer_handle=payload["customer_handle"],
            event_id=payload["event_id"],
            filename=payload["filename"],
            mime_type=payload["mime_type"],
            data=data,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {
        "stored": True,
        "attachment": result,
        "guardrails": {
            "max_bytes": 10 * 1024 * 1024,
            "mime_allowlist_enforced": True,
            "filename_sanitized": True,
        },
    }


@router.post("/consent/request")
async def consent_request_endpoint(payload: dict = Body(default_factory=dict)) -> dict:
    """Request consent for publishing a narrative."""
    from auto_client_acquisition.proof_ledger.consent_signature import request_consent

    customer_handle = payload.get("customer_handle")
    scope = payload.get("scope", "single_pack")
    narrative = payload.get("narrative", "")
    target_event_ids = payload.get("target_event_ids", [])
    target_pack_id = payload.get("target_pack_id")
    if not customer_handle or not narrative:
        raise HTTPException(
            status_code=422, detail="customer_handle + narrative required",
        )
    if scope not in ("single_event", "single_pack", "all_future"):
        raise HTTPException(status_code=422, detail=f"invalid scope: {scope}")
    sig = request_consent(
        customer_handle=customer_handle,
        scope=scope,
        narrative=narrative,
        target_event_ids=target_event_ids,
        target_pack_id=target_pack_id,
    )
    return {
        "signature": sig.model_dump(mode="json"),
        "guardrails": {
            "no_publish_without_signed_status": True,
            "document_hash_binds_consent": True,
        },
    }


@router.post("/pack/build")
async def pack_build_endpoint(payload: dict = Body(default_factory=dict)) -> dict:
    """Assemble a Proof Pack from N events.

    Body: {
      'customer_handle': 'acme',
      'events': [...event dicts...],
      'audience': 'internal_only' | 'external_publishable'
    }
    """
    from auto_client_acquisition.proof_ledger.pack_assembly import assemble_proof_pack

    customer_handle = payload.get("customer_handle")
    events = payload.get("events", [])
    audience = payload.get("audience", "internal_only")
    if not customer_handle or not isinstance(events, list):
        raise HTTPException(
            status_code=422, detail="customer_handle + events list required",
        )
    try:
        pack = assemble_proof_pack(
            customer_handle=customer_handle,
            events=events,
            audience=audience,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return pack
