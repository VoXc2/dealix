# العربية

## الاستجابة للحوادث — الطبقة السابعة

Owner: قائد موثوقية المنصة (Platform Reliability Lead)

### الغرض

عند إطلاق تنبيه أو رصد فشل، الاستجابة للحوادث هي العملية المنظَّمة التي تعيد الخدمة وتسجّل ما جرى. القاعدة: كل حادث له مسؤول واحد وحالة واضحة، ولا يُغلق دون تسجيل.

### دورة حياة الحادث

1. **الرصد:** تنبيه أو بلاغ يُنشئ حادثًا.
2. **التصنيف:** تُحدَّد درجة الخطورة (SEV-1 / SEV-2 / SEV-3) ويُعيَّن مسؤول واحد.
3. **الاحتواء:** خطوة لإيقاف الضرر — تراجع، أو تعطيل ميزة، أو تحويل حركة.
4. **الإصلاح:** المعالجة الجذرية واستعادة الخدمة.
5. **التسجيل:** يُكتب سجل الحادث تحت `observability/incident_logs/`.
6. **المراجعة:** مراجعة لاحقة بلا لوم لتحديد الإجراءات الوقائية.

### قالب سجل الحادث

كل سجل حادث يحمل: المعرّف، التاريخ، درجة الخطورة، المسؤول، الحالة (`open` / `mitigated` / `resolved`)، الأثر، السبب الجذري، الإجراءات التصحيحية، و `trace_id` المرتبط. التفاصيل في `observability/incident_logs/README.md`.

### قائمة الجاهزية

- [x] درجات خطورة معرَّفة (SEV-1 / SEV-2 / SEV-3).
- [x] قالب سجل حادث موثَّق في `observability/incident_logs/`.
- [x] كل حادث له مسؤول واحد وحالة واضحة.
- [x] ربط الحادث بـ `trace_id` للتتبّع من طرف لطرف.
- [ ] دمج صفحة المناوب (on-call) موثَّق ومُختبَر.
- [ ] مراجعة لاحقة للحوادث موثَّقة بشكل منتظم.

### المقاييس

- زمن الإقرار بحادث SEV-1: أقل من 15 دقيقة.
- زمن احتواء حادث SEV-1: أقل من 60 دقيقة.
- نسبة الحوادث الموثَّقة بسجل: 100%.
- نسبة الحوادث ذات مراجعة لاحقة: 100% لـ SEV-1.

### خطاطيف المراقبة

- تنبيهات تُنشئ الحوادث عبر `docs/observability/sentry_alerts.yaml` و `observability/alerts/`.
- ربط الحادث بالأثر عبر `trace_id` من `dealix/observability/otel.py`.
- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- سجلات الحوادث تحت `observability/incident_logs/`.

### قواعد الحوكمة

- لا يحتوي سجل الحادث على PII؛ يُشار إلى `request_id` و `trace_id` و `tenant_id` فقط.
- كل حادث SEV-1 يتطلب مراجعة لاحقة بلا لوم موثَّقة.
- لا يُغلق حادث دون سبب جذري مكتوب وإجراءات تصحيحية.
- الاحتواء عبر التراجع يتبع إجراء التراجع الموثَّق لكل خدمة.

### إجراء التراجع

1. حدِّد الإصدار المستقر السابق للخدمة المتأثرة.
2. نفّذ التراجع وفق إجراء التراجع الموثَّق لتلك الخدمة.
3. تحقّق من صحّة الخدمة عبر اللوحة ذات الصلة وتنبيهاتها.
4. حدّث حالة الحادث إلى `mitigated` ثم `resolved` بعد التأكد.
5. سجّل التراجع داخل سجل الحادث وأبلغ قائد موثوقية المنصة.

### درجة الجاهزية الحالية

**الدرجة: 72 / 100 — بيتا داخلي (Internal Beta).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Incident Response — Layer 7

Owner: Platform Reliability Lead

### Purpose

When an alert fires or a failure is observed, incident response is the structured process that restores the service and records what happened. The rule: every incident has a single owner and a clear status, and is never closed without a record.

### Incident lifecycle

1. **Detection:** an alert or report creates an incident.
2. **Triage:** severity is set (SEV-1 / SEV-2 / SEV-3) and a single owner is assigned.
3. **Containment:** a step to stop the damage — rollback, feature disable, or traffic shift.
4. **Remediation:** root-cause fix and service restoration.
5. **Recording:** an incident log is written under `observability/incident_logs/`.
6. **Review:** a blameless post-incident review to define preventive actions.

### Incident log template

Every incident log carries: ID, date, severity, owner, status (`open` / `mitigated` / `resolved`), impact, root cause, corrective actions, and the linked `trace_id`. Details in `observability/incident_logs/README.md`.

### Readiness checklist

- [x] Severity levels defined (SEV-1 / SEV-2 / SEV-3).
- [x] Incident log template documented in `observability/incident_logs/`.
- [x] Every incident has a single owner and a clear status.
- [x] Incident linked to a `trace_id` for end-to-end tracing.
- [ ] On-call paging integration documented and tested.
- [ ] Post-incident reviews documented on a regular cadence.

### Metrics

- SEV-1 acknowledgement time: under 15 minutes.
- SEV-1 containment time: under 60 minutes.
- Incidents documented with a log: 100%.
- Incidents with a post-incident review: 100% for SEV-1.

### Observability hooks

- Alerts create incidents via `docs/observability/sentry_alerts.yaml` and `observability/alerts/`.
- Incident-to-trace linkage via `trace_id` from `dealix/observability/otel.py`.
- Error capture via `dealix/observability/sentry.py`.
- Incident logs under `observability/incident_logs/`.

### Governance rules

- An incident log contains no PII; it references only `request_id`, `trace_id`, and `tenant_id`.
- Every SEV-1 incident requires a documented blameless post-incident review.
- An incident is not closed without a written root cause and corrective actions.
- Containment via rollback follows the documented rollback procedure for each service.

### Rollback procedure

1. Identify the previous stable release of the affected service.
2. Execute the rollback per that service's documented rollback procedure.
3. Verify service health via the relevant dashboard and its alerts.
4. Update the incident status to `mitigated`, then `resolved` after confirmation.
5. Record the rollback inside the incident log and notify the Platform Reliability Lead.

### Current readiness score

**Score: 72 / 100 — Internal Beta.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
