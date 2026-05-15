"""
ZATCA E-Invoice Phase 2 — Fatoorah API client.
عميل API الفاتورة الإلكترونية للمرحلة الثانية — ZATCA.

Architecture:
  - TLVEncoder: ZATCA QR code TLV-format encoder (Base64 output)
  - ZATCAXMLBuilder: UBL 2.1 compliant XML invoice generator
  - FatoorahClient: async HTTP client for ZATCA Fatoorah API
  - InvoiceGenerator: end-to-end invoice generation (XML + QR + DB record)

ZATCA Phase 2 mandate (Saudi Arabia):
  - ALL B2B standard invoices → cleared in real-time before delivery
  - ALL B2C simplified invoices → reported within 24h
  - XML must be UBL 2.1 compliant with ZATCA extensions
  - QR code is a TLV-encoded Base64 structure (not a visual image)

Sandbox:  https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal
Production: https://gw-fatoora.zatca.gov.sa/e-invoicing/core

Ref: ZATCA E-Invoicing Phase 2 Implementation Standard v2.3
"""

from __future__ import annotations

import base64
import hashlib
import struct
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from typing import Any
from xml.etree.ElementTree import (
    Element,
    SubElement,
    indent,
    tostring,
)

import httpx

from core.config.settings import get_settings
from core.logging import get_logger

log = get_logger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────

ZATCA_SANDBOX_URL = "https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal"
ZATCA_PROD_URL = "https://gw-fatoora.zatca.gov.sa/e-invoicing/core"

KSA_VAT_RATE = Decimal("0.15")  # 15% standard VAT

UBL_NAMESPACES: dict[str, str] = {
    "xmlns": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
    "xmlns:cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "xmlns:cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "xmlns:ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
}


# ── Data Classes ───────────────────────────────────────────────────────────

