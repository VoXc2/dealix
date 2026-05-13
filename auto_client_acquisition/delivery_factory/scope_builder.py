"""Scope Builder — produces the fixed-scope SOW for a starting offer.

منشئ نطاق العمل — يولّد SOW ثابت لكل عرض افتتاحي.

Per docs/strategy/three_starting_offers.md and the master plan, Dealix sells
three productized sprints. First-meeting rule: no bespoke quotes. This module
turns an accepted IntakeRequest into a fixed-scope SOW (statement of work)
ready for signature from one of three templates.

Pure module — caller persists the result.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.delivery_factory.client_intake import (
    IntakeRequest,
    IntakeResult,
    StartingOffer,
)
from core.logging import get_logger

log = get_logger(__name__)


class ScopeDeliverable(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name_ar: str
    name_en: str
    description_ar: str
    description_en: str


class ScopeOfWork(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    sow_id: str = Field(default_factory=lambda: f"sow_{uuid4().hex[:12]}")
    project_id: str
    offer: StartingOffer
    title_ar: str
    title_en: str
    duration_days: int
    price_sar: int
    vat_sar: int
    total_sar: int
    deliverables: list[ScopeDeliverable]
    inclusions_ar: list[str]
    inclusions_en: list[str]
    exclusions_ar: list[str]
    exclusions_en: list[str]
    customer_inputs_required: list[str]
    success_criteria: list[str]
    payment_terms: str
    governing_law: str = "Kingdom of Saudi Arabia"
    sla_text: str
    start_date: str
    target_end_date: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _vat(price: int) -> int:
    """Saudi VAT 15% rounded to nearest riyal."""
    return round(price * 0.15)


def _revenue_intelligence_deliverables() -> list[ScopeDeliverable]:
    return [
        ScopeDeliverable(
            name_ar="مجموعة بيانات منظفة وموحّدة",
            name_en="Cleaned & unified dataset",
            description_ar="حتى 5,000 سجل، إزالة تكرار، توحيد كيانات سعودية.",
            description_en="Up to 5,000 records, dedupe, Saudi entity normalization.",
        ),
        ScopeDeliverable(
            name_ar="تقرير جودة البيانات",
            name_en="Data quality report",
            description_ar="درجة الجودة، الحقول الناقصة، التوصيات.",
            description_en="Quality score, missing fields, repair recommendations.",
        ),
        ScopeDeliverable(
            name_ar="أفضل 50 حسابًا مرتّبًا",
            name_en="Top 50 ranked accounts",
            description_ar="مرتّبة حسب ICP العميل مع تفسير قابل للفهم.",
            description_en="Ranked against customer ICP with human-readable rationale.",
        ),
        ScopeDeliverable(
            name_ar="أفضل 10 إجراءات مبيعات",
            name_en="Top 10 next actions",
            description_ar="إجراءات فورية مع رسائل تواصل (عربي/إنجليزي).",
            description_en="Immediate next actions with bilingual outreach drafts.",
        ),
        ScopeDeliverable(
            name_ar="لوحة Mini CRM",
            name_en="Mini CRM board",
            description_ar="مراحل واضحة، حقول قابلة للتحرير.",
            description_en="Clear stages, editable fields.",
        ),
        ScopeDeliverable(
            name_ar="تقرير تنفيذي",
            name_en="Executive report",
            description_ar="PDF ثنائي اللغة جاهز للإدارة.",
            description_en="Bilingual PDF report ready for leadership review.",
        ),
        ScopeDeliverable(
            name_ar="جلسة تسليم 60 دقيقة",
            name_en="60-min handoff session",
            description_ar="مسجّلة، مع تدريب على الـ Mini CRM.",
            description_en="Recorded, includes Mini CRM walkthrough.",
        ),
    ]


def _ai_quick_win_deliverables() -> list[ScopeDeliverable]:
    return [
        ScopeDeliverable(
            name_ar="اختيار حالة استخدام واحدة",
            name_en="One use case selected",
            description_ar="من قائمة جاهزة (تقرير CEO/توزيع leads/فرز tickets/توليد عرض/تلخيص inbox).",
            description_en="From curated list (CEO report / lead routing / ticket triage / proposal gen / inbox summary).",
        ),
        ScopeDeliverable(
            name_ar="أتمتة عاملة في بيئة العميل",
            name_en="Live automation in customer environment",
            description_ar="مع approval workflow وaudit log مدمج.",
            description_en="With approval workflow and audit log baked in.",
        ),
        ScopeDeliverable(
            name_ar="جولتا ملاحظات",
            name_en="Two feedback rounds",
            description_ar="خلال أسبوع الـ Sprint.",
            description_en="Within the sprint week.",
        ),
        ScopeDeliverable(
            name_ar="Runbook + جلسة تدريب",
            name_en="Runbook + 1-hour training",
            description_ar="مع تسجيل وتعليمات صيانة.",
            description_en="Recorded, with maintenance instructions.",
        ),
        ScopeDeliverable(
            name_ar="خط أساس ROI",
            name_en="ROI baseline",
            description_ar="الوقت الموفّر / الأخطاء المُخفّضة / السرعة المُكتسبة.",
            description_en="Hours saved / errors reduced / speed gained.",
        ),
    ]


def _company_brain_deliverables() -> list[ScopeDeliverable]:
    return [
        ScopeDeliverable(
            name_ar="استيعاب حتى 500 وثيقة",
            name_en="Ingest up to 500 documents",
            description_ar="PDF / Docs / KB / سياسات.",
            description_en="PDF / Docs / KB / policies.",
        ),
        ScopeDeliverable(
            name_ar="فحص PII وإخفاء للحساس",
            name_en="PII detection + redaction",
            description_ar="قبل الفهرسة، تطبيق سياسة PDPL.",
            description_en="Before indexing, PDPL policy applied.",
        ),
        ScopeDeliverable(
            name_ar="فهرسة RAG مع تتبّع المصادر",
            name_en="RAG indexing with source tracking",
            description_ar="قاعدة: لا إجابة بدون مصدر.",
            description_en='Rule: "no source = no answer".',
        ),
        ScopeDeliverable(
            name_ar="واجهة استعلام لفريق واحد (≤20 مقعدًا)",
            name_en="Query interface for one team (≤20 seats)",
            description_ar="Web / Slack / Teams.",
            description_en="Web / Slack / Teams.",
        ),
        ScopeDeliverable(
            name_ar="قواعد وصول بثلاث مستويات",
            name_en="3-tier access rules",
            description_ar="إدارة صلاحيات حسب الدور.",
            description_en="Role-based permissions.",
        ),
        ScopeDeliverable(
            name_ar="تتبّع حداثة الوثائق",
            name_en="Document freshness tracking",
            description_ar="Auto-flag للوثائق > 90 يومًا.",
            description_en="Auto-flag for documents > 90 days old.",
        ),
        ScopeDeliverable(
            name_ar="تدريب فريق ساعتين",
            name_en="2-hour team training",
            description_ar="مع تسجيل + admin guide.",
            description_en="Recorded + admin guide.",
        ),
    ]


_OFFER_PACK: dict[StartingOffer, dict[str, Any]] = {
    StartingOffer.REVENUE_INTELLIGENCE: {
        "title_ar": "Revenue Intelligence Sprint — تحويل البيانات إلى فرص",
        "title_en": "Revenue Intelligence Sprint — Data to Opportunities",
        "deliverables": _revenue_intelligence_deliverables,
        "inclusions_ar": [
            "استيعاب حتى 5,000 سجل",
            "تنظيف وإثراء وتصنيف",
            "رسائل تواصل ثنائية اللغة",
            "Mini CRM board",
            "تقرير تنفيذي + جلسة تسليم",
        ],
        "inclusions_en": [
            "Ingest up to 5,000 records",
            "Clean + enrich + score",
            "Bilingual outreach drafts",
            "Mini CRM board",
            "Executive report + handoff session",
        ],
        "exclusions_ar": [
            "تنفيذ مكالمات أو رسائل بدون موافقة مكتوبة",
            "تكامل CRM مخصص (خارج الـ scope)",
            "حملات تسويق رقمي مدفوعة",
        ],
        "exclusions_en": [
            "Executing calls or messages without written consent",
            "Custom CRM integration (out of scope)",
            "Paid digital marketing campaigns",
        ],
        "customer_inputs_required": [
            "Customer-provided seed list or CRM export (CSV/Excel)",
            "Description of products/services",
            "Target verticals and regions",
            "Existing outreach examples (if any)",
            "PDPL DPO contact (if a DPO exists)",
        ],
        "success_criteria": [
            "Data quality score ≥ 90 on cleaned dataset",
            "Top 50 accounts delivered within 10 business days",
            "≥ 8 of 10 ranked outreach drafts approved by customer without major edits",
            "Customer can independently use the Mini CRM by handoff session",
            "PDPL Art. 13 notice text included in every outreach draft",
        ],
        "sla_text": "Delivery within 10 business days. P95 issue response < 1 business day.",
    },
    StartingOffer.AI_QUICK_WIN: {
        "title_ar": "AI Quick Win Sprint — أتمتة عملية في 7 أيام",
        "title_en": "AI Quick Win Sprint — One Use Case in 7 Days",
        "deliverables": _ai_quick_win_deliverables,
        "inclusions_ar": [
            "اختيار حالة استخدام واحدة",
            "تنفيذ مع approval + audit",
            "جولتا ملاحظات",
            "Runbook + تدريب ساعة",
            "قياس ROI خط الأساس",
        ],
        "inclusions_en": [
            "Single use case selected",
            "Build with approval + audit",
            "Two feedback rounds",
            "Runbook + 1-hour training",
            "ROI baseline measurement",
        ],
        "exclusions_ar": [
            "تكاملات أنظمة متعدّدة",
            "أكثر من حالة استخدام واحدة",
            "تدريب أكثر من جلستين",
        ],
        "exclusions_en": [
            "Multi-system integrations",
            "More than one use case",
            "More than two training sessions",
        ],
        "customer_inputs_required": [
            "30-min discovery call slot",
            "Description of target process",
            "Sample inputs / outputs",
            "Process owner contact",
            "System access (or credentials in sealed vault) for the source system",
        ],
        "success_criteria": [
            "Live automation in customer environment by day 7",
            "Customer process owner can run end-to-end by handoff",
            "Audit log enabled and queryable",
            "ROI baseline captured (hours saved / errors / cycle time)",
            "Approval gate fires for every action that has side-effects",
        ],
        "sla_text": "Delivery within 7 business days. P95 issue response < 4 business hours.",
    },
    StartingOffer.COMPANY_BRAIN: {
        "title_ar": "Company Brain Sprint — مساعد معرفي بإجابات موثّقة",
        "title_en": "Company Brain Sprint — Cited Internal Assistant",
        "deliverables": _company_brain_deliverables,
        "inclusions_ar": [
            "استيعاب حتى 500 وثيقة",
            "PII redaction",
            "RAG + استشهادات",
            "واجهة لفريق واحد (≤20 مقعدًا)",
            "تتبّع حداثة + إدارة وصول",
            "تدريب ساعتين",
        ],
        "inclusions_en": [
            "Ingest up to 500 documents",
            "PII redaction",
            "RAG + citations",
            "Interface for one team (≤20 seats)",
            "Freshness + access management",
            "2-hour training",
        ],
        "exclusions_ar": [
            "وثائق تتجاوز 500 (محاسبة Overage)",
            "أكثر من فريق واحد (يحتاج باقة أعلى)",
            "تكاملات شبكات مهنية / CRM مخصصة",
        ],
        "exclusions_en": [
            "Documents beyond 500 (overage billed)",
            "More than one team (requires higher tier)",
            "Professional-network / custom CRM integrations",
        ],
        "customer_inputs_required": [
            "Document inventory list (file names + categories)",
            "Permissions matrix (who sees what)",
            "Sensitive document flagging",
            "10 sample questions the assistant should answer",
            "Document owner contacts for each category",
        ],
        "success_criteria": [
            "≥ 95% of test answers carry a verifiable citation",
            "Zero PII surfaced in assistant outputs",
            "Access rules enforced (verified on 3 personas)",
            "Documents > 90 days flagged in the freshness report",
            "Customer team confirms self-service usability post-training",
        ],
        "sla_text": "Delivery within 21 business days. P95 issue response < 1 business day.",
    },
}


def build_scope(
    intake: IntakeRequest, result: IntakeResult, start_date: datetime | None = None
) -> ScopeOfWork:
    """Build a fixed-scope SOW from an accepted intake.

    Raises ValueError if the intake was not accepted.
    """
    if not result.accepted or result.matched_offer is None:
        raise ValueError("scope cannot be built for a non-accepted intake")

    pack = _OFFER_PACK[StartingOffer(result.matched_offer)]
    start = start_date or datetime.now(UTC)
    end = start + timedelta(days=int(result.estimated_duration_days or 0))
    price = int(result.estimated_price_sar or 0)
    vat = _vat(price)

    sow = ScopeOfWork(
        project_id=result.project_id,
        offer=StartingOffer(result.matched_offer),
        title_ar=pack["title_ar"],
        title_en=pack["title_en"],
        duration_days=int(result.estimated_duration_days or 0),
        price_sar=price,
        vat_sar=vat,
        total_sar=price + vat,
        deliverables=pack["deliverables"](),
        inclusions_ar=list(pack["inclusions_ar"]),
        inclusions_en=list(pack["inclusions_en"]),
        exclusions_ar=list(pack["exclusions_ar"]),
        exclusions_en=list(pack["exclusions_en"]),
        customer_inputs_required=list(pack["customer_inputs_required"]),
        success_criteria=list(pack["success_criteria"]),
        payment_terms="Net 14 after SOW countersignature; 100% upon delivery for sprints.",
        sla_text=pack["sla_text"],
        start_date=start.date().isoformat(),
        target_end_date=end.date().isoformat(),
    )
    log.info(
        "scope_built",
        project_id=sow.project_id,
        offer=sow.offer,
        price_sar=sow.price_sar,
        total_sar=sow.total_sar,
    )
    return sow
