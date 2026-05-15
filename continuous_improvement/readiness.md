# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

تجمّع هذه الوثيقة جاهزية الطبقة 12 — التطوّر المستمر — في مكان واحد: قائمة تحقّق، مقاييس، خطّافات مراقبة، قواعد حوكمة، إجراء تراجع، ودرجة جاهزية حالية. هدف الطبقة أن تتطوّر Dealix دون أن تنهار: كل تحديث يمرّ بإصدار وتقييمات وحوكمة وطرح وتراجع.

## 1. قائمة التحقّق من الجاهزية

- [x] لا نشر مباشر إلى الإنتاج يتجاوز التقييمات — مفروض في `continuous_improvement/release_process.md`.
- [x] كل تغيير له إدخال في `CHANGELOG.md`.
- [x] كل إصدار له مالك مُسمَّى.
- [x] يمكن استعادة إصدار سابق — `versions/<category>/` + `continuous_improvement/rollback_policy.md`.
- [x] ملاحظات العملاء تدخل سجل التحسين — `continuous_improvement/feedback_loop.md`.
- [x] كل إصدار يحمل درجة جاهزية.
- [x] الانحدارات تُكتشف قبل الإنتاج — محاكاة + طرح مرحلي + `watchdog_drift.yml`.
- [x] إجراء التراجع مُختبَر — تمرين شهري.
- [x] كل وكيل / مسار عمل / سياسة / مطالبة / مخطط ذاكرة مُؤرشَف ومُصدَّر.
- [ ] لوحة جاهزية حيّة موحَّدة عبر كل الطبقات — قيد التنفيذ.

## 2. المقاييس

- نسبة الإصدارات التي اجتازت كل البوّابات قبل الإنتاج.
- متوسط زمن الالتقاط حتى تحويل ملاحظة العميل إلى بند.
- عدد التراجعات شهرياً ومتوسط زمن الاستعادة.
- نسبة القطع القابلة للنشر التي لها إصدار سابق مؤرشف.
- عدد الانحدارات المُكتشَفة في المحاكاة مقابل المُكتشَفة في الإنتاج.

## 3. خطّافات المراقبة

- `.github/workflows/watchdog_drift.yml` — فحص الانحراف الساعي للبوّابات الصلبة.
- `.github/workflows/weekly_self_improvement.yml` — توليد اقتراحات أسبوعية.
- `auto_client_acquisition/self_growth_os/weekly_growth_scorecard.py` — بطاقة النمو الأسبوعية.
- `auto_client_acquisition/friction_log/aggregator.py` — تجميع إشارات الاحتكاك.

## 4. قواعد الحوكمة

- لا إصدار بلا مالك مُسمَّى وإدخال في `CHANGELOG.md`.
- لا تغيير يمسّ العميل بلا اجتياز `auto_client_acquisition/self_growth_os/safe_publishing_gate.py`.
- لا نشر يتجاوز التقييمات أو الطرح المرحلي.
- لا وعد بأرقام مبيعات أو تحويل — أنماط قابلة للملاحظة فقط.
- لا إرسال خارجي نيابة عن العميل دون موافقة صريحة.

## 5. إجراء التراجع

عند انخفاض الجاهزية تحت 75 أو اكتشاف انحراف: يُجمَّد الطرح، تُحدَّد القطعة، يُستعاد إصدارها السابق من `versions/<category>/`، يُضاف إدخال تراجع إلى `CHANGELOG.md`، تُعاد التقييمات، ويُسجَّل الدرس في سجل التحسين. التفاصيل الكاملة في `continuous_improvement/rollback_policy.md`.

## 6. درجة الجاهزية الحالية

**الدرجة: 81 / 100 — تجريبي مع العميل (Client pilot).**

مقياس النطاقات الخمسة:

