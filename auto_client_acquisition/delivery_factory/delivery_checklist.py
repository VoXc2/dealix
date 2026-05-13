"""Delivery Checklist — per-offer checklist for the 8-stage Standard.

قائمة التسليم لكل عرض ضمن معيار التسليم الثماني.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict

from auto_client_acquisition.delivery_factory.client_intake import StartingOffer


class Stage(StrEnum):
    DISCOVER = "discover"
    DIAGNOSE = "diagnose"
    DESIGN = "design"
    BUILD = "build"
    VALIDATE = "validate"
    DELIVER = "deliver"
    PROVE = "prove"
    EXPAND = "expand"


STAGES_ORDER: tuple[Stage, ...] = (
    Stage.DISCOVER,
    Stage.DIAGNOSE,
    Stage.DESIGN,
    Stage.BUILD,
    Stage.VALIDATE,
    Stage.DELIVER,
    Stage.PROVE,
    Stage.EXPAND,
)


class ChecklistItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    stage: Stage
    label_ar: str
    label_en: str
    required: bool = True


_COMMON: list[ChecklistItem] = [
    ChecklistItem(stage=Stage.DISCOVER, label_ar="جمع بيانات الشركة والقطاع", label_en="Collect company + sector profile"),
    ChecklistItem(stage=Stage.DISCOVER, label_ar="توثيق المشكلة بكلمات العميل", label_en="Document the problem in customer's words"),
    ChecklistItem(stage=Stage.DIAGNOSE, label_ar="حساب درجة جودة البيانات الأولية", label_en="Compute baseline data quality score"),
    ChecklistItem(stage=Stage.DIAGNOSE, label_ar="رسم خريطة المخاطر (PDPL/AI/تشغيلية)", label_en="Map risks (PDPL / AI / operational)"),
    ChecklistItem(stage=Stage.DESIGN, label_ar="تصميم workflow", label_en="Design workflow"),
    ChecklistItem(stage=Stage.DESIGN, label_ar="تعريف KPIs قابلة للقياس", label_en="Define measurable KPIs"),
    ChecklistItem(stage=Stage.BUILD, label_ar="بناء بدون تعقيد زائد", label_en="Build with minimum complexity"),
    ChecklistItem(stage=Stage.BUILD, label_ar="تفعيل Audit Log منذ اليوم الأول", label_en="Audit log enabled from day 1"),
    ChecklistItem(stage=Stage.VALIDATE, label_ar="تشغيل بوّابات الجودة الخمس", label_en="Run the 5 QA gates"),
    ChecklistItem(stage=Stage.VALIDATE, label_ar="حساب Quality Score (الحد الأدنى 80)", label_en="Compute Quality Score (floor 80)"),
    ChecklistItem(stage=Stage.DELIVER, label_ar="تسليم Dashboard أو Workflow حي", label_en="Deliver live dashboard or workflow"),
    ChecklistItem(stage=Stage.DELIVER, label_ar="تقرير تنفيذي + SOP + جلسة تدريب", label_en="Executive report + SOP + training session"),
    ChecklistItem(stage=Stage.PROVE, label_ar="قياس الأثر (قبل/بعد) خلال 14 يومًا", label_en="Measure before/after impact within 14 days"),
    ChecklistItem(stage=Stage.PROVE, label_ar="كتابة Proof Pack في Proof Ledger", label_en="Write Proof Pack into Proof Ledger"),
    ChecklistItem(stage=Stage.EXPAND, label_ar="فتح محادثة Retainer/توسّع", label_en="Open Retainer / expansion conversation"),
    ChecklistItem(stage=Stage.EXPAND, label_ar="عرض تالٍ مكتوب (موقّع أو موثّق كلا)", label_en="Next-step proposal drafted (signed or documented no)"),
]


_PER_OFFER: dict[StartingOffer, list[ChecklistItem]] = {
    StartingOffer.REVENUE_INTELLIGENCE: [
        ChecklistItem(stage=Stage.DISCOVER, label_ar="استلام seed أو CRM export", label_en="Receive seed or CRM export"),
        ChecklistItem(stage=Stage.BUILD, label_ar="تشغيل lead_scoring + dedupe", label_en="Run lead_scoring + dedupe"),
        ChecklistItem(stage=Stage.BUILD, label_ar="صياغة top-10 outreach drafts ثنائية اللغة", label_en="Draft top-10 bilingual outreach"),
        ChecklistItem(stage=Stage.DELIVER, label_ar="تسليم Mini CRM Board", label_en="Deliver Mini CRM Board"),
    ],
    StartingOffer.AI_QUICK_WIN: [
        ChecklistItem(stage=Stage.DISCOVER, label_ar="اختيار حالة استخدام واحدة من القائمة", label_en="Select one use case from curated list"),
        ChecklistItem(stage=Stage.BUILD, label_ar="بناء automation + approval workflow", label_en="Build automation + approval workflow"),
        ChecklistItem(stage=Stage.DELIVER, label_ar="جلسة تدريب ساعة واحدة + Runbook", label_en="1-hour training + Runbook"),
        ChecklistItem(stage=Stage.PROVE, label_ar="ROI baseline (ساعات/أخطاء/سرعة)", label_en="ROI baseline (hours / errors / speed)"),
    ],
    StartingOffer.COMPANY_BRAIN: [
        ChecklistItem(stage=Stage.DISCOVER, label_ar="جمع قائمة الوثائق + أصحابها", label_en="Collect document inventory + owners"),
        ChecklistItem(stage=Stage.BUILD, label_ar="فحص PII + إخفاء قبل الفهرسة", label_en="PII detection + redaction before indexing"),
        ChecklistItem(stage=Stage.BUILD, label_ar="فهرسة RAG مع تتبّع المصادر", label_en="RAG indexing with source tracking"),
        ChecklistItem(stage=Stage.VALIDATE, label_ar="اختبار 'no source = no answer'", label_en='Test "no source = no answer" rule'),
        ChecklistItem(stage=Stage.DELIVER, label_ar="إعداد قواعد الوصول بثلاث مستويات", label_en="Set 3-tier access rules"),
    ],
}


def checklist_for(offer: StartingOffer) -> list[ChecklistItem]:
    return list(_COMMON) + list(_PER_OFFER.get(offer, []))


def checklist_to_dict(items: list[ChecklistItem]) -> list[dict[str, Any]]:
    return [i.model_dump(mode="json") for i in items]
