# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## اختبار عابر للطبقات: فشل التكامل يظهر في لوحة المراقبة

الطبقات المشاركة: 6 (التنفيذ والتكاملات) + 7 (المراقبة).

## الهدف

التحقق من أن فشل تكامل خارجي يظهر في لوحة المراقبة وينبّه مالكاً مُسمّى، فلا يبقى أي فشل صامتاً.

## المتطلبات المسبقة

- تكامل خارجي عبر `integrations/` (مثل `integrations/hubspot.py` أو `integrations/calendar.py`).
- مسار مراقبة عبر `dealix/observability/otel.py` و`dealix/observability/sentry.py`.
- لوحة موصوفة في `platform/observability/dashboards.md` ومالك مُسمّى للتنبيهات.

## الخطوات

1. أوقع فشلاً اصطناعياً في التكامل (مثل خطأ مصادقة أو مهلة).
2. راقب أثر العملية في `dealix/observability/otel.py`.
3. افحص لوحة المراقبة بحثاً عن الفشل.
4. تحقق من إطلاق تنبيه إلى المالك المُسمّى.
5. سجّل زمن الكشف من لحظة الفشل إلى ظهوره.

## النتيجة المتوقعة

- الخطوة 2: الفشل ملتقَط في الأثر مع سببه.
- الخطوة 3: الفشل ظاهر ومُصنَّف في اللوحة.
- الخطوة 4: تنبيه يصل إلى المالك ضمن الزمن المحدد في الخطة.
- الخطوة 5: زمن الكشف مُسجَّل.

## معيار النجاح/الفشل

- **نجاح:** كل فشل تكامل ظاهر في اللوحة ويطلق تنبيهاً ضمن الزمن المحدد.
- **فشل:** فشل صامت لا يظهر في اللوحة، أو لا يطلق تنبيهاً. الفشل يوقف الدمج ويضع سقفاً على الطبقتين 6 و7 عند نطاق تجربة عميل.

## روابط ذات صلة

- `readiness/observability/readiness.md`
- `platform/integrations/readiness.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Cross-layer test: an integration failure surfaces on the observability dashboard

Participating layers: 6 (Execution & Integrations) + 7 (Observability).

## Goal

Verify that an external integration failure surfaces on the observability dashboard and alerts a named owner, so no failure stays silent.

## Preconditions

- An external integration via `integrations/` (such as `integrations/hubspot.py` or `integrations/calendar.py`).
- An observability path via `dealix/observability/otel.py` and `dealix/observability/sentry.py`.
- A dashboard described in `platform/observability/dashboards.md` and a named alert owner.

## Steps

1. Inject a synthetic failure in the integration (such as an auth error or a timeout).
2. Observe the operation trace in `dealix/observability/otel.py`.
3. Inspect the observability dashboard for the failure.
4. Verify an alert fired to the named owner.
5. Record the detection time from the moment of failure to its appearance.

## Expected result

- Step 2: the failure is captured in the trace with its cause.
- Step 3: the failure is visible and classified on the dashboard.
- Step 4: an alert reaches the owner within the plan-defined time.
- Step 5: the detection time is recorded.

## Pass/fail criteria

- **Pass:** every integration failure is visible on the dashboard and fires an alert within the defined time.
- **Fail:** a silent failure that does not surface on the dashboard, or fires no alert. A failure blocks the merge and caps Layers 6 and 7 at the client-pilot band.

## Related links

- `readiness/observability/readiness.md`
- `platform/integrations/readiness.md`

Estimated value is not Verified value.
