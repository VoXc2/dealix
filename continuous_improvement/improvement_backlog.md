# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

تحدّد هذه الوثيقة كيف يُحفظ سجل التحسين ويُرتَّب ويُسحَب منه إلى دورة الإصدار. السجل هو المصدر الوحيد للتغيير المخطَّط؛ لا يدخل تغيير الإنتاج ما لم يكن له بند هنا.

## مصادر البنود

- حلقة التغذية الراجعة — `continuous_improvement/feedback_loop.md`.
- التحسين الأسبوعي الآلي — `.github/workflows/weekly_self_improvement.yml`.
- تنبيهات الانحراف — `.github/workflows/watchdog_drift.yml`.
- دروس التراجع — من `continuous_improvement/rollback_policy.md`.
- رادار التقنية — `dealix/registers/technology_radar.yaml` عند تغيّر حالة تقنية.

## بنية البند

كل بند يحمل: معرّفاً، عنواناً، المصدر، الفئة المتأثرة (وكيل / مسار عمل / مطالبة / سياسة / مخطط ذاكرة)، التصنيف (تصحيح / ميزة / كاسر)، المالك المُسمَّى، درجة الأولوية، والحالة.

| الحقل | الوصف |
|---|---|
| المعرّف | رقم متسلسل ثابت |
| الفئة | الفئة القابلة للنشر المتأثرة |
| التصنيف | تصحيح / ميزة / كاسر |
| المالك | دور مُسمَّى مسؤول |
| الأولوية | عالية / متوسطة / منخفضة |
| الحالة | مقترح / مقبول / قيد التنفيذ / مُصدَر / مرفوض |

## الترتيب

تُرتَّب البنود عبر `auto_client_acquisition/full_ops/prioritizer.py` على أساس الأثر والتكرار وكلفة عدم الفعل. تُراجَع الأولويات أسبوعياً بالتزامن مع بطاقة النمو الأسبوعية.

## السحب إلى الإصدار

عند بدء العمل على بند، يدخل دورة `continuous_improvement/change_management.md` ثم `continuous_improvement/release_process.md`. لا يُغلَق البند كـ«مُصدَر» إلا بعد إدخال في `CHANGELOG.md` ووصول الطرح إلى المرحلة الكاملة.

## قواعد الحوكمة

- لا بند بلا مالك مُسمَّى.
- لا بند يصف الكشط أو الأتمتة الباردة أو الإرسال بالجملة — يُرفَض عند التسجيل.
- لا يُسجَّل أثر متوقَّع كوعد بأرقام مبيعات أو تحويل.
- كل بند قابل للتتبّع من مصدره حتى إغلاقه.

انظر أيضاً: `continuous_improvement/feedback_loop.md`، `continuous_improvement/change_management.md`، `continuous_improvement/readiness.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This document defines how the improvement backlog is kept, ranked, and pulled into the release cycle. The backlog is the single source of planned change; no production change proceeds unless it has an item here.

## Item sources

- The feedback loop — `continuous_improvement/feedback_loop.md`.
- The automated weekly improvement — `.github/workflows/weekly_self_improvement.yml`.
- Drift alerts — `.github/workflows/watchdog_drift.yml`.
- Rollback lessons — from `continuous_improvement/rollback_policy.md`.
- The technology radar — `dealix/registers/technology_radar.yaml` when a technology's status changes.

## Item structure

Every item carries: an identifier, a title, the source, the affected category (agent / workflow / prompt / policy / memory schema), the classification (patch / feature / breaking), the named owner, a priority grade, and a status.

| Field | Description |
|---|---|
| Identifier | Stable sequential number |
| Category | The affected deployable category |
| Classification | Patch / feature / breaking |
| Owner | A named responsible role |
| Priority | High / medium / low |
| Status | Proposed / accepted / in progress / released / rejected |

## Ranking

Items are ranked via `auto_client_acquisition/full_ops/prioritizer.py` based on impact, frequency, and cost of inaction. Priorities are reviewed weekly alongside the weekly growth scorecard.

## Pulling into a release

When work begins on an item, it enters the `continuous_improvement/change_management.md` cycle and then `continuous_improvement/release_process.md`. The item is not closed as "released" until there is a `CHANGELOG.md` entry and the rollout has reached the full stage.

## Governance rules

- No item without a named owner.
- No item that describes scraping, cold automation, or bulk outreach — rejected at recording.
- No expected impact is recorded as a promise of sales or conversion numbers.
- Every item is traceable from its source to its closure.

See also: `continuous_improvement/feedback_loop.md`, `continuous_improvement/change_management.md`, `continuous_improvement/readiness.md`.
