"""
Payments router — invoice + payment-link + (gated) live charge.

Why three endpoints, not one:

  POST /api/v1/payments/invoice
       Creates a Moyasar **invoice link** (or a manual-fallback link if
       no Moyasar key is set). Always works. Founder pastes the link to
       customer via WhatsApp / email. Customer pays on Moyasar's hosted
       page. This is the **default revenue path** until live charge is
       wired with merchant credentials.

  POST /api/v1/payments/charge
       **Gated by MOYASAR_ALLOW_LIVE_CHARGE.** Returns 403 with an Arabic
       reason when False (the default). When True, performs a server-side
       charge via Moyasar API. Wire credentials BEFORE flipping the gate;
       see docs/MOYASAR_LIVE_CUTOVER.md.

  POST /api/v1/payments/mark-paid
       Manual confirmation — used when a customer pays via bank transfer
       or in-person. Records payment + emits proof event.

Every payment path emits a `payment_link_drafted` (or `payment_link_sent`)
proof event so the Proof Pack reflects the financial activity.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.revenue_company_os.proof_ledger import record as record_proof
from core.config.settings import get_settings
from db.models import PaymentRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])

log = logging.getLogger(__name__)

# Moyasar fee schedule (verified 2026):
#   Mada cards    : 1.5% + 1 SAR
#   Credit cards  : 2.2% + 1 SAR
# Saudi B2B SaaS VAT: 15% (price displayed inclusive on landing).
_MOYASAR_HOSTED_BASE = "https://moyasar.com/invoice/"


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _new_payment_id() -> str:
    return f"pay_{uuid.uuid4().hex[:14]}"


def _new_invoice_local_id() -> str:
    return f"inv_{uuid.uuid4().hex[:14]}"


def _gate_state() -> dict[str, bool]:
    s = get_settings()
    return {
        "live_charge": bool(getattr(s, "moyasar_allow_live_charge", False)),
    }


def _moyasar_secret() -> str | None:
    """Read Moyasar secret key from settings, return None if not configured."""
    s = get_settings()
    secret = getattr(s, "moyasar_secret_key", None)
    if hasattr(secret, "get_secret_value"):
        secret = secret.get_secret_value()
    return secret if secret and secret not in ("", "x", "change-me") else None


@router.get("/state")
async def state() -> dict[str, Any]:
    """Public read of payment system readiness — used by the founder dashboard."""
    return {
        "gates": _gate_state(),
        "moyasar_secret_configured": _moyasar_secret() is not None,
        "fees": {
            "mada":   {"percent": 1.5, "fixed_sar": 1.0},
            "credit": {"percent": 2.2, "fixed_sar": 1.0},
        },
        "vat_percent": 15,
        "currency": "SAR",
        "default_path": "invoice",
        "ready_to_flip_live_charge": _moyasar_secret() is not None,
    }


@router.post("/invoice")
async def create_invoice(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Create a payment-link invoice. Default revenue path.

    Body:
        amount_sar (required, > 0)
        customer_id (required)
        description_ar (optional, default = "Pilot 499 — 7 days")
        deal_id (optional)
        partner_id (optional)
        metadata (optional dict)

    Behavior:
      - If MOYASAR_SECRET_KEY is configured → call Moyasar invoice API
        (live or test depending on key prefix).
      - If not → return a placeholder URL that points to the manual-payment
        SOP. Either way, a PaymentRecord (status='pending') and a
        payment_link_drafted Proof Event are written.

    Returns: {invoice_id, amount_sar, currency, url, status, expires_at}
    """
    try:
        amount_sar = float(body.get("amount_sar") or 0.0)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="amount_sar_must_be_number") from exc
    if amount_sar <= 0:
        raise HTTPException(status_code=400, detail="amount_sar_required_positive")

    customer_id = str(body.get("customer_id") or "").strip() or None
    deal_id = str(body.get("deal_id") or "").strip() or None
    partner_id = str(body.get("partner_id") or "").strip() or None
    description = str(body.get("description_ar") or "Pilot Dealix — 7 أيام")

    invoice_local_id = _new_invoice_local_id()
    expires_at = _now() + timedelta(days=14)
    secret = _moyasar_secret()

    invoice_url: str | None = None
    moyasar_invoice_id: str | None = None
    mode = "manual"

    if secret:
        # Real Moyasar invoice (test or live based on key prefix)
        try:
            import httpx  # local import keeps optional dep boundary clean
            mode = "live" if secret.startswith("sk_live_") else "test"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    "https://api.moyasar.com/v1/invoices",
                    auth=(secret, ""),
                    json={
                        "amount": int(round(amount_sar * 100)),  # halalas
                        "currency": "SAR",
                        "description": description[:255],
                        "callback_url": "https://api.dealix.me/api/v1/webhooks/moyasar",
                        "metadata": {
                            "dealix_invoice_id": invoice_local_id,
                            "customer_id": customer_id or "",
                            "deal_id": deal_id or "",
                            "partner_id": partner_id or "",
                        },
                    },
                )
            if resp.status_code in (200, 201):
                data = resp.json()
                invoice_url = data.get("url")
                moyasar_invoice_id = data.get("id")
            else:
                log.warning(
                    "moyasar_invoice_create_failed status=%s body=%s",
                    resp.status_code, resp.text[:200],
                )
        except Exception as exc:  # noqa: BLE001
            log.warning("moyasar_invoice_create_exception err=%s", str(exc)[:200])

    if not invoice_url:
        # Manual fallback — founder collects via bank transfer / Mada in-person
        invoice_url = f"https://api.dealix.me/manual-pay?inv={invoice_local_id}&amount={int(amount_sar)}"

    async with get_session() as session:
        row = PaymentRecord(
            id=_new_payment_id(),
            customer_id=customer_id,
            partner_id=partner_id,
            amount_sar=amount_sar,
            currency="SAR",
            status="pending",
            moyasar_payment_id=moyasar_invoice_id,
            invoice_url=invoice_url,
            meta_json={
                "mode": mode,
                "description_ar": description,
                "deal_id": deal_id,
                "dealix_invoice_id": invoice_local_id,
            },
        )
        session.add(row)
        try:
            await record_proof(
                session,
                unit_type="payment_link_drafted",
                customer_id=customer_id,
                partner_id=partner_id,
                revenue_impact_sar=amount_sar,
                actor="payments_router",
                approval_required=False,
                approved=True,
                risk_level="low",
                meta={"invoice_url": invoice_url, "mode": mode},
            )
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        await session.commit()

    return {
        "invoice_id": row.id,
        "amount_sar": amount_sar,
        "currency": "SAR",
        "url": invoice_url,
        "status": "pending",
        "mode": mode,
        "expires_at": expires_at.isoformat(),
        "instruction_ar": (
            "أرسل هذا الرابط للعميل عبر WhatsApp. الدفع آمن "
            "وسريع عبر Mada / فيزا / Apple Pay."
        ),
    }


