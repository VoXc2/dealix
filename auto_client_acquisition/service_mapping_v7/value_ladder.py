"""V7 value ladder — the founder's pitch ladder.

7 rungs: 6 customer-facing service bundles + a Compliance/Trust pack as
rung 7. Pure data; safe to render in any language.
"""
from __future__ import annotations


def value_ladder() -> list[dict]:
    """Return the 7-rung value ladder."""
    return [
        {
            "rung": 1,
            "service": "diagnostic",
            "name_ar": "Diagnostic مجاني",
            "name_en": "Free Growth Diagnostic",
            "price_band_sar": "0",
            "summary_ar": "جلسة 30-60 دقيقة + 3 توصيات محدّدة + توصية بأفضل عرض أوّل.",
            "summary_en": "30-60 min session + 3 specific recommendations + best-first-offer pick.",
        },
        {
            "rung": 2,
            "service": "growth_starter",
            "name_ar": "باقة بداية النمو — Pilot",
            "name_en": "Growth Starter Pilot",
            "price_band_sar": "499",
            "summary_ar": "7 أيام: 10 فرص + مسوّدات عربيّة + خطة متابعة + Proof Pack موقَّع.",
            "summary_en": "7 days: 10 opportunities + Arabic drafts + follow-up plan + signed Proof Pack.",
        },
        {
            "rung": 3,
            "service": "data_to_revenue",
            "name_ar": "من البيانات إلى الإيراد",
            "name_en": "Data to Revenue",
            "price_band_sar": "1500-3000",
            "summary_ar": "تنظيف قائمة + درجة contactability + رسائل مقسّمة + تقرير مخاطر.",
            "summary_en": "List cleanup + contactability score + segmented drafts + risk report.",
        },
        {
            "rung": 4,
            "service": "executive_growth_os",
            "name_ar": "نظام تشغيل القيادة التنفيذية",
            "name_en": "Executive Growth OS",
            "price_band_sar": "2999/month",
            "summary_ar": "حزمة أسبوعيّة: قرارات معلّقة + عوائق + مخاطر + actual vs forecast.",
            "summary_en": "Weekly pack: pending decisions + blockers + risks + actual-vs-forecast.",
        },
        {
            "rung": 5,
            "service": "partnership_growth",
            "name_ar": "نمو الشراكات",
            "name_en": "Partnership Growth",
            "price_band_sar": "3000-7500",
            "summary_ar": "8 فئات شراكة + fit-score + مسوّدات تواصل دافئة + Proof Pack مشترك.",
            "summary_en": "8 partner categories + fit-score + warm-intro drafts + co-branded Proof Pack.",
        },
        {
            "rung": 6,
            "service": "full_control_tower",
            "name_ar": "برج التحكّم الكامل",
            "name_en": "Full Control Tower",
            "price_band_sar": "custom",
            "summary_ar": "تخصيص كامل لمؤسسات متعدّدة الأقسام + لوحة قرارات + إيقاع شهريّ.",
            "summary_en": "Full customisation for multi-division orgs + decision board + monthly cadence.",
        },
        {
            "rung": 7,
            "service": "compliance_trust_pack",
            "name_ar": "حزمة الامتثال والثقة",
            "name_en": "Compliance / Trust Pack",
            "price_band_sar": "custom",
            "summary_ar": "PDPL، DPA، سجلّ موافقات، Proof Pack مشترك للجهات التنظيميّة.",
            "summary_en": "PDPL, DPA, consent ledger, regulator-ready Proof Pack.",
        },
    ]
