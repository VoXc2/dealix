"""Weekly Dealix B2B content pack — evidence-led, channel-native, approval-first."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any

_WEEKLY_SLOTS: list[dict[str, str]] = [
    {
        "channel": "founder_linkedin",
        "title_ar": "الفجوة ليست في أدوات AI — الفجوة بين القرار والتنفيذ",
        "body_draft_ar": (
            "الشركة قد تملك CRM وERP وWhatsApp وعشرات الأدوات، ومع ذلك تضيع الفرص والقرارات بين الفرق. "
            "المشكلة التي نركز عليها في Dealix هي Execution Gap: كيف تتحول الإشارة إلى قرار، ثم action محكوم، ثم proof يمكن مراجعته. "
            "هذه هي المساحة التي نبني فيها الاستراتيجية والأنظمة والذكاء — وليس مجرد إضافة bot جديد."
        ),
        "cta_label_ar": "ابدأ Execution Diagnostic",
        "utm_campaign": "founder_execution_gap",
    },
    {
        "channel": "company_linkedin",
        "title_ar": "Dealix أكبر من منتج واحد",
        "body_draft_ar": (
            "Dealix تعمل عبر أربع طبقات مترابطة: Strategy & Transformation، Systems & Automation، "
            "Intelligence & Market Access، وTrust/Proof. Dealix OS هو منتجنا الرئيسي عندما تحتاج المشكلة إلى تشغيل مستمر، "
            "لكنه ليس نقطة البداية الإلزامية لكل عميل. نبدأ بالمشكلة والـevidence ثم نختار الحل."
        ),
        "cta_label_ar": "استكشف الحلول الاستراتيجية",
        "utm_campaign": "company_architecture",
    },
    {
        "channel": "x",
        "title_ar": "Signal ≠ Opportunity ≠ Revenue",
        "body_draft_ar": (
            "إشارة السوق ليست علاقة. العلاقة ليست consent. الـquote ليست payment. "
            "أسرع أنظمة النمو ليست التي تقفز بين هذه المراحل — بل التي تعرف بالضبط ما الدليل المطلوب للانتقال بينها."
        ),
        "cta_label_ar": "منهج Dealix",
        "utm_campaign": "truth_firewall",
    },
    {
        "channel": "short_video",
        "title_ar": "60 ثانية: متى تحتاج AI agent ومتى لا تحتاجه؟",
        "body_draft_ar": (
            "Hook: لا تبدأ بـAgent. ابدأ بالقرار الذي يتأخر أو الـworkflow الذي يتسرب. "
            "Body: حدّد signal، owner، action، authority وproof. إذا تكرر المسار واستحق automation عندها agent أو Dealix OS يصبح منطقيًا. "
            "Close: التقنية تأتي بعد وضوح المشكلة، لا قبلها."
        ),
        "cta_label_ar": "ابدأ بالمشكلة",
        "utm_campaign": "agent_when_needed",
    },
    {
        "channel": "research_brief",
        "title_ar": "Saudi Opportunity Brief — من الإشارة الرسمية إلى قرار B2B",
        "body_draft_ar": (
            "اختر إشارة سعودية رسمية واحدة هذا الأسبوع. لخّص ماذا تغير، من يتأثر، ما المشكلة التشغيلية المحتملة، "
            "ما الذي لا نعرفه بعد، وما التجربة التجارية الأقل تكلفة لاختبار الفرضية. لا تُحوّل public signal إلى buyer intent."
        ),
        "cta_label_ar": "استكشف Market Intelligence",
        "utm_campaign": "saudi_opportunity_brief",
    },
    {
        "channel": "proof_snippet",
        "title_ar": "Proof قبل Case Study",
        "body_draft_ar": (
            "قبل أن نسمي أي شيء نجاحًا: نحتاج baseline، action receipt، measured outcome، ثم customer acceptance/permission عندما يكون الادعاء customer-facing. "
            "Demo أو synthetic output يمكن أن يثبت capability — لكنه لا يصبح Customer Proof تلقائيًا."
        ),
        "cta_label_ar": "شاهد Proof Model",
        "utm_campaign": "proof_before_claim",
        "slot_kind": "proof_methodology",
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
                "cta_path": "/book",
                "utm_campaign": tpl["utm_campaign"],
                "utm_medium": "social" if tpl["channel"] != "email_newsletter" else "email",
                "utm_source": "dealix",
                "status": "draft",
                "slot_kind": tpl.get("slot_kind", "content"),
                "policy_ar": "مسودة فقط — لا نشر خارجي تلقائي قبل المراجعة والسلطة المناسبة.",
            },
        )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "week_start": monday.isoformat(),
        "slot_count": len(slots),
        "slots": slots,
        "governance_en": "Evidence-led draft-only weekly pack; external publication remains approval/action-bound.",
    }
