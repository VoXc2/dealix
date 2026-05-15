# العربية

## التنبيهات — الطبقة السابعة

Owner: قائد موثوقية المنصة (Platform Reliability Lead)

### الغرض

التنبيه يحوّل إشارة مراقبة إلى إخطار لإنسان. القاعدة: عند فشل ذي معنى، يُطلق تنبيه إلى قناة محدَّدة بمسؤول واضح — لا اعتماد على ملاحظة بشرية عرضية. التنبيه الجيّد قابل للتنفيذ: يقول ماذا فشل، وأين، وما درجة الخطورة.

### مصادر قواعد التنبيه

- `docs/observability/sentry_alerts.yaml` — مصدر الحقيقة لتنبيهات Sentry (أخطاء webhook، طفرات الأخطاء، تراجع P95، حصّة الاستهلاك).
- `observability/alerts/latency_alerts.yaml` — تنبيهات تجاوز زمن الاستجابة لهذه الطبقة.
- `observability/alerts/error_rate_alerts.yaml` — تنبيهات معدّل الأخطاء.
- `observability/alerts/policy_violation_alerts.yaml` — تنبيهات انتهاك السياسات (PII، أسرار، تجاوز موافقة).

### درجات الخطورة

| الدرجة | المعنى | الاستجابة المتوقّعة |
|--------|--------|----------------------|
| SEV-1 | فقدان إيراد أو بيانات أو خرق سياسة | إخطار فوري للمناوب، استجابة خلال 15 دقيقة |
| SEV-2 | تدهور خدمة دون انقطاع كامل | إخطار خلال ساعة عمل |
| SEV-3 | تراجع أداء أو تحذير حصّة | مراجعة في يوم العمل |

### قائمة الجاهزية

- [x] تنبيهات Sentry معرَّفة كملف (`sentry_alerts.yaml`).
- [x] تنبيهات الزمن ومعدّل الأخطاء وانتهاك السياسات معرَّفة في `observability/alerts/`.
- [x] كل تنبيه له قناة ومسؤول ودرجة خطورة.
- [x] تنبيه عند عدم تطابق توقيع webhook الدفع (لا تكرار).
- [ ] تمرين موثَّق للتأكد من إطلاق التنبيهات فعليًا (تمرين game-day).
- [ ] دمج صفحة المناوب (on-call) موثَّق ومُختبَر.

### المقاييس

- زمن من الفشل إلى إطلاق التنبيه: أقل من 5 دقائق.
- نسبة الفشل الحرج (SEV-1) المغطّى بتنبيه: 100% (هدف).
- نسبة التنبيهات الكاذبة: أقل من 10% شهريًا.
- زمن الإقرار بتنبيه SEV-1: أقل من 15 دقيقة.

### خطاطيف المراقبة

- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- قواعد Sentry عبر `docs/observability/sentry_alerts.yaml`.
- قواعد الطبقة عبر `observability/alerts/`.
- بوّابات السياسات الصارمة عبر `_HARD_GATES` في `api/routers/agent_observability.py`.

### قواعد الحوكمة

- لا يحتوي نص التنبيه على PII؛ يُشار إلى `request_id` و `trace_id` فقط.
- تنبيهات انتهاك السياسة (PII، أسرار) دائمًا SEV-1 ولا تُكتم.
- إضافة أو تعطيل تنبيه يتطلب موافقة موثَّقة من قائد موثوقية المنصة.
- لا يُكتم تنبيه دون قيد تدقيق يوضّح السبب والمدّة.

### إجراء التراجع

1. إن أطلق تنبيه ضوضاء كاذبة، ارفع عتبته أو عطّله مؤقتًا بقيد تدقيق.
2. استرجع نسخة `sentry_alerts.yaml` السابقة إن سبّب التغيير فقدان تغطية.
3. تأكّد بعد أي تغيير أن تنبيهات SEV-1 ما زالت فعّالة عبر تمرين تحقّق.
4. سجّل التراجع كقيد تدقيق وأبلغ قائد موثوقية المنصة.

### درجة الجاهزية الحالية

**الدرجة: 75 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Alerting — Layer 7

Owner: Platform Reliability Lead

### Purpose

An alert turns a monitoring signal into a notification for a human. The rule: on a meaningful failure, an alert fires to a defined channel with a clear owner — no reliance on incidental human observation. A good alert is actionable: it says what failed, where, and at what severity.

### Alert rule sources

- `docs/observability/sentry_alerts.yaml` — source of truth for Sentry alerts (webhook errors, error spikes, P95 regression, quota burn).
- `observability/alerts/latency_alerts.yaml` — this layer's latency-breach alerts.
- `observability/alerts/error_rate_alerts.yaml` — error-rate alerts.
- `observability/alerts/policy_violation_alerts.yaml` — policy-violation alerts (PII, secrets, approval bypass).

### Severity levels

| Severity | Meaning | Expected response |
|----------|---------|-------------------|
| SEV-1 | Revenue/data loss or policy breach | Immediate on-call notify, response within 15 minutes |
| SEV-2 | Service degradation without full outage | Notify within one business hour |
| SEV-3 | Performance regression or quota warning | Review within the business day |

### Readiness checklist

- [x] Sentry alerts defined as a file (`sentry_alerts.yaml`).
- [x] Latency, error-rate, and policy-violation alerts defined under `observability/alerts/`.
- [x] Every alert has a channel, an owner, and a severity.
- [x] Alert on payment webhook signature mismatch (no deduplication).
- [ ] Documented drill confirming alerts actually fire (game-day).
- [ ] On-call paging integration documented and tested.

### Metrics

- Time from failure to alert firing: under 5 minutes.
- Critical failures (SEV-1) covered by an alert: 100% (target).
- False-alert rate: under 10% monthly.
- SEV-1 acknowledgement time: under 15 minutes.

### Observability hooks

- Error capture via `dealix/observability/sentry.py`.
- Sentry rules via `docs/observability/sentry_alerts.yaml`.
- Layer rules via `observability/alerts/`.
- Strict policy gates via `_HARD_GATES` in `api/routers/agent_observability.py`.

### Governance rules

- Alert text contains no PII; it references only `request_id` and `trace_id`.
- Policy-violation alerts (PII, secrets) are always SEV-1 and are never muted.
- Adding or disabling an alert requires a documented approval from the Platform Reliability Lead.
- No alert is muted without an audit entry stating the reason and duration.

### Rollback procedure

1. If an alert fires false noise, raise its threshold or disable it temporarily with an audit entry.
2. Revert to the previous `sentry_alerts.yaml` version if a change causes coverage loss.
3. After any change, confirm SEV-1 alerts still fire via a verification drill.
4. Record the rollback as an audit entry and notify the Platform Reliability Lead.

### Current readiness score

**Score: 75 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