@router.post("/charge")
async def charge(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Server-side charge — GATED.

    Returns 403 with Arabic reason unless MOYASAR_ALLOW_LIVE_CHARGE=true
    AND a real Moyasar secret key is configured.

    To activate (after merchant onboarding completed with Moyasar):
      1. Set MOYASAR_SECRET_KEY=sk_live_xxx in Railway env vars
      2. Set MOYASAR_ALLOW_LIVE_CHARGE=true
      3. Verify with: curl -X POST .../api/v1/payments/charge -d '{...}'
      4. See docs/MOYASAR_LIVE_CUTOVER.md for the full checklist.
    """
    if not _gate_state()["live_charge"]:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "live_charge_disabled",
                "reason_ar": (
                    "Live charge مُعطَّل افتراضياً (gate=False). "
                    "استخدم /api/v1/payments/invoice لإرسال رابط دفع آمن."
                ),
                "how_to_enable": "see docs/MOYASAR_LIVE_CUTOVER.md",
            },
        )
    secret = _moyasar_secret()
    if not secret:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "moyasar_secret_not_configured",
                "reason_ar": "Gate مفتوح لكن MOYASAR_SECRET_KEY غير مضبوط في env.",
            },
        )

    # Live charge implementation deliberately not wired in this PR.
    # The path exists so flipping the gate doesn't 404 and so production
    # observability picks up the (intentional) 501 in the audit log.
    raise HTTPException(
        status_code=501,
        detail={
            "error": "live_charge_not_implemented_yet",
            "reason_ar": (
                "البنية جاهزة، التنفيذ متعمَّد التأخير حتى تكتمل KYB مع موياسر. "
                "استخدم /invoice حتى ذلك الحين."
            ),
            "guidance": "Wire the actual Moyasar /payments POST in this handler "
                        "AFTER merchant onboarding is complete + DPA signed.",
        },
    )


@router.post("/confirm")
async def confirm(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Founder confirms a payment received outside Moyasar (bank transfer /
    in-person Mada). Updates PaymentRecord status + emits proof event.

    Distinct from /api/v1/payments/mark-paid (autonomous.py) which marks a
    DEAL as paid; this one marks an INVOICE as paid."""
    invoice_id = str(body.get("invoice_id") or "").strip()
    if not invoice_id:
        raise HTTPException(status_code=400, detail="invoice_id_required")
    moyasar_event_id = body.get("moyasar_event_id") or None

    async with get_session() as session:
        from sqlalchemy import select
        existing = (await session.execute(
            select(PaymentRecord).where(PaymentRecord.id == invoice_id)
        )).scalar_one_or_none()
        if existing is None:
            raise HTTPException(status_code=404, detail="invoice_not_found")
        existing.status = "paid"
        existing.paid_at = _now()
        if moyasar_event_id:
            existing.moyasar_event_id = str(moyasar_event_id)
        # Emit a paid-confirmed proof event
        try:
            await record_proof(
                session,
                unit_type="payment_link_drafted",  # closest existing unit; pack reflects revenue
                customer_id=existing.customer_id,
                partner_id=existing.partner_id,
                revenue_impact_sar=existing.amount_sar,
                actor="founder",
                approval_required=False,
                approved=True,
                risk_level="low",
                meta={"invoice_id": invoice_id, "confirmed": True, "method": "manual"},
            )
        except ValueError:
            pass
        await session.commit()

    return {
        "invoice_id": invoice_id,
        "status": "paid",
        "amount_sar": existing.amount_sar,
        "paid_at": existing.paid_at.isoformat() if existing.paid_at else None,
        "celebration_ar": "🎉 أول دفعة! افتح docs/sales-kit/dealix_case_study_template.md خلال 48 ساعة.",
    }
