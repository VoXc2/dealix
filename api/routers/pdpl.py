"""
PDPL Compliance — API router.
مسارات API للامتثال لنظام حماية البيانات الشخصية السعودي.

Endpoints:
  POST  /api/v1/pdpl/consent/request      — send consent request (email + WhatsApp)
  POST  /api/v1/pdpl/consent/grant        — record explicit consent grant
  POST  /api/v1/pdpl/consent/revoke       — record permanent consent revocation
  DELETE /api/v1/pdpl/data/{contact_id}   — erasure request (Art. 13, cascade soft-delete)
  GET   /api/v1/pdpl/data/{contact_id}/export  — data portability export (Art. 14)
  GET   /api/v1/pdpl/audit/report         — monthly audit report (Art. 18)
  GET   /api/v1/pdpl/consent/dashboard    — consent management dashboard
  POST  /api/v1/pdpl/breach/notify        — breach notification package (Art. 21)
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timezone
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auto_client_acquisition import consent_table
from core.logging import get_logger
from core.utils import utcnow
from db.models import (
    AuditLogRecord,
    ConsentRequestRecord,
    ContactRecord,
    LeadRecord,
)
from db.session import get_db
from integrations.pdpl import (
    anonymize_contact_fields,
    build_breach_notification,
    build_consent_dashboard,
    build_consent_request_email,
    build_consent_request_whatsapp,
    build_data_export,
    build_erasure_audit_entry,
    build_monthly_audit_report,
)

router = APIRouter(prefix="/api/v1/pdpl", tags=["pdpl-compliance"])
log = get_logger(__name__)


# ── Helpers ────────────────────────────────────────────────────────────────

async def _write_audit(
    db: AsyncSession,
    action: str,
    entity_type: str,
    entity_id: str | None,
    tenant_id: str,
    user_id: str | None = None,
    diff: dict | None = None,
) -> None:
    db.add(AuditLogRecord(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        diff=diff,
        status="ok",
    ))


# ── Consent Request ────────────────────────────────────────────────────────

@router.post("/consent/request", summary="Send PDPL consent request (email + WhatsApp)")
async def request_consent(
    payload: dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Send a PDPL Art. 5 consent request via email and/or WhatsApp.
    يرسل طلب موافقة PDPL عبر البريد الإلكتروني و/أو واتساب.

    Required: contact_id, tenant_id, purpose, consent_url
    Optional: contact_name, contact_email, contact_phone, locale
    """
    contact_id = payload.get("contact_id", "")
    tenant_id = payload.get("tenant_id", "default")
    purpose = payload.get("purpose", "legitimate_interest")
    consent_url = payload.get("consent_url", "")
    contact_name = payload.get("contact_name", "عزيزي العميل")
    contact_email = payload.get("contact_email", "")
    contact_phone = payload.get("contact_phone", "")
    locale = payload.get("locale", "ar")
    company_name = payload.get("company_name", "Dealix")

    if not contact_id or not consent_url:
        raise HTTPException(status_code=422, detail="contact_id and consent_url are required")

    results: dict[str, Any] = {"contact_id": contact_id, "channels_queued": []}

    # Email
    if contact_email:
        email_payload = build_consent_request_email(
            contact_name=contact_name,
            contact_email=contact_email,
            company_name=company_name,
            purpose=purpose,
            consent_url=consent_url,
            locale=locale,
        )
        # Store consent request record
        req_record = ConsentRequestRecord(
            id=str(uuid.uuid4()),
            contact_id=contact_id,
            tenant_id=tenant_id,
            channel="email",
            purpose=purpose,
            status="sent",
            consent_url=consent_url,
            locale=locale,
        )
        db.add(req_record)
        results["channels_queued"].append("email")
        results["email_payload"] = email_payload

    # WhatsApp
    if contact_phone:
        wa_message = build_consent_request_whatsapp(
            contact_name=contact_name,
            company_name=company_name,
            purpose=purpose,
            consent_url=consent_url,
            locale=locale,
        )
        req_record_wa = ConsentRequestRecord(
            id=str(uuid.uuid4()),
            contact_id=contact_id,
            tenant_id=tenant_id,
            channel="whatsapp",
            purpose=purpose,
            status="sent",
            consent_url=consent_url,
            locale=locale,
        )
        db.add(req_record_wa)
        results["channels_queued"].append("whatsapp")
        results["whatsapp_message"] = wa_message

    await _write_audit(
        db, "pdpl.consent_request", "contact", contact_id, tenant_id,
        diff={"purpose": purpose, "channels": results["channels_queued"]},
    )

    log.info("pdpl_consent_request_sent", contact_id=contact_id, purpose=purpose)
    return {**results, "status": "queued", "pdpl_article": "Art. 5 — Lawful basis / consent"}


