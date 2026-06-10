"""Security & Privacy v5 — code-level helpers as endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.security_privacy import (
    data_minimization_for,
    list_known_object_types,
    redact_log_entry,
    scan_text_for_secrets,
)

router = APIRouter(prefix="/api/v1/security-privacy", tags=["security-privacy"])


@router.get("/status")
async def status() -> dict:
    return {
        "module": "security_privacy",
        "known_object_types": list_known_object_types(),
        "guardrails": {
            "no_pii_in_logs": True,
            "no_secrets_in_responses": True,
            "no_raw_secret_in_findings": True,
        },
    }


@router.post("/scan-text")
async def scan_text(payload: dict = Body(...)) -> dict:
    text = payload.get("text", "")
    if not isinstance(text, str):
        raise HTTPException(status_code=400, detail="payload.text must be a string")
    findings = scan_text_for_secrets(text)
    return {
        "clean": len(findings) == 0,
        "findings_count": len(findings),
        "findings": [f.to_dict() for f in findings],
    }


@router.post("/redact-log")
async def redact_log(payload: dict = Body(...)) -> dict:
    """Apply PII + secret redaction to a log entry (string or dict)."""
    entry = payload.get("entry")
    if entry is None:
        raise HTTPException(status_code=400, detail="payload.entry is required")
    return {"redacted": redact_log_entry(entry)}


@router.get("/data-minimization/{object_type}")
async def data_minimization(object_type: str) -> dict:
    try:
        contract = data_minimization_for(object_type)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return contract.to_dict()


@router.get("/data-minimization")
async def data_minimization_list() -> dict:
    return {"object_types": list_known_object_types()}