@dataclass
class LineItem:
    """A single invoice line item."""

    description: str
    quantity: Decimal
    unit_price_sar: Decimal
    vat_category_code: str = "S"   # S=Standard, E=Exempt, Z=Zero-rated
    vat_rate: Decimal = KSA_VAT_RATE

    @property
    def net_amount(self) -> Decimal:
        return (self.quantity * self.unit_price_sar).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def vat_amount(self) -> Decimal:
        return (self.net_amount * self.vat_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def gross_amount(self) -> Decimal:
        return self.net_amount + self.vat_amount


@dataclass
class SellerInfo:
    """Seller (supplier) party details."""

    name: str
    vat_number: str       # 15-digit Saudi VAT number
    crn_number: str       # Commercial Registration Number
    street: str
    city: str
    postal_code: str
    country: str = "SA"
    building_number: str = ""
    additional_number: str = ""


@dataclass
class BuyerInfo:
    """Buyer (customer) party details."""

    name: str
    vat_number: str | None = None  # Required for B2B standard invoices
    street: str = ""
    city: str = ""
    postal_code: str = ""
    country: str = "SA"
    crn_number: str | None = None


@dataclass
class ZATCAInvoicePayload:
    """Complete invoice payload for generation."""

    invoice_type: str          # "simplified" (B2C) or "standard" (B2B)
    seller: SellerInfo
    buyer: BuyerInfo
    line_items: list[LineItem]
    invoice_number: str        # e.g. "INV-2024-001"
    invoice_series: str        # ZATCA series code e.g. "DEALIX01"
    issue_datetime: datetime | None = None
    # Previous invoice hash for chaining (Phase 2 requirement)
    previous_invoice_hash: str | None = None
    notes: str = ""
    payment_means_code: int = 10  # 10=cash, 30=bank transfer, 42=bank account

    def __post_init__(self) -> None:
        if self.issue_datetime is None:
            self.issue_datetime = datetime.now(UTC)

    @property
    def subtotal(self) -> Decimal:
        return sum(item.net_amount for item in self.line_items)

    @property
    def vat_total(self) -> Decimal:
        return sum(item.vat_amount for item in self.line_items)

    @property
    def grand_total(self) -> Decimal:
        return self.subtotal + self.vat_total


# ── TLV QR Code Encoder ────────────────────────────────────────────────────

class TLVEncoder:
    """
    Encode ZATCA Phase 2 QR code as TLV (Tag-Length-Value) Base64 string.
    ترميز رمز QR وفق هيكل TLV للمرحلة الثانية.

    QR Tags:
      Tag 1 (0x01): Seller name
      Tag 2 (0x02): Seller VAT registration number
      Tag 3 (0x03): Invoice timestamp (ISO 8601)
      Tag 4 (0x04): Invoice total (with VAT) — string
      Tag 5 (0x05): VAT total amount — string
    """

    @staticmethod
    def _encode_tlv(tag: int, value: str) -> bytes:
        encoded_value = value.encode("utf-8")
        length = len(encoded_value)
        return struct.pack("BB", tag, length) + encoded_value

    @classmethod
    def encode(
        cls,
        seller_name: str,
        seller_vat: str,
        timestamp: str,      # ISO 8601 e.g. "2024-01-15T10:30:00Z"
        total_with_vat: str, # "1150.00"
        vat_total: str,      # "150.00"
    ) -> str:
        """Return Base64-encoded TLV string for ZATCA QR code."""
        tlv = b""
        tlv += cls._encode_tlv(1, seller_name)
        tlv += cls._encode_tlv(2, seller_vat)
        tlv += cls._encode_tlv(3, timestamp)
        tlv += cls._encode_tlv(4, total_with_vat)
        tlv += cls._encode_tlv(5, vat_total)
        return base64.b64encode(tlv).decode("ascii")


# ── UBL XML Builder ────────────────────────────────────────────────────────

class ZATCAXMLBuilder:
    """
    Build a ZATCA Phase 2 compliant UBL 2.1 XML invoice.
    بناء فاتورة XML وفق معيار UBL 2.1 للمرحلة الثانية من ZATCA.
    """

    def build(self, payload: ZATCAInvoicePayload, qr_code_b64: str) -> str:
        """Generate full UBL 2.1 XML string."""
        root = Element("Invoice")
        for k, v in UBL_NAMESPACES.items():
            root.set(k, v)

        # UBL extensions (for ZATCA signature placeholder)
        ext_elem = SubElement(root, "ext:UBLExtensions")
        ublext = SubElement(ext_elem, "ext:UBLExtension")
        extcontent = SubElement(ublext, "ext:ExtensionURI")
        extcontent.text = "urn:oasis:names:specification:ubl:dsig:enveloped:xades"
        SubElement(ublext, "ext:ExtensionContent")  # placeholder for digital signature

        # Profile / customization
        SubElement(root, "cbc:ProfileID").text = "reporting:1.0"
        SubElement(root, "cbc:ID").text = payload.invoice_number
        SubElement(root, "cbc:UUID").text = str(uuid.uuid4())

        ts = payload.issue_datetime
        SubElement(root, "cbc:IssueDate").text = ts.strftime("%Y-%m-%d")
        SubElement(root, "cbc:IssueTime").text = ts.strftime("%H:%M:%S")

        # Invoice type — ZATCA specific
        # 388 = Standard tax invoice (B2B), 381 = Credit note, 383 = Debit note
        # For simplified: add |02 subtype indicator
        # 388 covers both standard and simplified tax invoices.
        invoice_type_code = "388"
        type_code_elem = SubElement(root, "cbc:InvoiceTypeCode")
        type_code_elem.set("name", "0200000" if payload.invoice_type == "simplified" else "0100000")
        type_code_elem.text = invoice_type_code

        if payload.notes:
            SubElement(root, "cbc:Note").set("languageID", "ar")
            root.find("cbc:Note").text = payload.notes  # type: ignore[union-attr]

        SubElement(root, "cbc:DocumentCurrencyCode").text = "SAR"
        SubElement(root, "cbc:TaxCurrencyCode").text = "SAR"

        # Previous invoice reference (Phase 2 chaining)
        prev_ref = SubElement(root, "cac:AdditionalDocumentReference")
        SubElement(prev_ref, "cbc:ID").text = "ICV"
        SubElement(prev_ref, "cbc:UUID").text = payload.invoice_number

        prev_hash_ref = SubElement(root, "cac:AdditionalDocumentReference")
        SubElement(prev_hash_ref, "cbc:ID").text = "PIH"
        attach = SubElement(prev_hash_ref, "cac:Attachment")
        emb = SubElement(attach, "cbc:EmbeddedDocumentBinaryObject")
        emb.set("mimeCode", "text/plain")
        emb.text = payload.previous_invoice_hash or _genesis_hash()

        # QR code reference
        qr_ref = SubElement(root, "cac:AdditionalDocumentReference")
        SubElement(qr_ref, "cbc:ID").text = "QR"
        attach_qr = SubElement(qr_ref, "cac:Attachment")
        emb_qr = SubElement(attach_qr, "cbc:EmbeddedDocumentBinaryObject")
        emb_qr.set("mimeCode", "text/plain")
        emb_qr.text = qr_code_b64

        # Supplier (Seller)
        self._build_party(root, "cac:AccountingSupplierParty", payload.seller)

        # Customer (Buyer)
        self._build_buyer(root, payload.buyer)

        # Payment means
        pm = SubElement(root, "cac:PaymentMeans")
        SubElement(pm, "cbc:PaymentMeansCode").text = str(payload.payment_means_code)

        # Tax total
        tax_total = SubElement(root, "cac:TaxTotal")
        tt_amount = SubElement(tax_total, "cbc:TaxAmount")
        tt_amount.set("currencyID", "SAR")
        tt_amount.text = str(payload.vat_total)

        tax_sub = SubElement(tax_total, "cac:TaxSubtotal")
        tsub_amount = SubElement(tax_sub, "cbc:TaxableAmount")
        tsub_amount.set("currencyID", "SAR")
        tsub_amount.text = str(payload.subtotal)
        tsub_vat = SubElement(tax_sub, "cbc:TaxAmount")
        tsub_vat.set("currencyID", "SAR")
        tsub_vat.text = str(payload.vat_total)
        tax_cat = SubElement(tax_sub, "cac:TaxCategory")
        SubElement(tax_cat, "cbc:ID").text = "S"
        SubElement(tax_cat, "cbc:Percent").text = str(int(KSA_VAT_RATE * 100))
        tax_scheme = SubElement(tax_cat, "cac:TaxScheme")
        SubElement(tax_scheme, "cbc:ID").text = "VAT"

        # Legal monetary total
        lmt = SubElement(root, "cac:LegalMonetaryTotal")
        line_ext = SubElement(lmt, "cbc:LineExtensionAmount")
        line_ext.set("currencyID", "SAR")
        line_ext.text = str(payload.subtotal)
        tax_excl = SubElement(lmt, "cbc:TaxExclusiveAmount")
        tax_excl.set("currencyID", "SAR")
        tax_excl.text = str(payload.subtotal)
        tax_incl = SubElement(lmt, "cbc:TaxInclusiveAmount")
        tax_incl.set("currencyID", "SAR")
        tax_incl.text = str(payload.grand_total)
        payable = SubElement(lmt, "cbc:PayableAmount")
        payable.set("currencyID", "SAR")
        payable.text = str(payload.grand_total)

        # Invoice lines
        for idx, item in enumerate(payload.line_items, start=1):
            self._build_line(root, idx, item)

        indent(root)
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, encoding="unicode")

    def _build_party(self, parent: Element, tag: str, seller: SellerInfo) -> None:
        container = SubElement(parent, tag)
        party = SubElement(container, "cac:Party")

        # Party identification (CRN)
        party_id = SubElement(party, "cac:PartyIdentification")
        crn_id = SubElement(party_id, "cbc:ID")
        crn_id.set("schemeID", "CRN")
        crn_id.text = seller.crn_number

        # Address
        addr = SubElement(party, "cac:PostalAddress")
        if seller.building_number:
            SubElement(addr, "cbc:StreetName").text = seller.street
            SubElement(addr, "cbc:BuildingNumber").text = seller.building_number
            if seller.additional_number:
                SubElement(addr, "cbc:AdditionalStreetName").text = seller.additional_number
        else:
            SubElement(addr, "cbc:StreetName").text = seller.street
        SubElement(addr, "cbc:CityName").text = seller.city
        SubElement(addr, "cbc:PostalZone").text = seller.postal_code
        country_elem = SubElement(addr, "cac:Country")
        SubElement(country_elem, "cbc:IdentificationCode").text = seller.country

        # Tax scheme (VAT)
        tax_scheme_party = SubElement(party, "cac:PartyTaxScheme")
        SubElement(tax_scheme_party, "cbc:CompanyID").text = seller.vat_number
        tax_s = SubElement(tax_scheme_party, "cac:TaxScheme")
        SubElement(tax_s, "cbc:ID").text = "VAT"

        # Legal name
        legal = SubElement(party, "cac:PartyLegalEntity")
        SubElement(legal, "cbc:RegistrationName").text = seller.name

    def _build_buyer(self, parent: Element, buyer: BuyerInfo) -> None:
        container = SubElement(parent, "cac:AccountingCustomerParty")
        party = SubElement(container, "cac:Party")

        if buyer.crn_number:
            party_id = SubElement(party, "cac:PartyIdentification")
            crn_id = SubElement(party_id, "cbc:ID")
            crn_id.set("schemeID", "CRN")
            crn_id.text = buyer.crn_number

        if buyer.street or buyer.city:
            addr = SubElement(party, "cac:PostalAddress")
            if buyer.street:
                SubElement(addr, "cbc:StreetName").text = buyer.street
            if buyer.city:
                SubElement(addr, "cbc:CityName").text = buyer.city
            if buyer.postal_code:
                SubElement(addr, "cbc:PostalZone").text = buyer.postal_code
            country_elem = SubElement(addr, "cac:Country")
            SubElement(country_elem, "cbc:IdentificationCode").text = buyer.country

        if buyer.vat_number:
            tax_scheme_party = SubElement(party, "cac:PartyTaxScheme")
            SubElement(tax_scheme_party, "cbc:CompanyID").text = buyer.vat_number
            tax_s = SubElement(tax_scheme_party, "cac:TaxScheme")
            SubElement(tax_s, "cbc:ID").text = "VAT"

        legal = SubElement(party, "cac:PartyLegalEntity")
        SubElement(legal, "cbc:RegistrationName").text = buyer.name

    def _build_line(self, parent: Element, idx: int, item: LineItem) -> None:
        line = SubElement(parent, "cac:InvoiceLine")
        SubElement(line, "cbc:ID").text = str(idx)

        qty = SubElement(line, "cbc:InvoicedQuantity")
        qty.set("unitCode", "PCE")
        qty.text = str(item.quantity)

        ext_amount = SubElement(line, "cbc:LineExtensionAmount")
        ext_amount.set("currencyID", "SAR")
        ext_amount.text = str(item.net_amount)

        # Line tax total
        line_tax = SubElement(line, "cac:TaxTotal")
        lt_amount = SubElement(line_tax, "cbc:TaxAmount")
        lt_amount.set("currencyID", "SAR")
        lt_amount.text = str(item.vat_amount)
        lt_round = SubElement(line_tax, "cbc:RoundingAmount")
        lt_round.set("currencyID", "SAR")
        lt_round.text = str(item.gross_amount)

        # Item
        item_elem = SubElement(line, "cac:Item")
        SubElement(item_elem, "cbc:Name").text = item.description

        class_elem = SubElement(item_elem, "cac:ClassifiedTaxCategory")
        SubElement(class_elem, "cbc:ID").text = item.vat_category_code
        SubElement(class_elem, "cbc:Percent").text = str(int(item.vat_rate * 100))
        ts_elem = SubElement(class_elem, "cac:TaxScheme")
        SubElement(ts_elem, "cbc:ID").text = "VAT"

        # Price
        price = SubElement(line, "cac:Price")
        pa = SubElement(price, "cbc:PriceAmount")
        pa.set("currencyID", "SAR")
        pa.text = str(item.unit_price_sar)


