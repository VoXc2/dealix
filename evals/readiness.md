# العربية

Owner: مالك جاهزية الطبقة الثامنة — قائد جودة الذكاء الاصطناعي (AI Quality Lead)

## الغرض

تقيس الطبقة الثامنة (التقييم) جودة الوكلاء والاسترجاع وسير العمل والحوكمة والأثر التجاري في منصة دياليكس. الهدف صريح: التوقف عن خداع النفس — قياس الجودة بدل افتراضها، عبر مجموعات ذهبية وحدود واضحة وتقييمات تعمل في CI.

## 1. قائمة الجاهزية

- [x] لكل وكيل درجة تقييم محدّثة (مبيعات، دعم).
- [x] تقييم استرجاع يقيس الاسترجاع والاستناد — `evals/retrieval/`.
- [x] تقييم هلوسة بمعيار تسجيل — `evals/hallucination/`.
- [x] تقييمات تنفيذ سير العمل — `evals/workflow_execution/`.
- [x] تقييمات سلوك الوكلاء — `evals/agent_behavior/`.
- [x] تقييمات حوكمة لحالات عالية الخطورة والموافقات — `evals/governance/`.
- [x] تقييمات أثر تجاري بقالب خط أساس — `evals/business_impact/`.
- [x] حدود واضحة قابلة للقياس — `evals/retrieval/thresholds.yaml`.
- [x] التقييمات تعمل في CI عبر `scripts/run_evals.py` ضمن `.github/workflows/ci.yml`.
- [x] خط أساس قبل/بعد لكل تغيير على وكيل أو موجّه أو سير عمل.
- [x] كشف انحدار: انخفاض مقياس دون الحد أو دون خط الأساس يوقف الدمج.
- [x] لكل إصدار تقرير تقييم.
- [ ] أرشفة آلية لتقارير التقييم التاريخية (مخطّط لها).

## 2. المقاييس

| المقياس | المصدر | حد النجاح |
|---|---|---|
| استناد الاسترجاع | `evals/retrieval/thresholds.yaml` | ≥ 0.95 |
| الاستدعاء عند 5 | `evals/retrieval/thresholds.yaml` | ≥ 0.90 |
| متوسط درجة الهلوسة | `evals/hallucination/rubric.md` | ≥ 1.8 من 2 |
| نسبة نجاح حالات الحوكمة | `evals/governance/` | 100٪ |
| تغطية درجة التقييم للوكلاء | سجل التقييم | 100٪ من الوكلاء النشطين |
| معدل التقاط الانحدار | تقرير التقييم في CI | تقديري حتى التحقق |

## 3. ربط المراقبة

- يُسجَّل لكل تشغيل تقييم: المعرّف، الدرجات، الحدود، قرار النشر.
- يُصدَّر تقرير تقييم لكل إصدار ويُرفق به قالب خط الأساس.
- تنبيه انحدار يُرفع قبل الدمج عند أي تراجع تحت الحد.
- مراجع: `scripts/verify_ai_output_quality.py`، `scripts/verify_governance_rules.py`.

## 4. قواعد الحوكمة

- لا نشر إذا فشلت أي حالة تقييم حوكمة — انظر `evals/governance/`.
- كل تحديث موجّه أو وكيل أو سير عمل يجب أن يجتاز التقييمات قبل الدمج.
- لا تُذكر أرقام مضمونة؛ كل أثر تقديري حتى التحقق.
- لا بيانات شخصية ولا عملاء وهميون في أي مجموعة تقييم.

## 5. إجراء التراجع

1. إيقاف النشر فور رصد فشل تقييم أو إشارة انحدار.
2. العودة إلى آخر نسخة موجّه/وكيل خضراء مسجّلة في خط الأساس.
3. إعادة تشغيل `scripts/run_evals.py` للتأكد من عودة المقاييس فوق الحدود.
4. تسجيل سبب التراجع في تقرير التقييم قبل أي محاولة إعادة نشر.
5. لا إعادة نشر قبل اجتياز كل حالات الحوكمة من جديد.

## 6. درجة الجاهزية الحالية

الدرجة: 78 / 100 — **تجربة عميل (client pilot)**.

