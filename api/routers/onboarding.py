"""
Onboarding router — public submission from the wizard at /onboarding.html.

Endpoints:
    POST /api/v1/onboarding/submit
        body: {
            company_name, sector, monthly_revenue_band, contact_name,
            contact_email, bundle_id?, intake_answers? {key: value},
            locale?, partner_id?
        }
        Effects (one transaction):
          1. Upserts a LeadRecord (by contact_email).
          2. Records two Proof Events (opportunity_created + target_ranked).
          3. Returns lead_id + proof event ids + ETA for first Proof Pack.
        Defensive — returns 200 with `_errors` rather than 500.

    GET  /api/v1/onboarding/eta
        Returns the first-pack ETA policy (7 days default) — used by
        the wizard confirmation screen so copy stays in one place.
"""

from __future__ import annotations

import hashlib
import logging
import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import select

from auto_client_acquisition.revenue_company_os.proof_ledger import record as record_proof
from db.models import LeadRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])

log = logging.getLogger(__name__)

_FIRST_PACK_DAYS = 7
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_VALID_REVENUE_BANDS = {
    "lt_50k", "50k_200k", "200k_1m", "1m_5m", "5m_plus", "unknown",
}


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _new_lead_id() -> str:
    return f"led_{uuid.uuid4().hex[:14]}"


def _dedup_hash(email: str) -> str:
    return hashlib.sha256(email.encode("utf-8")).hexdigest()[:32]


@router.get("/eta")
async def eta() -> dict[str, Any]:
    """Public copy hook — wizard reads from here so the policy is one source."""
    return {
        "first_pack_days": _FIRST_PACK_DAYS,
        "promise_ar": "Proof Pack أول خلال ٧ أيام من اكتمال الـ intake.",
        "promise_en": "First Proof Pack within 7 days of intake completion.",
    }


@router.post("/submit")
async def submit(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Persist wizard submission as a LeadRecord + emit two proof events."""
    company_name = str(body.get("company_name") or "").strip()
    sector = str(body.get("sector") or "").strip()
    contact_name = str(body.get("contact_name") or "").strip()
    contact_email = str(body.get("contact_email") or "").strip().lower()
    revenue_band = str(body.get("monthly_revenue_band") or "unknown").lower()
    bundle_id = str(body.get("bundle_id") or "free_diagnostic").strip()
    locale = str(body.get("locale") or "ar").lower()[:4]
    partner_id = body.get("partner_id") or None
    intake_answers = body.get("intake_answers") or {}
    if not isinstance(intake_answers, dict):
        intake_answers = {}

    if not company_name:
        raise HTTPException(status_code=400, detail="company_name_required")
    if not contact_email or not _EMAIL_RE.match(contact_email):
        raise HTTPException(status_code=400, detail="valid_contact_email_required")
    if revenue_band not in _VALID_REVENUE_BANDS:
        revenue_band = "unknown"

    errors: dict[str, str] = {}
    lead_id: str | None = None
    proof_ids: list[str] = []
    dedup = _dedup_hash(contact_email)

    try:
        async with get_session() as session:
            existing = (await session.execute(
                select(LeadRecord).where(LeadRecord.dedup_hash == dedup)
            )).scalar_one_or_none()

            meta_addon = {
                "monthly_revenue_band": revenue_band,
                "intake_answers": intake_answers,
                "bundle_id": bundle_id,
                "wizard_completed_at": _now().isoformat(),
            }

            if existing is None:
                lead = LeadRecord(
                    id=_new_lead_id(),
                    source="onboarding_wizard",
                    company_name=company_name,
                    contact_name=contact_name or contact_email.split("@")[0],
                    contact_email=contact_email,
                    sector=sector or None,
                    locale=locale,
                    status="new",
                    partner_id=partner_id,
                    dedup_hash=dedup,
                    meta_json=meta_addon,
                )
                session.add(lead)
                lead_id = lead.id
            else:
                lead_id = existing.id
                existing_meta = dict(existing.meta_json or {})
                existing_meta.update(meta_addon)
                existing.meta_json = existing_meta
                if existing.company_name != company_name and company_name:
                    existing.company_name = company_name
                if sector and not existing.sector:
                    existing.sector = sector
                if partner_id and not existing.partner_id:
                    existing.partner_id = partner_id

            for unit in ("opportunity_created", "target_ranked"):
                row = await record_proof(
                    session,
                    unit_type=unit,
                    customer_id=None,  # not yet a customer
                    partner_id=partner_id,
                    actor="onboarding_wizard",
                    risk_level="low",
                    meta={
                        "lead_id": lead_id,
                        "bundle_id": bundle_id,
                        "company": company_name[:64],
                    },
                )
                proof_ids.append(row.id)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        errors["submit"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        log.warning("onboarding_submit_failed err=%s", errors["submit"])

    response: dict[str, Any] = {
        "ok": "submit" not in errors,
        "lead_id": lead_id,
        "proof_event_ids": proof_ids,
        "first_pack_eta": (_now() + timedelta(days=_FIRST_PACK_DAYS)).isoformat(),
        "promise_ar": "Proof Pack أول خلال ٧ أيام.",
    }
    if errors:
        response["_errors"] = errors
    return response
