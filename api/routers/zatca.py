"""
ZATCA E-Invoice Phase 2 — API router.
مسارات API للفاتورة الإلكترونية للمرحلة الثانية — ZATCA.

Endpoints:
  POST   /api/v1/zatca/invoices          — generate a new e-invoice
  POST   /api/v1/zatca/invoices/{id}/submit  — submit to ZATCA Fatoorah API
  GET    /api/v1/zatca/invoices/{id}/status  — get clearance/reporting status
  GET    /api/v1/zatca/invoices           — list invoices for tenant
  POST   /api/v1/zatca/compliance/check   — sandbox compliance check
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timezone
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.settings import get_settings
from core.logging import get_logger
from core.utils import utcnow
from db.models import AuditLogRecord, ZATCAInvoiceRecord
from db.session import get_db
from integrations.zatca import (
    FatoorahClient,
    InvoiceGenerator,
    build_invoice_payload_from_record,
)

router = APIRouter(prefix="/api/v1/zatca", tags=["zatca"])
log = get_logger(__name__)
_generator = InvoiceGenerator()


# ── Helpers ────────────────────────────────────────────────────────────────

def _get_zatca_credentials() -> tuple[str, str, bool]:
    """
    Return (csid, secret, sandbox) from settings.
    يجلب بيانات اعتماد ZATCA من الإعدادات.
    """
    s = get_settings()
    csid_val = s.zatca_csid
    secret_val = s.zatca_secret
    csid = csid_val.get_secret_value() if csid_val else ""
    secret = secret_val.get_secret_value() if secret_val else ""
    sandbox = s.zatca_sandbox
    return csid, secret, sandbox


async def _audit(
    db: AsyncSession,
    action: str,
    entity_id: str,
    tenant_id: str,
    diff: dict | None = None,
) -> None:
    db.add(AuditLogRecord(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        action=action,
        entity_type="zatca_invoice",
        entity_id=entity_id,
        diff=diff,
        status="ok",
    ))


# ── Endpoints ──────────────────────────────────────────────────────────────

@router.post("/invoices", summary="Generate ZATCA Phase 2 e-invoice")
async def generate_invoice(
    payload: dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Generate a ZATCA Phase 2 compliant e-invoice (UBL 2.1 XML + QR code).
    يُنشئ فاتورة إلكترونية متوافقة مع المرحلة الثانية من ZATCA.

    Required fields:
      - tenant_id, invoice_number, invoice_type (simplified|standard)
      - seller: {name, vat_number, crn_number, street, city, postal_code}
      - buyer: {name, vat_number?}
      - line_items: [{description, quantity, unit_price_sar}]

    Optional:
      - deal_id, customer_id, previous_invoice_hash, notes
    """
    tenant_id = payload.get("tenant_id", "default")
    invoice_number = payload.get("invoice_number", "")
    invoice_type = payload.get("invoice_type", "simplified")

    if not invoice_number:
        raise HTTPException(status_code=422, detail="invoice_number is required")
    if invoice_type not in ("simplified", "standard"):
        raise HTTPException(status_code=422, detail="invoice_type must be 'simplified' or 'standard'")

    seller_data = payload.get("seller", {})
    buyer_data = payload.get("buyer", {})
    line_items_data = payload.get("line_items", [])

    if not seller_data.get("vat_number") or not seller_data.get("name"):
        raise HTTPException(status_code=422, detail="seller.name and seller.vat_number are required")
    if not buyer_data.get("name"):
        raise HTTPException(status_code=422, detail="buyer.name is required")
    if not line_items_data:
        raise HTTPException(status_code=422, detail="At least one line_item is required")

    # Check duplicate invoice number
    existing = await db.execute(
        select(ZATCAInvoiceRecord).where(ZATCAInvoiceRecord.invoice_number == invoice_number)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"Invoice {invoice_number} already exists")

    # Build and generate
    invoice_payload = build_invoice_payload_from_record(
        invoice_number=invoice_number,
        seller_name=seller_data["name"],
        seller_vat=seller_data["vat_number"],
        seller_crn=seller_data.get("crn_number", ""),
        seller_street=seller_data.get("street", ""),
        seller_city=seller_data.get("city", ""),
        seller_postal=seller_data.get("postal_code", ""),
        buyer_name=buyer_data["name"],
        buyer_vat=buyer_data.get("vat_number"),
        line_items_data=line_items_data,
        invoice_type=invoice_type,
        previous_hash=payload.get("previous_invoice_hash"),
    )

    try:
        _xml_string, xml_b64, qr_code_b64 = _generator.generate(invoice_payload)
    except Exception as exc:
        log.exception("zatca_generation_failed", error=str(exc))
        raise HTTPException(status_code=500, detail=f"Invoice generation failed: {exc}") from exc

    now_utc = datetime.now(UTC)
    invoice_record = ZATCAInvoiceRecord(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        deal_id=payload.get("deal_id"),
        customer_id=payload.get("customer_id"),
        invoice_number=invoice_number,
        invoice_type=invoice_type,
        issue_date=now_utc.strftime("%Y-%m-%d"),
        issue_time=now_utc.strftime("%H:%M:%S"),
        seller_vat_number=seller_data["vat_number"],
        buyer_vat_number=buyer_data.get("vat_number"),
        buyer_name=buyer_data["name"],
        subtotal_sar=float(invoice_payload.subtotal),
        vat_amount_sar=float(invoice_payload.vat_total),
        total_sar=float(invoice_payload.grand_total),
        vat_rate=0.15,
        line_items=line_items_data,
        zatca_xml_b64=xml_b64,
        qr_code_b64=qr_code_b64,
        zatca_status="draft",
    )
    db.add(invoice_record)

    await _audit(db, "zatca_invoice.create", invoice_record.id, tenant_id)
    await db.flush()

    log.info("zatca_invoice_created", invoice_number=invoice_number, tenant_id=tenant_id)
    return {
        "id": invoice_record.id,
        "invoice_number": invoice_number,
        "invoice_type": invoice_type,
        "status": "draft",
        "subtotal_sar": float(invoice_payload.subtotal),
        "vat_amount_sar": float(invoice_payload.vat_total),
        "total_sar": float(invoice_payload.grand_total),
        "qr_code_b64": qr_code_b64,
        "xml_b64": xml_b64,
        "created_at": now_utc.isoformat(),
    }


