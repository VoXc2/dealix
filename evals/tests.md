# العربية

Owner: مالك مواصفة الاختبارات — قائد جودة الذكاء الاصطناعي (AI Quality Lead)

## الغرض

تصف هذه الوثيقة — بلا أي كود — كيف تُشغَّل تقييمات الطبقة الثامنة، وما الذي يوقف الدمج أو النشر. هي مواصفة مرجعية تربط المجموعات الذهبية بالحدود وبخطوات CI.

## 1. نطاق الاختبار

| المجموعة | الملف | ما تقيسه |
|---|---|---|
| استرجاع | `evals/retrieval/dataset.jsonl` | الاستدعاء، الدقة، الاستناد |
| هلوسة | `evals/hallucination/test_cases.jsonl` | اختلاق، ضمانات، عملاء وهميون |
| تنفيذ سير العمل | `evals/workflow_execution/*.jsonl` | تأهيل العملاء والدعم |
| سلوك الوكلاء | `evals/agent_behavior/*.jsonl` | سلوك وكيل المبيعات والدعم |
| حوكمة | `evals/governance/*.jsonl` | حالات عالية الخطورة والموافقات |
| أثر تجاري | `evals/business_impact/*.md` | قبل/بعد مقابل خط الأساس |

## 2. كيفية التشغيل في CI

- خطوة `Deterministic eval smoke` في `.github/workflows/ci.yml` تشغّل `scripts/run_evals.py`.
- يحمّل المُشغِّل كل ملفات `.jsonl` ويقارن النتائج بـ `evals/retrieval/thresholds.yaml`.
- خطوات تحقق مساندة: `scripts/verify_ai_output_quality.py` و`scripts/verify_governance_rules.py`.
- اختبارات الموافقات في `tests/governance/test_approvals.py` تعمل ضمن حزمة pytest نفسها.

## 3. قواعد البوابة

- لا دمج إذا تراجع أي مقياس استرجاع دون حد النجاح في `thresholds.yaml`.
- لا نشر إذا فشلت أي حالة في `evals/governance/` — بوابة صارمة.
- متوسط درجة الهلوسة دون 1.8 من 2 يوقف الدمج.
- أي حالة تسجّل صفراً على بند غير قابل للتفاوض توقف الدمج بصرف النظر عن المتوسط.

## 4. كشف الانحدار

- تُقارن كل نتيجة بآخر خط أساس أخضر مسجّل عبر `evals/business_impact/baseline_template.md`.
- انخفاض يتجاوز هامش الانحدار (`regression_tolerance` في `thresholds.yaml`) يُعدّ انحداراً حتى لو بقي فوق حد النجاح.
- يُرفع تنبيه انحدار قبل الدمج.

## 5. اختبارات الانحدار للمجموعات الذهبية

- المجموعات الذهبية ثابتة؛ أي تغيير عليها يتطلب مراجعة وموافقة.
- إضافة حالة جديدة لا تُسقط حالة قائمة دون توثيق السبب.
- كل تحديث موجّه أو وكيل يعيد تشغيل المجموعات الذهبية كاملة.

## 6. تقرير التقييم لكل إصدار

- ينتج عن كل تشغيل تقرير يحوي: الدرجات، الحدود، فرق قبل/بعد، الحالات الفاشلة، قرار النشر.
- يُرفق التقرير بقالب خط الأساس المكتمل.

## روابط ذات صلة

- `evals/readiness.md`
- `evals/retrieval/thresholds.yaml`
- `evals/governance/high_risk_cases.jsonl`
- `evals/business_impact/baseline_template.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Test Spec Owner — AI Quality Lead

## Purpose

This document describes — with no code — how Layer 8 evals run and what blocks a merge or deploy. It is a reference spec linking golden datasets to thresholds and CI steps.

## 1. Test scope

| Dataset | File | What it measures |
|---|---|---|
| Retrieval | `evals/retrieval/dataset.jsonl` | Recall, precision, groundedness |
| Hallucination | `evals/hallucination/test_cases.jsonl` | Fabrication, guarantees, fake customers |
| Workflow execution | `evals/workflow_execution/*.jsonl` | Lead qualification and support |
| Agent behavior | `evals/agent_behavior/*.jsonl` | Sales and support agent behavior |
| Governance | `evals/governance/*.jsonl` | High-risk and approval cases |
| Business impact | `evals/business_impact/*.md` | Before/after against the baseline |

## 2. How it runs in CI

- The `Deterministic eval smoke` step in `.github/workflows/ci.yml` runs `scripts/run_evals.py`.
- The runner loads all `.jsonl` files and compares results against `evals/retrieval/thresholds.yaml`.
- Supporting verification steps: `scripts/verify_ai_output_quality.py` and `scripts/verify_governance_rules.py`.
- Approval tests in `tests/governance/test_approvals.py` run inside the same pytest bundle.

## 3. Gate rules

- No merge if any retrieval metric drops below its pass threshold in `thresholds.yaml`.
- No deploy if any case in `evals/governance/` fails — a strict gate.
- A mean hallucination score below 1.8 of 2 blocks the merge.
- Any case scoring zero on a non-negotiable item blocks the merge regardless of the average.

## 4. Regression detection

- Every result is compared against the last green baseline recorded via `evals/business_impact/baseline_template.md`.
- A drop beyond the regression tolerance (`regression_tolerance` in `thresholds.yaml`) counts as a regression even if still above the pass threshold.
- A regression alert is raised before merge.

## 5. Golden dataset regression tests

- Golden datasets are fixed; any change to them requires review and approval.
- Adding a new case must not drop an existing case without a documented reason.
- Every prompt or agent update re-runs the full golden datasets.

## 6. Per-release eval report

- Each run produces a report containing: scores, thresholds, before/after delta, failed cases, and the deploy decision.
- The report is attached with the completed baseline template.

## Related links

- `evals/readiness.md`
- `evals/retrieval/thresholds.yaml`
- `evals/governance/high_risk_cases.jsonl`
- `evals/business_impact/baseline_template.md`

Estimated value is not Verified value.