| النطاق | الدرجة | الوصف |
|---|---|---|
| نموذج أولي | 0–59 | غير جاهز للاستخدام الخارجي |
| بيتا داخلي | 60–74 | استخدام الفريق فقط |
| تجريبي مع العميل | 75–84 | عملاء موافِقون، شريحة محدودة |
| جاهز للمؤسسات | 85–94 | استخدام إنتاجي واسع |
| حرج للمهمّة | 95+ | اعتماد كامل بلا تحفّظ |

**سبب الدرجة:** بوّابات الإصدار والتراجع والطرح المرحلي قائمة وموثَّقة، والتأريخ مفعَّل. ما يخفض الدرجة عن 85: لوحة الجاهزية الموحَّدة قيد التنفيذ، وتمرين التراجع لم يُؤتمَت بعد.

انظر أيضاً: `continuous_improvement/release_process.md`، `continuous_improvement/rollback_policy.md`، `continuous_improvement/scorecard.yaml`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This document gathers the readiness of Layer 12 — Continuous Evolution — in one place: a checklist, metrics, observability hooks, governance rules, a rollback procedure, and a current readiness score. The layer's goal is for Dealix to evolve without collapsing: every update passes versioning, evals, governance, rollout, and rollback.

## 1. Readiness checklist

- [x] No direct deploy to production that bypasses evals — enforced in `continuous_improvement/release_process.md`.
- [x] Every change has a `CHANGELOG.md` entry.
- [x] Every release has a named owner.
- [x] A previous version can be restored — `versions/<category>/` + `continuous_improvement/rollback_policy.md`.
- [x] Customer feedback enters the improvement backlog — `continuous_improvement/feedback_loop.md`.
- [x] Every release carries a readiness score.
- [x] Regressions are caught before production — simulation + staged rollout + `watchdog_drift.yml`.
- [x] The rollback procedure is tested — a monthly drill.
- [x] Every agent / workflow / policy / prompt / memory schema is archived and versioned.
- [ ] A unified live readiness dashboard across all layers — in progress.

## 2. Metrics

- Share of releases that passed all gates before production.
- Average time from capture to converting customer feedback into an item.
- Number of rollbacks per month and average restore time.
- Share of deployable artifacts that have an archived previous version.
- Number of regressions caught in simulation versus caught in production.

## 3. Observability hooks

- `.github/workflows/watchdog_drift.yml` — hourly drift check on the hard gates.
- `.github/workflows/weekly_self_improvement.yml` — weekly suggestion generation.
- `auto_client_acquisition/self_growth_os/weekly_growth_scorecard.py` — the weekly growth scorecard.
- `auto_client_acquisition/friction_log/aggregator.py` — aggregation of friction signals.

## 4. Governance rules

- No release without a named owner and a `CHANGELOG.md` entry.
- No customer-facing change without passing `auto_client_acquisition/self_growth_os/safe_publishing_gate.py`.
- No deploy that bypasses evals or the staged rollout.
- No promise of sales or conversion numbers — observable patterns only.
- No external send on a customer's behalf without explicit approval.

## 5. Rollback procedure

When readiness drops below 75 or drift is detected: the rollout is frozen, the artifact is identified, its previous version is restored from `versions/<category>/`, a rollback entry is added to `CHANGELOG.md`, the evals are re-run, and the lesson is recorded in the improvement backlog. Full detail is in `continuous_improvement/rollback_policy.md`.

## 6. Current readiness score

**Score: 81 / 100 — Client pilot.**

The five-band scale:

| Band | Score | Description |
|---|---|---|
| Prototype | 0–59 | Not ready for external use |
| Internal beta | 60–74 | Team use only |
| Client pilot | 75–84 | Consenting customers, limited segment |
| Enterprise-ready | 85–94 | Broad production use |
| Mission-critical | 95+ | Full reliance without reservation |

**Reason for the score:** The release, rollback, and staged-rollout gates exist and are documented, and versioning is in place. What holds the score below 85: the unified readiness dashboard is in progress, and the rollback drill is not yet automated.

See also: `continuous_improvement/release_process.md`, `continuous_improvement/rollback_policy.md`, `continuous_improvement/scorecard.yaml`.
