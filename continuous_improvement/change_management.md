# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead).

## الغرض

تحدّد هذه الوثيقة كيف تُقترح التغييرات وتُصنَّف وتُراجَع وتُوثَّق في Dealix. القاعدة: كل تغيير له أثر مكتوب، تصنيف واضح، مالك مُسمَّى، وإدخال في `CHANGELOG.md` قبل أن يُعد جزءاً من المنصة.

## مصادر التغيير

التغيير يدخل من أربعة مصادر فقط:
1. حلقة التغذية الراجعة — `continuous_improvement/feedback_loop.md` وسجل الاحتكاك `auto_client_acquisition/friction_log/`.
2. سجل التحسين — `continuous_improvement/improvement_backlog.md`.
3. التحسين الأسبوعي الآلي — `.github/workflows/weekly_self_improvement.yml`.
4. اكتشاف الانحراف — `.github/workflows/watchdog_drift.yml`.

## تصنيف التغيير

| التصنيف | الوصف | البوّابات اللازمة |
|---|---|---|
| تصحيح (patch) | إصلاح بلا تغيير سلوك ظاهر | تكامل مستمر + تقييمات |
| ميزة (minor) | سلوك جديد متوافق للخلف | تكامل + تقييمات + حوكمة + طرح مرحلي |
| كاسر (major) | تغيير يكسر التوافق أو يمسّ العميل | كل البوّابات + محاكاة + موافقة المالك |

## دورة المراجعة

1. **تسجيل.** يُسجَّل التغيير المقترح كبند في سجل التحسين بمالك وتصنيف مبدئي.
2. **تقييم الأثر.** يُحدَّد ما القطع المتأثرة (وكلاء، مسارات عمل، مطالبات، سياسات، مخططات ذاكرة).
3. **مراجعة الند.** يراجع مهندس آخر التغيير؛ لا دمج ذاتي للتغييرات الكاسرة.
4. **مراجعة الحوكمة.** التغييرات التي تمسّ المحتوى الموجَّه للعملاء تمرّ على بوّابة النشر الآمن `auto_client_acquisition/self_growth_os/safe_publishing_gate.py`.
5. **التوثيق.** يُحدَّث `CHANGELOG.md` ويُؤرشَف الإصدار السابق تحت `versions/`.

## قواعد الحوكمة

- لا تغيير بلا مالك مُسمَّى.
- لا تغيير كاسر بلا مراجعة ند وموافقة المالك.
- لا تغيير يمسّ العميل بلا تمرير بوّابة النشر الآمن.
- التغييرات التي تصف الكشط أو الأتمتة الباردة أو الإرسال بالجملة مرفوضة عند المراجعة، لا تُصعَّد.
- كل تغيير قابل للتتبّع من مصدره في سجل التحسين إلى إدخاله في `CHANGELOG.md`.

## ما لا نقيسه كأرقام نهائية

لا نُسجّل أثر التغيير كوعد بمبيعات أو تحويل. الأثر يُوصف كنمط قابل للملاحظة فقط، تماشياً مع `dealix/registers/no_overclaim.yaml`.

انظر أيضاً: `continuous_improvement/release_process.md`، `continuous_improvement/improvement_backlog.md`، `continuous_improvement/feedback_loop.md`.

---

# English

**Owner:** Continuous Evolution Lead.

## Purpose

This document defines how changes are proposed, classified, reviewed, and documented in Dealix. The rule: every change has a written trail, a clear classification, a named owner, and a `CHANGELOG.md` entry before it counts as part of the platform.

## Sources of change

Change enters from only four sources:
1. The feedback loop — `continuous_improvement/feedback_loop.md` and the friction log `auto_client_acquisition/friction_log/`.
2. The improvement backlog — `continuous_improvement/improvement_backlog.md`.
3. The automated weekly improvement — `.github/workflows/weekly_self_improvement.yml`.
4. Drift detection — `.github/workflows/watchdog_drift.yml`.

## Change classification

| Classification | Description | Required gates |
|---|---|---|
| Patch | Fix with no visible behavior change | CI + evals |
| Minor (feature) | New backward-compatible behavior | CI + evals + governance + staged rollout |
| Major (breaking) | Change that breaks compatibility or touches the customer | All gates + simulation + owner approval |

## Review cycle

1. **Record.** The proposed change is recorded as a backlog item with an owner and a provisional classification.
2. **Impact assessment.** The affected artifacts are identified (agents, workflows, prompts, policies, memory schemas).
3. **Peer review.** Another engineer reviews the change; no self-merge for breaking changes.
4. **Governance review.** Changes that touch customer-facing content pass the safe-publishing gate `auto_client_acquisition/self_growth_os/safe_publishing_gate.py`.
5. **Documentation.** `CHANGELOG.md` is updated and the previous version is archived under `versions/`.

## Governance rules

- No change without a named owner.
- No breaking change without peer review and owner approval.
- No customer-facing change without passing the safe-publishing gate.
- Changes describing scraping, cold automation, or bulk outreach are rejected at review, never escalated.
- Every change is traceable from its source in the improvement backlog to its `CHANGELOG.md` entry.

## What we do not measure as final numbers

We do not record a change's impact as a promise of sales or conversion. Impact is described only as an observable pattern, in line with `dealix/registers/no_overclaim.yaml`.

See also: `continuous_improvement/release_process.md`, `continuous_improvement/improvement_backlog.md`, `continuous_improvement/feedback_loop.md`.
