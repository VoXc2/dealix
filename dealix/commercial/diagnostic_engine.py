"""Commercial Diagnostic Engine — 10-section bilingual report (AR+EN).

Input:  DiagnosticRequest (company_name, sector, pain_points)
Output: DiagnosticReport (10 structured sections + Markdown)
Gate:   approval_required — never auto-sent to customer (NO_LIVE_SEND)
LLM:    Claude claude-sonnet-4-6 via ANTHROPIC_API_KEY; gracefully degrades
        to template-only output when LLM is unavailable.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

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


class DiagnosticSection(BaseModel):
    title_ar: str
    title_en: str
    body_ar: str
    body_en: str


class DiagnosticReport(BaseModel):
    report_id: str
    company_name: str
    sector: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sections: list[DiagnosticSection]
    markdown_ar_en: str
    recommended_service: str = "sprint_499_sar"
    payment_url_placeholder: str = ""
    approval_status: str = "approval_required"
    governance_decision: str = "pending"  # pending | approved | rejected
    llm_used: bool = False

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class DiagnosticEngine:
    """Generates a 10-section bilingual diagnostic for a Saudi B2B company."""

    def generate(self, req: DiagnosticRequest) -> DiagnosticReport:
        report_id = hashlib.sha256(
            f"{req.company_name}{req.sector}{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:16]

        pain_labels_ar = [
            _PAIN_MAP.get(p, {}).get("ar", p) for p in (req.pain_points or [])
        ]
        pain_labels_en = [
            _PAIN_MAP.get(p, {}).get("en", p) for p in (req.pain_points or [])
        ]
        sector_ar = SECTORS.get(req.sector, {}).get("ar", req.sector)
        sector_en = SECTORS.get(req.sector, {}).get("en", req.sector)
        pains_ar = "، ".join(pain_labels_ar) if pain_labels_ar else "لم تُحدَّد بعد"
        pains_en = ", ".join(pain_labels_en) if pain_labels_en else "not specified"

        llm_used = False
        sections = self._llm_sections(req, sector_ar, sector_en, pains_ar, pains_en)
        if sections:
            llm_used = True
        else:
            sections = self._template_sections(req, sector_ar, sector_en, pains_ar, pains_en)

        md = self._render_markdown(req, sections, report_id)
        return DiagnosticReport(
            report_id=report_id,
            company_name=req.company_name,
            sector=req.sector,
            sections=sections,
            markdown_ar_en=md,
            llm_used=llm_used,
        )

    def _llm_sections(
        self, req: DiagnosticRequest, sector_ar: str, sector_en: str,
        pains_ar: str, pains_en: str,
    ) -> list[DiagnosticSection]:
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            return []
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            prompt = (
                f"أنت مستشار B2B سعودي متخصص في تحليل عمليات الإيراد. "
                f"اكتب تشخيصاً احترافياً موجزاً لشركة '{req.company_name}' "
                f"في قطاع '{sector_ar}' ({sector_en}). "
                f"أبرز نقاط الألم: {pains_ar}.\n\n"
                f"أنتج JSON مصفوفة من 10 كائنات، كل كائن يحتوي:\n"
                f"title_ar, title_en, body_ar (3-4 جمل), body_en (3-4 sentences).\n"
                f"الأقسام العشرة بالترتيب:\n"
                f"1. ملخص تنفيذي / Executive Summary\n"
                f"2. الوضع الراهن / Current State\n"
                f"3. فجوات الإيراد / Revenue Gaps\n"
                f"4. فرص الذكاء الاصطناعي / AI Opportunities\n"
                f"5. خارطة الأولويات / Priority Map\n"
                f"6. خطة 30 يوماً / 30-Day Plan\n"
                f"7. مؤشرات النجاح / Success KPIs\n"
                f"8. المخاطر والضمانات / Risks & Guardrails\n"
                f"9. الخطوة التالية / Next Step\n"
                f"10. إشعار PDPL / PDPL Notice\n\n"
                f"أرجع JSON فقط — لا نص خارج JSON."
            )
            msg = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = msg.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw)
            return [DiagnosticSection(**s) for s in data]
        except Exception as exc:
            log.warning("diagnostic_llm_failed error=%s", exc)
            return []

    def _template_sections(
        self, req: DiagnosticRequest, sector_ar: str, sector_en: str,
        pains_ar: str, pains_en: str,
    ) -> list[DiagnosticSection]:
        name = req.company_name
        return [
            DiagnosticSection(
                title_ar="ملخص تنفيذي",
                title_en="Executive Summary",
                body_ar=f"شركة {name} في قطاع {sector_ar} لديها إمكانات نمو واضحة. "
                        f"التحديات الرئيسية تشمل: {pains_ar}. "
                        f"Dealix تقترح خطة تشغيل ذكية تُحقق نتائج قابلة للقياس خلال 30 يوماً.",
                body_en=f"{name} in the {sector_en} sector shows clear growth potential. "
                        f"Key challenges include: {pains_en}. "
                        f"Dealix proposes a smart ops plan to deliver measurable results within 30 days.",
            ),
            DiagnosticSection(
                title_ar="الوضع الراهن",
                title_en="Current State",
                body_ar=f"بناءً على المعطيات المتاحة، تعتمد {name} على عمليات يدوية في معظم مراحل "
                        f"دورة المبيعات. غياب أتمتة المتابعة يُكلّف وقتاً وفرصاً. "
                        f"المنافسون يتحركون بسرعة أكبر في قطاع {sector_ar}.",
                body_en=f"Based on available data, {name} relies on manual processes across most "
                        f"sales cycle stages. Lack of follow-up automation costs time and opportunities. "
                        f"Competitors are moving faster in the {sector_en} sector.",
            ),
            DiagnosticSection(
                title_ar="فجوات الإيراد",
                title_en="Revenue Gaps",
                body_ar=f"الفجوات المحددة: {pains_ar}. "
                        f"تشير الدراسات السعودية إلى أن شركات B2B تخسر 20-35% من فرصها "
                        f"بسبب بطء الاستجابة وغياب التوثيق. "
                        f"الأثر المالي المقدر: 15,000-50,000 ر.س سنوياً للشركات المتوسطة.",
                body_en=f"Identified gaps: {pains_en}. "
                        f"Saudi B2B studies indicate companies lose 20-35% of opportunities "
                        f"due to slow response and lack of documentation. "
                        f"Estimated financial impact: 15,000-50,000 SAR annually for mid-size firms.",
            ),
            DiagnosticSection(
                title_ar="فرص الذكاء الاصطناعي",
                title_en="AI Opportunities",
                body_ar="يمكن لـ Dealix أتمتة: مسودات التواصل الأولي (توفير 3 ساعات/أسبوع)، "
                        "تقييم العملاء المحتملين (دقة +40%)، "
                        "توثيق نتائج الجلسات تلقائياً، "
                        "وتوليد تقارير KPI بنقرة واحدة.",
                body_en="Dealix can automate: initial outreach drafts (saving 3 hrs/week), "
                        "lead scoring (accuracy +40%), "
                        "automatic session documentation, "
                        "and one-click KPI report generation.",
            ),
            DiagnosticSection(
                title_ar="خارطة الأولويات",
                title_en="Priority Map",
                body_ar="الأولوية 1 (هذا الأسبوع): أتمتة متابعة العملاء المحتملين. "
                        "الأولوية 2 (الأسبوع الثاني): بناء نظام التوثيق. "
                        "الأولوية 3 (الأسبوع الثالث): لوحة KPI للمبيعات. "
                        "الأولوية 4 (الشهر الثاني): نظام الاحتفاظ بالعملاء.",
                body_en="Priority 1 (this week): Automate lead follow-up. "
                        "Priority 2 (week 2): Build documentation system. "
                        "Priority 3 (week 3): Sales KPI dashboard. "
                        "Priority 4 (month 2): Customer retention system.",
            ),
            DiagnosticSection(
                title_ar="خطة 30 يوماً",
                title_en="30-Day Plan",
                body_ar="الأسبوع 1: إعداد نظام تقييم العملاء + أول 5 مسودات تواصل. "
                        "الأسبوع 2: تفعيل متابعة تلقائية + قالب الاقتراح. "
                        "الأسبوع 3: لوحة KPI + تقرير الأداء الأسبوعي. "
                        "الأسبوع 4: مراجعة النتائج + خطة الشهر الثاني.",
                body_en="Week 1: Set up lead scoring + first 5 outreach drafts. "
                        "Week 2: Activate automated follow-up + proposal template. "
                        "Week 3: KPI dashboard + weekly performance report. "
                        "Week 4: Review results + month-2 plan.",
            ),
            DiagnosticSection(
                title_ar="مؤشرات النجاح",
                title_en="Success KPIs",
                body_ar="نستهدف خلال 30 يوماً: معدل استجابة العملاء +25%، "
                        "وقت إغلاق الصفقة -30%، "
                        "وثيقة KPI أسبوعية منجزة 4/4 أسابيع، "
                        "توفير 5+ ساعات أسبوعياً من المهام المتكررة.",
                body_en="30-day targets: customer response rate +25%, "
                        "deal close time -30%, "
                        "weekly KPI doc completed 4/4 weeks, "
                        "5+ hours/week saved from repetitive tasks.",
            ),
            DiagnosticSection(
                title_ar="المخاطر والضمانات",
                title_en="Risks & Guardrails",
                body_ar="جميع المسودات تتطلب موافقة الفاوندر قبل الإرسال. "
                        "لا إرسال تلقائي لأي رسالة خارجية. "
                        "البيانات محمية وفق نظام PDPL السعودي. "
                        "في حال عدم تحقيق نتيجة قابلة للقياس، نُعيد الجلسة مجاناً.",
                body_en="All drafts require founder approval before sending. "
                        "No automated external message sending. "
                        "Data protected under Saudi PDPL. "
                        "If no measurable result achieved, we repeat the session free.",
            ),
            DiagnosticSection(
                title_ar="الخطوة التالية",
                title_en="Next Step",
                body_ar=f"نوصي ببدء برنامج الأسبوع المكثف (499 ر.س) مع {name}. "
                        f"يشمل: جلسة استلام، خريطة ألم مفصلة، 3 مسودات تواصل موافق عليها، "
                        f"وتقرير إثبات مرقّم. "
                        f"سيرسل الرابط بعد موافقة المؤسس على هذا التشخيص.",
                body_en=f"We recommend starting the Intensive Week Program (499 SAR) with {name}. "
                        f"Includes: intake session, detailed pain map, 3 approved outreach drafts, "
                        f"and a numbered proof report. "
                        f"Payment link will be sent after the founder approves this diagnostic.",
            ),
            DiagnosticSection(
                title_ar="إشعار PDPL",
                title_en="PDPL Notice",
                body_ar="تُعالَج البيانات المُقدَّمة في هذا التشخيص وفق نظام حماية البيانات "
                        "الشخصية السعودي (PDPL). "
                        "تُستخدم فقط لأغراض التحليل الداخلي ولا تُشارَك مع أطراف خارجية. "
                        "يحق لك طلب حذف بياناتك في أي وقت.",
                body_en="Data provided in this diagnostic is processed under Saudi PDPL. "
                        "Used solely for internal analysis and not shared with third parties. "
                        "You may request data deletion at any time.",
            ),
        ]

    def _render_markdown(
        self, req: DiagnosticRequest, sections: list[DiagnosticSection], report_id: str,
    ) -> str:
        now = datetime.now(UTC).strftime("%Y-%m-%d")
        lines = [
            f"# تشخيص Dealix — {req.company_name}",
            f"**Dealix Diagnostic — {req.company_name}**",
            f"",
            f"المعرف: `{report_id}` | التاريخ: {now} | الحالة: **يتطلب موافقة المؤسس**",
            f"ID: `{report_id}` | Date: {now} | Status: **approval_required**",
            f"",
            "---",
            "",
        ]
        for i, s in enumerate(sections, 1):
            lines += [
                f"## {i}. {s.title_ar} / {s.title_en}",
                "",
                f"**{s.body_ar}**",
                "",
                f"*{s.body_en}*",
                "",
            ]
        lines += [
            "---",
            "",
            "> هذا التشخيص للمراجعة فقط — لن يُرسَل لأي عميل دون موافقة المؤسس.",
            "> This diagnostic is for review only — will not be sent without founder approval.",
            "",
            "> **القيمة التقديرية ليست قيمة مُتحقَّقة** — Estimated value is not Verified value.",
        ]
        return "\n".join(lines)
