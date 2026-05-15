# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

يحفظ هذا المجلد الإصدارات المؤرشفة من مخططات الذاكرة (memory schemas). تغيّر المخطط يمسّ كل البيانات المخزَّنة، لذا يخضع لانضباط إصدار صارم، ووجود إصدار سابق هنا شرط مسبق للتراجع وفق `continuous_improvement/rollback_policy.md`.

## كيف تُخزَّن الأرشيفات

كل إصدار من مخطط يُحفظ في مجلد فرعي: `versions/memory_schemas/<schema_name>/<version>/`. يحوي المجلد تعريف المخطط الكامل كما كان وقت الإصدار، ومذكّرة هجرة توضح كيف تنتقل البيانات من الإصدار السابق.

## قواعد التسمية

- `<schema_name>` يطابق اسم المخطط في الكود المصدري (مثل مخططات `auto_client_acquisition/self_growth_os/schemas.py` أو `auto_client_acquisition/friction_log/schemas.py`).
- `<version>` إصدار دلالي: `MAJOR.MINOR.PATCH`. أي تغيير غير متوافق للخلف يرفع الرقم الرئيسي (MAJOR).
- كل مجلد إصدار يحوي ملف `manifest` يحمل: رقم الإصدار، التاريخ، المالك، التصنيف، ومرجع إدخال `CHANGELOG.md`.

## التراجع

لاستعادة إصدار سابق: يُحدَّد المجلد `versions/memory_schemas/<schema_name>/<previous_version>/`، يُستعاد تعريف المخطط، وتُطبَّق مذكّرة الهجرة العكسية إن لزم، ويُضاف إدخال تراجع إلى `CHANGELOG.md`. الإجراء الكامل في `continuous_improvement/rollback_policy.md`.

## قواعد الحوكمة

- لا يُحذف مجلد إصدار مؤرشف.
- كل تغيير كاسر للمخطط يتطلّب مذكّرة هجرة أمامية وعكسية قبل الأرشفة.
- لا يُخزَّن في أي مخطط حقل يحمل بيانات تعريف شخصية بلا تعقيم مسبق.

انظر أيضاً: `continuous_improvement/change_management.md`، `continuous_improvement/rollback_policy.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This folder holds the archived versions of memory schemas. Changing a schema touches all stored data, so it follows strict versioning discipline, and the presence of a previous version here is a precondition for rollback per `continuous_improvement/rollback_policy.md`.

## How archives are stored

Each schema version is kept in a subfolder: `versions/memory_schemas/<schema_name>/<version>/`. The folder holds the complete schema definition as it stood at release time, plus a migration note describing how data moves from the previous version.

## Naming rules

- `<schema_name>` matches the schema name in the source code (such as the schemas in `auto_client_acquisition/self_growth_os/schemas.py` or `auto_client_acquisition/friction_log/schemas.py`).
- `<version>` is a semantic version: `MAJOR.MINOR.PATCH`. Any backward-incompatible change raises the MAJOR number.
- Each version folder contains a `manifest` file carrying: version number, date, owner, classification, and a reference to the `CHANGELOG.md` entry.

## Rollback

To restore a previous version: identify the folder `versions/memory_schemas/<schema_name>/<previous_version>/`, restore the schema definition, apply the reverse migration note if needed, and add a rollback entry to `CHANGELOG.md`. The full procedure is in `continuous_improvement/rollback_policy.md`.

## Governance rules

- An archived version folder is never deleted.
- Every breaking schema change requires a forward and a reverse migration note before archival.
- No schema stores a field carrying personally identifying data without prior sanitization.

See also: `continuous_improvement/change_management.md`, `continuous_improvement/rollback_policy.md`.
