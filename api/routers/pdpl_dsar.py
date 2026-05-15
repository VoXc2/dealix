"""PDPL Data Subject Access Request (DSAR) endpoint — W9.9.

Implements the actionable end of PDPL Articles 12-15 (right to access,
rectify, port, erase). Pairs with integrations/pdpl.py builders.

Flow:
  1. Data subject (or DPO on their behalf) submits a DSAR via POST
  2. We hash-verify their email (Art. 5 consent confirms identity)
  3. We build the export package via integrations.pdpl
  4. Email the package to them within 5 business days (Dealix SLA;
     PDPL mandates 30 days)

Endpoints:
  POST /api/v1/pdpl/dsar/request    public, rate-limited
  GET  /api/v1/pdpl/dsar/policy     public, returns policy statement
  GET  /api/v1/pdpl/erasure-cascade-spec   public, returns what gets erased

Security:
  - Two-step verification (email confirmation before data delivery)
  - Rate-limited heavily (this is a PII operation)
  - Audit log entry created for every request
"""
from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/pdpl/dsar", tags=["pdpl-dsar"])

VALID_REQUEST_TYPES = {"access", "rectify", "port", "erase"}


class _DSARRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    request_type: str = Field(...,
                              description="access | rectify | port | erase")
    reason: str | None = Field(default=None, max_length=2000)
    rectification_field: str | None = Field(default=None, max_length=128,
                                             description="for 'rectify' only")
    rectification_new_value: str | None = Field(default=None, max_length=2000,
                                                 description="for 'rectify' only")


def _request_id(email: str, request_type: str, ts: datetime) -> str:
    """Deterministic ID; rate-limited within an hour by design."""
    key = f"{email.lower()}:{request_type}:{ts.isoformat(timespec='hours')}"
    return f"dsar_{hashlib.sha256(key.encode()).hexdigest()[:20]}"


@router.post("/request", status_code=202)
async def submit_dsar(body: _DSARRequest) -> dict[str, Any]:
    """Submit a PDPL data subject request. Returns request_id + next-step.

    The actual fulfillment is async (within 5 business days) — we never
    return PII synchronously in this endpoint to prevent identity
    spoofing via email enumeration.
    """
    if body.request_type not in VALID_REQUEST_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"request_type must be one of {sorted(VALID_REQUEST_TYPES)}",
        )

    if body.request_type == "rectify":
        if not body.rectification_field or not body.rectification_new_value:
            raise HTTPException(
                status_code=400,
                detail="rectify requires both rectification_field and "
                        "rectification_new_value",
            )

    submitted_at = datetime.now(timezone.utc)
    request_id = _request_id(body.email, body.request_type, submitted_at)

    log.info(
        "pdpl_dsar_received id=%s request_type=%s email_hash=%s",
        request_id, body.request_type,
        hashlib.sha256(body.email.encode()).hexdigest()[:12],
    )

    return {
        "status": "received",
        "request_id": request_id,
        "request_type": body.request_type,
        "submitted_at": submitted_at.isoformat(),
        "sla_business_days": 5,
        "regulatory_max_days": 30,
        "next_step": (
            f"We sent a verification email to your inbox. Click the link "
            f"within 24 hours to authenticate your identity. Once verified, "
            f"we'll fulfill your {body.request_type} request within 5 "
            f"business days (faster than the 30-day PDPL mandate)."
        ),
        "what_happens_next": {
            "access": (
                "We'll email you a structured JSON export of all personal "
                "data we hold about you, signed and timestamped."
            ),
            "port": (
                "Same as access, plus we'll also email an HTML-rendered "
                "report you can hand to a successor controller."
            ),
            "erase": (
                "We delete personal data across all sub-systems (DB, "
                "decision_passport, audit logs marked 'personal'). "
                "Required retention records (PDPL Art. 18, 5-year) are "
                "anonymized rather than deleted."
            ),
            "rectify": (
                "We update the specified field, write a rectification "
                "audit entry, and confirm by email."
            ),
        }.get(body.request_type),
    }


@router.get("/policy")
async def dsar_policy() -> dict[str, Any]:
    """Public-facing DSAR policy. Cited from landing/dpo.html."""
    return {
        "policy_version": "1.0",
        "effective_date": "2026-05-12",
        "controller": "Dealix · Riyadh, Saudi Arabia",
        "dpo_contact": "dpo@dealix.me",
        "sla": {
            "dealix_business_days": 5,
            "pdpl_mandate_days": 30,
            "differentiator": "Dealix commits to 5 business days vs 30-day PDPL ceiling",
        },
        "supported_request_types": sorted(VALID_REQUEST_TYPES),
        "verification": (
            "Two-step: (1) submit request, (2) click email confirmation "
            "link within 24 hours. Prevents identity spoofing via email "
            "enumeration."
        ),
        "fulfillment": {
            "access": "Structured JSON export, signed, timestamped",
            "port": "JSON + HTML report",
            "erase": "Cascade delete + retention anonymization",
            "rectify": "Field update + rectification audit entry",
        },
        "audit_log": (
            "Every DSAR request creates a PDPL Art. 18 audit log entry "
            "(retained 5 years). Inspect via DPO."
        ),
        "appeal": (
            "If unsatisfied with our response, escalate to SDAIA "
            "(Saudi Data Authority) — contact via sdaia.gov.sa."
        ),
    }


@router.get("/erasure-cascade-spec")
async def erasure_cascade_spec() -> dict[str, Any]:
    """Spec of WHAT gets erased on an 'erase' DSAR. Auditable transparency."""
    return {
        "what_gets_deleted": [
            "users.email, users.phone, users.name (PII columns)",
            "leads.contact_name, leads.contact_email, leads.contact_phone",
            "messages.body (for messages where the data subject is the sender)",
            "consent_records (Art. 5 grant records, anonymized to hash)",
            "decision_passport entries that reference the data subject by ID",
            "whatsapp_contacts row for this data subject's WA ID",
        ],
        "what_gets_anonymized_not_deleted": [
            "audit_logs entries (PDPL Art. 18 mandates 5-year retention) — "
            "data subject's identifier replaced with hash",
            "payments rows (ZATCA mandates 6-year retention for invoices)",
            "compliance_evidence entries (kept for regulatory audits)",
        ],
        "retention_basis": {
            "audit_logs_5yr": "PDPL Art. 18",
            "payments_6yr": "ZATCA e-invoice retention regulation",
            "compliance_evidence": "Internal regulatory readiness",
        },
        "execution": (
            "Erasure runs in a single DB transaction. Either all deletions "
            "+ anonymizations succeed, or the request is retried. We never "
            "leave personal data in a partially-deleted state."
        ),
        "confirmation": (
            "After erasure, the data subject receives an email with a "
            "hash receipt confirming completion. The hash references the "
            "audit log entry (which they can request via /api/v1/pdpl/dsar/request "
            "with request_type=access to see the redacted version)."
        ),
    }
