# العربية

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead) — قسم هندسة المنصة.

## الغرض

تعرّف هذه الوثيقة مجموعة المقاييس التي تجعل أثر Dealix مرئياً للقيادة. كل مقياس مرصود أو محسوب من بيانات حقيقية؛ لا يوجد رقم مفبرك ولا وعد مضمون. حين يكون الرقم تقديرياً يُعلَن ذلك صراحةً مع مدى الثقة.

## فئات المقاييس

### 1. مقاييس الأثر (Impact)

- **ساعات موفَّرة (Hours Saved):** مجموع الوقت المرصود الذي وفّرته أتمتة سير العمل، مصدره أحداث `value_ledger`. يُعرض كرقم مرصود مع نافذة القياس.
- **عملاء مؤهَّلون (Qualified Leads):** عدد العملاء المحتملين الذين بلغوا حد التأهيل، من خطّاف الإيراد في `auto_client_acquisition/revenue_intelligence_founder_hooks.py`.
- **احتكاك مُزال (Friction Removed):** عدد نقاط الاحتكاك المغلقة من سجل الاحتكاك المجمَّع.

### 2. مقاييس التبنّي (Adoption)

- **معدّل التبنّي (Adoption Rate):** نسبة الخدمات المفعَّلة فعلياً إلى الخدمات المتعاقد عليها.
- **عمق الاستخدام (Usage Depth):** عدد الميزات المستخدمة لكل خدمة مفعَّلة.

### 3. مقاييس الإيراد (Revenue)

- **خط الأنابيب المرئي (Visible Pipeline):** قيمة الفرص في كل مرحلة، من لوحة خط الأنابيب في `panels.py`.
- **فرص مُثبتة بأدلة (Evidenced Opportunities):** فرص مرتبطة بدليل من حزمة الأدلة — تستبدل صراحةً أي ادعاء بـ "مبيعات مضمونة".

### 4. مقاييس الهدر والاختناقات (Waste & Bottlenecks)

- **اختناقات مرئية (Visible Bottlenecks):** قائمة المعوّقات مرتّبة حسب الأثر من `blockers.py`.
- **تكلفة لكل نتيجة (Cost per Outcome):** التكلفة المرصودة من `cost_summary.py` مقسومة على النتائج.

## خطافات المراقبة

- أحداث القيمة عبر `auto_client_acquisition/value_os/value_ledger.py`.
- التقرير الشهري للقيمة عبر `auto_client_acquisition/value_os/monthly_report.py`.
- التكلفة عبر `auto_client_acquisition/founder_v10/cost_summary.py`.
- البطاقة اليومية عبر `scripts/founder_daily_scorecard.py` و`docs/ops/daily_scorecard.md`.

## قواعد الحوكمة

- كل مقياس مُعلَن المصدر ونافذة القياس.
- المقاييس التقديرية تُوسَم "تقديري" دائماً ولا تُعرض كحقيقة.
- لا يُعرض أي مقياس يحوي بيانات شخصية في تقرير موجَّه للعميل.
- يُراجَع تعريف كل مقياس ربع سنوياً من مالك الطبقة.

## درجة الجاهزية الحالية

**74 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/executive_intelligence/readiness.md`، `platform/executive_intelligence/architecture.md`.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

**Owner:** Executive Intelligence Layer Lead — Platform Engineering.

## Purpose

This document defines the metric set that makes Dealix impact visible to leadership. Every metric is observed or computed from real data; there is no fabricated number and no guaranteed promise. When a number is an estimate, that is stated explicitly with a confidence range.

## Metric categories

### 1. Impact metrics

- **Hours Saved:** total observed time saved by workflow automation, sourced from `value_ledger` events. Presented as an observed number with its measurement window.
- **Qualified Leads:** count of prospects that crossed the qualification threshold, from the revenue hook in `auto_client_acquisition/revenue_intelligence_founder_hooks.py`.
- **Friction Removed:** count of friction points closed, from the aggregated friction log.

### 2. Adoption metrics

- **Adoption Rate:** ratio of services actually activated to services contracted.
- **Usage Depth:** number of features used per activated service.

### 3. Revenue metrics

- **Visible Pipeline:** value of opportunities per stage, from the pipeline panel in `panels.py`.
- **Evidenced Opportunities:** opportunities tied to evidence from the proof pack — explicitly replaces any "guaranteed sales" claim.

### 4. Waste & Bottleneck metrics

- **Visible Bottlenecks:** blocker list ranked by impact from `blockers.py`.
- **Cost per Outcome:** observed cost from `cost_summary.py` divided by outcomes.

## Observability hooks

- Value events via `auto_client_acquisition/value_os/value_ledger.py`.
- Monthly value report via `auto_client_acquisition/value_os/monthly_report.py`.
- Cost via `auto_client_acquisition/founder_v10/cost_summary.py`.
- Daily scorecard via `scripts/founder_daily_scorecard.py` and `docs/ops/daily_scorecard.md`.

## Governance rules

- Every metric declares its source and measurement window.
- Estimated metrics are always labelled "estimated" and never presented as fact.
- No metric containing PII is shown in a customer-facing report.
- Every metric definition is reviewed quarterly by the Layer Lead.

## Current readiness score

**74 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/executive_intelligence/readiness.md`, `platform/executive_intelligence/architecture.md`.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
