# العربية

## لوحات المتابعة — الطبقة السابعة

Owner: قائد موثوقية المنصة (Platform Reliability Lead)

### الغرض

لكل خدمة لوحة متابعة. اللوحة هي الصفحة التي يفتحها المناوب أولاً ليرى صحّة الخدمة في لحظة: الزمن، معدّل الأخطاء، الإنتاجية، التكلفة التقديرية. القاعدة: خدمة بلا لوحة هي خدمة عمياء.

### اللوحات المُعرَّفة

تعريفات اللوحات تحت `observability/dashboards/` بصيغة JSON قابلة للاستيراد:

- **`agent_health.json`** — صحّة الوكلاء: معدّل نجاح الوكلاء، زمن P95 لكل وكيل، التكلفة التقديرية لكل وكيل، أنواع الأخطاء الأكثر تكرارًا.
- **`workflow_health.json`** — صحّة أسيرة العمل: عدد عمليات التشغيل، معدّل النجاح لكل سير عمل، الزمن لكل خطوة، أسيرة العمل الفاشلة الأخيرة.
- **`revenue_os.json`** — نظام الإيراد: زمن واجهة الدفع P95، أخطاء webhook الدفع، الإنتاجية، التكلفة التقديرية مقابل النشاط.

### مصادر بيانات اللوحات

| اللوحة | المصدر الفعلي |
|--------|----------------|
| `agent_health.json` | `api/routers/agent_observability.py` — `/recent`، `/cost-summary` |
| `workflow_health.json` | `api/routers/agent_observability.py` و امتدادات `dealix/observability/otel.py` |
| `revenue_os.json` | تتبّع أداء Sentry و `docs/observability/sentry_alerts.yaml` و `cost_tracker.py` |

### قائمة الجاهزية

- [x] لوحة لكل من: الوكلاء، أسيرة العمل، نظام الإيراد.
- [x] كل لوحة تعرض الزمن ومعدّل الأخطاء والتكلفة التقديرية.
- [x] تعريفات اللوحات محفوظة كملفات JSON قابلة للمراجعة.
- [ ] لوحة موحَّدة لصحّة المنصة على مستوى أعلى.
- [ ] مراجعة دورية موثَّقة للوحات مع المناوبين.

### المقاييس

- نسبة الخدمات الحرجة التي لها لوحة: 100% (هدف).
- زمن تحميل اللوحة: أقل من 5 ثوانٍ.
- زمن من فتح اللوحة إلى تحديد المكوّن الفاشل: أقل من دقيقتين.
- تحديث بيانات اللوحة: كل دقيقة على الأكثر.

### خطاطيف المراقبة

- بيانات الوكلاء عبر `api/routers/agent_observability.py`.
- امتدادات الزمن عبر `dealix/observability/otel.py`.
- التكلفة التقديرية عبر `dealix/observability/cost_tracker.py`.
- إشارات الأخطاء عبر `dealix/observability/sentry.py`.

### قواعد الحوكمة

- لا تعرض اللوحات PII؛ تُستخدم `tenant_id` و `customer_handle` فقط.
- كل رقم تكلفة على اللوحة موسوم "تقديري".
- تغيير تعريف لوحة يُحفظ في التحكّم بالإصدارات ويُراجَع.
- لوحات الإيراد لا تعرض مقاييس سرّية للعملاء؛ أنماط مجمَّعة فقط.

### إجراء التراجع

1. إن عرضت لوحة بيانات خاطئة، استرجع نسخة JSON السابقة من التحكّم بالإصدارات.
2. استبعد أي لوحة من مصدر بيانات معطوب حتى يُصحَّح المصدر.
3. تحقّق بعد الاسترجاع أن المؤشّرات الأساسية تظهر بشكل صحيح.
4. سجّل التراجع كقيد تدقيق وأبلغ قائد موثوقية المنصة.

### درجة الجاهزية الحالية

**الدرجة: 73 / 100 — بيتا داخلي (Internal Beta).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Dashboards — Layer 7

Owner: Platform Reliability Lead

### Purpose

Every service has a dashboard. The dashboard is the first page an on-call engineer opens to see a service's health at a glance: latency, error rate, throughput, estimated cost. The rule: a service without a dashboard is a blind service.

### Defined dashboards

Dashboard definitions live under `observability/dashboards/` as importable JSON:

- **`agent_health.json`** — agent health: agent success rate, P95 latency per agent, estimated cost per agent, most frequent error types.
- **`workflow_health.json`** — workflow health: run count, success rate per workflow, latency per step, recent failed workflows.
- **`revenue_os.json`** — revenue OS: checkout P95 latency, payment webhook errors, throughput, estimated cost against activity.

### Dashboard data sources

| Dashboard | Real source |
|-----------|-------------|
| `agent_health.json` | `api/routers/agent_observability.py` — `/recent`, `/cost-summary` |
| `workflow_health.json` | `api/routers/agent_observability.py` and spans from `dealix/observability/otel.py` |
| `revenue_os.json` | Sentry performance tracing, `docs/observability/sentry_alerts.yaml`, and `cost_tracker.py` |

### Readiness checklist

- [x] A dashboard for each of: agents, workflows, revenue OS.
- [x] Each dashboard shows latency, error rate, and estimated cost.
- [x] Dashboard definitions stored as reviewable JSON files.
- [ ] A unified higher-level platform health dashboard.
- [ ] Documented periodic dashboard review with on-call engineers.

### Metrics

- Critical services with a dashboard: 100% (target).
- Dashboard load time: under 5 seconds.
- Time from opening the dashboard to identifying the failed component: under 2 minutes.
- Dashboard data refresh: at most every minute.

### Observability hooks

- Agent data via `api/routers/agent_observability.py`.
- Latency spans via `dealix/observability/otel.py`.
- Estimated cost via `dealix/observability/cost_tracker.py`.
- Error signals via `dealix/observability/sentry.py`.

### Governance rules

- Dashboards display no PII; only `tenant_id` and `customer_handle` are used.
- Every cost number on a dashboard is labeled "estimated".
- A dashboard definition change is kept in version control and reviewed.
- Revenue dashboards do not display confidential customer metrics; aggregated patterns only.

### Rollback procedure

1. If a dashboard shows wrong data, revert to the previous JSON version from version control.
2. Exclude any dashboard fed by a broken data source until the source is fixed.
3. After rollback, verify the core indicators render correctly.
4. Record the rollback as an audit entry and notify the Platform Reliability Lead.

### Current readiness score

**Score: 73 / 100 — Internal Beta.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
