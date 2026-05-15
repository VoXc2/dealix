# العربية

Owner: قائد التقييم (Evaluation Lead)

## درجة الطبقة

طبقة التقييم (Layer 8): **78 من 100 — نطاق تجربة عميل**.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `evals/README.md`، `evals/company_brain_eval.yaml`، `evals/lead_intelligence_eval.yaml` |
| جاهزية | متوفر | هذه الوثيقة و`evals/readiness.md` |
| اختبارات | متوفر | `readiness/evals/tests.md`، `evals/tests.md` |
| مراقبة | متوفر | `dealix/observability/`، نتائج التقييم في CI |
| حوكمة | متوفر | `evals/governance_eval.yaml`، `evals/arabic_quality_eval.yaml` |
| تراجع | متوفر | عتبات تقييم تمنع طرح إصدار متراجع |
| مقاييس | متوفر | `readiness/evals/scorecard.yaml` |
| مالك | متوفر | قائد التقييم |

## الفجوات المحددة

- **مقارنة آلية بين الإصدار 1 والإصدار 2:** ملفات التقييم قائمة (`evals/*.yaml` و`evals/*.jsonl`)، لكن مقارنة آلية تمنع طرح إصدار يتراجع في التقييم غير مُنفَّذة على وتيرة متحقَّقة.
- **تغطية حالات التقييم:** حالات `evals/personal_operator_cases.jsonl` و`evals/revenue_os_cases.jsonl` تحتاج توسيعاً مُسجَّلاً لتغطية حالات الحافة.

## روابط ذات صلة

- `readiness/evals/tests.md`
- `readiness/evals/scorecard.yaml`
- `readiness/cross_layer/rollback_drill.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Evaluation Lead

## Layer score

Evaluation layer (Layer 8): **78 out of 100 — client pilot band**.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `evals/README.md`, `evals/company_brain_eval.yaml`, `evals/lead_intelligence_eval.yaml` |
| readiness | present | this document and `evals/readiness.md` |
| tests | present | `readiness/evals/tests.md`, `evals/tests.md` |
| observability | present | `dealix/observability/`, eval results in CI |
| governance | present | `evals/governance_eval.yaml`, `evals/arabic_quality_eval.yaml` |
| rollback | present | eval thresholds block rollout of a regressing version |
| metrics | present | `readiness/evals/scorecard.yaml` |
| owner | present | Evaluation Lead |

## Specific gaps

- **Automated v1/v2 comparison:** eval files exist (`evals/*.yaml` and `evals/*.jsonl`), but an automated comparison that blocks rollout of a version that regresses on evals is not run on a verified cadence.
- **Eval case coverage:** the `evals/personal_operator_cases.jsonl` and `evals/revenue_os_cases.jsonl` cases need a documented expansion to cover edge cases.

## Related links

- `readiness/evals/tests.md`
- `readiness/evals/scorecard.yaml`
- `readiness/cross_layer/rollback_drill.md`

Estimated value is not Verified value.
