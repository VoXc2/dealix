# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

يحفظ هذا المجلد الإصدارات المؤرشفة من مسارات العمل في `.github/workflows/`. وجود إصدار سابق هنا شرط مسبق لاعتماد أي تغيير على مسار عمل، ويجعل التراجع ممكناً وفق `continuous_improvement/rollback_policy.md`.

## كيف تُخزَّن الأرشيفات

كل إصدار من مسار عمل يُحفظ في مجلد فرعي: `versions/workflows/<workflow_name>/<version>/`. يحوي المجلد نسخة كاملة من ملف المسار كما كان وقت الإصدار.

## قواعد التسمية

- `<workflow_name>` يطابق اسم ملف المسار في `.github/workflows/` (مثال: `weekly_self_improvement`، `watchdog_drift`).
- `<version>` إصدار دلالي: `MAJOR.MINOR.PATCH`.
- كل مجلد إصدار يحوي ملف `manifest` يحمل: رقم الإصدار، التاريخ، المالك، التصنيف، ومرجع إدخال `CHANGELOG.md`.

## التراجع

لاستعادة إصدار سابق: يُحدَّد المجلد `versions/workflows/<workflow_name>/<previous_version>/`، تُستعاد محتوياته لتحلّ محلّ الإصدار الفاشل، ويُضاف إدخال تراجع إلى `CHANGELOG.md`. الإجراء الكامل في `continuous_improvement/rollback_policy.md`.

## قواعد الحوكمة

- لا يُحذف مجلد إصدار مؤرشف.
- كل تغيير على مسار عمل قابل للتتبّع إلى إدخال في `CHANGELOG.md`.
- التغييرات على مسارات المراقبة مثل `watchdog_drift` تمرّ على مراجعة الند قبل الأرشفة.

انظر أيضاً: `continuous_improvement/release_process.md`، `continuous_improvement/rollback_policy.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This folder holds the archived versions of the workflows in `.github/workflows/`. The presence of a previous version here is a precondition for approving any change to a workflow, and it makes rollback possible per `continuous_improvement/rollback_policy.md`.

## How archives are stored

Each workflow version is kept in a subfolder: `versions/workflows/<workflow_name>/<version>/`. The folder holds a complete copy of the workflow file as it stood at release time.

## Naming rules

- `<workflow_name>` matches the workflow file name in `.github/workflows/` (example: `weekly_self_improvement`, `watchdog_drift`).
- `<version>` is a semantic version: `MAJOR.MINOR.PATCH`.
- Each version folder contains a `manifest` file carrying: version number, date, owner, classification, and a reference to the `CHANGELOG.md` entry.

## Rollback

To restore a previous version: identify the folder `versions/workflows/<workflow_name>/<previous_version>/`, restore its contents to replace the failed version, and add a rollback entry to `CHANGELOG.md`. The full procedure is in `continuous_improvement/rollback_policy.md`.

## Governance rules

- An archived version folder is never deleted.
- Every workflow change is traceable to a `CHANGELOG.md` entry.
- Changes to monitoring workflows such as `watchdog_drift` go through peer review before archival.

See also: `continuous_improvement/release_process.md`, `continuous_improvement/rollback_policy.md`.
