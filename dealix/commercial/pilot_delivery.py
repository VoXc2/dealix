"""Pilot Delivery Kit — 7-day structured delivery for the 499 SAR Sprint.

Generates day-by-day action templates, daily message drafts (approval-gated),
and a Week 1 proof report ready for customer delivery.
"""

from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta
from typing import Any

from pydantic import BaseModel, Field


class PilotStartRequest(BaseModel):
    account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    contact_name: str = ""
    sector: str = "b2b_services"
    pain_points: list[str] = Field(default_factory=list)
    diagnostic_id: str = ""
    founder_name: str = "سامي"
    start_date: str = ""  # ISO date string, defaults to today


class DayPlan(BaseModel):
    day: int
    date_str: str
    title_ar: str
    title_en: str
    tasks_ar: list[str]
    tasks_en: list[str]
    draft_messages_ar: list[str] = Field(default_factory=list)
    proof_event: str = ""
    approval_required: bool = True


class PilotPlan(BaseModel):
    pilot_id: str
    account_id: str
    company_name: str
    start_date: str
    end_date: str
    day_plans: list[DayPlan]
    week1_report_template: str
    upsell_script: str
    approval_status: str = "approval_required"
    governance_decision: str = "pending"  # pending | approved | rejected

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class PilotDeliveryKit:
    """Generates structured 7-day pilot delivery plan for a 499 SAR engagement."""

    def create_pilot_plan(self, req: PilotStartRequest) -> PilotPlan:
        import hashlib
        pilot_id = hashlib.sha256(
            f"{req.account_id}{req.company_name}{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:16]

        start = date.fromisoformat(req.start_date) if req.start_date else date.today()
        end = start + timedelta(days=6)

        day_plans = [
            DayPlan(
                day=1,
                date_str=str(start),
                title_ar="جلسة الاستلام وتحديد الألم",
                title_en="Intake & Pain Mapping",
                tasks_ar=[
                    f"مكالمة استلام 45 دقيقة مع {req.contact_name or req.company_name}",
                    "توثيق أكبر 3 تحديات بالتفصيل",
                    f"طلب البيانات: قائمة العملاء، معدل الإغلاق، متوسط قيمة الصفقة",
                    "إرسال ملخص كتابي للمكالمة (يتطلب موافقة الفاوندر)",
                ],
                tasks_en=[
                    f"45-min intake call with {req.contact_name or req.company_name}",
                    "Document top 3 challenges in detail",
                    "Request data: client list, close rate, average deal value",
                    "Send written call summary (requires founder approval)",
                ],
                draft_messages_ar=[
                    f"شكراً على وقتك اليوم {req.contact_name}. ملخص ما ناقشناه في المرفق. نبدأ غداً بـ [المهمة الأولى]. أي تعديلات؟",
                ],
                proof_event="intake_completed",
            ),
            DayPlan(
                day=2,
                date_str=str(start + timedelta(days=1)),
                title_ar="تدقيق الوضع الراهن",
                title_en="Current State Audit",
                tasks_ar=[
                    "تحليل بيانات الـ pipeline المُرسَلة",
                    "رسم خريطة العملية الحالية (مبيعات → تسليم → متابعة)",
                    "تحديد 5 نقاط احتكاك رئيسية",
                    "إعداد قائمة الفجوات مع الأولويات",
                ],
                tasks_en=[
                    "Analyze submitted pipeline data",
                    "Map current process (sales → delivery → follow-up)",
                    "Identify 5 key friction points",
                    "Prepare gap list with priorities",
                ],
                draft_messages_ar=[
                    "حللنا البيانات اليوم. أبرز ما وجدناه: [3 نقاط]. سنركز الأسبوع على هذه النقاط. نرسل الخطة التفصيلية غداً.",
                ],
                proof_event="current_state_documented",
            ),
            DayPlan(
                day=3,
                date_str=str(start + timedelta(days=2)),
                title_ar="تصميم الحل الأول",
                title_en="Solution Design — Day 1",
                tasks_ar=[
                    "بناء قالب متابعة العملاء الخاص بالقطاع",
                    "إعداد 2 مسودة تواصل للعملاء غير المُستجيبين",
                    "تصميم سكريبت المكالمة القصيرة (3 دقائق)",
                    "مراجعة الفاوندر للمسودات",
                ],
                tasks_en=[
                    "Build sector-specific follow-up template",
                    "Prepare 2 outreach drafts for non-responsive leads",
                    "Design short call script (3 minutes)",
                    "Founder review of drafts",
                ],
                draft_messages_ar=[
                    f"أهلاً {req.contact_name}، جهّزنا اليوم [أداة 1] و [أداة 2]. هل تريد نراجعها معاً في مكالمة قصيرة غداً؟",
                ],
                proof_event="solution_designed",
            ),
            DayPlan(
                day=4,
                date_str=str(start + timedelta(days=3)),
                title_ar="تطبيق الحل وأول قياس",
                title_en="Solution Implementation & First Measurement",
                tasks_ar=[
                    "تطبيق أدوات اليوم الثالث على الحالات الفعلية",
                    "قياس: وقت الاستجابة قبل وبعد",
                    "جمع أول دليل قابل للقياس (screenshot أو رقم)",
                    "توثيق الدليل في proof_event",
                ],
                tasks_en=[
                    "Apply day-3 tools on real cases",
                    "Measure: response time before and after",
                    "Collect first measurable evidence (screenshot or number)",
                    "Document evidence in proof_event",
                ],
                draft_messages_ar=[
                    "تحديث اليوم الرابع: طبّقنا [الأداة] على [X] حالة. النتيجة الأولية: [رقم]. سنكمل القياس غداً.",
                ],
                proof_event="first_measurement_captured",
            ),
            DayPlan(
                day=5,
                date_str=str(start + timedelta(days=4)),
                title_ar="توسيع التطبيق",
                title_en="Scaling the Solution",
                tasks_ar=[
                    "توسيع تطبيق الأدوات على كامل pipeline",
                    "إعداد تقرير مقارنة (قبل/بعد)",
                    "تحديد: أيّ الأدوات جلبت أكبر تأثير؟",
                    "تحضير مسودة التقرير الأسبوعي",
                ],
                tasks_en=[
                    "Scale tool application across full pipeline",
                    "Prepare before/after comparison report",
                    "Identify: which tools had the most impact?",
                    "Draft weekly report",
                ],
                draft_messages_ar=[
                    f"اليوم الخامس — النتائج تتشكل. جهّزنا مقارنة قبل/بعد. التقرير الأسبوعي سيصلك نهاية الأسبوع.",
                ],
                proof_event="impact_measured",
            ),
            DayPlan(
                day=6,
                date_str=str(start + timedelta(days=5)),
                title_ar="توثيق الإثبات",
                title_en="Proof Documentation",
                tasks_ar=[
                    "توثيق كل الأدلة المجمّعة طوال الأسبوع",
                    "إعداد طقم الإثبات (L1 Proof Pack)",
                    "حساب: وفورات الوقت، تحسين معدل الاستجابة، قيمة المخرجات",
                    "مراجعة الفاوندر للطقم قبل إرساله",
                ],
                tasks_en=[
                    "Document all evidence collected throughout the week",
                    "Prepare proof pack (L1 level)",
                    "Calculate: time savings, response rate improvement, output value",
                    "Founder reviews pack before delivery",
                ],
                draft_messages_ar=[
                    "جهّزنا طقم الإثبات الأسبوعي. يشمل [X نتيجة]. سنراجعه معك غداً في تقرير الإغلاق.",
                ],
                proof_event="proof_pack_built",
            ),
            DayPlan(
                day=7,
                date_str=str(start + timedelta(days=6)),
                title_ar="تقرير الإغلاق وعرض الاستمرار",
                title_en="Closing Report & Continuation Offer",
                tasks_ar=[
                    "تقديم التقرير الأسبوعي الكامل للعميل",
                    "مراجعة ما تم + ما بقي",
                    "تقديم عرض Managed Ops (2,999-4,999 ر.س/شهر) إن كانت النتائج واضحة",
                    "الحصول على شهادة موافقة كتابية إن رغب العميل",
                ],
                tasks_en=[
                    "Deliver full weekly report to client",
                    "Review completed + remaining items",
                    "Present Managed Ops offer (2,999-4,999 SAR/mo) if results are clear",
                    "Obtain written consent for testimonial if client agrees",
                ],
                draft_messages_ar=[
                    f"أهلاً {req.contact_name}،\nختام أسبوعنا الأول. نتائج هذا الأسبوع:\n"
                    f"✅ [نتيجة 1]\n✅ [نتيجة 2]\n✅ [نتيجة 3]\n\n"
                    f"هل تريد الاستمرار بنظام Managed Ops الشهري لتحقيق [الهدف التالي]؟",
                ],
                proof_event="week1_delivered",
            ),
        ]

        week1_report = self._week1_report_template(req)
        upsell_script = self._upsell_script(req)

        return PilotPlan(
            pilot_id=pilot_id,
            account_id=req.account_id,
            company_name=req.company_name,
            start_date=str(start),
            end_date=str(end),
            day_plans=day_plans,
            week1_report_template=week1_report,
            upsell_script=upsell_script,
        )

    def _week1_report_template(self, req: PilotStartRequest) -> str:
        return f"""# تقرير الأسبوع الأول — {req.company_name}
**Week 1 Report — {req.company_name}**

التاريخ: {{date}} | المعرف: {{pilot_id}}

---

## ما أنجزناه هذا الأسبوع / What We Accomplished This Week

| اليوم | المهمة | الحالة |
|-------|--------|--------|
| 1 | جلسة الاستلام | ✅ |
| 2 | تدقيق الوضع الراهن | ✅ |
| 3-4 | تصميم وتطبيق الحل | ✅ |
| 5-6 | القياس والإثبات | ✅ |
| 7 | تقرير الإغلاق | ✅ |

## النتائج القابلة للقياس / Measurable Results

- **[مؤشر 1]**: من {{before_1}} إلى {{after_1}} (+{{delta_1}}%)
- **[مؤشر 2]**: وفّرنا {{saved_hours}} ساعة/أسبوع
- **[مؤشر 3]**: {{other_result}}

## الأدلة / Evidence

1. {{evidence_1}}
2. {{evidence_2}}
3. {{evidence_3}}

## الخطوة التالية / Next Step

لتحويل هذه النتائج إلى نمو مستمر، نقترح برنامج **Managed Ops** (2,999 ر.س/شهر):
- 12 جلسة عمل شهرية
- لوحة KPI حية
- تقرير شهري + طقم إثبات
- أولوية الدعم

> هذا التقرير معتمد من الفاوندر — للمراجعة الداخلية قبل الإرسال.
"""

    def _upsell_script(self, req: PilotStartRequest) -> str:
        return f"""# سكريبت عرض Managed Ops — {req.company_name}

**المدة**: 10-15 دقيقة | **الهدف**: إغلاق عقد شهري (2,999-4,999 ر.س/شهر)

---

## الافتتاح (2 دقيقة)

"أهلاً {{contact_name}}، أولاً شكراً على ثقتك هذا الأسبوع.
نتائجنا كانت [أذكر أبرز نتيجتين].
السؤال الطبيعي الآن: كيف نحافظ على هذا الزخم؟"

## عرض القيمة (5 دقائق)

"برنامج Managed Ops يعني:
✅ أنا أشتغل معك بشكل مستمر — مش مشروع واحد ثم الوداع
✅ 12 جلسة شهرية = شغل منتظم كل أسبوع
✅ لوحة KPI مباشرة تحديث أسبوعي
✅ أولوية في أي طارئ
✅ تقرير إثبات شهري للمحاسبة

السعر: 2,999 ر.س/شهر — أقل من موظف واحد بدوام جزئي."

## معالجة الاعتراضات

**"سعره غالي"**:
"وقتك يساوي أكثر. في الأسبوع الأول وفّرنا [X ساعة]. بـ 12 شهر هذا [X*52 ساعة] = [قيمة وقتك]."

**"أحتاج أفكر"**:
"طبعاً. الاتفاق لشهر واحد قابل للإلغاء. جرّب شهراً واحداً بدون التزام طويل."

## الإغلاق

"هل نبدأ الشهر القادم؟ أرسل لك العقد الآن."

---
> موافقة الفاوندر مطلوبة قبل استخدام هذا السكريبت.
"""
