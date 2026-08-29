"""Evidence-bound commercial diagnostic engine.

This compatibility surface is deterministic and source-bound. It may prepare an
internal diagnostic draft, but it must not invent benchmarks, ROI, revenue,
savings, conversion lifts, compliance certifications, or customer outcomes.
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
    unknowns: list[str] = Field(default_factory=list)
    claim_status: str = "EVIDENCE_BOUND_NO_UNSUPPORTED_CLAIMS"
    customer_value_claim: bool = False
    guarantee: bool = False
    payment_url_placeholder: str = ""
    approval_status: str = "approval_required"
    governance_decision: str = "pending"
    llm_used: bool = False

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class DiagnosticEngine:
    """Generate a deterministic, bilingual, evidence-bound diagnostic draft."""

    def generate(self, req: DiagnosticRequest) -> DiagnosticReport:
        normalized = {
            "company_name": req.company_name.strip(),
            "sector": req.sector.strip(),
            "pain_points": sorted({p.strip() for p in req.pain_points if p.strip()}),
            "evidence_refs": sorted({r.strip() for r in req.evidence_refs if r.strip()}),
            "baseline_ref": req.baseline_ref.strip(),
            "source_context": req.source_context.strip(),
        }
        report_id = hashlib.sha256(
            json.dumps(normalized, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:16]

        sector_ar = SECTORS.get(req.sector, {}).get("ar", req.sector)
        sector_en = SECTORS.get(req.sector, {}).get("en", req.sector)
        pains_ar = self._pain_labels(req.pain_points, "ar")
        pains_en = self._pain_labels(req.pain_points, "en")

        unknowns = [
            "No customer-approved baseline was supplied."
            if not req.baseline_ref.strip()
            else "",
            "No source-linked evidence was supplied."
            if not req.evidence_refs
            else "",
            "Observed business impact remains unknown until the customer validates it."
            if not req.source_context.strip()
            else "",
        ]
        unknowns = [item for item in unknowns if item]

        sections = self._template_sections(
            req=req,
            sector_ar=sector_ar,
            sector_en=sector_en,
            pains_ar=pains_ar,
            pains_en=pains_en,
            unknowns=unknowns,
        )
        markdown = self._render_markdown(req, sections, report_id, unknowns)
        return DiagnosticReport(
            report_id=report_id,
            company_name=req.company_name,
            sector=req.sector,
            sections=sections,
            markdown_ar_en=markdown,
            evidence_refs=sorted({r.strip() for r in req.evidence_refs if r.strip()}),
            unknowns=unknowns,
        )

    @staticmethod
    def _pain_labels(pain_points: list[str], locale: str) -> str:
        labels = [
            _PAIN_MAP.get(point, {}).get(locale, point)
            for point in pain_points
            if point.strip()
        ]
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
        unknowns: list[str],
    ) -> list[DiagnosticSection]:
        name = req.company_name
        unknown_ar = "المعلومات غير المتوفرة تبقى غير معروفة إلى حين التحقق منها."
        unknown_en = "Unavailable information remains unknown until it is verified."
        pain_ar = (
            f"المشكلات التي أُدخلت في الطلب: {pains_ar}."
            if pains_ar != UNKNOWN
            else "لم تُدخل نقاط ألم قابلة للتقييم بعد."
        )
        pain_en = (
            f"Problems entered in the request: {pains_en}."
            if pains_en != UNKNOWN
            else "No pain points have been entered for assessment yet."
        )
        return [
            DiagnosticSection(
                title_ar="ملخص تنفيذي",
                title_en="Executive Summary",
                body_ar=(
                    f"هذا مسوّدة تشخيص داخلية لشركة {name} في قطاع {sector_ar}. "
                    "تعرض ما تم إدخاله، وتفصل الملاحظات عن الفرضيات، ولا تثبت نتيجة تجارية."
                ),
                body_en=(
                    f"This is an internal diagnostic draft for {name} in {sector_en}. "
                    "It separates supplied context from hypotheses and does not establish a business outcome."
                ),
            ),
            DiagnosticSection(
                title_ar="الوضع الراهن",
                title_en="Current State",
                body_ar=(
                    f"السياق المتاح يقتصر على المعلومات المقدمة عن {name}. "
                    f"{unknown_ar} لا تُعتبر أي معلومة غير موثقة حقيقة تشغيلية."
                ),
                body_en=(
                    f"The available context is limited to information supplied about {name}. "
                    f"{unknown_en} Unlinked information is not treated as an operating fact."
                ),
            ),
            DiagnosticSection(
                title_ar="فجوات الإيراد المحتملة",
                title_en="Potential Revenue Gaps",
                body_ar=f"{pain_ar} هذه إشارات أولية؛ لا تتحول إلى فجوة مثبتة دون مرجع دليل أو تحقق من العميل.",
                body_en=f"{pain_en} These are initial signals; they do not become verified gaps without evidence or customer validation.",
            ),
            DiagnosticSection(
                title_ar="فرضيات فرص الذكاء الاصطناعي",
                title_en="AI Opportunity Hypotheses",
                body_ar=(
                    "يمكن بحث استخدامات مثل ترتيب المتابعة، تلخيص السياق، كشف فجوات الملكية، "
                    "وتجهيز مسودات داخلية. كل ذلك فرضيات تحتاج إلى بيانات ونطاق وموافقة."
                ),
                body_en=(
                    "Potential uses include follow-up prioritization, context summarization, "
                    "ownership-gap detection, and internal draft preparation. These remain hypotheses requiring data, scope, and approval."
                ),
            ),
            DiagnosticSection(
                title_ar="خارطة الأولويات",
                title_en="Priority Map",
                body_ar=(
                    "الأولوية الأولى: تثبيت المشكلة والأدلة. الثانية: تحديد خط أساس يوافق عليه العميل. "
                    "الثالثة: اختيار تدخل صغير قابل للقياس قبل أي توسع."
                ),
                body_en=(
                    "Priority one: validate the problem and evidence. Priority two: define a customer-approved baseline. "
                    "Priority three: select a small measurable intervention before scaling."
                ),
            ),
            DiagnosticSection(
                title_ar="خطة العمل المقترحة",
                title_en="Proposed Work Plan",
                body_ar=(
                    "بعد التأهيل والاكتشاف يمكن إعداد نطاق خاص بالعميل لبرنامج Revenue Command Pilot لمدة 30 يومًا. "
                    "لا يمثل هذا التشخيص التزامًا بالتنفيذ أو مدة تسليم."
                ),
                body_en=(
                    "After qualification and discovery, a customer-specific 30-day Revenue Command Pilot scope may be prepared. "
                    "This diagnostic is not a delivery commitment or implementation schedule."
                ),
            ),
            DiagnosticSection(
                title_ar="مؤشرات القياس",
                title_en="Measurement Plan",
                body_ar=(
                    "تُحدد مؤشرات القياس مع العميل من خط أساس موثق، ومالك مسؤول، ومصدر بيانات، "
                    "وقاعدة قرار واضحة. لا توجد نتيجة أو نسبة مثبتة في هذه المسودة."
                ),
                body_en=(
                    "Measurement is defined with the customer using a documented baseline, accountable owner, data source, "
                    "and decision rule. This draft contains no verified result or percentage."
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
                    "This draft is internal and requires approval before sharing. No automatic external sending, pricing or contractual commitment, "
                    "or compliance/outcome claim is allowed without appropriate evidence."
                ),
            ),
            DiagnosticSection(
                title_ar="الخطوة التالية",
                title_en="Next Step",
                body_ar=(
                    "الخطوة المقترحة هي استكمال Free Mini Diagnostic ثم Qualified Discovery إذا وجدت مشكلة مؤهلة. "
                    "بعدها فقط يمكن تجهيز Customer-Specific Quote للمراجعة."
                ),
                body_en=(
                    "The suggested next step is to complete the Free Mini Diagnostic and then Qualified Discovery if a qualified problem exists. "
                    "Only after that may a Customer-Specific Quote be prepared for review."
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
                    "Use the minimum necessary data, link each fact to its source, and retain consent and deletion state under the approved policy. "
                    "This is an operating notice, not a compliance certification or legal opinion."
                ),
            ),
        ]

    @staticmethod
    def _render_markdown(
        req: DiagnosticRequest,
        sections: list[DiagnosticSection],
        report_id: str,
        unknowns: list[str],
    ) -> str:
        evidence = ", ".join(req.evidence_refs) if req.evidence_refs else UNKNOWN
        lines = [
            f"# تشخيص Dealix — {req.company_name}",
            f"**Dealix Diagnostic — {req.company_name}**",
            "",
            f"المعرف: `{report_id}` | الحالة: **مسودة داخلية تتطلب موافقة**",
            f"ID: `{report_id}` | Status: **internal draft — approval required**",
            f"Evidence refs / مراجع الأدلة: `{evidence}`",
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
                *(
                    [f"- {item}" for item in unknowns]
                    if unknowns
                    else ["- No material unknowns recorded from the supplied request."]
                ),
                "",
                "---",
                "",
                "> This diagnostic separates evidence, observations, and hypotheses. It does not establish revenue, savings, ROI, conversion lift, or customer value.",
                "> هذا التشخيص يفصل بين الأدلة والملاحظات والفرضيات، ولا يثبت إيرادًا أو وفرًا أو عائد استثمار أو تحسن تحويل أو قيمة للعميل.",
                "",
                "> DRAFT_NOT_SENT — لا مشاركة خارجية دون الموافقة والبوابات المعتمدة.",
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