@router.post("/invoices/{invoice_id}/submit", summary="Submit invoice to ZATCA Fatoorah API")
async def submit_invoice(
    invoice_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Submit a draft invoice to ZATCA Fatoorah API for clearance/reporting.
    إرسال الفاتورة المسودة إلى API ZATCA للتخليص أو الإبلاغ.

    - standard invoices  → clearance endpoint (real-time, blocking)
    - simplified invoices → reporting endpoint (within 24h)
    """
    result = await db.execute(
        select(ZATCAInvoiceRecord).where(ZATCAInvoiceRecord.id == invoice_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if record.zatca_status not in ("draft", "error"):
        raise HTTPException(
            status_code=409,
            detail=f"Invoice is already in status '{record.zatca_status}' — cannot resubmit",
        )
    if not record.zatca_xml_b64:
        raise HTTPException(status_code=422, detail="Invoice has no XML — regenerate first")

    csid, secret, sandbox = _get_zatca_credentials()
    if not csid or not secret:
        # Sandbox mode without credentials: mark as simulated_cleared
        record.zatca_status = "reported" if record.invoice_type == "simplified" else "cleared"
        record.zatca_response = {"simulated": True, "note": "No ZATCA credentials configured"}
        record.zatca_cleared_at = datetime.now(UTC)
        await _audit(db, "zatca_invoice.submit_simulated", record.id, record.tenant_id)
        return {
            "id": record.id,
            "invoice_number": record.invoice_number,
            "status": record.zatca_status,
            "simulated": True,
            "message": "No ZATCA credentials configured — simulated submission",
        }

    record.zatca_status = "pending_clearance"

    try:
        client = FatoorahClient(csid=csid, secret=secret, sandbox=sandbox)
        invoice_uuid = str(uuid.uuid4())
        if record.invoice_type == "standard":
            response = await client.clear_invoice(record.zatca_xml_b64, invoice_uuid)
        else:
            response = await client.report_invoice(record.zatca_xml_b64, invoice_uuid)
    except Exception as exc:
        record.zatca_status = "error"
        record.zatca_response = {"error": str(exc)}
        await _audit(db, "zatca_invoice.submit_error", record.id, record.tenant_id, {"error": str(exc)})
        raise HTTPException(status_code=502, detail=f"ZATCA API error: {exc}") from exc

    record.zatca_response = response
    if response.get("ok"):
        record.zatca_status = "reported" if record.invoice_type == "simplified" else "cleared"
        record.zatca_cleared_at = datetime.now(UTC)
    else:
        record.zatca_status = "rejected"

    await _audit(
        db,
        "zatca_invoice.submitted",
        record.id,
        record.tenant_id,
        {"http_status": response.get("http_status"), "ok": response.get("ok")},
    )

    return {
        "id": record.id,
        "invoice_number": record.invoice_number,
        "status": record.zatca_status,
        "zatca_response": response,
    }


@router.get("/invoices/{invoice_id}/status", summary="Get ZATCA invoice clearance status")
async def invoice_status(
    invoice_id: str,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get the current ZATCA clearance/reporting status of an invoice.
    يجلب حالة التخليص الحالية للفاتورة.
    """
    result = await db.execute(
        select(ZATCAInvoiceRecord).where(ZATCAInvoiceRecord.id == invoice_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return {
        "id": record.id,
        "invoice_number": record.invoice_number,
        "invoice_type": record.invoice_type,
        "status": record.zatca_status,
        "issue_date": record.issue_date,
        "issue_time": record.issue_time,
        "subtotal_sar": record.subtotal_sar,
        "vat_amount_sar": record.vat_amount_sar,
        "total_sar": record.total_sar,
        "buyer_name": record.buyer_name,
        "seller_vat_number": record.seller_vat_number,
        "zatca_cleared_at": record.zatca_cleared_at.isoformat() if record.zatca_cleared_at else None,
        "zatca_response": record.zatca_response,
        "qr_code_b64": record.qr_code_b64,
        "has_xml": bool(record.zatca_xml_b64),
        "created_at": record.created_at.isoformat(),
    }


@router.get("/invoices", summary="List ZATCA invoices for a tenant")
async def list_invoices(
    tenant_id: str = Query(..., description="Tenant ID"),
    status: str | None = Query(None, description="Filter by status"),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    List all e-invoices for a tenant with optional status filter.
    يسرد جميع الفواتير الإلكترونية لمستأجر معين مع فلترة اختيارية.
    """
    q = select(ZATCAInvoiceRecord).where(ZATCAInvoiceRecord.tenant_id == tenant_id)
    if status:
        q = q.where(ZATCAInvoiceRecord.zatca_status == status)
    q = q.order_by(ZATCAInvoiceRecord.created_at.desc()).limit(limit).offset(offset)

    result = await db.execute(q)
    records = result.scalars().all()

    return {
        "tenant_id": tenant_id,
        "total": len(records),
        "invoices": [
            {
                "id": r.id,
                "invoice_number": r.invoice_number,
                "invoice_type": r.invoice_type,
                "status": r.zatca_status,
                "total_sar": r.total_sar,
                "vat_amount_sar": r.vat_amount_sar,
                "buyer_name": r.buyer_name,
                "issue_date": r.issue_date,
                "created_at": r.created_at.isoformat(),
            }
            for r in records
        ],
    }


@router.post("/compliance/check", summary="ZATCA sandbox compliance check")
async def compliance_check(
    payload: dict[str, Any] = Body(...),
) -> dict[str, Any]:
    """
    Run a compliance check on an invoice XML using the ZATCA sandbox.
    تشغيل فحص امتثال على XML الفاتورة باستخدام بيئة الاختبار.

    Requires: xml_b64 (Base64-encoded invoice XML)
    """
    xml_b64 = payload.get("xml_b64", "")
    if not xml_b64:
        raise HTTPException(status_code=422, detail="xml_b64 is required")

    csid, secret, _ = _get_zatca_credentials()
    if not csid or not secret:
        return {
            "status": "skipped",
            "message": "No ZATCA credentials configured — compliance check skipped",
            "sandbox": True,
        }

    try:
        client = FatoorahClient(csid=csid, secret=secret, sandbox=True)
        result = await client.check_compliance(xml_b64, str(uuid.uuid4()))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"ZATCA compliance check failed: {exc}") from exc

    return {
        "status": "completed",
        "sandbox": True,
        "result": result,
    }
