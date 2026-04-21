"""
Moyasar FastAPI Routes:
- POST /webhooks/moyasar          → Receive Moyasar payment/subscription webhooks
- POST /payments/moyasar/invoice  → Create a payment invoice (admin)
- GET  /payments/moyasar/callback → Post-payment redirect callback

مسارات FastAPI لبوابة الدفع ميسر.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Header, HTTPException, Request, Query
from fastapi.responses import JSONResponse, RedirectResponse

from .webhooks import handle_moyasar_webhook, verify_moyasar_signature
from .client import MoyasarClient
from .subscriptions import MoyasarSubscriptions

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["moyasar"])


# ── Webhook Endpoint ──────────────────────────────────────────────────────────

@router.post("/webhooks/moyasar", summary="Moyasar Webhook Receiver")
async def moyasar_webhook(
    request: Request,
    x_moyasar_signature: str = Header(default="", alias="X-Moyasar-Signature"),
):
    """
    Receive and dispatch webhook events from Moyasar.
    استقبال وتوجيه أحداث Webhook من ميسر.

    Verifies HMAC-SHA256 signature before processing.
    يتحقق من توقيع HMAC-SHA256 قبل المعالجة.
    """
    body = await request.body()

    if not verify_moyasar_signature(body, x_moyasar_signature):
        raise HTTPException(status_code=401, detail="Invalid Moyasar webhook signature")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Moyasar sends event type in payload.type or payload.event
    event_type = payload.get("type") or payload.get("event")
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing event type in payload")

    result = await handle_moyasar_webhook(event_type, payload, db=None)
    return JSONResponse(content={"received": True, **result})


# ── Payment Callback ──────────────────────────────────────────────────────────

@router.get("/payments/moyasar/callback", summary="Post-payment Redirect Callback")
async def moyasar_payment_callback(
    id: str = Query(..., description="Moyasar payment ID"),
    status: str = Query(..., description="Payment status from Moyasar"),
    message: str = Query(default="", description="Status message"),
):
    """
    Moyasar redirects customer here after payment attempt.
    يعيد ميسر توجيه العميل هنا بعد محاولة الدفع.

    Docs: https://docs.moyasar.com/api/payments/create#callback_url
    """
    logger.info(f"Moyasar payment callback: id={id} status={status}")

    if status == "paid":
        # Verify payment server-side before granting access
        client = MoyasarClient()
        try:
            payment = await client.get_payment(id)
            verified_status = payment.get("status")
            metadata = payment.get("metadata", {})
            tenant_id = metadata.get("tenant_id")

            if verified_status == "paid":
                # TODO: Provision service for tenant_id
                return JSONResponse(content={
                    "success": True,
                    "payment_id": id,
                    "status": "paid",
                    "tenant_id": tenant_id,
                    "message": "تم الدفع بنجاح — Payment successful",
                })
        except Exception as exc:
            logger.error(f"Failed to verify Moyasar payment {id}: {exc}")

    return JSONResponse(
        status_code=400 if status == "failed" else 200,
        content={
            "success": False,
            "payment_id": id,
            "status": status,
            "message": message or "فشل الدفع — Payment failed",
        },
    )


# ── Invoice creation (internal/admin) ────────────────────────────────────────

@router.post("/payments/moyasar/invoice", summary="Create Moyasar Payment Invoice (Admin)")
async def create_moyasar_invoice(request: Request):
    """
    Create a Moyasar payment invoice for a tenant.
    إنشاء فاتورة دفع ميسر لتاجر.

    Expects JSON body:
    {
        "tenant_id": "abc123",
        "amount_sar": 1499,
        "description": "Dealix Starter subscription",
        "callback_url": "https://api.dealix.sa/payments/moyasar/callback"
    }
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    amount_sar = float(body.get("amount_sar", 0))
    if amount_sar <= 0:
        raise HTTPException(status_code=400, detail="amount_sar must be positive")

    amount_halalas = int(amount_sar * 100)

    client = MoyasarClient()
    try:
        invoice = await client.create_invoice(
            amount=amount_halalas,
            currency="SAR",
            description=body.get("description", "Dealix Subscription"),
            callback_url=body.get("callback_url", ""),
            metadata={"tenant_id": body.get("tenant_id")},
        )
    except Exception as exc:
        logger.error(f"Failed to create Moyasar invoice: {exc}")
        raise HTTPException(status_code=502, detail=f"Moyasar API error: {exc}")

    return JSONResponse(content={
        "invoice_id": invoice.get("id"),
        "payment_url": invoice.get("url") or invoice.get("payment_url"),
        "amount_sar": amount_sar,
        "status": invoice.get("status"),
    })
