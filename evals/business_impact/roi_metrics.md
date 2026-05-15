# العربية

Owner: مالك تقييم الأثر التجاري — قائد العمليات التجارية (Commercial Ops Lead)

## الغرض

تقيس هذه الوثيقة الأثر التجاري لمنصة دياليكس: هل تُحدث الوكلاء وسير العمل فرقاً قابلاً للقياس مقارنةً بخط أساس موثّق. الطبقة الثامنة تهدف إلى التوقف عن خداع النفس؛ لا يُحتسب أي أثر إلا إذا كان مقاساً قبل/بعد، لا مُفترَضاً.

## مبادئ القياس

- كل مقياس تقديري حتى يُتحقَّق منه؛ القيمة التقديرية ليست قيمة مُتحقَّقة.
- لا أرقام مضمونة ولا نسب تحويل تُذكر كحقيقة؛ تُذكر كنمط آمن للحالة أو نطاق تقديري.
- يلزم خط أساس قبل أي ادعاء بتحسّن — انظر `evals/business_impact/baseline_template.md`.
- لا تُنشر مقاييس عملاء سرية؛ تُجمَّع الأنماط فقط.

## المقاييس

| المقياس | التعريف | المصدر | الحالة |
|---|---|---|---|
| الوقت حتى المسودة الأولى | الزمن من وصول العميل المحتمل إلى مسودة عرض جاهزة للمراجعة | سجل سير العمل | تقديري حتى التحقق |
| نسبة العملاء المؤهَّلين بإشارات موثقة | حصة العملاء الذين استند تأهيلهم إلى إشارات موثقة لا حدس | تقييم تأهيل العملاء | تقديري حتى التحقق |
| معدل المسودات المرفوضة عند الموافقة | حصة المسودات المردودة في بوابة الموافقة | مركز الموافقات | مقياس جودة لا وعد |
| معدل التقاط الانحدار | حصة تحديثات الموجّهات التي رُصد انحدارها قبل النشر | تقرير التقييم في CI | تقديري حتى التحقق |
| تغطية درجة التقييم للوكلاء | حصة الوكلاء النشطين الذين يملكون درجة تقييم محدّثة | سجل التقييم | إشارة جاهزية |
| فجوة قبل/بعد | الفرق بين خط الأساس والقياس بعد التغيير | قالب خط الأساس | لا يُذكر إلا بعد التحقق |

## كيفية الربط بالتقييم

- يُشغَّل احتساب الأثر بعد كل إصدار عبر تقرير التقييم الناتج من `scripts/run_evals.py`.
- تُقارن النتيجة بخط الأساس المسجّل في `evals/business_impact/baseline_template.md`.
- أي ادعاء تحسّن بلا قياس قبل/بعد يُرفض في المراجعة.

## ربط المراقبة

- يُسجَّل لكل إصدار: المقاييس المجمّعة، خط الأساس المرجعي، فرق قبل/بعد، حالة التحقق.
- تراجع أي مقياس دون خط الأساس يرفع تنبيه انحدار تجاري.

## روابط ذات صلة

- `evals/business_impact/baseline_template.md`
- `evals/readiness.md`
- `evals/tests.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Business Impact Eval Owner — Commercial Ops Lead

## Purpose

This document measures the business impact of the Dealix platform: do the agents and workflows make a measurable difference against a documented baseline. Layer 8 exists to stop fooling yourself; no impact counts unless it is measured before/after, not assumed.

## Measurement principles

- Every metric is estimated until verified; estimated value is not verified value.
- No guaranteed numbers and no conversion rates stated as fact; they are stated as a case-safe pattern or an estimated range.
- A baseline is required before any improvement claim — see `evals/business_impact/baseline_template.md`.
- No confidential client metrics are published; patterns are aggregated only.

## Metrics

| Metric | Definition | Source | Status |
|---|---|---|---|
| Time to first draft | Time from lead arrival to a review-ready proposal draft | Workflow log | Estimated until verified |
| Share of leads qualified on documented signals | Share of leads whose qualification traced to documented signals, not a guess | Lead qualification eval | Estimated until verified |
| Draft rejection rate at approval | Share of drafts returned at the approval gate | Approval center | A quality metric, not a promise |
| Regression catch rate | Share of prompt updates whose regression was caught before deploy | CI eval report | Estimated until verified |
| Agent eval score coverage | Share of active agents holding an up-to-date eval score | Eval registry | Readiness signal |
| Before/after gap | Difference between baseline and post-change measurement | Baseline template | Stated only after verification |

## How it links to evaluation

- Impact computation runs after every release via the eval report produced by `scripts/run_evals.py`.
- The result is compared against the baseline recorded in `evals/business_impact/baseline_template.md`.
- Any improvement claim without a before/after measurement is rejected in review.

## Observability hooks

- For each release the aggregated metrics, reference baseline, before/after delta, and verification status are logged.
- Any metric regressing below baseline raises a business regression alert.

## Related links

- `evals/business_impact/baseline_template.md`
- `evals/readiness.md`
- `evals/tests.md`

Estimated value is not Verified value.
