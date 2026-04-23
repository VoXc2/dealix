"""
Sector Playbooks — 4 focus verticals with sector-aware workflows.

Each playbook declares:
  - qualification signals (what counts as a lead)
  - value bands (expected deal size by sub-segment)
  - outreach channels with order
  - negotiation guardrails (thresholds, content-guards)
  - red flags (auto-block triggers)
  - evidence sources (Saudi-native first)

Used by:
  - Strategist agent (pick channel + script)
  - Policy engine (tier thresholds)
  - Reporting layer (sector KPIs)

No external I/O — pure data with lightweight helpers. Safe to import anywhere.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any


# --------------------------------------------------------------- data types

@dataclass
class Playbook:
    sector: str
    name_ar: str
    qualification_signals: list[str]
    value_bands_sar: dict[str, tuple[int, int]]
    outreach_order: list[str]                  # e.g. ["email", "whatsapp", "call"]
    negotiation_guardrails: dict[str, Any]
    red_flags: list[str]
    evidence_sources: list[dict[str, str]]     # [{name, url}]
    opening_hooks_ar: list[str]                # sample first-line templates
    typical_objections_ar: list[dict[str, str]]
    win_criteria: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# --------------------------------------------------------- the 4 playbooks

REAL_ESTATE = Playbook(
    sector="real_estate",
    name_ar="العقار — تطوير وإدارة",
    qualification_signals=[
        "مشروع جديد مُعلن على Sakani / Wafi",
        "رخصة بناء جديدة (البلديات)",
        "تغيير في مساهمي الشركة (واثق)",
        "جولة تمويل عقاري (SAMA / ReDF)",
        "توظيف Head of Sales / Marketing",
    ],
    value_bands_sar={
        "developer_large": (80_000, 500_000),
        "developer_mid":   (30_000, 120_000),
        "property_mgmt":   (15_000,  60_000),
        "broker_network":  (10_000,  40_000),
    },
    outreach_order=["linkedin", "email", "whatsapp", "call"],
    negotiation_guardrails={
        "max_discount_pct": 15,
        "never_promise": ["حصرية على منطقة", "سعر مدى الحياة", "ضمانات عائد"],
        "require_approval_above_sar": 200_000,
    },
    red_flags=[
        "شركة ناشئة بلا CR ساري",
        "طلب دمج عقود مع جهات حكومية بلا تفويض",
        "وعود عائد > 25% سنوياً",
    ],
    evidence_sources=[
        {"name": "Wathq CR", "url": "https://developer.wathq.sa/en/apis"},
        {"name": "Sakani", "url": "https://sakani.sa"},
        {"name": "Monsha'at SME", "url": "https://www.monshaat.gov.sa/en/node/12768"},
    ],
    opening_hooks_ar=[
        "رأيت إعلانكم عن مشروع {project_name} — كم فرصة البيع التي لم تُغلق لأن الوكيل لم يرد في 10 دقائق؟",
        "في شركات عقار بحجم {employees} موظف، أكثر سبب لفقد الفرصة = تأخير المتابعة. Dealix يتابع عنكم بضوابطكم.",
    ],
    typical_objections_ar=[
        {"objection": "عندنا CRM", "rebuttal": "Dealix ليس CRM — هو AI CRO يجلس فوق CRM الحالي ويقود التنفيذ"},
        {"objection": "العملاء يبغون شخص", "rebuttal": "تماماً — Dealix يرفع الفرص الجاهزة لمسوقينا بدل ضياعها"},
    ],
    win_criteria=["3 فرص جديدة/شهر", "تقليل وقت الرد < 5 دقائق", "تقرير أسبوعي للبورد"],
)


CONSTRUCTION = Playbook(
    sector="construction",
    name_ar="المقاولات والبنية التحتية",
    qualification_signals=[
        "ترسية مناقصة حكومية (Etimad)",
        "تأهيل جديد في قائمة المقاولين المصنفين",
        "إعلان عن Joint Venture",
        "توظيف PMO / Project Director",
        "طلب موردين جدد على Monsha'at",
    ],
    value_bands_sar={
        "tier1_contractor": (100_000, 800_000),
        "mid_contractor":    (40_000, 150_000),
        "subcontractor":     (15_000,  60_000),
    },
    outreach_order=["email", "linkedin", "call", "whatsapp"],
    negotiation_guardrails={
        "max_discount_pct": 10,
        "never_promise": ["إنجاز مناقصة", "علاقات حكومية مضمونة"],
        "require_approval_above_sar": 300_000,
    },
    red_flags=[
        "تصنيف مقاولين منتهي",
        "قضايا تأخير تسليم موثقة",
        "طلب ضمانات أداء غير معتادة",
    ],
    evidence_sources=[
        {"name": "Etimad", "url": "https://etimad.sa"},
        {"name": "Contractors Classification Agency", "url": "https://cca.gov.sa"},
        {"name": "Wathq", "url": "https://developer.wathq.sa/en/apis"},
    ],
    opening_hooks_ar=[
        "بعد ترسية {tender_name} — كيف تدير pipeline المناقصات القادمة من مصدر واحد مع بيانات Etimad؟",
        "شركات البنية التحتية عادة تفقد 30% من فرص الإحالة لأن تواصل المورد متفرق. Dealix يوحده.",
    ],
    typical_objections_ar=[
        {"objection": "فريقنا يعرف المقاولين",
         "rebuttal": "Dealix لا يحل محل العلاقة — يظهر لك فرص Etimad قبل أن يراها منافسوكم"},
    ],
    win_criteria=["كشف 5+ مناقصات ذات صلة أسبوعياً", "تأهيل مقاول ثانوي جاهز", "تقارير الترسيات"],
)


RETAIL = Playbook(
    sector="retail",
    name_ar="التجزئة والتجارة الإلكترونية",
    qualification_signals=[
        "إطلاق متجر Salla / Zid جديد",
        "حملة ضخمة على Snapchat / TikTok",
        "جولة تمويل (Sanabil / STV / Wa'ed)",
        "توظيف Growth Lead / CMO",
        "إطلاق منتج أو فئة جديدة",
    ],
    value_bands_sar={
        "brand_dtc_large": (50_000, 200_000),
        "brand_dtc_mid":   (15_000,  60_000),
        "marketplace":     (25_000, 100_000),
        "franchise":       (10_000,  40_000),
    },
    outreach_order=["whatsapp", "linkedin", "email", "call"],
    negotiation_guardrails={
        "max_discount_pct": 20,
        "never_promise": ["ضمان مبيعات", "حصرية فئة"],
        "require_approval_above_sar": 100_000,
    },
    red_flags=[
        "مراجعات سلبية كثيرة على Maroof",
        "شكاوى PDPL مفتوحة",
        "توقف شحن أكثر من 30 يوماً",
    ],
    evidence_sources=[
        {"name": "Maroof (MoC)", "url": "https://maroof.sa"},
        {"name": "Monsha'at", "url": "https://www.monshaat.gov.sa/en"},
        {"name": "Salla Partners", "url": "https://salla.partners"},
    ],
    opening_hooks_ar=[
        "متجركم على Salla بمتوسط {orders_per_day} طلب/يوم — كم طلب يضيع قبل checkout؟ Dealix يتابع مباشرة.",
        "بعد جولة {funding_stage}، الضغط على المبيعات مضاعف — Dealix يحول leads إلى تقارير نمو يومية.",
    ],
    typical_objections_ar=[
        {"objection": "عندنا Klaviyo / HubSpot",
         "rebuttal": "Dealix يغطي فجوة الرد العربي + قنوات السعودية المحلية، ويتكامل مع أدواتكم"},
    ],
    win_criteria=["تقليل cart abandonment 15%", "تقرير نمو أسبوعي", "ربط WhatsApp مقيد"],
)


FINTECH = Playbook(
    sector="fintech",
    name_ar="الخدمات المالية والفنتك",
    qualification_signals=[
        "ترخيص SAMA Regulatory Sandbox",
        "ترخيص CMA Fintech",
        "جولة تمويل من Sanabil / Raed / Wa'ed",
        "إطلاق منتج BNPL / Payments / Lending",
        "شراكة بنكية مُعلنة",
    ],
    value_bands_sar={
        "licensed_fintech": (60_000, 300_000),
        "sandbox_company":  (25_000,  80_000),
        "embedded_finance": (40_000, 150_000),
    },
    outreach_order=["email", "linkedin", "call"],  # WhatsApp rarely allowed here
    negotiation_guardrails={
        "max_discount_pct": 8,
        "never_promise": ["موافقة ساما", "عائد مضمون", "حماية رأس المال"],
        "require_approval_above_sar": 150_000,
        "pdpl_strict": True,
    },
    red_flags=[
        "نشاط بلا ترخيص ساما / هيئة سوق مال",
        "شكاوى عملاء موثقة بالإعلام",
        "طلب دمج بدون DPA",
    ],
    evidence_sources=[
        {"name": "SAMA Sandbox", "url": "https://www.sama.gov.sa/en-US/RegulatorySandbox"},
        {"name": "CMA Fintech Lab", "url": "https://cma.org.sa/en/Market/FinTech"},
        {"name": "Wathq", "url": "https://developer.wathq.sa/en/apis"},
    ],
    opening_hooks_ar=[
        "بعد دخولكم Sandbox ساما، الـ design partners خطوة حاسمة — Dealix يُنشئ pipeline design partners مفلتر.",
        "شركات BNPL عادة تفقد 40% من merchants لأن متابعة التوقيع تأخذ أسبوعين. Dealix يختصرها إلى أيام.",
    ],
    typical_objections_ar=[
        {"objection": "PDPL / Data residency",
         "rebuttal": "Dealix: In-Kingdom hosting + Audit logs + Approval gates. PDPL-aware by design."},
    ],
    win_criteria=["10 design partners مؤهلين", "تقرير أسبوعي مطابق", "Audit log نظيف"],
)


PLAYBOOKS: dict[str, Playbook] = {
    "real_estate":  REAL_ESTATE,
    "construction": CONSTRUCTION,
    "retail":       RETAIL,
    "fintech":      FINTECH,
}


# ----------------------------------------------------------------- helpers

def get(sector: str) -> Playbook | None:
    return PLAYBOOKS.get(sector)


def suggest_outreach_channel(sector: str, tier: str = "pro") -> str:
    pb = get(sector)
    if not pb:
        return "email"
    # fintech + starter tier → still email (conservative default)
    return pb.outreach_order[0]


def tier_threshold(sector: str, tier: str) -> int:
    """Returns the approval threshold (SAR) for this sector+tier combo."""
    base = {"starter": 2_000, "pro": 10_000, "enterprise": 50_000}[tier]
    pb = get(sector)
    if pb:
        # fintech is stricter — halve the threshold
        if sector == "fintech":
            return base // 2
        # construction higher — scale up 1.5x
        if sector == "construction":
            return int(base * 1.5)
    return base


# ----------------------------------------------------------------- self-test

def _test():
    assert len(PLAYBOOKS) == 4
    for name, pb in PLAYBOOKS.items():
        assert pb.sector == name
        assert pb.qualification_signals
        assert pb.value_bands_sar
        assert pb.outreach_order
        assert pb.evidence_sources, f"{name} missing evidence sources"
        assert len(pb.opening_hooks_ar) >= 2
        print(f"  {pb.sector:13s} · {pb.name_ar} · "
              f"{len(pb.qualification_signals)} signals · "
              f"{len(pb.outreach_order)} channels · "
              f"thr/pro={tier_threshold(pb.sector, 'pro'):,} SAR")

    # suggestion
    assert suggest_outreach_channel("real_estate") == "linkedin"
    assert suggest_outreach_channel("fintech") == "email"

    # thresholds: fintech stricter, construction looser
    assert tier_threshold("fintech", "pro") == 5_000
    assert tier_threshold("construction", "pro") == 15_000
    assert tier_threshold("real_estate", "pro") == 10_000

    # JSON round-trip
    import json
    for pb in PLAYBOOKS.values():
        blob = json.dumps(pb.to_dict(), ensure_ascii=False)
        assert "sector" in blob

    print("\n✅ 4 sector playbooks validated · suggest/threshold helpers working")


if __name__ == "__main__":
    _test()