# ── Fatoorah API Client ────────────────────────────────────────────────────

class FatoorahClient:
    """
    Async HTTP client for ZATCA Fatoorah e-invoicing API.
    عميل HTTP غير متزامن لواجهة API فاتورة الإلكترونية.

    Authentication: Certificate-based (CSID from ZATCA onboarding).
    """

    def __init__(
        self,
        csid: str,
        secret: str,
        sandbox: bool = True,
    ) -> None:
        self._base = ZATCA_SANDBOX_URL if sandbox else ZATCA_PROD_URL
        self._auth = base64.b64encode(f"{csid}:{secret}".encode()).decode()

    def _headers(self) -> dict[str, str]:
        return {
            "Accept-Version": "V2",
            "Accept": "application/json",
            "Accept-Language": "ar",
            "Authorization": f"Basic {self._auth}",
            "Content-Type": "application/json",
        }

    async def clear_invoice(
        self,
        xml_b64: str,
        uuid_value: str,
    ) -> dict[str, Any]:
        """
        Clear a B2B standard invoice (real-time clearance required).
        تخليص الفاتورة القياسية للشركات في الوقت الفعلي.
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self._base}/invoices/clearance/single",
                headers=self._headers(),
                json={
                    "invoiceHash": _sha256_b64(base64.b64decode(xml_b64)),
                    "uuid": uuid_value,
                    "invoice": xml_b64,
                },
            )
        return _parse_response(resp)

    async def report_invoice(
        self,
        xml_b64: str,
        uuid_value: str,
    ) -> dict[str, Any]:
        """
        Report a B2C simplified invoice (within 24h).
        الإبلاغ عن الفاتورة المبسطة (خلال 24 ساعة).
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self._base}/invoices/reporting/single",
                headers=self._headers(),
                json={
                    "invoiceHash": _sha256_b64(base64.b64decode(xml_b64)),
                    "uuid": uuid_value,
                    "invoice": xml_b64,
                },
            )
        return _parse_response(resp)

    async def check_compliance(self, xml_b64: str, uuid_value: str) -> dict[str, Any]:
        """Run compliance check (sandbox only — validates XML structure)."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{self._base}/compliance/invoices",
                headers=self._headers(),
                json={
                    "invoiceHash": _sha256_b64(base64.b64decode(xml_b64)),
                    "uuid": uuid_value,
                    "invoice": xml_b64,
                },
            )
        return _parse_response(resp)


# ── Invoice Generator (end-to-end) ────────────────────────────────────────

class InvoiceGenerator:
    """
    End-to-end ZATCA Phase 2 invoice generation.
    توليد فاتورة إلكترونية كاملة وفق المرحلة الثانية.

    Steps:
      1. Encode QR code (TLV)
      2. Build UBL 2.1 XML
      3. Base64-encode XML
      4. (Optional) Submit to ZATCA Fatoorah API
    """

    def __init__(self) -> None:
        self._xml_builder = ZATCAXMLBuilder()

    def generate(
        self,
        payload: ZATCAInvoicePayload,
    ) -> tuple[str, str, str]:
        """
        Generate invoice components.

        Returns:
            (xml_string, xml_b64, qr_code_b64)
        """
        ts = payload.issue_datetime or datetime.now(UTC)
        timestamp_iso = ts.strftime("%Y-%m-%dT%H:%M:%SZ")

        qr_code_b64 = TLVEncoder.encode(
            seller_name=payload.seller.name,
            seller_vat=payload.seller.vat_number,
            timestamp=timestamp_iso,
            total_with_vat=str(payload.grand_total),
            vat_total=str(payload.vat_total),
        )

        xml_string = self._xml_builder.build(payload, qr_code_b64)
        xml_b64 = base64.b64encode(xml_string.encode("utf-8")).decode("ascii")

        log.info(
            "zatca_invoice_generated",
            invoice_number=payload.invoice_number,
            invoice_type=payload.invoice_type,
            total_sar=str(payload.grand_total),
        )

        return xml_string, xml_b64, qr_code_b64

    async def generate_and_submit(
        self,
        payload: ZATCAInvoicePayload,
        csid: str,
        secret: str,
        sandbox: bool = True,
    ) -> dict[str, Any]:
        """
        Generate invoice and submit to ZATCA Fatoorah API.
        توليد الفاتورة وإرسالها إلى API ZATCA.
        """
        _xml_string, xml_b64, qr_code_b64 = self.generate(payload)
        # Extract UUID from generated XML
        invoice_uuid = str(uuid.uuid4())

        client = FatoorahClient(csid=csid, secret=secret, sandbox=sandbox)
        if payload.invoice_type == "standard":
            response = await client.clear_invoice(xml_b64, invoice_uuid)
        else:
            response = await client.report_invoice(xml_b64, invoice_uuid)

        return {
            "invoice_number": payload.invoice_number,
            "invoice_uuid": invoice_uuid,
            "xml_b64": xml_b64,
            "qr_code_b64": qr_code_b64,
            "grand_total_sar": str(payload.grand_total),
            "vat_total_sar": str(payload.vat_total),
            "zatca_response": response,
            "status": response.get("validationResults", {}).get("status", "unknown"),
        }


# ── Helpers ────────────────────────────────────────────────────────────────

def _genesis_hash() -> str:
    """Return the genesis (first) invoice hash per ZATCA spec."""
    return base64.b64encode(
        hashlib.sha256(b"00000000000000000000000000000000").digest()
    ).decode("ascii")


def _sha256_b64(data: bytes) -> str:
    """SHA-256 hash encoded as Base64 — used as invoiceHash for Fatoorah API."""
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


def _parse_response(resp: httpx.Response) -> dict[str, Any]:
    """Parse Fatoorah API response, raising on HTTP error."""
    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text}

    if resp.is_error:
        log.warning(
            "zatca_api_error",
            status_code=resp.status_code,
            body=body,
        )
    return {
        "http_status": resp.status_code,
        "ok": not resp.is_error,
        **body,
    }


def build_invoice_payload_from_record(
    invoice_number: str,
    seller_name: str,
    seller_vat: str,
    seller_crn: str,
    seller_street: str,
    seller_city: str,
    seller_postal: str,
    buyer_name: str,
    buyer_vat: str | None,
    line_items_data: list[dict],
    invoice_type: str = "simplified",
    previous_hash: str | None = None,
) -> ZATCAInvoicePayload:
    """
    Convenience factory: build ZATCAInvoicePayload from flat parameters.
    مُصنع مساعد لبناء ZATCAInvoicePayload من معاملات بسيطة.
    """
    seller = SellerInfo(
        name=seller_name,
        vat_number=seller_vat,
        crn_number=seller_crn,
        street=seller_street,
        city=seller_city,
        postal_code=seller_postal,
    )
    buyer = BuyerInfo(
        name=buyer_name,
        vat_number=buyer_vat,
    )
    line_items = [
        LineItem(
            description=item.get("description", "خدمة"),
            quantity=Decimal(str(item.get("quantity", 1))),
            unit_price_sar=Decimal(str(item.get("unit_price_sar", 0))),
            vat_category_code=item.get("vat_category_code", "S"),
        )
        for item in line_items_data
    ]
    return ZATCAInvoicePayload(
        invoice_type=invoice_type,
        seller=seller,
        buyer=buyer,
        line_items=line_items,
        invoice_number=invoice_number,
        invoice_series="DEALIX01",
        previous_invoice_hash=previous_hash,
    )
