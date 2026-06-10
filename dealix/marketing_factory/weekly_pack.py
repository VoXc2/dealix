"""Weekly content pack — Arabic draft templates, approval-first."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any

_WEEKLY_SLOTS: list[dict[str, str]] = [
    {
        "channel": "linkedin",
        "title_ar": "لماذا الإيراد يحتاج حوكمة قبل الأتمتة",
        "body_draft_ar": (
            "كثير من فرق B2B في الخليج تسرّع الذكاء الاصطناعي قبل تثبيت: مصدر الـlead، "
            "موافقة الإرسال، وسجل الأدلة. Dealix تبدأ بتشخيص 7 أيام محكوم — Risk Score + Proof Pack "
            "بدون وعود إيراد وهمية. رابط التقييم في التعليق الأول (بعد موافقتي)."
        ),
        "cta_label_ar": "Risk Score مجاني",
        "utm_campaign": "weekly_linkedin_governance",
    },
    {
        "channel": "email_newsletter",
        "title_ar": "نشرة: 3 إشارات أن CRM جاهز للأتمتة المحكومة",
        "body_draft_ar": (
            "1) كل lead له مرحلة واضحة.\n"
            "2) لا رسالة خارجية بلا موافقة.\n"
            "3) كل فاتورة مربوطة بـscope.\n"
            "إن تطابقت — جرّب تشخيص Dealix (مسودة فقط، بدون إرسال آلي)."
        ),
        "cta_label_ar": "احجز تقييم Risk",
        "utm_campaign": "weekly_newsletter_crm",
    },
    {
        "channel": "x",
        "title_ar": "تغريدة: لا cold WhatsApp — بديل محكوم",
        "body_draft_ar": (
            "نموذجنا: inbound + Lead Ads + مسودات بموافقة المؤسس. "
            "لا نبيع «بوت يبيع عنك» — نبيع تشغيل إيراد بأدلة."
        ),
        "cta_label_ar": "التشخيص",
        "utm_campaign": "weekly_x_inbound",
    },
    {
        "channel": "proof_snippet",
        "title_ar": "مقتطف Proof Pack للمبيعات",
        "body_draft_ar": (
            "اعتراض شائع: «نخاف الأتمتة تكسر الثقة». "
            "الرد: كل إجراء خارجي عالي الخطورة يمر Approval Center + Evidence Ledger."
        ),
        "cta_label_ar": "اطلب Proof Pack",
        "utm_campaign": "weekly_objection_proof",
        "slot_kind": "objection_trust",
    },
    {
        "channel": "objection_pricing",
        "title_ar": "اعتراض: السعر مرتفع",
        "body_draft_ar": (
            "objection_pricing: نبدأ بتشخيص محدود النطاق بأسعار معلنة (Starter/Standard/Executive) "
            "— القرار النهائي بعد Risk Score وProof Pack، لا التزام بلا دليل."
        ),
        "cta_label_ar": "Risk Score",
        "utm_campaign": "weekly_objection_pricing",
        "slot_kind": "objection_pricing",
    },
    {
        "channel": "objection_timing",
        "title_ar": "اعتراض: ليس الوقت المناسب",
        "body_draft_ar": (
            "objection_timing: إن كان الـpipeline يضيع leads اليوم، تأجيل الحوكمة يكلف أكثر. "
            "عرض تشخيص 7 أيام بمخرجات قابلة للتنفيذ — بدون أتمتة خارجية بلا موافقة."
        ),
        "cta_label_ar": "تشخيص 7 أيام",
        "utm_campaign": "weekly_objection_timing",
        "slot_kind": "objection_timing",
    },
]


def generate_weekly_pack(*, week_start: date | None = None) -> dict[str, Any]:
    start = week_start or date.today()
    monday = start - timedelta(days=start.weekday())
    slots: list[dict[str, Any]] = []
    for i, tpl in enumerate(_WEEKLY_SLOTS):
        day = monday + timedelta(days=min(i, 4))
        slots.append(
            {
                "scheduled_date": day.isoformat(),
                "channel": tpl["channel"],
                "title_ar": tpl["title_ar"],
                "body_draft_ar": tpl["body_draft_ar"],
                "cta_label_ar": tpl["cta_label_ar"],
                "cta_path": "/dealix-diagnostic",
                "utm_campaign": tpl["utm_campaign"],
                "utm_medium": "social" if tpl["channel"] != "email_newsletter" else "email",
                "utm_source": "dealix",
                "status": "draft",
                "slot_kind": tpl.get("slot_kind", "content"),
                "policy_ar": "لا نشر خارجي تلقائي — مراجعة المؤسس ثم نشر يدوي.",
            },
        )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "week_start": monday.isoformat(),
        "slot_count": len(slots),
        "slots": slots,
        "governance_en": "Draft-only weekly pack; queue approvals before any external publish.",
    }
