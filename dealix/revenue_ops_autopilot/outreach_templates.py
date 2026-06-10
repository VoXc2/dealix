"""Segment-based outreach drafts (Arabic) — draft-only, no auto-send."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

_YAML_PATH = Path(__file__).resolve().parents[1] / "config" / "outreach_templates.yaml"


@lru_cache(maxsize=1)
def _load_yaml_templates() -> dict[str, str]:
    if not _YAML_PATH.is_file():
        return {}
    data = yaml.safe_load(_YAML_PATH.read_text(encoding="utf-8")) or {}
    raw = data.get("templates") or {}
    return {str(k): str(v).strip() for k, v in raw.items() if isinstance(v, str)}


TEMPLATES: dict[str, str] = {
    "agency_wedge": (
        "مرحباً {contact} — في {company}، كثير من الوكالات تواجه سؤال العميل: "
        "«ماذا حدث بعد الحملة؟»\n\n"
        "نقدّم تشخيص Post-Lead Revenue Ops محكوم: مالك المتابعة، مسار أدلة، وProof Pack "
        "لعميلكم — بدون إرسال آلي أو وعود إيراد.\n\n"
        "هل يناسبكم Risk Score مجاني أو عيّنة Proof Pack؟"
    ),
    "agency_partner": (
        "مرحباً {contact} — نعمل مع وكالات مثل {company} على طبقة إثبات ما بعد الـ lead "
        "(Dealix يشخّص · الشريك ينفّذ · العميل يحصل على Proof).\n\n"
        "نموذج pilot واحد بعميل end — بدون التزام طويل. هل نرتّب ١٠ دقائق؟"
    ),
    "crm_partner": (
        "مرحباً {contact} — قبل توسيع HubSpot/Zoho لعميل {company}، "
        "نضيف طبقة Diagnostic + Proof Pack لجاهزية المتابعة والحوكمة.\n\n"
        "مسودة فقط — نرسل بعد موافقتكم."
    ),
    "direct_b2b": (
        "مرحباً {contact} — في {company}، نساعد فرق B2B على تشغيل الإيراد والـ AI "
        "بحدود موافقة ومسار أدلة واضح.\n\n"
        "عرضنا: تشخيص ٧ أيام Governed Revenue & AI Ops — هل نرسل Risk Score؟"
    ),
    "executive_governance": (
        "مرحباً {contact} — قبل توسيع وكلاء AI في {company}، "
        "نرسم حدود الموافقة ومسار الأدلة وقرارات قابلة للتنفيذ (ليس dashboard عاماً).\n\n"
        "ديمو ١٢ دقيقة من Business Now — بموافقة مسبقة للوقت."
    ),
    "default": (
        "مرحباً {contact} — نساعد {company} على تحويل تجارب AI وعمليات الإيراد "
        "إلى تشغيل محكوم بأدلة وموافقات.\n\n"
        "الخطوة الأولى: Risk Score + عيّنة Proof Pack — بدون إرسال تلقائي."
    ),
}


def build_outreach_draft(
    *,
    company: str,
    contact: str = "",
    segment: str = "",
    pain: str = "",
) -> str:
    merged = {**TEMPLATES, **_load_yaml_templates()}
    key = segment.strip() or "default"
    if key not in merged:
        for cand in ("agency_wedge", "agency_partner", "crm_partner", "direct_b2b"):
            if cand in key:
                key = cand
                break
        else:
            key = "default"
    body = merged[key]
    contact_label = contact.strip() or "فريقكم"
    company_label = company.strip() or "شركتكم"
    text = body.format(contact=contact_label, company=company_label)
    from dealix.revenue_ops_autopilot.config_loader import wedge_message_for_segment

    wedge = wedge_message_for_segment(key)
    if wedge:
        text = f"{wedge}\n\n{text}"
    if pain.strip():
        text += f"\n\n(سياق: {pain.strip()[:200]})"
    return text
