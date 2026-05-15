# العربية

Owner: مالك خط الأساس — قائد العمليات التجارية (Commercial Ops Lead)

## الغرض

قالب لتسجيل خط أساس موثّق قبل أي تغيير على وكيل أو موجّه أو سير عمل. بدون خط أساس لا يجوز ادعاء أي تحسّن؛ هذا جوهر الطبقة الثامنة — قياس قبل/بعد لا افتراض.

## كيفية الاستخدام

- يُملأ هذا القالب قبل التغيير (خط الأساس) ثم بعد التغيير (القياس البعدي).
- تُؤخذ القيم من تقرير التقييم الناتج عن `scripts/run_evals.py` ومن سجلات سير العمل.
- يُرفق القالب المكتمل بتقرير التقييم لكل إصدار.
- كل قيمة تقديرية حتى يُتحقَّق منها؛ لا أرقام مضمونة.

## بطاقة خط الأساس

| الحقل | القيمة |
|---|---|
| معرّف التغيير | (مثال: تحديث موجّه وكيل المبيعات v2) |
| التاريخ | |
| المالك | |
| النطاق المتأثر | (الوكيل / الموجّه / سير العمل) |
| تاريخ خط الأساس | |

## جدول قبل/بعد

| المقياس | قيمة خط الأساس (قبل) | القياس البعدي (بعد) | الفرق | الحالة |
|---|---|---|---|---|
| استناد الاسترجاع | | | | تقديري حتى التحقق |
| الاستدعاء عند 5 | | | | تقديري حتى التحقق |
| متوسط درجة الهلوسة | | | | تقديري حتى التحقق |
| نسبة نجاح حالات الحوكمة | | | | يجب أن يكون 100٪ |
| الوقت حتى المسودة الأولى | | | | تقديري حتى التحقق |
| معدل المسودات المرفوضة | | | | مقياس جودة |

## قواعد القرار

- يُسمح بالنشر فقط إذا لم يتراجع أي مقياس دون حد النجاح، ولم تفشل أي حالة حوكمة.
- تراجع مقياس فوق حد النجاح لكن دون خط الأساس بأكثر من هامش الانحدار يُعدّ انحداراً.
- أي تحسّن يُذكر بلغة تقديرية أو كنمط آمن للحالة، لا كوعد.

## ربط المراقبة

- يُسجَّل القالب المكتمل ومعرّف الإصدار وقرار النشر.
- يُحفظ خط الأساس الأخضر الأخير كمرجع للمقارنة التالية.

## روابط ذات صلة

- `evals/business_impact/roi_metrics.md`
- `evals/readiness.md`
- `evals/retrieval/thresholds.yaml`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Baseline Owner — Commercial Ops Lead

## Purpose

A template for recording a documented baseline before any change to an agent, prompt, or workflow. Without a baseline no improvement may be claimed; this is the core of Layer 8 — measure before/after, do not assume.

## How to use

- Fill this template before the change (baseline) and again after the change (post-measurement).
- Values come from the eval report produced by `scripts/run_evals.py` and from workflow logs.
- Attach the completed template to the per-release eval report.
- Every value is estimated until verified; no guaranteed numbers.

## Baseline card

| Field | Value |
|---|---|
| Change ID | (e.g. sales agent prompt update v2) |
| Date | |
| Owner | |
| Affected scope | (agent / prompt / workflow) |
| Baseline date | |

## Before/after table

| Metric | Baseline value (before) | Post-measurement (after) | Delta | Status |
|---|---|---|---|---|
| Retrieval groundedness | | | | Estimated until verified |
| recall@5 | | | | Estimated until verified |
| Mean hallucination score | | | | Estimated until verified |
| Governance case pass rate | | | | Must be 100% |
| Time to first draft | | | | Estimated until verified |
| Draft rejection rate | | | | Quality metric |

## Decision rules

- Deploy is allowed only if no metric regressed below its pass threshold and no governance case failed.
- A metric above its pass threshold but below baseline by more than the regression tolerance counts as a regression.
- Any improvement is stated in estimate language or as a case-safe pattern, never as a promise.

## Observability hooks

- The completed template, release ID, and deploy decision are logged.
- The last green baseline is kept as the reference for the next comparison.

## Related links

- `evals/business_impact/roi_metrics.md`
- `evals/readiness.md`
- `evals/retrieval/thresholds.yaml`

Estimated value is not Verified value.
