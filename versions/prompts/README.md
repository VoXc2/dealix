# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

يحفظ هذا المجلد الإصدارات المؤرشفة من المطالبات (prompts) المستخدمة في وقت التشغيل. تغيّر المطالبة يغيّر سلوك المنصة، لذا تخضع لنفس انضباط الإصدار، ووجود إصدار سابق هنا شرط مسبق للتراجع وفق `continuous_improvement/rollback_policy.md`.

## كيف تُخزَّن الأرشيفات

كل إصدار من مطالبة يُحفظ في مجلد فرعي: `versions/prompts/<prompt_name>/<version>/`. يحوي المجلد النصّ الكامل للمطالبة كما كان وقت الإصدار.

## قواعد التسمية

- `<prompt_name>` يطابق المعرّف الذي تُستدعى به المطالبة في الكود المصدري.
- `<version>` إصدار دلالي: `MAJOR.MINOR.PATCH`.
- كل مجلد إصدار يحوي ملف `manifest` يحمل: رقم الإصدار، التاريخ، المالك، التصنيف، ومرجع إدخال `CHANGELOG.md`.

## التراجع

لاستعادة إصدار سابق: يُحدَّد المجلد `versions/prompts/<prompt_name>/<previous_version>/`، يُستعاد النصّ ليحلّ محلّ الإصدار الفاشل، ويُضاف إدخال تراجع إلى `CHANGELOG.md`. الإجراء الكامل في `continuous_improvement/rollback_policy.md`.

## قواعد الحوكمة

- لا يُحذف مجلد إصدار مؤرشف.
- كل مطالبة موجَّهة لمحتوى العميل تمرّ على بوّابة النشر الآمن `auto_client_acquisition/self_growth_os/safe_publishing_gate.py` قبل الأرشفة.
- لا أرشفة لمطالبة تَعِد بأرقام مبيعات أو تصف الكشط أو الأتمتة الباردة.

انظر أيضاً: `continuous_improvement/release_process.md`، `continuous_improvement/rollback_policy.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This folder holds the archived versions of prompts used at runtime. Changing a prompt changes platform behavior, so prompts follow the same versioning discipline, and the presence of a previous version here is a precondition for rollback per `continuous_improvement/rollback_policy.md`.

## How archives are stored

Each prompt version is kept in a subfolder: `versions/prompts/<prompt_name>/<version>/`. The folder holds the complete prompt text as it stood at release time.

## Naming rules

- `<prompt_name>` matches the identifier by which the prompt is called in the source code.
- `<version>` is a semantic version: `MAJOR.MINOR.PATCH`.
- Each version folder contains a `manifest` file carrying: version number, date, owner, classification, and a reference to the `CHANGELOG.md` entry.

## Rollback

To restore a previous version: identify the folder `versions/prompts/<prompt_name>/<previous_version>/`, restore the text to replace the failed version, and add a rollback entry to `CHANGELOG.md`. The full procedure is in `continuous_improvement/rollback_policy.md`.

## Governance rules

- An archived version folder is never deleted.
- Every customer-facing prompt passes the safe-publishing gate `auto_client_acquisition/self_growth_os/safe_publishing_gate.py` before archival.
- No archiving of a prompt that promises sales numbers or describes scraping or cold automation.

See also: `continuous_improvement/release_process.md`, `continuous_improvement/rollback_policy.md`.
