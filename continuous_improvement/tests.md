# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

تحدّد هذه الوثيقة حالات الاختبار ومعايير القبول للطبقة 12 كمواصفة مكتوبة. لا تحتوي على شيفرة. كل حالة تصف شرطاً يجب التحقّق منه قبل أن يجتاز تغيير بوّابات الإصدار.

## حالة 1 — لا نشر يتجاوز التقييمات

- **الوصف:** محاولة دفع تغيير قابل للنشر دون اجتياز تقييمات الإصدار.
- **معيار القبول:** يُرفَض الدفع. لا يصل تغيير لشريحة حيّة قبل اجتياز التقييمات المذكورة في `continuous_improvement/release_process.md`.

## حالة 2 — كل تغيير له إدخال سجل

- **الوصف:** فحص إصدار جديد مقابل `CHANGELOG.md`.
- **معيار القبول:** يوجد إدخال يحمل رقم الإصدار والتاريخ والمالك. غياب الإدخال يفشل البوّابة.

## حالة 3 — كل إصدار له مالك

- **الوصف:** فحص بطاقة الإصدار.
- **معيار القبول:** حقل المالك يحمل دوراً مُسمَّى غير فارغ.

## حالة 4 — الإصدار السابق مؤرشف

- **الوصف:** فحص فئة القطعة المعدَّلة تحت `versions/<category>/`.
- **معيار القبول:** يوجد مجلد إصدار سابق وفق قواعد التسمية في `README.md` لتلك الفئة قبل اعتماد الإصدار الجديد.

## حالة 5 — ملاحظة العميل تدخل السجل

- **الوصف:** تسجيل ملاحظة عبر `auto_client_acquisition/friction_log/store.py`.
- **معيار القبول:** بعد التعقيم والتجميع، تصبح الملاحظة بنداً في `continuous_improvement/improvement_backlog.md` أو تُغلَق بسبب موثَّق.

## حالة 6 — لا بيانات تعريف شخصية في سجل الاحتكاك

- **الوصف:** فحص مخرجات `auto_client_acquisition/friction_log/sanitizer.py`.
- **معيار القبول:** لا إيميل ولا هاتف ولا اسم حقيقي في السجل المُخزَّن.

## حالة 7 — الانحدار يُكتشف قبل الإنتاج

- **الوصف:** إدخال تغيير ذي انحدار معروف في المحاكاة.
- **معيار القبول:** تكتشفه المحاكاة أو الطرح المرحلي قبل المرحلة الكاملة؛ لا يصل 100% من العملاء.

## حالة 8 — التراجع مُختبَر

- **الوصف:** تمرين تراجع شهري على قطعة غير حرجة.
- **معيار القبول:** يُستعاد الإصدار السابق بنجاح، يُضاف إدخال تراجع، تُعاد التقييمات. التمرين خلال آخر 30 يوماً.

## حالة 9 — رفض المزاعم الممنوعة

- **الوصف:** تغيير يصف الكشط أو الأتمتة الباردة أو الإرسال بالجملة أو يَعِد بأرقام مبيعات.
- **معيار القبول:** يُرفَض عند المراجعة ولا يُصعَّد.

## حالة 10 — درجة الجاهزية مُسنَدة

- **الوصف:** فحص بطاقة الإصدار مقابل `continuous_improvement/readiness.md`.
- **معيار القبول:** الدرجة (0–100) مُسنَدة، والإصدارات تحت 75 لا تصل العملاء.

انظر أيضاً: `continuous_improvement/release_process.md`، `continuous_improvement/readiness.md`، `continuous_improvement/scorecard.yaml`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This document defines the test cases and acceptance criteria for Layer 12 as a written specification. It contains no code. Each case describes a condition that must be verified before a change passes the release gates.

## Case 1 — No deploy bypasses evals

- **Description:** Attempt to push a deployable change without passing the release evals.
- **Acceptance criterion:** The push is rejected. No change reaches a live segment before passing the evals listed in `continuous_improvement/release_process.md`.

## Case 2 — Every change has a changelog entry

- **Description:** Check a new release against `CHANGELOG.md`.
- **Acceptance criterion:** An entry exists carrying the version number, date, and owner. A missing entry fails the gate.

## Case 3 — Every release has an owner

- **Description:** Check the release card.
- **Acceptance criterion:** The owner field carries a non-empty named role.

## Case 4 — Previous version is archived

- **Description:** Check the modified artifact's category under `versions/<category>/`.
- **Acceptance criterion:** A previous-version folder exists, following the naming rules in that category's `README.md`, before the new release is approved.

## Case 5 — Customer feedback enters the backlog

- **Description:** Record feedback via `auto_client_acquisition/friction_log/store.py`.
- **Acceptance criterion:** After sanitization and aggregation, the feedback becomes an item in `continuous_improvement/improvement_backlog.md` or is closed with a documented reason.

## Case 6 — No PII in the friction log

- **Description:** Check the output of `auto_client_acquisition/friction_log/sanitizer.py`.
- **Acceptance criterion:** No email, no phone, no real name in the stored log.

## Case 7 — Regression caught before production

- **Description:** Introduce a change with a known regression into simulation.
- **Acceptance criterion:** Simulation or staged rollout catches it before the full stage; it does not reach 100% of customers.

## Case 8 — Rollback is tested

- **Description:** Monthly rollback drill on a non-critical artifact.
- **Acceptance criterion:** The previous version is restored successfully, a rollback entry is added, evals are re-run. The drill occurred within the last 30 days.

## Case 9 — Forbidden claims rejected

- **Description:** A change that describes scraping, cold automation, or bulk outreach, or promises sales numbers.
- **Acceptance criterion:** It is rejected at review and never escalated.

## Case 10 — Readiness score is assigned

- **Description:** Check the release card against `continuous_improvement/readiness.md`.
- **Acceptance criterion:** A score (0–100) is assigned, and releases below 75 do not reach customers.

See also: `continuous_improvement/release_process.md`, `continuous_improvement/readiness.md`, `continuous_improvement/scorecard.yaml`.
