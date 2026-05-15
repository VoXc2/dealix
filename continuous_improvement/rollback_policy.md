# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

تحدّد هذه السياسة كيف تعود Dealix إلى إصدار سابق معروف الاستقرار عند فشل تغيير أو انحداره. المبدأ: لا يُسمح بإصدار لا يمكن التراجع عنه. كل قطعة قابلة للنشر لها إصدار سابق مؤرشف يمكن استعادته.

## متى نتراجع

يُفعَّل التراجع عند أيّ من:
- اكتشف `.github/workflows/watchdog_drift.yml` انحرافاً في بوّابة صلبة.
- انخفضت درجة الجاهزية تحت 75 (انظر `continuous_improvement/readiness.md`).
- ظهر تصعيد حرج في سجل الاحتكاك `auto_client_acquisition/friction_log/`.
- فشلت بوّابة النشر الآمن على محتوى وصل بالفعل لشريحة حيّة.

## شرط التراجع المسبق

لا يُعتمَد أي إصدار ما لم يكن إصداره السابق مؤرشفاً تحت `versions/<category>/` وفق قواعد التسمية في `README.md` لتلك الفئة. الفئات: `versions/agents/`، `versions/workflows/`، `versions/prompts/`، `versions/policies/`، `versions/memory_schemas/`.

## إجراء التراجع

1. **التجميد.** يُوقَف الطرح المرحلي عند الشريحة الحالية فوراً.
2. **تحديد القطعة.** تُحدَّد القطعة المعدَّلة وفئتها.
3. **استعادة الإصدار.** يُستعاد الملف من `versions/<category>/<previous_version>/` ويحلّ محلّ الإصدار الفاشل.
4. **إدخال السجل.** يُضاف إدخال تراجع إلى `CHANGELOG.md` يحمل رقم الإصدار المُستعاد والسبب والمالك.
5. **إعادة التقييم.** يُعاد تشغيل التقييمات في `continuous_improvement/tests.md` للتأكّد من عودة الاستقرار.
6. **تسجيل الدرس.** يُسجَّل سبب الفشل كبند في `continuous_improvement/improvement_backlog.md`.

## اختبار التراجع

التراجع ليس افتراضاً — يُختبَر. مرّة شهرياً يُجرى تمرين تراجع على قطعة غير حرجة في بيئة معزولة، ويُسجَّل ناتجه. لا يُعدّ التراجع جاهزاً ما لم يُختبَر خلال آخر 30 يوماً.

## ما لا تسمح به السياسة

- لا إصدار بلا إصدار سابق مؤرشف.
- لا تراجع بلا إدخال في `CHANGELOG.md`.
- لا تراجع بلا مالك مُسمَّى يقود الإجراء.
- لا وعد للعميل بنتائج التراجع كأرقام — الوصف أنماط قابلة للملاحظة فقط.

انظر أيضاً: `continuous_improvement/staged_rollout.md`، `continuous_improvement/release_process.md`، `versions/agents/README.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This policy defines how Dealix returns to a known-stable previous version when a change fails or regresses. The principle: no release that cannot be reverted is permitted. Every deployable artifact has an archived previous version that can be restored.

## When we roll back

A rollback is triggered by any of:
- `.github/workflows/watchdog_drift.yml` detects drift in a hard gate.
- The readiness score drops below 75 (see `continuous_improvement/readiness.md`).
- A critical escalation appears in the friction log `auto_client_acquisition/friction_log/`.
- The safe-publishing gate fails on content that has already reached a live segment.

## Rollback precondition

No release is approved unless its previous version is archived under `versions/<category>/` following the naming rules in that category's `README.md`. Categories: `versions/agents/`, `versions/workflows/`, `versions/prompts/`, `versions/policies/`, `versions/memory_schemas/`.

## Rollback procedure

1. **Freeze.** The staged rollout is halted at the current segment immediately.
2. **Identify the artifact.** The modified artifact and its category are identified.
3. **Restore the version.** The file is restored from `versions/<category>/<previous_version>/` and replaces the failed version.
4. **Changelog entry.** A rollback entry is added to `CHANGELOG.md` carrying the restored version number, the reason, and the owner.
5. **Re-evaluate.** The evals in `continuous_improvement/tests.md` are re-run to confirm stability is restored.
6. **Record the lesson.** The failure cause is recorded as an item in `continuous_improvement/improvement_backlog.md`.

## Rollback testing

Rollback is not an assumption — it is tested. Once a month a rollback drill is run on a non-critical artifact in an isolated environment, and its outcome is recorded. Rollback is not considered ready unless it has been tested within the last 30 days.

## What the policy does not allow

- No release without an archived previous version.
- No rollback without a `CHANGELOG.md` entry.
- No rollback without a named owner driving the procedure.
- No promising the customer rollback outcomes as numbers — description is observable patterns only.

See also: `continuous_improvement/staged_rollout.md`, `continuous_improvement/release_process.md`, `versions/agents/README.md`.
