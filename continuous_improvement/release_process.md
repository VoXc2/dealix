# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

تصف هذه الوثيقة عملية الإصدار للطبقة 12 — التطوّر المستمر. القاعدة الحاكمة: لا يصل أي تغيير إلى الإنتاج دون المرور بأربع بوّابات متسلسلة — الإصدار (versioning)، التقييمات (evals)، الحوكمة (governance)، والطرح المرحلي (staged rollout). الهدف أن تتطوّر Dealix دون أن تنهار.

## نطاق العملية

تنطبق هذه العملية على كل تغيير قابل للنشر:
- وكلاء (تعريفات `agent.yaml` ومنطق التشغيل).
- مسارات عمل (workflows في `.github/workflows/`).
- مطالبات (prompts) المستخدمة في وقت التشغيل.
- سياسات الحوكمة والنشر الآمن.
- مخططات الذاكرة (memory schemas).

## مراحل الإصدار

1. **اقتراح التغيير.** يُسجَّل التغيير كبند في `continuous_improvement/improvement_backlog.md` أو يصل من حلقة التغذية الراجعة في `continuous_improvement/feedback_loop.md`.
2. **التصنيف.** يصنَّف التغيير: تصحيح (patch)، ميزة (minor)، أو كاسر للتوافق (major). يحدّد التصنيف بوّابات الإصدار اللازمة.
3. **الإصدار والأرشفة.** قبل الدمج يُؤرشَف الإصدار السابق من القطعة المعدَّلة تحت `versions/<category>/` وفق قواعد التسمية في `README.md` لكل فئة.
4. **بوّابات الإصدار (Release gates).** يجب أن تمرّ كل البوّابات التالية:
   - فحص التكامل المستمر في `.github/workflows/ci.yml`.
   - بوّابة النشر الآمن `auto_client_acquisition/self_growth_os/safe_publishing_gate.py` على أي محتوى موجَّه للعملاء.
   - التقييمات وحالات القبول في `continuous_improvement/tests.md`.
   - فحص المزاعم الممنوعة (مضمون، كشط، رسائل باردة) — يجب أن يكون نظيفاً.
5. **سجل التغييرات.** يُحدَّث `CHANGELOG.md` بإدخال يحمل رقم الإصدار والتاريخ والمالك. لا إصدار بلا إدخال سجل.
6. **درجة الجاهزية.** يُسند للإصدار درجة جاهزية (0–100) وفق المقياس في `continuous_improvement/readiness.md`. الإصدارات تحت 75 لا تصل إلى عملاء.
7. **الموافقة.** يوافق مالك التطوير المستمر على بطاقة الإصدار النهائية.
8. **الطرح المرحلي.** يُنفَّذ الطرح وفق `continuous_improvement/staged_rollout.md`.

## بطاقة الإصدار

كل إصدار يحمل بطاقة تتضمّن: رقم الإصدار، المالك المُسمَّى، التاريخ، التصنيف، قائمة البوّابات المُجتازة، مرجع الإصدار السابق المؤرشف، درجة الجاهزية، وخطة التراجع.

## ما لا تسمح به العملية

- لا نشر مباشر إلى الإنتاج يتجاوز التقييمات.
- لا تغيير بلا إدخال في `CHANGELOG.md`.
- لا إصدار بلا مالك مُسمَّى.
- لا وعود بأرقام مبيعات أو معدّلات تحويل — الأدلة فقط أنماط قابلة للملاحظة.
- لا إرسال خارجي نيابة عن العميل دون موافقة صريحة.

انظر أيضاً: `continuous_improvement/change_management.md`، `continuous_improvement/staged_rollout.md`، `continuous_improvement/rollback_policy.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This document describes the release process for Layer 12 — Continuous Evolution. The governing rule: no change reaches production without passing four sequential gates — versioning, evals, governance, and staged rollout. The goal is for Dealix to evolve without collapsing.

## Process scope

This process applies to every deployable change:
- Agents (`agent.yaml` definitions and runtime logic).
- Workflows (the workflows in `.github/workflows/`).
- Prompts used at runtime.
- Governance and safe-publishing policies.
- Memory schemas.

## Release stages

1. **Change proposal.** The change is recorded as an item in `continuous_improvement/improvement_backlog.md` or arrives from the feedback loop in `continuous_improvement/feedback_loop.md`.
2. **Classification.** The change is classified: patch, minor (feature), or major (breaking). The classification determines which release gates are required.
3. **Versioning and archival.** Before merge, the previous version of the modified artifact is archived under `versions/<category>/` following the naming rules in each category's `README.md`.
4. **Release gates.** All of the following gates must pass:
   - Continuous integration in `.github/workflows/ci.yml`.
   - The safe-publishing gate `auto_client_acquisition/self_growth_os/safe_publishing_gate.py` on any customer-facing content.
   - The evals and acceptance criteria in `continuous_improvement/tests.md`.
   - The forbidden-claims sweep (guaranteed, scraping, cold messaging) — must be clean.
5. **Changelog.** `CHANGELOG.md` is updated with an entry carrying the version number, date, and owner. No release without a changelog entry.
6. **Readiness score.** The release is assigned a readiness score (0–100) per the scale in `continuous_improvement/readiness.md`. Releases below 75 do not reach customers.
7. **Approval.** The Continuous Evolution Lead approves the final release card.
8. **Staged rollout.** The rollout is executed per `continuous_improvement/staged_rollout.md`.

## Release card

Every release carries a card containing: version number, named owner, date, classification, list of passed gates, reference to the archived previous version, readiness score, and rollback plan.

## What the process does not allow

- No direct deploy to production that bypasses evals.
- No change without a `CHANGELOG.md` entry.
- No release without a named owner.
- No promises of sales numbers or conversion rates — evidence is only observable patterns.
- No external send on a customer's behalf without explicit approval.

See also: `continuous_improvement/change_management.md`, `continuous_improvement/staged_rollout.md`, `continuous_improvement/rollback_policy.md`.
