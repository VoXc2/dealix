# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

يحفظ هذا المجلد الإصدارات المؤرشفة من سياسات الحوكمة والنشر الآمن. السياسات تحكم ما يُسمح به في المنصة، لذا يخضع تغييرها لانضباط إصدار صارم، ووجود إصدار سابق هنا شرط مسبق للتراجع وفق `continuous_improvement/rollback_policy.md`.

## كيف تُخزَّن الأرشيفات

كل إصدار من سياسة يُحفظ في مجلد فرعي: `versions/policies/<policy_name>/<version>/`. يحوي المجلد نسخة كاملة من السياسة كما كانت وقت الإصدار.

## قواعد التسمية

- `<policy_name>` يطابق المعرّف الذي تُرجَع به السياسة (مثال: السياسات المرتبطة بـ`auto_client_acquisition/self_growth_os/safe_publishing_gate.py` أو سجلّات `dealix/registers/`).
- `<version>` إصدار دلالي: `MAJOR.MINOR.PATCH`.
- كل مجلد إصدار يحوي ملف `manifest` يحمل: رقم الإصدار، التاريخ، المالك، التصنيف، ومرجع إدخال `CHANGELOG.md`.

## التراجع

لاستعادة إصدار سابق: يُحدَّد المجلد `versions/policies/<policy_name>/<previous_version>/`، تُستعاد محتوياته لتحلّ محلّ الإصدار الفاشل، ويُضاف إدخال تراجع إلى `CHANGELOG.md`. الإجراء الكامل في `continuous_improvement/rollback_policy.md`.

## قواعد الحوكمة

- لا يُحذف مجلد إصدار مؤرشف.
- أي تغيير على سياسة يمسّ العميل هو تغيير كاسر يتطلّب مراجعة ند وموافقة المالك.
- لا تُخفَّف سياسة لتسمح بالكشط أو الأتمتة الباردة أو الإرسال بالجملة.

انظر أيضاً: `continuous_improvement/change_management.md`، `continuous_improvement/rollback_policy.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This folder holds the archived versions of governance and safe-publishing policies. Policies govern what the platform permits, so changing them follows strict versioning discipline, and the presence of a previous version here is a precondition for rollback per `continuous_improvement/rollback_policy.md`.

## How archives are stored

Each policy version is kept in a subfolder: `versions/policies/<policy_name>/<version>/`. The folder holds a complete copy of the policy as it stood at release time.

## Naming rules

- `<policy_name>` matches the identifier the policy is referenced by (example: policies linked to `auto_client_acquisition/self_growth_os/safe_publishing_gate.py` or the registers under `dealix/registers/`).
- `<version>` is a semantic version: `MAJOR.MINOR.PATCH`.
- Each version folder contains a `manifest` file carrying: version number, date, owner, classification, and a reference to the `CHANGELOG.md` entry.

## Rollback

To restore a previous version: identify the folder `versions/policies/<policy_name>/<previous_version>/`, restore its contents to replace the failed version, and add a rollback entry to `CHANGELOG.md`. The full procedure is in `continuous_improvement/rollback_policy.md`.

## Governance rules

- An archived version folder is never deleted.
- Any change to a customer-facing policy is a breaking change requiring peer review and owner approval.
- A policy is never relaxed to permit scraping, cold automation, or bulk outreach.

See also: `continuous_improvement/change_management.md`, `continuous_improvement/rollback_policy.md`.