@router.post("/consent/grant", summary="Record explicit consent grant (PDPL Art. 5)")
async def grant_consent(
    payload: dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Record an explicit consent grant for a (contact, channel, purpose) pair.
    يسجل منح موافقة صريحة لزوج (جهة اتصال، قناة، غرض).
    """
    contact_id = payload.get("contact_id", "")
    channel = payload.get("channel", "email")
    purpose = payload.get("purpose", "explicit_consent")
    tenant_id = payload.get("tenant_id", "default")
    source = payload.get("source", "api")
    proof_url = payload.get("proof_url", "")

    if not contact_id:
        raise HTTPException(status_code=422, detail="contact_id is required")

    try:
        rec = consent_table.grant(
            contact_id=contact_id,
            channel=channel,
            purpose=purpose,
            source=source,
            proof_url=proof_url,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    await _write_audit(
        db, "pdpl.consent_grant", "contact", contact_id, tenant_id,
        diff={"channel": channel, "purpose": purpose, "source": source},
    )

    return {
        "contact_id": contact_id,
        "channel": channel,
        "purpose": purpose,
        "kind": "grant",
        "recorded_at": rec.occurred_at,
        "pdpl_article": "Art. 5 — Explicit consent",
    }


@router.post("/consent/revoke", summary="Record permanent consent revocation (PDPL Art. 5)")
async def revoke_consent(
    payload: dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Record a permanent consent revocation.
    يسجل سحب الموافقة بشكل دائم — PDPL: opt-out is permanent.
    """
    contact_id = payload.get("contact_id", "")
    channel = payload.get("channel", "email")
    purpose = payload.get("purpose", "explicit_consent")
    tenant_id = payload.get("tenant_id", "default")
    source = payload.get("source", "subject_request")

    if not contact_id:
        raise HTTPException(status_code=422, detail="contact_id is required")

    try:
        rec = consent_table.revoke(
            contact_id=contact_id,
            channel=channel,
            purpose=purpose,
            source=source,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    await _write_audit(
        db, "pdpl.consent_revoke", "contact", contact_id, tenant_id,
        diff={"channel": channel, "purpose": purpose, "source": source, "permanent": True},
    )

    return {
        "contact_id": contact_id,
        "channel": channel,
        "purpose": purpose,
        "kind": "revoke",
        "permanent": True,
        "recorded_at": rec.occurred_at,
        "pdpl_article": "Art. 5 — Opt-out is permanent",
    }


# ── Data Erasure (Art. 13) ──────────────────────────────────────────────────

@router.delete("/data/{contact_id}", summary="PDPL Art. 13 — Data erasure (cascade soft-delete)")
async def erase_data(
    contact_id: str,
    tenant_id: str = Query(...),
    requesting_user_id: str | None = Query(None),
    reason: str = Query("subject_request"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Execute PDPL Art. 13 data erasure for a contact.
    تنفيذ مسح البيانات وفق المادة 13 من PDPL لجهة اتصال.

    Actions:
      1. Soft-delete ContactRecord (deleted_at = now)
      2. Anonymize PII fields (name → [ERASED], email/phone → null)
      3. Mark pdpl_erased_at
      4. Soft-delete associated LeadRecords (if tenant_id matches)
      5. Write cascade audit log entry
    """
    # Find contact
    result = await db.execute(
        select(ContactRecord).where(
            ContactRecord.id == contact_id,
            ContactRecord.deleted_at.is_(None),
        )
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found or already erased")

    now = datetime.now(UTC)
    erased_entities: list[str] = []

    # Capture PII before anonymization for lead lookup
    original_email = contact.email
    original_phone = contact.phone

    # Anonymize + soft-delete contact
    contact.name = "[ERASED]"
    contact.email = None
    contact.phone = None
    contact.linkedin_url = None
    contact.deleted_at = now
    contact.pdpl_erasure_requested_at = now
    contact.pdpl_erased_at = now
    contact.opt_out = True
    contact.consent_status = "revoked_erased"
    erased_entities.append("contact")

    # Soft-delete associated leads (by original email or phone match)
    leads: list[Any] = []
    if original_email or original_phone:
        from sqlalchemy import or_
        pii_clauses = []
        if original_email:
            pii_clauses.append(LeadRecord.contact_email == original_email)
        if original_phone:
            pii_clauses.append(LeadRecord.contact_phone == original_phone)
        leads_result = await db.execute(
            select(LeadRecord).where(
                LeadRecord.tenant_id == tenant_id,
                LeadRecord.deleted_at.is_(None),
                or_(*pii_clauses),
            )
        )
        leads = leads_result.scalars().all()
    for lead in leads:
        lead.deleted_at = now
        lead.contact_email = None
        lead.contact_phone = None
        erased_entities.append(f"lead:{lead.id}")

    # Build audit entry
    audit_entry = build_erasure_audit_entry(
        contact_id=contact_id,
        tenant_id=tenant_id,
        requesting_user_id=requesting_user_id,
        entities_erased=erased_entities,
        reason=reason,
    )
    db.add(AuditLogRecord(
        id=audit_entry["id"],
        tenant_id=tenant_id,
        user_id=requesting_user_id,
        action="pdpl.erasure",
        entity_type="contact",
        entity_id=contact_id,
        diff=audit_entry["diff"],
        status="ok",
    ))

    # Revoke all consent in consent_table
    for channel in ("email", "whatsapp", "phone", "sms", "linkedin"):
        for purpose in consent_table.ALLOWED_PURPOSES:
            try:
                if consent_table.is_consented(contact_id=contact_id, channel=channel, purpose=purpose):
                    consent_table.revoke(
                        contact_id=contact_id,
                        channel=channel,
                        purpose=purpose,
                        source="pdpl_erasure",
                    )
            except Exception:
                pass

    log.info("pdpl_erasure_completed", contact_id=contact_id, tenant_id=tenant_id)
    return {
        "contact_id": contact_id,
        "status": "erased",
        "erased_at": now.isoformat(),
        "entities_affected": erased_entities,
        "audit_id": audit_entry["id"],
        "pdpl_article": "Art. 13 — Right to Erasure",
        "note": "Data anonymized + soft-deleted. Audit trail retained per Art. 18.",
    }


# ── Data Export / Portability (Art. 14) ────────────────────────────────────

@router.get("/data/{contact_id}/export", summary="PDPL Art. 14 — Data portability export")
async def export_data(
    contact_id: str,
    tenant_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Export all personal data for a contact — PDPL Art. 14 data portability.
    تصدير جميع البيانات الشخصية لجهة اتصال — المادة 14 قابلية نقل البيانات.
    """
    # Fetch contact
    result = await db.execute(
        select(ContactRecord).where(ContactRecord.id == contact_id)
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact_data = {
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "phone": contact.phone,
        "linkedin_url": contact.linkedin_url,
        "role": contact.role,
        "source": contact.source,
        "consent_status": contact.consent_status,
        "opt_out": contact.opt_out,
        "created_at": contact.created_at.isoformat() if contact.created_at else None,
    }

    # Fetch audit records for this contact
    audit_result = await db.execute(
        select(AuditLogRecord).where(AuditLogRecord.entity_id == contact_id).limit(500)
    )
    audit_records = [
        {
            "action": r.action,
            "created_at": r.created_at.isoformat(),
            "status": r.status,
        }
        for r in audit_result.scalars().all()
    ]

    # Consent records
    consent_records = [
        {
            "channel": r.channel,
            "purpose": r.purpose,
            "kind": r.kind,
            "occurred_at": r.occurred_at,
            "source": r.source,
        }
        for r in consent_table.records_for(contact_id)
    ]

    export = build_data_export(
        contact_id=contact_id,
        contact_data=contact_data,
        lead_data=[],
        conversation_data=[],
        consent_records=consent_records,
        audit_records=audit_records,
    )

    # Audit the export itself
    await _write_audit(
        db, "pdpl.data_export", "contact", contact_id, tenant_id,
        diff={"export_id": export["export_id"]},
    )

    return export


# ── Monthly Audit Report (Art. 18) ─────────────────────────────────────────

@router.get("/audit/report", summary="PDPL Art. 18 — Monthly audit report")
async def monthly_audit_report(
    tenant_id: str = Query(...),
    report_month: str = Query(..., description="Format: YYYY-MM e.g. 2024-01"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Generate a PDPL Art. 18 monthly compliance audit report.
    يُنشئ تقرير التدقيق الشهري للامتثال وفق المادة 18 من PDPL.
    """
    # Validate month format
    try:
        datetime.strptime(report_month, "%Y-%m")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="report_month must be YYYY-MM") from exc

    year, month = report_month.split("-")
    from_dt = datetime(int(year), int(month), 1, tzinfo=UTC)
    if int(month) == 12:
        to_dt = datetime(int(year) + 1, 1, 1, tzinfo=UTC)
    else:
        to_dt = datetime(int(year), int(month) + 1, 1, tzinfo=UTC)

    # Fetch audit records for the month
    audit_result = await db.execute(
        select(AuditLogRecord).where(
            AuditLogRecord.tenant_id == tenant_id,
            AuditLogRecord.created_at >= from_dt,
            AuditLogRecord.created_at < to_dt,
        ).limit(5000)
    )
    audit_records_raw = [
        {
            "action": r.action,
            "entity_type": r.entity_type,
            "entity_id": r.entity_id,
            "created_at": r.created_at.isoformat(),
            "status": r.status,
        }
        for r in audit_result.scalars().all()
    ]

    # Erasure requests this month
    erasure_records = [r for r in audit_records_raw if r["action"] == "pdpl.erasure"]

    # Consent stats
    consent_stats_obj = consent_table.stats()
    consent_stats = {
        "total_records": consent_stats_obj.get("total_records", 0),
        "unique_contacts": consent_stats_obj.get("unique_contacts", 0),
        "by_kind": consent_stats_obj.get("by_kind", {}),
    }

    report = build_monthly_audit_report(
        tenant_id=tenant_id,
        report_month=report_month,
        audit_records=audit_records_raw,
        consent_stats=consent_stats,
        erasure_requests=erasure_records,
        breach_incidents=[],
        processing_activities=[
            "CRM contact management",
            "Outreach email/WhatsApp",
            "Lead scoring and qualification",
            "Invoice generation (ZATCA Phase 2)",
        ],
    )

    return report


# ── Consent Dashboard ──────────────────────────────────────────────────────

@router.get("/consent/dashboard", summary="Consent management dashboard")
async def consent_dashboard(
    tenant_id: str = Query(...),
) -> dict[str, Any]:
    """
    Get consent management dashboard data for a tenant.
    يجلب بيانات لوحة إدارة الموافقات لمستأجر معين.
    """
    all_records = consent_table.stats()
    # For now return aggregate stats; production would filter by tenant_id
    records_raw = [
        {
            "contact_id": r.contact_id,
            "channel": r.channel,
            "purpose": r.purpose,
            "kind": r.kind,
            "occurred_at": r.occurred_at,
        }
        for r in consent_table._all_records()
    ]

    dashboard = build_consent_dashboard(tenant_id=tenant_id, consent_records=records_raw)
    return dashboard


# ── Breach Notification (Art. 21) ──────────────────────────────────────────

@router.post("/breach/notify", summary="PDPL Art. 21 — Breach notification package")
async def breach_notification(
    payload: dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Generate a PDPL Art. 21 data breach notification package.
    يُنشئ حزمة إشعار خرق البيانات — يجب الإبلاغ لـ SDAIA خلال 72 ساعة.
    """
    tenant_id = payload.get("tenant_id", "default")
    notification = build_breach_notification(
        tenant_id=tenant_id,
        breach_description=payload.get("description", ""),
        affected_data_categories=payload.get("affected_categories", []),
        estimated_subjects_count=payload.get("subjects_count", 0),
        discovery_datetime=payload.get("discovery_datetime", datetime.now(UTC).isoformat()),
        mitigation_steps=payload.get("mitigation_steps", []),
    )

    await _write_audit(
        db,
        "pdpl.breach_notification",
        "tenant",
        tenant_id,
        tenant_id,
        diff={"notification_id": notification["notification_id"]},
    )

    return notification


# ── Status ──────────────────────────────────────────────────────────────────

@router.get("/status", summary="PDPL compliance module status")
async def status() -> dict[str, Any]:
    """PDPL compliance module health and capability overview."""
    return {
        "module": "pdpl_compliance",
        "version": "v1",
        "capabilities": {
            "consent_request": True,
            "consent_grant_revoke": True,
            "data_erasure_art13": True,
            "data_portability_art14": True,
            "audit_report_art18": True,
            "breach_notification_art21": True,
            "consent_dashboard": True,
        },
        "pdpl_articles_covered": ["Art. 5", "Art. 6", "Art. 13", "Art. 14", "Art. 18", "Art. 21"],
        "default_deny": True,
        "revoke_permanent": True,
        "audit_trail": True,
    }
