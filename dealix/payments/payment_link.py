"""Payment Link — thin wrapper around MoyasarClient for commercial offers.

Constitutional gate: NO_LIVE_CHARGE — invoice created in test mode unless
MOYASAR_LIVE_MODE=1 is explicitly set. All payment events require
founder approval before being surfaced to the customer.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from pydantic import BaseModel, Field

_LIVE_MODE = os.getenv("MOYASAR_LIVE_MODE", "0").strip() in ("1", "true", "yes")

# Historical fixed-price tier identifiers are retained only to reject stale
# requests explicitly. Current payment authority comes from an approved named-
# customer invoice amount, never from a public/service tier.
LEGACY_FIXED_PRICE_TIER_KEYS = frozenset({
    "sprint_499", "data_pack_1500", "managed_ops_2999",
    "managed_ops_4999", "custom_ai_15000",
})
SERVICE_TIERS: dict[str, dict[str, Any]] = {}



class PaymentLinkRequest(BaseModel):
    service_tier: str | None = Field(
        None,
        description="Historical metadata only; current links require an approved customer-specific invoice amount",
    )
    amount_sar: float | None = Field(None, description="Amount in SAR for custom invoices")
    amount_halalas: int | None = Field(None, description="Amount in halalas for custom invoices")
    customer_name: str = Field(..., min_length=1)
    customer_email: str = ""
    account_id: str = ""
    pilot_id: str = ""
    callback_url: str = ""
    description: str = ""
    notes: str = ""


class PaymentLinkResponse(BaseModel):
    payment_url: str
    invoice_id: str
    invoice_ref: str
    amount_sar: int
    service_name_ar: str
    service_name_en: str
    is_live_mode: bool
    expires_at: str
    approval_status: str = "approval_required"
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        import json
        return cast(dict[str, Any], json.loads(self.model_dump_json()))


class PaymentLinkError(Exception):
    pass


async def create_payment_link(req: PaymentLinkRequest) -> PaymentLinkResponse:
    """Generate a Moyasar hosted invoice link for a Dealix service tier.

    Raises PaymentLinkError if the tier is unknown or Moyasar call fails.
    In sandbox mode (default), returns a placeholder URL with invoice_id prefixed 'sandbox_'.
    """
    if req.service_tier:
        if req.service_tier in LEGACY_FIXED_PRICE_TIER_KEYS:
            raise PaymentLinkError(
                "Legacy fixed-price tier is retired; use the approved named-customer invoice amount."
            )
        raise PaymentLinkError(
            "Service tiers do not carry current pricing authority; use an approved named-customer invoice amount."
        )

    if req.amount_halalas is None and req.amount_sar is None:
        raise PaymentLinkError(
            "Customer-specific payment links require amount_sar or amount_halalas from an approved invoice."
        )
    if req.amount_halalas is not None:
        amount_halalas = req.amount_halalas
        amount_sar = req.amount_sar if req.amount_sar is not None else (amount_halalas / 100)
    else:
        assert req.amount_sar is not None
        amount_halalas = int(req.amount_sar * 100)
        amount_sar = req.amount_sar
    description = req.description or f"Dealix Invoice — {req.customer_name}"
    if req.notes:
        description += f" — {req.notes}"
    service_name_ar = "فاتورة Dealix مخصصة للعميل"
    service_name_en = "Customer-Specific Dealix Invoice"

    expires_at = (datetime.now(UTC) + timedelta(days=7)).isoformat()

    if not _LIVE_MODE:
        # Sandbox mode — return placeholder without hitting Moyasar API
        import hashlib
        sandbox_id = "sandbox_" + hashlib.sha256(
            f"{req.account_id}{req.service_tier or 'custom'}{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:12]
        return PaymentLinkResponse(
            payment_url=f"https://sandbox.moyasar.com/invoices/{sandbox_id}",
            invoice_id=sandbox_id,
            invoice_ref=sandbox_id,
            amount_sar=amount_sar,
            service_name_ar=service_name_ar,
            service_name_en=service_name_en,
            is_live_mode=False,
            expires_at=expires_at,
        )

    # Live mode — call Moyasar
    from dealix.payments.moyasar import MoyasarClient
    client = MoyasarClient()
    metadata: dict[str, str] = {
        "account_id": req.account_id or "",
        "pilot_id": req.pilot_id or "",
        "customer_name": req.customer_name,
        "service_tier": req.service_tier or "custom",
    }
    try:
        invoice = await client.create_invoice(
            amount_halalas=amount_halalas,
            description=description,
            callback_url=req.callback_url or None,
            metadata=metadata,
        )
    except Exception as exc:
        raise PaymentLinkError(f"Moyasar API error: {exc}") from exc

    return PaymentLinkResponse(
        payment_url=invoice.get("url", ""),
        invoice_id=invoice.get("id", ""),
        invoice_ref=invoice.get("id", ""),
        amount_sar=amount_sar,
        service_name_ar=service_name_ar,
        service_name_en=service_name_en,
        is_live_mode=True,
        expires_at=expires_at,
    )
