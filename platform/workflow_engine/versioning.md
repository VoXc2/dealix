# العربية

**Owner:** مالك محرّك سير العمل (Workflow Engine Platform Lead).

## الغرض

يحدّد هذا المستند كيف تُدار إصدارات سير العمل. كل تعريف سير عمل يحمل مفتاح `version` بصيغة دلالية (`MAJOR.MINOR.PATCH`)، وكل تشغيل يثبّت إصداراً واحداً طوال دورة حياته.

## قاعدة الإصدار المثبَّت

عند بدء تشغيل، يُسجَّل رقم إصدار سير العمل ضمن سجل التشغيل ولا يتغيّر حتى لو نُشر إصدار أحدث منتصف التشغيل. التشغيل الجاري يكمل على إصداره الأصلي؛ التشغيلات الجديدة تستخدم الإصدار الأحدث.

## دلالة أرقام الإصدار

- **PATCH** (مثل 1.0.0 → 1.0.1): تصحيح لا يغيّر بنية الخطوات — تعديل نص، تشديد شرط.
- **MINOR** (1.0.0 → 1.1.0): إضافة خطوة أو مقياس دون كسر التوافق.
- **MAJOR** (1.0.0 → 2.0.0): تغيير بنية الخطوات أو المحفّز أو المخرج النهائي بشكل غير متوافق.

## النشر والتراجع

كل تغيير على ملف سير عمل يمر بمراجعة في التكامل المستمر (`.github/workflows/ci.yml`). الإصدار السابق يبقى محفوظاً في سجل git. التراجع يعني إعادة الإصدار المستقر السابق وإعادة توجيه التشغيلات الجديدة إليه.

## مقارنة الإصدارات

يُحتفظ بسجل تغييرات لكل سير عمل: ما الخطوات المضافة أو المحذوفة، وما أثر التغيير على المقاييس. عند ترقية MAJOR يُوثَّق دليل ترحيل للتشغيلات قيد الانتظار.

## الحوكمة

- لا يُنشر إصدار جديد دون مالك معلن واختبار قبول مُحدَّث في `platform/workflow_engine/tests.md`.
- ترقية MAJOR تتطلب موافقة موثَّقة من مالك الطبقة.
- أي إصدار يحتوي خطوة تواصل خارجي يجب أن يبقي خطوة الموافقة البشرية سابقة لها.

انظر أيضاً: `platform/workflow_engine/readiness.md`، `platform/workflow_engine/architecture.md`.

---

# English

**Owner:** Workflow Engine Platform Lead.

## Purpose

This document defines how workflow versions are managed. Every workflow definition carries a `version` key in semantic form (`MAJOR.MINOR.PATCH`), and every run pins a single version for its whole lifecycle.

## Pinned-version rule

When a run starts, the workflow version number is recorded in the run log and does not change even if a newer version is published mid-run. An in-flight run completes on its original version; new runs use the latest version.

## Meaning of version numbers

- **PATCH** (e.g. 1.0.0 to 1.0.1): a fix that does not change step structure — text edit, condition tightening.
- **MINOR** (1.0.0 to 1.1.0): adding a step or metric without breaking compatibility.
- **MAJOR** (1.0.0 to 2.0.0): an incompatible change to step structure, trigger, or final output.

## Release and rollback

Every change to a workflow file passes review in continuous integration (`.github/workflows/ci.yml`). The previous version stays preserved in the git history. Rollback means restoring the previous stable version and routing new runs to it.

## Version comparison

A change log is kept per workflow: which steps were added or removed, and how the change affects metrics. On a MAJOR upgrade, a migration guide is documented for pending runs.

## Governance

- No new version is published without a declared owner and an updated acceptance test in `platform/workflow_engine/tests.md`.
- A MAJOR upgrade requires a documented approval from the layer owner.
- Any version containing an external communication step must keep the human-approval step preceding it.

See also: `platform/workflow_engine/readiness.md`, `platform/workflow_engine/architecture.md`.
