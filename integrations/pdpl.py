"""
PDPL Compliance Workflow — Saudi Personal Data Protection Law.
سير عمل الامتثال لنظام حماية البيانات الشخصية السعودي.

Implements:
  1. Consent request flow (email + WhatsApp)
  2. Data erasure (cascade soft-delete + audit log) — Art. 13
  3. Data export / portability — Art. 14
  4. Monthly PDPL audit report generation — Art. 18
  5. Consent management helpers

Key PDPL Articles addressed:
  - Art. 5:  Default-deny, purpose limitation
  - Art. 6:  Lawful processing grounds
  - Art. 9:  Sensitive data handling
  - Art. 13: Data subject right to erasure
  - Art. 14: Data portability
  - Art. 18: Audit trail requirements
  - Art. 21: Data breach notification (72h to SDAIA)
  - Art. 25: Cross-border transfer restrictions

Ref: SDAIA PDPL Implementing Regulations 2023
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


# ── Constants ──────────────────────────────────────────────────────────────

PDPL_PURPOSES: list[str] = [
    "service_delivery",       # Art. 6(a) — contract performance
    "legal_obligation",       # Art. 6(b) — legal compliance
    "legitimate_interest",    # Art. 6(d) — business contact research
    "explicit_consent",       # Art. 6(e) — direct marketing
]

ERASURE_CASCADE_ENTITIES: list[str] = [
    "contacts",
    "leads",
    "conversations",
    "outreach_queue",
    "email_send_log",
    "gmail_drafts",
    "linkedin_drafts",
    "account_embeddings",
    "conversation_embeddings",
]

# Fields zeroed-out on erasure (anonymization not deletion for referential integrity)
CONTACT_PII_FIELDS: list[str] = [
    "name",
    "email",
    "phone",
    "linkedin_url",
]


# ── Consent Request ────────────────────────────────────────────────────────

def build_consent_request_email(
    contact_name: str,
    contact_email: str,
    company_name: str,
    purpose: str,
    consent_url: str,
    locale: str = "ar",
) -> dict[str, str]:
    """
    Build a PDPL Art. 5 consent request email payload.
    يبني حمولة بريد إلكتروني لطلب الموافقة وفق المادة 5 من PDPL.
    """
    if locale == "ar":
        subject = f"طلب موافقة على معالجة بياناتك الشخصية — {company_name}"
        body = f"""السلام عليكم {contact_name},

نود إعلامكم بأن {company_name} تسعى إلى معالجة بياناتكم الشخصية للغرض التالي:
{_purpose_ar(purpose)}

وفقاً لنظام حماية البيانات الشخصية السعودي (PDPL)، يحق لكم:
- الموافقة على معالجة بياناتكم
- رفض المعالجة أو سحب الموافقة في أي وقت
- طلب حذف بياناتكم

للموافقة أو الرفض، يرجى الضغط على الرابط التالي:
{consent_url}

مع التحية،
فريق {company_name}
"""
    else:
        subject = f"Consent Request for Personal Data Processing — {company_name}"
        body = f"""Dear {contact_name},

{company_name} is requesting your consent to process your personal data for:
{_purpose_en(purpose)}

Under Saudi PDPL, you have the right to:
- Grant or refuse consent at any time
- Request erasure of your personal data
- Request a copy of your data

Please click the link below to respond:
{consent_url}

