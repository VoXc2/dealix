# الجودة كرمز — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس التنفيذ
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [QUALITY_AS_CODE.md](./QUALITY_AS_CODE.md)

## السياق
تَعِد ديلكس بمعيار. والمعيار لا يقوم إذا حُكم على الجودة بالحدس. يحدّد
هذا الملف قواعد الجودة القابلة للاختبار التي تشغّلها ديلكس على كل أثر
ذي صلة، وبنية المجلدات المستهدفة للمقيّمات والمسطرات. ويربط انضباط
التقييم في `docs/EVALS_RUNBOOK.md` و
`docs/AI_OBSERVABILITY_AND_EVALS.md` مع لوحات المؤشرات في
`docs/BUSINESS_KPI_DASHBOARD_SPEC.md`.

## المبدأ

> كل ادعاء جودة يجب أن يكون **قاعدة** أو **مقيّماً** أو **مسطرة** —
> قابلاً للإعادة ومرئياً في CI.

## قواعد الجودة الأساسية (قابلة للاختبار)

- كل تقرير له ملخّص تنفيذي **و**إجراء تالٍ.
- كل حزمة إثبات لها مدخلات **و**مخرجات.
- كل إجابة Company Brain لها مصدر أو "insufficient evidence".
- كل مسودة تواصل تتجنب الادعاءات المضمونة.
- كل مخرَج عربي يجتاز مراجعة النبرة.

تنطبق هذه القواعد على مخرجات الذكاء الاصطناعي والمخرجات البشرية معاً.

## البنية المستقبلية

```
quality_os/
  rules/        # boolean assertions (e.g., has_exec_summary)
  evaluators/   # scoring functions (e.g., tone_score)
  rubrics/      # human-graded rubrics for offline runs
  fixtures/
```

- `rules/` — تأكيدات سريعة؛ الفشل يوقف التسليم.
- `evaluators/` — درجات تُغذّي لوحات الجودة.
- `rubrics/` — لحالات دقيقة تُراجَع بشرياً.
- `fixtures/` — أمثلة مثبّتة تُستخدم في CI.

## التدفق التشغيلي

```
artifact → rules pass? → evaluators score → rubric (if needed) → owner sign
```

- فشل قاعدة يوقف التسليم.
- مقيّم دون العتبة يُحدث تنبيهاً في برج التحكم.
- مراجعة المسطرة هي البوابة الأخيرة للمخرجات الموجَّهة للعميل.

## الأنماط الخاطئة

- "يبدو جيداً" بدون قاعدة نجحت.
- أرقام بلا مرجع بيانات مُؤرَّخ.
- نص عربي مترجم قالبياً لا مكتوب بأصالة.
- تقارير بلا "إجراء تالٍ".

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Artifact | Rule pass/fail | Quality OS | Per artifact |
| Artifact | Evaluator score | Quality OS | Per artifact |
| Sample artifact | Rubric score | Reviewer | Sampling |
| QA telemetry | Control Tower QA tile | Head of Delivery | Continuous |

## المقاييس
- Rule Pass Rate — نسبة الآثار المجتازة كل القواعد من المحاولة الأولى.
- Median Evaluator Score — لكل مقيّم خلال 30 يوماً.
- Rubric Sampling Coverage — نسبة الآثار الموجَّهة للعميل المُعَيَّنة.
- Defect Escape — عيوب مكتشفة بعد التسليم لكل 100 أثر.

## ذات صلة
- `docs/EVALS_RUNBOOK.md` — تشغيل التقييمات
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — تغطية التقييم
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — لوحات المؤشرات
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — موقف الجودة
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
