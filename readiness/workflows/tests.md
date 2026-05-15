# العربية

Owner: قائد محرك سير العمل (Workflow Engine Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة محرك سير العمل. مواصفة بالكلمات، لا كود.

## اختبارات الجاهزية

### ت-1: بوابة الموافقة عالية الخطورة

- **الهدف:** سير عمل لا ينفّذ فعلاً عالي الخطورة دون موافقة.
- **الخطوات:** شغّل سير عمل يحتوي خطوة عالية الخطورة عبر `execution_os/gates.py` بلا موافقة.
- **النتيجة المتوقعة:** سير العمل يتوقف عند البوابة بانتظار الموافقة.
- **معيار النجاح/الفشل:** تنفيذ فعل عالي الخطورة بلا موافقة = فشل يوقف الدمج.

### ت-2: إعادة المحاولة والتعويض

- **الهدف:** خطوة فاشلة تُعاد المحاولة عليها ثم تُعوَّض بلا أثر جزئي.
- **الخطوات:** أوقع خطوة وسطية في سير عمل متعدد الخطوات.
- **النتيجة المتوقعة:** التعويض يعيد الحالة، لا أثر جزئي باقٍ.
- **معيار النجاح/الفشل:** بقاء أثر جزئي = فشل.

### ت-3: المُحفِّزات والخمول

- **الهدف:** مُحفِّز مكرر لا يشغّل سير العمل مرتين.
- **الخطوات:** أرسل نفس المُحفِّز مرتين.
- **النتيجة المتوقعة:** تشغيل واحد فقط (خمول).
- **معيار النجاح/الفشل:** تشغيل مزدوج = فشل.

### ت-4: إصدار سير العمل

- **الهدف:** تعديل سير عمل يُنشئ إصداراً جديداً ولا يكسر التشغيلات الجارية.
- **الخطوات:** عدّل سير عمل أثناء تشغيل قائم.
- **النتيجة المتوقعة:** التشغيل القائم يكمل على إصداره.
- **معيار النجاح/الفشل:** كسر تشغيل جارٍ = فشل.

### ت-5: تمرين إعادة تشغيل DLQ (فجوة معروفة)

- **الهدف:** رسائل قائمة الرسائل الميتة تُعاد بنجاح.
- **الخطوات:** ادفع رسائل إلى `dealix/reliability/dlq.py`، أعد تشغيلها.
- **النتيجة المتوقعة:** الرسائل تُعالَج بلا تكرار أثر.
- **معيار النجاح/الفشل:** غياب تمرين دوري متحقَّق = فجوة تُبقي الطبقة في نطاق تجربة عميل.

## ما يوقف الدمج

فشل ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج. ت-5 فجوة موثَّقة.

## روابط ذات صلة

- `readiness/workflows/readiness.md`
- `readiness/cross_layer/workflow_governance_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Workflow Engine Lead

## Purpose

A readiness test specification for the Workflow Engine layer. A spec in words, not code.

## Readiness tests

### T-1: High-risk approval gate

- **Goal:** a workflow does not execute a high-risk action without approval.
- **Steps:** run a workflow containing a high-risk step via `execution_os/gates.py` with no approval.
- **Expected result:** the workflow halts at the gate awaiting approval.
- **Pass/fail:** executing a high-risk action without approval = fail that blocks the merge.

### T-2: Retry and compensation

- **Goal:** a failed step is retried then compensated with no partial effect.
- **Steps:** fail a middle step in a multi-step workflow.
- **Expected result:** compensation restores state, no partial effect remains.
- **Pass/fail:** any residual partial effect = fail.

### T-3: Triggers and idempotency

- **Goal:** a duplicate trigger does not run the workflow twice.
- **Steps:** send the same trigger twice.
- **Expected result:** a single run only (idempotent).
- **Pass/fail:** a double run = fail.

### T-4: Workflow versioning

- **Goal:** editing a workflow creates a new version and does not break running executions.
- **Steps:** edit a workflow during an in-flight run.
- **Expected result:** the in-flight run completes on its version.
- **Pass/fail:** breaking an in-flight run = fail.

### T-5: DLQ-replay drill (known gap)

- **Goal:** dead-letter queue messages replay successfully.
- **Steps:** push messages into `dealix/reliability/dlq.py`, replay them.
- **Expected result:** messages are processed with no duplicated effect.
- **Pass/fail:** absence of a periodic verified drill = a gap that keeps the layer in the client-pilot band.

## What blocks a merge

Failure in T-1, T-2, T-3, or T-4 blocks the merge. T-5 is a documented gap.

## Related links

- `readiness/workflows/readiness.md`
- `readiness/cross_layer/workflow_governance_test.md`

Estimated value is not Verified value.