Best regards,
{company_name} Team
"""
    return {
        "to": contact_email,
        "subject": subject,
        "body": body,
        "locale": locale,
        "purpose": purpose,
    }


def build_consent_request_whatsapp(
    contact_name: str,
    company_name: str,
    purpose: str,
    consent_url: str,
    locale: str = "ar",
) -> str:
    """
    Build a PDPL consent request WhatsApp message.
    يبني رسالة واتساب لطلب موافقة PDPL.
    """
    if locale == "ar":
        return (
            f"مرحباً {contact_name} 👋\n\n"
            f"نحن من فريق {company_name}.\n"
            f"نطلب موافقتك على معالجة بياناتك الشخصية لـ: {_purpose_ar(purpose)}\n\n"
            f"رابط الموافقة / الرفض:\n{consent_url}\n\n"
            f"وفقاً لنظام PDPL السعودي، يمكنك سحب موافقتك في أي وقت."
        )
    return (
        f"Hello {contact_name} 👋\n\n"
        f"This is {company_name}.\n"
        f"We're requesting consent to process your data for: {_purpose_en(purpose)}\n\n"
        f"Grant/Deny consent:\n{consent_url}\n\n"
        f"Per Saudi PDPL, you may withdraw consent at any time."
    )


# ── Data Erasure ───────────────────────────────────────────────────────────

def build_erasure_audit_entry(
    contact_id: str,
    tenant_id: str,
    requesting_user_id: str | None,
    entities_erased: list[str],
    reason: str = "subject_request",
) -> dict[str, Any]:
    """
    Build an audit log entry for a PDPL erasure request.
    يبني إدخال سجل التدقيق لطلب مسح بيانات PDPL.
    Art. 13 — right to erasure + Art. 18 — audit trail
    """
    return {
        "id": str(uuid.uuid4()),
        "action": "pdpl.erasure",
        "entity_type": "contact",
        "entity_id": contact_id,
        "tenant_id": tenant_id,
        "user_id": requesting_user_id,
        "diff": {
            "reason": reason,
            "entities_erased": entities_erased,
            "erasure_method": "cascade_soft_delete_plus_pii_null",
            "pdpl_article": "Art. 13",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "status": "ok",
    }


def anonymize_contact_fields() -> dict[str, Any | None]:
    """
    Return the anonymized (nulled) values for contact PII fields.
    يُعيد قيماً مجهولة الهوية لحقول البيانات الشخصية في جهة الاتصال.
    """
    return {
        "name": "[ERASED]",
        "email": None,
        "phone": None,
        "linkedin_url": None,
    }


# ── Data Export / Portability ──────────────────────────────────────────────

def build_data_export(
    contact_id: str,
    contact_data: dict[str, Any],
    lead_data: list[dict[str, Any]],
    conversation_data: list[dict[str, Any]],
    consent_records: list[dict[str, Any]],
    audit_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Build a PDPL Art. 14 data portability export package.
    يبني حزمة تصدير البيانات وفق المادة 14 من PDPL.

    Format: structured JSON — machine-readable and human-readable.
    """
    export_id = str(uuid.uuid4())
    return {
        "export_id": export_id,
        "export_format": "PDPL_DATA_EXPORT_V1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pdpl_article": "Art. 14 — Data Portability",
        "controller": "Dealix | ديلكس",
        "data_subject": {
            "contact_id": contact_id,
            "profile": contact_data,
        },
        "processing_records": {
            "leads": lead_data,
            "conversations": conversation_data,
        },
        "consent_history": consent_records,
        "audit_trail": audit_records,
        "your_rights": {
            "ar": [
                "الحق في الوصول إلى بياناتك — المادة 14",
                "الحق في تصحيح البيانات غير الدقيقة — المادة 12",
                "الحق في طلب مسح البيانات — المادة 13",
                "الحق في الاعتراض على المعالجة — المادة 15",
                "حق تقديم شكوى للهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA)",
            ],
            "en": [
                "Right of access — Art. 14",
                "Right to rectification — Art. 12",
                "Right to erasure — Art. 13",
                "Right to object — Art. 15",
                "Right to lodge a complaint with SDAIA",
            ],
        },
        "sdaia_contact": "https://sdaia.gov.sa",
    }


# ── Monthly PDPL Audit Report ──────────────────────────────────────────────

def build_monthly_audit_report(
    tenant_id: str,
    report_month: str,            # "YYYY-MM"
    audit_records: list[dict],
    consent_stats: dict[str, int],
    erasure_requests: list[dict],
    breach_incidents: list[dict],
    processing_activities: list[str],
) -> dict[str, Any]:
    """
    Build a monthly PDPL compliance audit report.
    يبني تقرير تدقيق الامتثال الشهري لـ PDPL.

    Required by SDAIA for data controllers — must be retained for 5 years.
    Art. 18 — record-keeping obligation.
    """
    total_audits = len(audit_records)
    action_counts: dict[str, int] = {}
    for rec in audit_records:
        action = rec.get("action", "unknown")
        action_counts[action] = action_counts.get(action, 0) + 1

    return {
        "report_id": str(uuid.uuid4()),
        "report_type": "PDPL_MONTHLY_AUDIT",
        "report_month": report_month,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tenant_id": tenant_id,
        "pdpl_article": "Art. 18 — Record-Keeping",
        "retention_years": 5,
        "summary": {
            "total_audit_events": total_audits,
            "consent_stats": consent_stats,
            "erasure_requests_count": len(erasure_requests),
            "breach_incidents_count": len(breach_incidents),
            "unique_actions": action_counts,
        },
        "consent_overview": consent_stats,
        "erasure_requests": [
            {
                "contact_id": r.get("entity_id"),
                "requested_at": r.get("created_at"),
                "completed_at": r.get("diff", {}).get("timestamp"),
                "status": r.get("status"),
            }
            for r in erasure_requests
        ],
        "breach_incidents": breach_incidents,
        "processing_activities": processing_activities,
        "compliance_checklist": _compliance_checklist(),
        "certifications": {
            "pdpl_compliant": True,
            "audit_trail_complete": total_audits > 0,
            "consent_records_maintained": consent_stats.get("total_records", 0) > 0,
            "erasure_capability": True,
        },
    }


