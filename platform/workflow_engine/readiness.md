# العربية

## جاهزية محرّك سير العمل — الطبقة الثالثة

Owner: مالك محرّك سير العمل (Workflow Engine Platform Lead)

### قائمة الجاهزية

- [x] كل عملية متكررة معرّفة كملف سير عمل معلن في `data/workflows/` أو `workflows/`.
- [x] كل سير عمل يعمل من المحفّز إلى المخرج النهائي عبر `dealix/execution/`.
- [x] الخطوة الفاشلة لها إعادة محاولة عبر `dealix/reliability/retry.py` أو مسار بديل.
- [x] الفشل النهائي يُدفع إلى DLQ عبر `dealix/reliability/dlq.py`.
- [x] كل خطوة مرئية في سجلات سير العمل مع طابع زمني ومالك.
- [x] كل سير عمل يحمل مفتاح `version` وكل تشغيل يثبّت إصداره.
- [x] كل خطوة تواصل خارجي مسبوقة بخطوة موافقة بشرية.
- [x] كل سير عمل له `owner` و`sla` ومقياس أعمال واحد على الأقل.
- [x] منع التكرار على المحفّزات الحدثية عبر `dealix/reliability/idempotency.py`.
- [ ] تمرين استرجاع DLQ كامل موثَّق ربع سنوياً (إجراء قائم، يحتاج توثيق دوري).
- [ ] لوحة مقاييس موحَّدة لكل سير عمل في الإنتاج (قيد الإنشاء).

### المقاييس

- `completion_rate` في السيناريو العادي: أعلى من 95% (هدف).
- زمن دورة سير العمل (`cycle_time_hours`): ضمن SLA المعلن لكل سير عمل.
- نسبة الخطوات المرئية في السجل: 100%.
- نسبة سير العمل الحامل لـ `owner` و`sla` ومقياس أعمال: 100%.
- عمق DLQ: مراجعة يومية، صفر بنود غير معالَجة أقدم من 24 ساعة (هدف).
- زمن التراجع عن إصدار سير عمل: أقل من 15 دقيقة.

### خطاطيف المراقبة

- تتبّع كل تشغيل عبر `dealix/observability/otel.py`.
- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- تتبّع التكلفة لكل تشغيل عبر `dealix/observability/cost_tracker.py`.
- قيود التدقيق عبر `dealix/trust/audit.py`.
- مقاييس سير العمل عبر `auto_client_acquisition/workflow_os/workflow_metrics.py`.
- تنبيه عند انخفاض `completion_rate` أو تجاوز عمق DLQ.

### قواعد الحوكمة

- أي خطوة تواصل خارجي تمر عبر خطوة موافقة بشرية؛ المحرّك يرفض تحميل سير عمل يخالف ذلك.
- لا إرسال واتساب بارد، لا أتمتة LinkedIn، لا كشط بيانات ضمن أي خطوة.
- لا تنفيذ تواصل خارجي نيابة عن العميل دون موافقته الصريحة.
- ترقية MAJOR لسير عمل تتطلب موافقة موثَّقة من مالك الطبقة.
- بيانات التعريف الشخصية تُنقَّح من السجلات عبر `redaction.py`.
- لا ادعاءات مبيعات مضمونة؛ المقاييس تقديرية وتُوصَف كأنماط آمنة الحالة.

### إجراء التراجع

1. تحديد الإصدار المستقر السابق لسير العمل من سجل git.
2. إعادة الإصدار السابق وتوجيه التشغيلات الجديدة إليه.
3. ترك التشغيلات الجارية تكمل على إصدارها المثبَّت.
4. عند فساد حالة جزئية: تشغيل خطوات التعويض المعرّفة.
5. مراجعة عمق DLQ وإعادة معالجة البنود المتأثرة عبر `drain()`.
6. تسجيل التراجع كقيد تدقيق وإبلاغ مالك الطبقة.

### درجة الجاهزية الحالية

**الدرجة: 79 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

## Workflow Engine Readiness — Layer 3

Owner: Workflow Engine Platform Lead

### Readiness checklist

- [x] Every repeated operation is defined as a declared workflow file in `data/workflows/` or `workflows/`.
- [x] Every workflow runs from trigger to final output via `dealix/execution/`.
- [x] A failed step has a retry via `dealix/reliability/retry.py` or a fallback path.
- [x] Final failure is pushed to the DLQ via `dealix/reliability/dlq.py`.
- [x] Every step is visible in the workflow logs with a timestamp and an owner.
- [x] Every workflow carries a `version` key and every run pins its version.
- [x] Every external communication step is preceded by a human-approval step.
- [x] Every workflow has an `owner`, an `sla`, and at least one business metric.
- [x] Event triggers are deduplicated via `dealix/reliability/idempotency.py`.
- [ ] Full DLQ replay drill documented quarterly (procedure exists, needs periodic documentation).
- [ ] Unified metrics dashboard for every production workflow (in progress).

### Metrics

- `completion_rate` in a normal scenario: above 95% (target).
- Workflow cycle time (`cycle_time_hours`): within the SLA declared per workflow.
- Share of steps visible in the log: 100%.
- Share of workflows carrying `owner`, `sla`, and a business metric: 100%.
- DLQ depth: reviewed daily, zero unprocessed items older than 24 hours (target).
- Workflow version rollback time: under 15 minutes.

### Observability hooks

- Every run traced via `dealix/observability/otel.py`.
- Error capture via `dealix/observability/sentry.py`.
- Per-run cost tracking via `dealix/observability/cost_tracker.py`.
- Audit entries via `dealix/trust/audit.py`.
- Workflow metrics via `auto_client_acquisition/workflow_os/workflow_metrics.py`.
- Alert on `completion_rate` drop or DLQ depth breach.

### Governance rules

- Any external communication step passes through a human-approval step; the engine refuses to load a workflow that violates this.
- No cold WhatsApp, no LinkedIn automation, no data scraping within any step.
- No external communication on a customer's behalf without their explicit consent.
- A MAJOR upgrade of a workflow requires a documented approval from the layer owner.
- Personally identifiable information is redacted from logs via `redaction.py`.
- No guaranteed sales claims; metrics are estimated and described as case-safe patterns.

### Rollback procedure

1. Identify the previous stable workflow version from the git history.
2. Restore the previous version and route new runs to it.
3. Let in-flight runs complete on their pinned version.
4. On corrupted partial state: run the defined compensation steps.
5. Review DLQ depth and reprocess affected items via `drain()`.
6. Record the rollback as an audit entry and notify the layer owner.

### Current readiness score

**Score: 79 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