سلّم النطاقات الخمسة:
- 0–59: نموذج أولي (prototype)
- 60–74: تجربة داخلية (internal beta)
- 75–84: تجربة عميل (client pilot)
- 85–94: جاهز للمؤسسات (enterprise-ready)
- 95+: حرج للمهمة (mission-critical)

التبرير: المجموعات الذهبية والحدود والتقييمات في CI قائمة، ولكل وكيل درجة. الفجوة المتبقية: أرشفة آلية لتقارير التقييم التاريخية واتساع مجموعات سير العمل، ما يبقي الدرجة دون نطاق الجاهزية للمؤسسات.

## روابط ذات صلة

- `evals/tests.md`
- `evals/retrieval/metrics.md`
- `evals/hallucination/rubric.md`
- `evals/business_impact/roi_metrics.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Layer 8 Readiness Owner — AI Quality Lead

## Purpose

Layer 8 (Evaluation) measures the quality of agents, retrieval, workflows, governance, and business impact in the Dealix platform. The goal is explicit: stop fooling yourself — measure quality instead of assuming it, through golden datasets, clear thresholds, and evals that run in CI.

## 1. Readiness checklist

- [x] Every agent has an up-to-date eval score (sales, support).
- [x] A retrieval eval measures retrieval and groundedness — `evals/retrieval/`.
- [x] A hallucination eval with a scoring rubric — `evals/hallucination/`.
- [x] Workflow execution evals — `evals/workflow_execution/`.
- [x] Agent behavior evals — `evals/agent_behavior/`.
- [x] Governance evals for high-risk and approval cases — `evals/governance/`.
- [x] Business impact evals with a baseline template — `evals/business_impact/`.
- [x] Clear, measurable thresholds — `evals/retrieval/thresholds.yaml`.
- [x] Evals run in CI via `scripts/run_evals.py` inside `.github/workflows/ci.yml`.
- [x] A before/after baseline for every agent, prompt, or workflow change.
- [x] Regression detection: a metric below threshold or below baseline blocks merge.
- [x] Every release has an eval report.
- [ ] Automated archiving of historical eval reports (planned).

## 2. Metrics

| Metric | Source | Pass threshold |
|---|---|---|
| Retrieval groundedness | `evals/retrieval/thresholds.yaml` | >= 0.95 |
| recall@5 | `evals/retrieval/thresholds.yaml` | >= 0.90 |
| Mean hallucination score | `evals/hallucination/rubric.md` | >= 1.8 of 2 |
| Governance case pass rate | `evals/governance/` | 100% |
| Agent eval score coverage | Eval registry | 100% of active agents |
| Regression catch rate | CI eval report | Estimated until verified |

## 3. Observability hooks

- For each eval run the ID, scores, thresholds, and deploy decision are logged.
- An eval report is exported per release with the baseline template attached.
- A regression alert is raised before merge on any drop below threshold.
- References: `scripts/verify_ai_output_quality.py`, `scripts/verify_governance_rules.py`.

## 4. Governance rules

- No deploy if any governance eval case fails — see `evals/governance/`.
- Every prompt, agent, or workflow update must pass the evals before merge.
- No guaranteed numbers are stated; every impact figure is estimated until verified.
- No PII and no fake customers in any eval dataset.

## 5. Rollback procedure

1. Halt the deploy as soon as an eval failure or a regression signal is detected.
2. Revert to the last green prompt/agent version recorded in the baseline.
3. Re-run `scripts/run_evals.py` to confirm metrics are back above thresholds.
4. Record the rollback reason in the eval report before any redeploy attempt.
5. No redeploy until all governance cases pass again.

## 6. Current readiness score

Score: 78 / 100 — **client pilot**.

Five-band scale:
- 0-59: prototype
- 60-74: internal beta
- 75-84: client pilot
- 85-94: enterprise-ready
- 95+: mission-critical

Rationale: golden datasets, thresholds, and CI evals are in place, and every agent has a score. The remaining gap is automated archiving of historical eval reports and broader workflow dataset coverage, which keeps the score below the enterprise-ready band.

## Related links

- `evals/tests.md`
- `evals/retrieval/metrics.md`
- `evals/hallucination/rubric.md`
- `evals/business_impact/roi_metrics.md`

Estimated value is not Verified value.