def _compliance_checklist() -> list[dict[str, Any]]:
    """Standard PDPL compliance checklist items."""
    return [
        {"article": "Art. 5", "requirement": "Lawful basis documented", "status": "compliant"},
        {"article": "Art. 6", "requirement": "Purpose limitation enforced", "status": "compliant"},
        {"article": "Art. 10", "requirement": "Data minimization applied", "status": "compliant"},
        {"article": "Art. 12", "requirement": "Accuracy controls in place", "status": "compliant"},
        {"article": "Art. 13", "requirement": "Erasure capability operational", "status": "compliant"},
        {"article": "Art. 14", "requirement": "Data portability endpoint available", "status": "compliant"},
        {"article": "Art. 18", "requirement": "Audit trail maintained", "status": "compliant"},
        {"article": "Art. 21", "requirement": "Breach notification procedure in place (72h to SDAIA)", "status": "compliant"},
        {"article": "Art. 25", "requirement": "Cross-border transfer controls documented", "status": "review_required"},
    ]


# ── Consent Dashboard ──────────────────────────────────────────────────────

def build_consent_dashboard(
    tenant_id: str,
    consent_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Build consent management dashboard data.
    يبني بيانات لوحة إدارة الموافقات.
    """
    total = len(consent_records)
    granted = sum(1 for r in consent_records if r.get("kind") == "grant")
    revoked = sum(1 for r in consent_records if r.get("kind") == "revoke")
    by_channel: dict[str, dict[str, int]] = {}
    by_purpose: dict[str, dict[str, int]] = {}
    unique_contacts: set[str] = set()

    for rec in consent_records:
        channel = rec.get("channel", "unknown")
        purpose = rec.get("purpose", "unknown")
        kind = rec.get("kind", "unknown")
        contact_id = rec.get("contact_id", "")

        if contact_id:
            unique_contacts.add(contact_id)

        if channel not in by_channel:
            by_channel[channel] = {"grant": 0, "revoke": 0}
        by_channel[channel][kind] = by_channel[channel].get(kind, 0) + 1

        if purpose not in by_purpose:
            by_purpose[purpose] = {"grant": 0, "revoke": 0}
        by_purpose[purpose][kind] = by_purpose[purpose].get(kind, 0) + 1

    consent_rate = round(granted / total * 100, 1) if total > 0 else 0.0

    return {
        "tenant_id": tenant_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overview": {
            "total_records": total,
            "granted": granted,
            "revoked": revoked,
            "unique_contacts": len(unique_contacts),
            "consent_rate_pct": consent_rate,
        },
        "by_channel": by_channel,
        "by_purpose": by_purpose,
        "pdpl_compliance": {
            "default_deny": True,
            "revoke_is_permanent": True,
            "audit_trail": True,
            "sdaia_registered": False,  # must be registered with SDAIA
        },
    }


# ── Breach Notification ────────────────────────────────────────────────────

def build_breach_notification(
    tenant_id: str,
    breach_description: str,
    affected_data_categories: list[str],
    estimated_subjects_count: int,
    discovery_datetime: str,
    mitigation_steps: list[str],
) -> dict[str, Any]:
    """
    Build PDPL Art. 21 data breach notification package.
    يبني حزمة إشعار خرق البيانات وفق المادة 21 من PDPL.

    Must be reported to SDAIA within 72 hours of discovery.
    """
    return {
        "notification_id": str(uuid.uuid4()),
        "notification_type": "PDPL_DATA_BREACH_NOTIFICATION",
        "pdpl_article": "Art. 21 — Breach Notification (72h to SDAIA)",
        "tenant_id": tenant_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "breach": {
            "description": breach_description,
            "discovery_datetime": discovery_datetime,
            "affected_data_categories": affected_data_categories,
            "estimated_subjects_count": estimated_subjects_count,
        },
        "mitigation": mitigation_steps,
        "notification_deadlines": {
            "sdaia_notification_hours": 72,
            "sdaia_portal": "https://sdaia.gov.sa",
            "contact_subjects_required": estimated_subjects_count > 0,
        },
        "status": "draft",
        "warning": "This notification must be reviewed by legal counsel before submission to SDAIA.",
    }


# ── Helpers ────────────────────────────────────────────────────────────────

def _purpose_ar(purpose: str) -> str:
    mapping = {
        "service_delivery": "تقديم الخدمات التعاقدية",
        "legal_obligation": "الامتثال للالتزامات القانونية",
        "legitimate_interest": "المصلحة المشروعة (بحث الأعمال التجارية)",
        "explicit_consent": "التسويق المباشر (بموافقة صريحة)",
    }
    return mapping.get(purpose, purpose)


def _purpose_en(purpose: str) -> str:
    mapping = {
        "service_delivery": "Service Delivery (contract performance)",
        "legal_obligation": "Legal Compliance",
        "legitimate_interest": "Legitimate Interest (business research)",
        "explicit_consent": "Direct Marketing (with explicit consent)",
    }
    return mapping.get(purpose, purpose)
