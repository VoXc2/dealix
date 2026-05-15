# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

يحفظ هذا المجلد الإصدارات المؤرشفة من تعريفات الوكلاء ومنطق تشغيلها. وجود إصدار سابق هنا شرط مسبق لاعتماد أي إصدار جديد، وهو ما يجعل التراجع ممكناً وفق `continuous_improvement/rollback_policy.md`.

## كيف تُخزَّن الأرشيفات

كل إصدار من وكيل يُحفظ في مجلد فرعي خاص به: `versions/agents/<agent_name>/<version>/`. يحوي المجلد نسخة كاملة من تعريف الوكيل كما كان وقت الإصدار، لا فرقاً جزئياً.

## قواعد التسمية

- `<agent_name>` يطابق اسم الوكيل في الكود المصدري.
- `<version>` إصدار دلالي: `MAJOR.MINOR.PATCH` (مثال: `2.3.0`).
- كل مجلد إصدار يحوي ملف `manifest` يحمل: رقم الإصدار، التاريخ، المالك، التصنيف، ومرجع إدخال `CHANGELOG.md`.

## التراجع

لاستعادة إصدار سابق: يُحدَّد المجلد `versions/agents/<agent_name>/<previous_version>/`، تُستعاد محتوياته لتحلّ محلّ الإصدار الفاشل، ويُضاف إدخال تراجع إلى `CHANGELOG.md`. الإجراء الكامل في `continuous_improvement/rollback_policy.md`.

## قواعد الحوكمة

- لا يُحذف مجلد إصدار مؤرشف.
- كل إصدار قابل للتتبّع إلى إدخال في `CHANGELOG.md`.
- لا أرشفة لوكيل يصف الكشط أو الأتمتة الباردة أو الإرسال بالجملة.

انظر أيضاً: `continuous_improvement/release_process.md`، `continuous_improvement/rollback_policy.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This folder holds the archived versions of agent definitions and their runtime logic. The presence of a previous version here is a precondition for approving any new release, which is what makes rollback possible per `continuous_improvement/rollback_policy.md`.

## How archives are stored

Each agent version is kept in its own subfolder: `versions/agents/<agent_name>/<version>/`. The folder holds a complete copy of the agent definition as it stood at release time — not a partial diff.

## Naming rules

- `<agent_name>` matches the agent's name in the source code.
- `<version>` is a semantic version: `MAJOR.MINOR.PATCH` (example: `2.3.0`).
- Each version folder contains a `manifest` file carrying: version number, date, owner, classification, and a reference to the `CHANGELOG.md` entry.

## Rollback

To restore a previous version: identify the folder `versions/agents/<agent_name>/<previous_version>/`, restore its contents to replace the failed version, and add a rollback entry to `CHANGELOG.md`. The full procedure is in `continuous_improvement/rollback_policy.md`.

## Governance rules

- An archived version folder is never deleted.
- Every version is traceable to a `CHANGELOG.md` entry.
- No archiving of an agent that describes scraping, cold automation, or bulk outreach.

See also: `continuous_improvement/release_process.md`, `continuous_improvement/rollback_policy.md`.
