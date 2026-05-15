# العربية

Owner: قائد المراقبة (Observability Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة المراقبة. مواصفة بالكلمات، لا كود.

## اختبارات الجاهزية

### ت-1: تغطية الأثر

- **الهدف:** كل تشغيل وكيل وسير عمل ينتج أثراً في `dealix/observability/otel.py`.
- **الخطوات:** شغّل وكيلاً وسير عمل، افحص الآثار.
- **النتيجة المتوقعة:** أثر كامل لكل تشغيل.
- **معيار النجاح/الفشل:** أي تشغيل بلا أثر = فشل يوقف الدمج.

### ت-2: حجب المعلومات الشخصية

- **الهدف:** الآثار والسجلات لا تحتوي معلومات تعريف شخصية.
- **الخطوات:** شغّل عملية تتضمن معلومات شخصية، افحص المخرجات عبر `observability_adapters/redaction.py`.
- **النتيجة المتوقعة:** المعلومات الشخصية محجوبة.
- **معيار النجاح/الفشل:** ظهور معلومات شخصية = فشل يوقف الدمج.

### ت-3: التنبيهات على الفشل

- **الهدف:** فشل خدمة يطلق تنبيهاً إلى مالك مُسمّى.
- **الخطوات:** أوقع فشلاً اصطناعياً، راقب التنبيه عبر `dealix/observability/sentry.py`.
- **النتيجة المتوقعة:** تنبيه يصل إلى المالك بزمن محدد.
- **معيار النجاح/الفشل:** فشل صامت = فشل.

### ت-4: ظهور فشل التكامل في اللوحة

- **الهدف:** فشل تكامل خارجي يظهر في لوحة المراقبة.
- **الخطوات:** أوقع فشل تكامل، افحص اللوحة عبر `platform/observability/dashboards.md`.
- **النتيجة المتوقعة:** الفشل ظاهر ومُصنَّف.
- **معيار النجاح/الفشل:** فشل غير ظاهر = فشل.

### ت-5: تمرين استجابة للحوادث (فجوة معروفة)

- **الهدف:** تمرين كامل من الكشف إلى التصعيد إلى الإغلاق.
- **الخطوات:** نفّذ سيناريو حادث، تتبّع زمن الكشف والاستجابة.
- **النتيجة المتوقعة:** أزمنة مُسجَّلة ضمن حدود الخطة.
- **معيار النجاح/الفشل:** غياب تمرين دوري متحقَّق = فجوة تُبقي الطبقة في نطاق تجربة عميل.

## ما يوقف الدمج

فشل ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج. ت-5 فجوة موثَّقة.

## روابط ذات صلة

- `readiness/observability/readiness.md`
- `readiness/cross_layer/observability_coverage_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Observability Lead

## Purpose

A readiness test specification for the Observability layer. A spec in words, not code.

## Readiness tests

### T-1: Trace coverage

- **Goal:** every agent and workflow run produces a trace in `dealix/observability/otel.py`.
- **Steps:** run an agent and a workflow, inspect the traces.
- **Expected result:** a complete trace per run.
- **Pass/fail:** any run with no trace = fail that blocks the merge.

### T-2: PII redaction

- **Goal:** traces and logs contain no personally identifiable information.
- **Steps:** run an operation involving PII, inspect output via `observability_adapters/redaction.py`.
- **Expected result:** PII is redacted.
- **Pass/fail:** any PII exposed = fail that blocks the merge.

### T-3: Alerting on failure

- **Goal:** a service failure fires an alert to a named owner.
- **Steps:** inject a synthetic failure, watch the alert via `dealix/observability/sentry.py`.
- **Expected result:** an alert reaches the owner within a defined time.
- **Pass/fail:** a silent failure = fail.

### T-4: Integration failure visibility on the dashboard

- **Goal:** an external integration failure surfaces on the observability dashboard.
- **Steps:** inject an integration failure, inspect the dashboard via `platform/observability/dashboards.md`.
- **Expected result:** the failure is visible and classified.
- **Pass/fail:** an invisible failure = fail.

### T-5: Incident-response drill (known gap)

- **Goal:** a full drill from detection to escalation to closure.
- **Steps:** run an incident scenario, track detection and response times.
- **Expected result:** recorded times within plan limits.
- **Pass/fail:** absence of a periodic verified drill = a gap that keeps the layer in the client-pilot band.

## What blocks a merge

Failure in T-1, T-2, T-3, or T-4 blocks the merge. T-5 is a documented gap.

## Related links

- `readiness/observability/readiness.md`
- `readiness/cross_layer/observability_coverage_test.md`

Estimated value is not Verified value.
