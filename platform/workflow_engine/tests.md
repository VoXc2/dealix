# العربية

**Owner:** مهندس ضمان جودة المنصة (Platform QA Engineer).

## الغرض

مواصفة اختبار قبول لمحرّك سير العمل — الطبقة الثالثة. كل حالة لها معرّف وشرط قبول صريح. لا شيفرة هنا؛ هذه مواصفة تُترجَم لاحقاً إلى اختبارات تنفيذية.

## حالات اختبار التنفيذ

### WE-T01 — تشغيل كامل من المحفّز إلى المخرج
- **الإجراء:** إطلاق سير عمل بمحفّز صالح.
- **القبول:** يصل التشغيل إلى حالة `completed` وينتج المخرج النهائي المعلن، وكل خطوة مسجَّلة.

### WE-T02 — منع تكرار المحفّز
- **الإجراء:** إرسال نفس المحفّز الحدثي مرتين بنفس المفتاح.
- **القبول:** يُخلق تشغيل واحد فقط؛ الثاني يُرفض بسلام دون أثر مزدوج.

### WE-T03 — إعادة محاولة خطأ عابر
- **الإجراء:** إفشال خطوة بخطأ عابر مرة ثم نجاحها.
- **القبول:** يعيد المحرّك المحاولة بتراجع أسّي ويكمل التشغيل؛ السجل يظهر المحاولات.

### WE-T04 — استنفاد إعادة المحاولة والدفع إلى DLQ
- **الإجراء:** إفشال خطوة بخطأ عابر مستمر بلا مسار بديل.
- **القبول:** بعد `max_attempts` يُدفع البند إلى DLQ بالمصدر والحمولة وعدد المحاولات.

### WE-T05 — المسار البديل
- **الإجراء:** إفشال خطوة لها مسار بديل معرّف.
- **القبول:** يتحوّل التشغيل إلى المسار البديل ويكمل دون إيقاف كامل.

### WE-T06 — التعويض عند فشل دائم
- **الإجراء:** إكمال خطوة ذات أثر جانبي ثم إفشال خطوة لاحقة فشلاً دائماً.
- **القبول:** تُشغَّل خطوات التعويض بترتيب عكسي، وكل خطوة تعويض مسجَّلة بوسم `compensation=true`.

## حالات اختبار الموافقة والحوكمة

### WE-T07 — توقف عند خطوة موافقة
- **الإجراء:** بلوغ خطوة تواصل خارجي.
- **القبول:** يتوقف التشغيل عند `waiting_approval` ولا يُرسل أي تواصل خارجي قبل موافقة بشرية.

### WE-T08 — رفض سير عمل بلا موافقة قبل الإرسال
- **الإجراء:** محاولة تحميل سير عمل يضع خطوة إرسال خارجي دون خطوة موافقة سابقة.
- **القبول:** يرفض المحرّك التحميل ويُسجَّل سبب الرفض.

### WE-T09 — الاستئناف بعد الموافقة
- **الإجراء:** الموافقة على بند عمل محتجَز.
- **القبول:** يستأنف التشغيل من الخطوة التالية دون إعادة الخطوات المكتملة.

### WE-T10 — حجب الحوكمة
- **الإجراء:** تشغيل سير عمل بشرط حوكمة غير محقَّق (قناة غير مسموحة).
- **القبول:** يُغلق التشغيل بحالة `skipped` مع أثر، ولا تُنفَّذ خطوات لاحقة.

## حالات اختبار الإصدارات والمراقبة

### WE-T11 — تثبيت الإصدار
- **الإجراء:** نشر إصدار أحدث أثناء تشغيل جارٍ.
- **القبول:** التشغيل الجاري يكمل على إصداره المثبَّت؛ التشغيل الجديد يستخدم الأحدث.

### WE-T12 — اكتمال البيانات الوصفية الإلزامية
- **الإجراء:** فحص كل ملف سير عمل في `workflows/`.
- **القبول:** كل ملف يحمل `name`, `version`, `trigger`, `owner`, `sla`, و`metrics` بعنصر واحد على الأقل.

