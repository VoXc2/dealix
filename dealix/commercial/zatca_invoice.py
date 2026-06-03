"""ZATCA e-invoice — Phase 2 compliant issuance layer.

Two entry points:

1. ``issue_zatca_invoice(payment=...)`` — lightweight, non-fatal wrapper used
   by the Moyasar payment webhook.  Delegates XML+QR generation to
   ``integrations.zatca`` when present.

2. ``generate_phase2_invoice(payload)`` — full Phase 2 invoice generation
   using the rich ``integrations.zatca.InvoiceGenerator``. Returns XML,
   Base64 XML, TLV QR code, and totals.

Phase 2 mandate:
  - B2B standard invoices (>1000 SAR): real-time clearance required
  - B2C simplified invoices: report within 24 hours
  - All invoices: UBL 2.1 XML with TLV QR code
  - Hash chain for invoice integrity (previous_invoice_hash field)
  - 15% KSA VAT

Arabic business names are supported via UTF-8 XML encoding.

Environment variables:
  ZATCA_CSID              — Cryptographic Stamp Identifier
  ZATCA_SECRET            — ZATCA API secret
  ZATCA_SANDBOX           — "true" (default) | "false" for production
  ZATCA_SELLER_VAT_NUMBER — 15-digit VAT number
  ZATCA_SELLER_NAME       — Seller name (Arabic or English)
  ZATCA_SELLER_CITY       — Seller city
  ZATCA_SELLER_CRN        — Commercial Registration Number
  ZATCA_SELLER_STREET     — Street address
  ZATCA_SELLER_POSTAL     — Postal code
"""

from __future__ import annotations

import logging
import os
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

log = logging.getLogger(__name__)

_SANDBOX = os.getenv("ZATCA_SANDBOX", "true").lower() not in ("false", "0", "no")
_VAT_RATE = 0.15  # 15% KSA VAT
_SELLER_VAT = os.getenv("ZATCA_SELLER_VAT_NUMBER", "")
_SELLER_NAME = os.getenv("ZATCA_SELLER_NAME", "Dealix")
_SELLER_CITY = os.getenv("ZATCA_SELLER_CITY", "Riyadh")
_SELLER_CRN = os.getenv("ZATCA_SELLER_CRN", "1010000000")
_SELLER_STREET = os.getenv("ZATCA_SELLER_STREET", "King Fahd Road")
_SELLER_POSTAL = os.getenv("ZATCA_SELLER_POSTAL", "12345")


# ---------------------------------------------------------------------------
# Phase 2 invoice result schema
# ---------------------------------------------------------------------------


@dataclass
class Phase2InvoiceResult:
    """Result of a Phase 2 invoice generation."""

    invoice_number: str
    invoice_uuid: str
    invoice_type: str  # "standard" | "simplified"
    xml_string: str
    xml_b64: str
    qr_code_b64: str
    grand_total_sar: str
    vat_total_sar: str
    subtotal_sar: str
    is_b2b: bool
    sandbox: bool
    hash_chain_ref: str  # Base64 hash of this invoice (for next invoice's PIH)

    def to_dict(self) -> dict[str, Any]:
        return {
            "invoice_number": self.invoice_number,
            "invoice_uuid": self.invoice_uuid,
            "invoice_type": self.invoice_type,
            "xml_b64": self.xml_b64,
            "qr_code_b64": self.qr_code_b64,
            "grand_total_sar": self.grand_total_sar,
            "vat_total_sar": self.vat_total_sar,
            "subtotal_sar": self.subtotal_sar,
            "is_b2b": self.is_b2b,
            "sandbox": self.sandbox,
            "hash_chain_ref": self.hash_chain_ref,
        }


async def issue_zatca_invoice(*, payment: dict[str, Any]) -> dict[str, Any]:
    """Issue a ZATCA-compliant e-invoice for a confirmed Moyasar payment.

    Returns a result dict with `status` and `invoice_uuid`.
    Never raises — logs errors and returns `{"status": "skipped", "reason": ...}`.
    """
    csid = os.getenv("ZATCA_CSID", "")
    secret = os.getenv("ZATCA_SECRET", "")

    if not csid or not secret:
        log.info(
            "zatca_invoice_skipped: ZATCA_CSID/ZATCA_SECRET not configured — "
            "set in Railway env vars to enable e-invoicing"
        )
        return {"status": "skipped", "reason": "zatca_creds_not_configured"}

    amount_halalas = payment.get("amount", 0)
    amount_sar = amount_halalas / 100
    vat_amount = round(amount_sar * _VAT_RATE / (1 + _VAT_RATE), 2)
    base_amount = round(amount_sar - vat_amount, 2)
    payment_id = payment.get("id", "")
    source = payment.get("source", {}) if isinstance(payment.get("source"), dict) else {}
    customer_name = source.get("company", source.get("name", "العميل"))
    invoice_uuid = str(uuid.uuid4())
    issue_date = datetime.now(UTC).strftime("%Y-%m-%d")
    issue_time = datetime.now(UTC).strftime("%H:%M:%S")

    # Determine invoice type: B2B (clearance) vs B2C (simplified/report)
    is_b2b = amount_sar > 1000

    try:
        from integrations.zatca import FatoorahClient, build_invoice_xml

        xml_b64 = build_invoice_xml(
            invoice_uuid=invoice_uuid,
            issue_date=issue_date,
            issue_time=issue_time,
            seller_name=_SELLER_NAME,
            seller_vat=_SELLER_VAT,
            seller_city=_SELLER_CITY,
            buyer_name=customer_name,
            line_amount=base_amount,
            vat_amount=vat_amount,
            total_amount=amount_sar,
            is_b2b=is_b2b,
            payment_ref=payment_id,
        )

        client = FatoorahClient(csid=csid, secret=secret, sandbox=_SANDBOX)

        if is_b2b:
            result = await client.clear_invoice(xml_b64=xml_b64, uuid_value=invoice_uuid)
            action = "clearance"
        else:
            result = await client.report_invoice(xml_b64=xml_b64, uuid_value=invoice_uuid)
            action = "report"

        log.info(
            "zatca_invoice_issued action=%s uuid=%s amount_sar=%.2f sandbox=%s",
            action, invoice_uuid, amount_sar, _SANDBOX,
        )
        return {
            "status": "issued",
            "action": action,
            "invoice_uuid": invoice_uuid,
            "amount_sar": amount_sar,
            "vat_amount": vat_amount,
            "sandbox": _SANDBOX,
            "zatca_response": result,
        }

    except ImportError:
        log.warning("zatca_invoice_skipped: integrations.zatca not available")
        return {"status": "skipped", "reason": "zatca_module_unavailable"}
    except Exception as exc:
        log.error("zatca_invoice_failed uuid=%s error=%s", invoice_uuid, exc)
        return {"status": "error", "reason": str(exc), "invoice_uuid": invoice_uuid}


