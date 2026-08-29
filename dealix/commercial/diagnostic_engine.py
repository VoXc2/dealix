"""Evidence-bound commercial diagnostic engine.

This compatibility surface prepares a deterministic internal diagnostic draft from
explicitly supplied context. It never invents benchmarks, ROI, revenue, savings,
conversion lifts, compliance certifications, customer outcomes, payment state, or
commercial authority.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

SECTORS = {
    "b2b_saas": {"ar": "برمجيات B2B", "en": "B2B SaaS"},
    "b2b_services": {"ar": "خدمات B2B", "en": "B2B Services"},
    "agency": {"ar": "وكالة", "en": "Agency"},
    "training_consulting": {"ar": "تدريب واستشارات", "en": "Training & Consulting"},
    "ecommerce_b2c": {"ar": "تجارة إلكترونية", "en": "E-commerce"},
    "real_estate": {"ar": "عقارات", "en": "Real Estate"},
    "healthcare_clinic": {"ar": "صحة وعيادات", "en": "Healthcare"},
    "marketing_agency": {"ar": "وكالة تسويق", "en": "Marketing Agency"},
    "logistics": {"ar": "لوجستيات", "en": "Logistics"},
    "engineering": {"ar": "هندسة ومقاولات", "en": "Engineering & Contracting"},
    "fintech": {"ar": "تقنية مالية", "en": "Fintech"},
    "food_beverage": {"ar": "مطاعم وأغذية", "en": "F&B"},
}

_PAIN_MAP = {
    "lead_gen": {"ar": "توليد عملاء محتملين", "en": "Lead generation"},
    "sales_close": {"ar": "إغلاق الصفقات", "en": "Sales closing"},
    "client_retention": {"ar": "الاحتفاظ بالعملاء", "en": "Client retention"},
    "reporting": {"ar": "التقارير والمؤشرات", "en": "Reporting & KPIs"},
    "automation": {"ar": "أتمتة العمليات", "en": "Process automation"},
    "pricing": {"ar": "التسعير والعروض", "en": "Pricing & proposals"},
    "team_ops": {"ar": "عمليات الفريق", "en": "Team operations"},
    "data_quality": {"ar": "جودة البيانات", "en": "Data quality"},
}


class DiagnosticRequest(BaseModel):
    company_name: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    pain_points: list[str] = Field(default_factory=list)
    website_url: str = ""
    contact_name: str = ""
    contact_phone: str = ""
    pipeline_state: str = ""
    notes: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    baseline_ref: str = ""
    source_context: str = ""
    customer_validation_ref: str = ""


class DiagnosticSection(BaseModel):
    title_ar: str
    title_en: str
    body_ar: str
    body_en: str
    classification: str = "INTERNAL_DRAFT"


class DiagnosticReport(BaseModel):
    report_id: str
    company_name: str
    sector: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sections: list[DiagnosticSection]
    markdown_ar_en: str
    recommended_service: str = "qualified_discovery"
    recommendation_status: str = "HYPOTHESIS_ONLY"
    evidence_refs: list[str] = Field(default_factory=list)
    baseline_ref: str = ""
    source_context_present: bool = False
    unknowns: list[str] = Field(default_factory=list)
    claim_status: str = "EVIDENCE_BOUND_NO_UNSUPPORTED_CLAIMS"
    customer_value_claim: bool = False
    guarantee: bool = False
    payment_url_placeholder: str = ""
    approval_status: str = "approval_required"
    governance_decision: str = "pending"
    llm_used: bool = False
    customer_validation_ref: str = ""
    customer_validation_status: str = UNKNOWN

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class DiagnosticEngine:
    """Generate a deterministic bilingual diagnostic draft from supplied evidence."""

    def generate(self, req: DiagnosticRequest) -> DiagnosticReport:
        evidence_refs = sorted({item.strip() for item in req.evidence_refs if item.strip()})
        baseline_ref = req.baseline_ref.strip()
        customer_validation_ref = req.customer_validation_ref.strip()
        source_context = req.source_context.strip()
        pains = sorted({item.strip() for item in req.pain_points if item.strip()})

        normalized = {
            "company_name": req.company_name.strip(),
            "sector": req.sector.strip(),
            "pain_points": pains,
            "evidence_refs": evidence_refs,
            "baseline_ref": baseline_ref,
            "source_context": source_context,
            "customer_validation_ref": customer_validation_ref,
        }
        report_id = hashlib.sha256(
            json.dumps(normalized, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:16]

        unknown_details: list[str] = []
        if not baseline_ref:
            unknown_details.append("customer_approved_baseline")
        if not evidence_refs:
            unknown_details.append("source_linked_evidence")
        if not customer_validation_ref:
            unknown_details.append("customer_validated_business_impact")

        unknowns = [UNKNOWN, *unknown_details] if unknown_details else []
        customer_validation_status = (
            "CUSTOMER_VALIDATED_WITH_REFERENCE" if customer_validation_ref else UNKNOWN
        )

        sector_ar = SECTORS.get(req.sector, {}).get("ar", req.sector)
        sector_en = SECTORS.get(req.sector, {}).get("en", req.sector)
        pains_ar = self._pain_labels(pains, "ar")
        pains_en = self._pain_labels(pains, "en")

        sections = self._template_sections(
            req=req,
            sector_ar=sector_ar,
            sector_en=sector_en,
            pains_ar=pains_ar,
            pains_en=pains_en,
            baseline_ref=baseline_ref,
            evidence_refs=evidence_refs,
            customer_validation_ref=customer_validation_ref,
        )
        markdown = self._render_markdown(
            req=req,
            sections=sections,
            report_id=report_id,
            evidence_refs=evidence_refs,
            baseline_ref=baseline_ref,
            unknowns=unknowns,
            customer_validation_status=customer_validation_status,
        )

        return DiagnosticReport(
            report_id=report_id,
            company_name=req.company_name,
            sector=req.sector,
            sections=sections,
            markdown_ar_en=markdown,
            evidence_refs=evidence_refs,
            baseline_ref=baseline_ref,
            source_context_present=bool(source_context),
            unknowns=unknowns,
            customer_validation_ref=customer_validation_ref,
            customer_validation_status=customer_validation_status,
        )

    @staticmethod
    def _pain_labels(pain_points: list[str], locale: str) -> str:
        labels = [_PAIN_MAP.get(point, {}).get(locale, point) for point in pain_points]
        if not labels:
            return UNKNOWN
        return "، ".join(labels) if locale == "ar" else ", ".join(labels)

    def _template_sections(
        self,
        *,
        req: DiagnosticRequest,
        sector_ar: str,
        sector_en: str,
        pains_ar: str,
        pains_en: str,
        baseline_ref: str,
        evidence_refs: list[str],
        customer_validation_ref: str,
    ) -> list[DiagnosticSection]:
        name = req.company_name.strip()
        pains_known = pains_en != UNKNOWN
        evidence_state = "EVIDENCE_LINKED" if evidence_refs else UNKNOWN
        baseline_state = "BASELINE_LINKED" if baseline_ref else UNKNOWN
        validation_state = (
            "CUSTOMER_VALIDATED_WITH_REFERENCE" if customer_validation_ref else UNKNOWN
        )

        pain_ar = (
            f"المشكلات المدخلة في الطلب: {pains_ar}."
            if pains_known
            else "لم تُدخل نقاط ألم قابلة للتقييم بعد."
        )
        pain_en = (
            f"Problems entered in the request: {pains_en}."
            if pains_known
            else "No pain points have been entered for assessment yet."
        )

        return [
            DiagnosticSection(
                title_ar="ملخص تنفيذي",
                title_en="Executive Summary",
                body_ar=(
                    f"هذه مسودة تشخيص داخلية لشركة {name} في قطاع {sector_ar}. "
                    "تعرض المدخلات والفرضيات فقط، ولا تثبت أثرًا تجاريًا أو نتيجة للعميل."
                ),
                body_en=(
                    f"This is an internal diagnostic draft for {name} in {sector_en}. "
                    "It presents supplied inputs and hypotheses only and does not establish customer value or a business outcome."
                ),
            ),
            DiagnosticSection(
                title_ar="الوضع الراهن",
                title_en="Current State",
                body_ar=(
                    f"حالة الدليل الحالية: {evidence_state}. حالة خط الأساس: {baseline_state}. "
                    "أي معلومة غير مرتبطة بمرجع تبقى غير مثبتة."
                ),
                body_en=(
                    f"Current evidence state: {evidence_state}. Baseline state: {baseline_state}. "
                    "Any information without a linked reference remains unverified."
                ),
            ),
            DiagnosticSection(
                title_ar="فجوات الإيراد المحتملة",
                title_en="Potential Revenue Gaps",
                body_ar=(
                    f"{pain_ar} هذه إشارات أو فرضيات أولية ولا تصبح فجوات مثبتة دون دليل مرتبط أو تحقق صريح من العميل."
                ),
                body_en=(
                    f"{pain_en} These are initial signals or hypotheses and do not become verified gaps without linked evidence or explicit customer validation."
                ),
            ),
            DiagnosticSection(
                title_ar="فرضيات فرص الذكاء الاصطناعي",
                title_en="AI Opportunity Hypotheses",
                body_ar=(
                    "يمكن تقييم ترتيب المتابعة، تلخيص السياق، كشف فجوات الملكية، وتجهيز المسودات الداخلية. "
                    "كل استخدام يبقى فرضية حتى يرتبط ببيانات ونطاق ومعيار نجاح معتمد."
                ),
                body_en=(
                    "Potential uses include follow-up prioritization, context summarization, ownership-gap detection, and internal draft preparation. "
                    "Each use remains a hypothesis until tied to data, scope, and an approved success criterion."
                ),
            ),
            DiagnosticSection(
                title_ar="خارطة الأولويات",
                title_en="Priority Map",
                body_ar=(
                    "الأولوية الأولى هي تثبيت المشكلة بالأدلة، ثم تحديد خط أساس يوافق عليه العميل، ثم اختيار تدخل صغير قابل للقياس."
                ),
                body_en=(
                    "Priority one is evidence-backed problem validation, followed by a customer-approved baseline and then one small measurable intervention."
                ),
            ),
            DiagnosticSection(
                title_ar="خطة العمل المقترحة",
                title_en="Proposed Work Plan",
                body_ar=(
                    "بعد Free Mini Diagnostic والتأهيل، يمكن الانتقال إلى Qualified Discovery. "
                    "بعد Discovery فقط يمكن تجهيز نطاق Customer-Specific Quote للمراجعة."
                ),
                body_en=(
                    "After the Free Mini Diagnostic and qualification, the next step may be Qualified Discovery. "
                    "Only after Discovery may a Customer-Specific Quote scope be prepared for review."
                ),
            ),
            DiagnosticSection(
                title_ar="خطة القياس",
                title_en="Measurement Plan",
                body_ar=(
                    f"حالة تحقق العميل: {validation_state}. لا توجد نسبة تحسن أو ROI أو وفر مثبت في هذه المسودة. "
                    "يجب تعريف القياس من خط أساس ومالك ومصدر وقاعدة قرار موثقة."
                ),
                body_en=(
                    f"Customer validation state: {validation_state}. This draft contains no verified improvement percentage, ROI, or savings. "
                    "Measurement must be defined from a documented baseline, owner, source, and decision rule."
                ),
            ),
            DiagnosticSection(
                title_ar="المخاطر والضوابط",
                title_en="Risks & Guardrails",
                body_ar=(
                    "المسودة داخلية وتتطلب موافقة قبل أي مشاركة. لا إرسال خارجي تلقائي، ولا التزام سعري أو تعاقدي، "
                    "ولا ادعاء امتثال أو نتيجة دون دليل مناسب."
                ),
                body_en=(
                    "This draft is internal and requires approval before sharing. No automatic external send, pricing or contractual commitment, "
                    "or compliance/outcome claim is allowed without appropriate evidence."
                ),
            ),
            DiagnosticSection(
                title_ar="الخطوة التالية",
                title_en="Next Step",
                body_ar=(
                    "استكمل الدليل الناقص في Free Mini Diagnostic. إذا ثبتت مشكلة مؤهلة، انتقل إلى Qualified Discovery؛ وإلا توقف أو أعد صياغة الفرضية."
                ),
                body_en=(
                    "Complete the missing evidence in the Free Mini Diagnostic. If a qualified problem is established, move to Qualified Discovery; otherwise stop or revise the hypothesis."
                ),
            ),
            DiagnosticSection(
                title_ar="إشعار البيانات",
                title_en="Data Notice",
                body_ar=(
                    "استخدم الحد الأدنى من البيانات اللازمة، واربط كل حقيقة بمصدرها، واحتفظ بحالة الموافقة والحذف وفق السياسة المعتمدة. "
                    "هذا إشعار تشغيلي وليس شهادة امتثال أو رأيًا قانونيًا."
                ),
                body_en=(
                    "Use the minimum necessary data, link each fact to its source, and retain consent/deletion state under the approved policy. "
                    "This is an operating notice, not a compliance certification or legal opinion."
                ),
            ),
        ]

    @staticmethod
    def _render_markdown(
        *,
        req: DiagnosticRequest,
        sections: list[DiagnosticSection],
        report_id: str,
        evidence_refs: list[str],
        baseline_ref: str,
        unknowns: list[str],
        customer_validation_status: str,
    ) -> str:
        evidence = ", ".join(evidence_refs) if evidence_refs else UNKNOWN
        baseline = baseline_ref if baseline_ref else UNKNOWN
        lines = [
            f"# تشخيص Dealix — {req.company_name}",
            f"**Dealix Diagnostic — {req.company_name}**",
            "",
            f"ID: `{report_id}` | Status: **INTERNAL_DRAFT / APPROVAL_REQUIRED**",
            f"Evidence refs: `{evidence}`",
            f"Baseline ref: `{baseline}`",
            f"Customer validation: `{customer_validation_status}`",
            "",
            "---",
            "",
        ]
        for index, section in enumerate(sections, 1):
            lines.extend(
                [
                    f"## {index}. {section.title_ar} / {section.title_en}",
                    "",
                    f"**{section.body_ar}**",
                    "",
                    f"*{section.body_en}*",
                    "",
                ]
            )
        lines.extend(
            [
                "## Unknowns / المجهولات",
                "",
                *([f"- {item}" for item in unknowns] if unknowns else ["- NONE_RECORDED_FROM_SUPPLIED_INPUT"]),
                "",
                "---",
                "",
                "> This diagnostic separates evidence, observations, and hypotheses. It does not establish revenue, savings, ROI, conversion lift, compliance status, or customer value.",
                "> هذا التشخيص يفصل بين الأدلة والملاحظات والفرضيات، ولا يثبت إيرادًا أو وفرًا أو عائد استثمار أو تحسن تحويل أو حالة امتثال أو قيمة للعميل.",
                "",
                "> DRAFT_NOT_SENT — no external sharing without the approved authority and channel gates.",
            ]
        )
        return "\n".join(lines)


__all__ = [
    "DiagnosticEngine",
    "DiagnosticReport",
    "DiagnosticRequest",
    "DiagnosticSection",
    "UNKNOWN",
]
