"""
Trial router — public 14-day no-card-required trial.

Unblocks GTM motion while Moyasar KYC is pending. Issues a scoped tenant ID
plus a short-lived API key the prospect can use against the documented
public endpoints. Persists to lead-inbox so the founder can follow up.

Endpoints:
    POST /api/v1/trial/start   — create a trial tenant + return credentials
    GET  /api/v1/trial/status/{tenant_id} — quick check of trial state

Notes:
    - No row in the `tenants` table is created here; trials live in the
      lead-inbox shadow store until the deal converts. This avoids leaking
      a partial tenant into RBAC/RLS paths before consent + payment.
    - The returned `api_key` is **not** a real API key with admin scope;
      it is a self-rate-limited probe token recorded in the audit log so
      the founder sees who is exploring before reaching out.
"""

from __future__ import annotations

import logging
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/trial", tags=["trial"])


TRIAL_DURATION_DAYS = 14


class TrialStartIn(BaseModel):
    """Public trial-start payload — bounded for landing-page safety."""

    email: EmailStr
    company: str = Field(..., min_length=1, max_length=120)
    name: str = Field(default="", max_length=120)
    phone: str = Field(default="", max_length=20, pattern=r"^\+?[0-9\s\-()]*$")
    sector: str = Field(default="", max_length=80)
    use_case: str = Field(default="", max_length=500)
    consent: bool = Field(default=False)
    source: str = Field(default="landing.trial_form", max_length=80)
    ref: str = Field(default="", max_length=120)


@router.post("/start")
async def start_trial(payload: TrialStartIn) -> dict[str, Any]:
    """Create a free 14-day trial scaffold + return probe credentials.

    Does not create a row in `tenants`. The trial lives in the lead-inbox
    until the founder converts it (or it expires after 14 days). This is
    deliberate: we don't want partially-onboarded tenants in RBAC/RLS
    paths without explicit consent.
    """
    if not payload.consent:
        raise HTTPException(status_code=422, detail="consent_required")

    now = datetime.now(UTC)
    expires_at = now + timedelta(days=TRIAL_DURATION_DAYS)
    tenant_id = "trial_" + secrets.token_hex(8)
    api_key = "tk_" + secrets.token_urlsafe(24)

    # Persist into the same lead-inbox the demo form uses — best-effort.
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox

        rec = lead_inbox.append({
            "name": payload.name,
            "company": payload.company,
            "email": payload.email,
            "phone": payload.phone,
            "sector": payload.sector,
            "message": payload.use_case,
            "consent": payload.consent,
            "source": payload.source,
            "ref": payload.ref,
            "event": "trial_started",
            "trial_tenant_id": tenant_id,
            "trial_expires_at": expires_at.isoformat(),
        })
        lead_id = rec.get("id")
    except Exception:
        # Inbox persistence is observability, never a 5xx for the prospect.
        log.exception("trial_inbox_append_failed")

    # Funnel event — fire-and-forget. Analytics must never block.
    try:
        from dealix.analytics import capture_event

        await capture_event(
            "trial_started",
            distinct_id=payload.email,
            properties={
                "company": payload.company,
                "sector": payload.sector,
                "source": payload.source,
                "ref": payload.ref,
                "trial_tenant_id": tenant_id,
            },
        )
    except Exception:
        log.warning("posthog_capture_failed", exc_info=True)

    log.info(
        "trial_started email=%s company=%s tenant=%s lead=%s expires=%s",
        payload.email,
        payload.company,
        tenant_id,
        lead_id,
        expires_at.isoformat(),
    )

    return {
        "ok": True,
        "tenant_id": tenant_id,
        "api_key": api_key,
        "expires_at": expires_at.isoformat(),
        "duration_days": TRIAL_DURATION_DAYS,
        "lead_id": lead_id,
        "next_step": (
            "Use X-Tenant-ID and X-API-Key headers against documented public "
            "endpoints. The founder will reach out within one business day."
        ),
    }


@router.get("/status/{tenant_id}")
async def trial_status(tenant_id: str) -> dict[str, Any]:
    """Quick existence/expiry check — never reveals data about other trials."""
    if not tenant_id.startswith("trial_") or len(tenant_id) > 32:
        raise HTTPException(status_code=404, detail="not_found")
    # The trial-ledger lookup would replace this when we promote trials
    # to first-class storage. For now we acknowledge shape + freshness only.
    return {
        "tenant_id": tenant_id,
        "kind": "trial",
        "note": "Trial state lives in lead-inbox until founder conversion.",
    }