# ---------------------------------------------------------------------------
# Phase 2 full generation
# ---------------------------------------------------------------------------


def generate_phase2_invoice(
    *,
    invoice_number: str,
    buyer_name: str,
    buyer_name_ar: str = "",
    amount_sar: float,
    description: str = "Revenue Intelligence Sprint",
    is_b2b: bool | None = None,
    buyer_vat: str | None = None,
    previous_invoice_hash: str | None = None,
    invoice_series: str = "DEALIX01",
    notes: str = "",
) -> Phase2InvoiceResult:
    """Generate a ZATCA Phase 2 compliant invoice locally (no API call).

    Returns a :class:`Phase2InvoiceResult` with the XML, Base64 XML, TLV QR
    code, and totals. The ``hash_chain_ref`` field should be stored and passed
    as ``previous_invoice_hash`` for the next invoice.

    :param invoice_number: Human-readable invoice number (e.g. "INV-2026-001").
    :param buyer_name: Buyer name (Arabic business names supported).
    :param buyer_name_ar: Optional Arabic version of the buyer name.
    :param amount_sar: Invoice total in SAR (VAT-inclusive).
    :param description: Line item description.
    :param is_b2b: Override B2B/B2C detection. If None, inferred from amount > 1000.
    :param buyer_vat: Buyer VAT number (required for B2B standard invoices).
    :param previous_invoice_hash: PIH from the previous invoice (hash chain).
    :param invoice_series: ZATCA series code.
    :param notes: Optional invoice note.
    """
    import base64
    import hashlib

    from integrations.zatca import (
        BuyerInfo,
        InvoiceGenerator,
        LineItem,
        SellerInfo,
        ZATCAInvoicePayload,
    )

    if is_b2b is None:
        is_b2b = amount_sar > 1000.0

    invoice_type = "standard" if is_b2b else "simplified"
    display_name = buyer_name_ar or buyer_name

    # Back-calculate net + VAT from VAT-inclusive total.
    amount_d = Decimal(str(round(amount_sar, 2)))
    vat_d = (amount_d * Decimal("0.15") / Decimal("1.15")).quantize(Decimal("0.01"))
    net_d = (amount_d - vat_d).quantize(Decimal("0.01"))

    seller = SellerInfo(
        name=_SELLER_NAME,
        vat_number=_SELLER_VAT or "300000000000000",
        crn_number=_SELLER_CRN,
        street=_SELLER_STREET,
        city=_SELLER_CITY,
        postal_code=_SELLER_POSTAL,
    )
    buyer = BuyerInfo(
        name=display_name,
        vat_number=buyer_vat,
    )
    line_items = [
        LineItem(
            description=description,
            quantity=Decimal("1"),
            unit_price_sar=net_d,
        )
    ]
    payload = ZATCAInvoicePayload(
        invoice_type=invoice_type,
        seller=seller,
        buyer=buyer,
        line_items=line_items,
        invoice_number=invoice_number,
        invoice_series=invoice_series,
        previous_invoice_hash=previous_invoice_hash,
        notes=notes,
    )

    gen = InvoiceGenerator()
    xml_string, xml_b64, qr_code_b64 = gen.generate(payload)

    # Compute this invoice's hash for use as the next invoice's PIH.
    hash_chain_ref = base64.b64encode(
        hashlib.sha256(xml_string.encode("utf-8")).digest()
    ).decode("ascii")

    inv_uuid = str(uuid.uuid4())

    return Phase2InvoiceResult(
        invoice_number=invoice_number,
        invoice_uuid=inv_uuid,
        invoice_type=invoice_type,
        xml_string=xml_string,
        xml_b64=xml_b64,
        qr_code_b64=qr_code_b64,
        grand_total_sar=str(payload.grand_total),
        vat_total_sar=str(payload.vat_total),
        subtotal_sar=str(payload.subtotal),
        is_b2b=is_b2b,
        sandbox=_SANDBOX,
        hash_chain_ref=hash_chain_ref,
    )


def compute_vat(amount_sar_inclusive: float) -> dict[str, float]:
    """Compute VAT breakdown from a VAT-inclusive SAR amount.

    Returns {"net": ..., "vat": ..., "total": ...} (all rounded to 2 dp).
    """
    total = round(amount_sar_inclusive, 2)
    vat = round(total * 0.15 / 1.15, 2)
    net = round(total - vat, 2)
    return {"net": net, "vat": vat, "total": total}


__all__ = [
    "Phase2InvoiceResult",
    "compute_vat",
    "generate_phase2_invoice",
    "issue_zatca_invoice",
]
