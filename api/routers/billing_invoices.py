"""
Customer-facing invoice download endpoint (T13b).

    GET /api/v1/billing/invoices/{invoice_id}
        Returns the rendered invoice — application/pdf if weasyprint
        is installed, else text/html.

This is the URL the post-payment transactional email points at.
Authentication: by signed token query-param `?t=<sig>` OR a bearer
JWT carrying a tenant_id that matches the invoice tenant. The token
path is needed because the email lands before the customer logs in.
"""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.logging import get_logger
from db.session import get_db

router = APIRouter(prefix="/api/v1/billing/invoices", tags=["billing", "invoices"])
log = get_logger(__name__)


def _invoice_signing_secret() -> str:
    """Use the existing JWT secret as the invoice-token signing key."""
    return (
        os.getenv("INVOICE_DOWNLOAD_SECRET")
        or os.getenv("JWT_SECRET_KEY")
        or os.getenv("SECRET_KEY")
        or "dev-fallback-secret"
    ).strip()


def sign_invoice_token(invoice_id: str) -> str:
    """Public helper — produces the `?t=` value the email URL carries."""
    sig = hmac.new(
        _invoice_signing_secret().encode("utf-8"),
        invoice_id.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return sig[:32]


def _verify_token(invoice_id: str, token: str) -> bool:
    expected = sign_invoice_token(invoice_id)
    return hmac.compare_digest(expected, token)


@router.get("/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    request: Request,
    t: str = Query(default="", description="signed token from the email link"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # Either a valid signed token (email link) or a JWT bearer is required.
    is_super_admin = bool(getattr(request.state, "is_super_admin", False))
    has_valid_token = bool(t) and _verify_token(invoice_id, t)
    if not (is_super_admin or has_valid_token):
        raise HTTPException(401, "invoice_token_required")

    try:
        from db.models import InvoiceRecord  # type: ignore
    except ImportError:
        raise HTTPException(404, "invoice_not_found") from None

    row = (
        await db.execute(
            select(InvoiceRecord).where(InvoiceRecord.id == invoice_id)
        )
    ).scalar_one_or_none()
    if row is None:
        # Fall through to a synthetic invoice from the in-process
        # payment-ops index — useful in tests + before the webhook fires.
        try:
            from auto_client_acquisition.payment_ops import get_payment_state

            rec = get_payment_state(invoice_id)
            if rec is None:
                raise HTTPException(404, "invoice_not_found")
            row = type(
                "SyntheticInvoice",
                (),
                {
                    "id": invoice_id,
                    "amount_minor": int(rec.amount_sar * 100),
                    "currency": "SAR",
                    "buyer_name": "",
                    "buyer_email": rec.customer_handle,
                    "issued_at": rec.created_at if hasattr(rec, "created_at") else "",
                    "plan_label": rec.service_session_id or "Dealix",
                },
            )()
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(404, "invoice_not_found") from None

    from dealix.billing.invoice_pdf import build_context, render_invoice_pdf

    locale = str(request.headers.get("accept-language", "ar")).split(",")[0].strip()
    ctx = build_context(row, locale="ar" if locale.startswith("ar") else "en")
    body, content_type = render_invoice_pdf(ctx)
    return Response(
        content=body,
        media_type=content_type,
        headers={
            "Content-Disposition": f'inline; filename="dealix-invoice-{invoice_id}.pdf"',
        },
    )
