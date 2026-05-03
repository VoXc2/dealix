"""
Inbound router — webhooks for customer-initiated replies.

When a prospect replies (via LinkedIn export, email, or WhatsApp inbound),
Dealix should auto-update the prospect status from `messaged` → `replied`
and emit an `opportunity_created` RWU. The founder sees this in
`dealix smart-launch` next morning.

Endpoints:
    POST /api/v1/inbound/linkedin
        body: {prospect_id, replied_at?, message_text?}
        Manually triggered (e.g., after founder pastes LinkedIn export).

    POST /api/v1/inbound/email
        body: {to_email or contact_email, message_text?}
        Resolves prospect by email; updates status if found.

    POST /api/v1/inbound/whatsapp
        body: {phone, message_text?}
        WhatsApp inbound — triggers 24h service window timestamp.
        Architecture ready; webhook signature verification happens here
        in the future Meta integration step.

All endpoints are thin: status update + RWU emit + audit log.
The actual transport-side webhook signatures are validated in middleware
when the gates flip.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import select

from auto_client_acquisition.revenue_company_os.proof_ledger import (
    record as record_proof,
)
from db.models import ProspectRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/inbound", tags=["inbound"])

log = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def _advance_to_replied(session, prospect: ProspectRecord, *, channel: str,
                              message_text: str = "") -> str | None:
    """Advance prospect to 'replied' if currently 'messaged'. Emit RWU."""
    if prospect.status not in ("messaged", "qualified", "new"):
        # Already past replied — append note instead
        notes = prospect.notes_ar or ""
        prospect.notes_ar = (
            (notes + f"\n[{_now().isoformat()}] inbound via {channel}: "
             f"{message_text[:120]}") if notes else
            f"[{_now().isoformat()}] inbound via {channel}: {message_text[:120]}"
        )[:8000]
        return None

    prospect.status = "replied"
    prospect.last_reply_at = _now()
    prospect.last_customer_inbound_at = _now()  # opens 24h WA window

    proof = await record_proof(
        session,
        unit_type="opportunity_created",
        customer_id=prospect.customer_id or prospect.id,
        actor=f"inbound_{channel}",
        approval_required=False,
        approved=True,
        risk_level="low",
        meta={
            "prospect_id": prospect.id,
            "channel": channel,
            "message_text": message_text[:500] if message_text else "",
            "via_inbound": True,
        },
    )
    return proof.id


@router.post("/linkedin")
async def linkedin_inbound(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Manual handoff after founder pastes LinkedIn export."""
    prospect_id = str(body.get("prospect_id") or "").strip()
    if not prospect_id:
        raise HTTPException(status_code=400, detail="prospect_id_required")
    message_text = str(body.get("message_text") or "")

    async with get_session() as session:
        p = (await session.execute(
            select(ProspectRecord).where(ProspectRecord.id == prospect_id)
        )).scalar_one_or_none()
        if p is None:
            raise HTTPException(status_code=404, detail="prospect_not_found")
        prev = p.status
        proof_id = await _advance_to_replied(
            session, p, channel="linkedin", message_text=message_text,
        )
        await session.commit()
        log.info(
            "inbound_linkedin prospect=%s prev=%s now=%s proof=%s",
            prospect_id, prev, p.status, proof_id,
        )
        return {
            "prospect_id": prospect_id,
            "previous_status": prev,
            "new_status": p.status,
            "proof_event_id": proof_id,
            "rwu_emitted": "opportunity_created" if proof_id else None,
        }


@router.post("/email")
async def email_inbound(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Email reply webhook — resolves by contact_email."""
    email = str(body.get("contact_email") or body.get("from_email") or "").strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="contact_email_required")
    message_text = str(body.get("message_text") or body.get("body") or "")

    async with get_session() as session:
        p = (await session.execute(
            select(ProspectRecord).where(ProspectRecord.contact_email == email)
        )).scalar_one_or_none()
        if p is None:
            return {
                "matched": False,
                "email": email,
                "note_ar": "البريد لا يطابق أي prospect — تجاهل (بدون lead pollution).",
            }
        prev = p.status
        proof_id = await _advance_to_replied(
            session, p, channel="email", message_text=message_text,
        )
        await session.commit()
        return {
            "matched": True,
            "prospect_id": p.id,
            "previous_status": prev,
            "new_status": p.status,
            "proof_event_id": proof_id,
        }


@router.post("/whatsapp")
async def whatsapp_inbound(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """WhatsApp inbound — opens the 24h service window."""
    phone = str(body.get("phone") or body.get("from") or "").strip()
    if not phone:
        raise HTTPException(status_code=400, detail="phone_required")
    message_text = str(body.get("message_text") or body.get("body") or "")

    async with get_session() as session:
        p = (await session.execute(
            select(ProspectRecord).where(ProspectRecord.contact_phone == phone)
        )).scalar_one_or_none()
        if p is None:
            return {
                "matched": False,
                "phone": phone[:6] + "***",
                "note_ar": (
                    "الرقم لا يطابق أي prospect. لا نُسجل أرقام لم تأتِ "
                    "من warm intro موثَّق (PDPL)."
                ),
            }
        prev = p.status
        proof_id = await _advance_to_replied(
            session, p, channel="whatsapp_inbound", message_text=message_text,
        )
        # Mark consent as recorded (customer initiated → implicit opt-in for replies)
        if p.consent_status == "none":
            p.consent_status = "opt_in_recorded"
            p.consent_source = "wa_customer_initiated"
        await session.commit()
        return {
            "matched": True,
            "prospect_id": p.id,
            "previous_status": prev,
            "new_status": p.status,
            "proof_event_id": proof_id,
            "consent_status": p.consent_status,
            "wa_24h_window_until": (
                p.last_customer_inbound_at.isoformat() + "Z (+24h from now)"
                if p.last_customer_inbound_at else None
            ),
        }