### WE-T13 — تنقية بيانات التعريف الشخصية من السجلات
- **الإجراء:** تشغيل سير عمل بحمولة تحتوي بيانات تعريف شخصية.
- **القبول:** لا تظهر بيانات تعريف شخصية في السجلات؛ تُنقَّح عبر `redaction.py`.

### WE-T14 — عتبة معدّل الإكمال
- **الإجراء:** قياس `completion_rate` على دفعة تشغيلات في سيناريو عادي.
- **القبول:** `completion_rate` أعلى من 95%؛ غير ذلك يُطلق تنبيهاً.

## معيار القبول الإجمالي

تُعتبر الطبقة جاهزة لتجريب العميل عندما تنجح WE-T01 إلى WE-T14 وكل ملفات سير العمل تجتاز WE-T12.

---

# English

**Owner:** Platform QA Engineer.

## Purpose

An acceptance test spec for the Workflow Engine — Layer 3. Each case has an id and an explicit acceptance criterion. No code here; this is a spec to be translated later into executable tests.

## Execution test cases

### WE-T01 — Full run from trigger to output
- **Action:** fire a workflow with a valid trigger.
- **Acceptance:** the run reaches state `completed` and produces the declared final output, with every step logged.

### WE-T02 — Trigger deduplication
- **Action:** send the same event trigger twice with the same key.
- **Acceptance:** exactly one run is created; the second is rejected gracefully with no duplicate effect.

### WE-T03 — Transient error retry
- **Action:** fail a step with a transient error once, then succeed.
- **Acceptance:** the engine retries with exponential backoff and completes the run; the log shows the attempts.

### WE-T04 — Retry exhaustion and DLQ push
- **Action:** fail a step with a persistent transient error and no fallback.
- **Acceptance:** after `max_attempts` the item is pushed to the DLQ with source, payload, and attempt count.

### WE-T05 — Fallback path
- **Action:** fail a step that has a defined fallback path.
- **Acceptance:** the run switches to the fallback path and completes without a full stop.

### WE-T06 — Compensation on permanent failure
- **Action:** complete a side-effecting step, then fail a later step permanently.
- **Acceptance:** compensation steps run in reverse order, each logged with the tag `compensation=true`.

## Approval and governance test cases

### WE-T07 — Halt at an approval step
- **Action:** reach an external communication step.
- **Acceptance:** the run halts at `waiting_approval` and no external communication is sent before human approval.

### WE-T08 — Reject a workflow with no approval before send
- **Action:** attempt to load a workflow that places an external send step with no prior approval step.
- **Acceptance:** the engine refuses the load and the rejection reason is logged.

### WE-T09 — Resume after approval
- **Action:** approve a parked work item.
- **Acceptance:** the run resumes from the next step without re-running completed steps.

### WE-T10 — Governance block
- **Action:** run a workflow with an unmet governance condition (a disallowed channel).
- **Acceptance:** the run closes with state `skipped` and a trace; no later steps execute.

## Versioning and observability test cases

### WE-T11 — Version pinning
- **Action:** publish a newer version during an in-flight run.
- **Acceptance:** the in-flight run completes on its pinned version; a new run uses the latest.

### WE-T12 — Mandatory metadata completeness
- **Action:** scan every workflow file in `workflows/`.
- **Acceptance:** every file carries `name`, `version`, `trigger`, `owner`, `sla`, and `metrics` with at least one item.

### WE-T13 — PII redaction from logs
- **Action:** run a workflow with a payload containing personally identifiable information.
- **Acceptance:** no PII appears in logs; it is redacted via `redaction.py`.

### WE-T14 — Completion rate threshold
- **Action:** measure `completion_rate` on a batch of runs in a normal scenario.
- **Acceptance:** `completion_rate` is above 95%; otherwise an alert fires.

## Overall acceptance criterion

The layer is considered ready for a client pilot when WE-T01 through WE-T14 pass and all workflow files pass WE-T12.
