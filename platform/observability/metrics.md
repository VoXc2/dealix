# العربية

## المقاييس و SLO — الطبقة السابعة

Owner: قائد موثوقية المنصة (Platform Reliability Lead)

### الغرض

المقاييس أرقام مجمَّعة عبر الزمن: زمن الاستجابة، معدّل الأخطاء، استهلاك الرموز، التكلفة التقديرية. الأثر يخبرنا عن طلب واحد؛ المقياس يخبرنا عن اتجاه الخدمة. على المقاييس تُبنى أهداف مستوى الخدمة (SLO) والتنبيهات.

### مجموعات المقاييس

- **زمن الاستجابة (Latency):** زمن كل واجهة برمجية، وكل وكيل، وكل أداة، وكل نداء نموذج. يُسجَّل `latency_ms` في `CostEntry` و `ObservabilityEvent`.
- **معدّل الأخطاء (Error rate):** نسبة الاستدعاءات بحالة `error` إلى الإجمالي، مفصَّلة حسب الوكيل وسير العمل.
- **استهلاك الرموز (Tokens):** رموز الإدخال والإخراج والمخزَّنة لكل نموذج، عبر `cost_tracker.py`.
- **التكلفة التقديرية (Cost):** تُحسب عبر `estimate_cost_usd` بأسعار `MODEL_PRICES`. كل أرقام التكلفة تقديرية لا مؤكَّدة.
- **الإنتاجية (Throughput):** عدد الطلبات وأسيرة العمل في النافذة الزمنية.

### مصادر المقاييس الفعلية

| المقياس | المصدر |
|---------|--------|
| تكلفة ورموز النماذج | `dealix/observability/cost_tracker.py` — جدول `llm_calls` و `totals()` |
| زمن وحالة الوكلاء | `api/routers/agent_observability.py` — `/recent` و `/cost-summary` |
| ملخّص التكلفة لكل وكيل وسير عمل | `api/routers/agent_observability.py` — `cost_summary()` |
| زمن الواجهات وأداؤها | تتبّع أداء Sentry عبر `dealix/observability/sentry.py` |
| امتدادات الزمن لكل خطوة | `dealix/observability/otel.py` |

### أهداف مستوى الخدمة (SLO) — مبدئية

| الخدمة | المؤشّر | الهدف |
|--------|---------|-------|
| واجهات الـ API | توافر | 99.5% شهريًا |
| الدفع | P95 لزمن الاستجابة | أقل من 1500 مللي ثانية |
| سير عمل الوكلاء | معدّل النجاح | 95% من عمليات التشغيل |
| نداء النموذج اللغوي | P95 لزمن الاستجابة | أقل من 8000 مللي ثانية |

هذه الأهداف مبدئية وتُراجَع ربع سنويًا بالبيانات الفعلية. ليست وعودًا تعاقدية.

### قائمة الجاهزية

- [x] زمن كل خطوة مُسجَّل عبر `latency_ms`.
- [x] استهلاك الرموز والتكلفة التقديرية مُسجَّل لكل نداء نموذج.
- [x] ملخّص التكلفة متاح لكل وكيل وسير عمل.
- [x] أسعار النماذج موثَّقة في `MODEL_PRICES` مع تاريخ آخر تحديث.
- [ ] أهداف SLO مُراجَعة ومُعتمَدة بالبيانات الفعلية.
- [ ] لوحة ميزانية الأخطاء (error budget) مُفعَّلة.

### المقاييس

- نسبة نداءات النماذج التي تحمل تكلفة تقديرية: 100%.
- دقّة تقدير التكلفة: أسعار تُحدَّث ربع سنويًا على الأقل.
- زمن حساب ملخّص التكلفة: أقل من ثانية للنافذة الافتراضية.
- نسبة الخطوات الحاملة لـ `latency_ms`: 100% (هدف).

### خطاطيف المراقبة

- تتبّع التكلفة عبر `dealix/observability/cost_tracker.py`.
- ملخّص الوكلاء عبر `api/routers/agent_observability.py`.
- امتدادات الزمن عبر `dealix/observability/otel.py`.
- تنبيهات الزمن ومعدّل الأخطاء عبر `observability/alerts/`.

### قواعد الحوكمة

- كل رقم تكلفة يُعرض موسومًا "تقديري" (`is_estimate: true`)، لا يُقدَّم كرقم مؤكَّد.
- النماذج المجهولة تُسعَّر بأسعار النموذج الأغلى تحفّظًا حتى لا نُقلِّل تقدير الإنفاق.
- لا تُربط المقاييس بمعرّفات عملاء حقيقية؛ تُستخدم `tenant_id` و `customer_handle`.
- تعديل أهداف SLO يتطلب موافقة موثَّقة من قائد موثوقية المنصة.

### إجراء التراجع

1. إن أعطى مصدر مقياس أرقامًا خاطئة، استبعد المصدر من اللوحات ريثما يُصحَّح.
2. عند تغيّر أسعار النماذج، حدّث `MODEL_PRICES` وأعد احتساب النوافذ المتأثرة.
3. استرجع تعريف SLO السابق إن سبّب الجديد تنبيهات كاذبة.
4. سجّل التراجع كقيد تدقيق وأبلغ قائد موثوقية المنصة.

### درجة الجاهزية الحالية

**الدرجة: 77 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

# English

## Metrics and SLOs — Layer 7

Owner: Platform Reliability Lead

### Purpose

Metrics are numbers aggregated over time: latency, error rate, token usage, estimated cost. A trace tells us about one request; a metric tells us about the trend of a service. Service Level Objectives (SLOs) and alerts are built on metrics.

### Metric groups

- **Latency:** the time of each API, agent, tool, and model call. `latency_ms` is recorded in `CostEntry` and `ObservabilityEvent`.
- **Error rate:** the ratio of `error`-status calls to the total, broken down by agent and workflow.
- **Tokens:** input, output, and cached tokens per model, via `cost_tracker.py`.
- **Estimated cost:** computed via `estimate_cost_usd` using `MODEL_PRICES` rates. All cost figures are estimated, not verified.
- **Throughput:** count of requests and workflows in the time window.

### Real metric sources

| Metric | Source |
|--------|--------|
| Model cost and tokens | `dealix/observability/cost_tracker.py` — `llm_calls` table and `totals()` |
| Agent latency and status | `api/routers/agent_observability.py` — `/recent` and `/cost-summary` |
| Cost summary per agent and workflow | `api/routers/agent_observability.py` — `cost_summary()` |
| API latency and performance | Sentry performance tracing via `dealix/observability/sentry.py` |
| Per-step latency spans | `dealix/observability/otel.py` |

### Service Level Objectives (SLOs) — provisional

| Service | Indicator | Target |
|---------|-----------|--------|
| API endpoints | Availability | 99.5% monthly |
| Checkout | P95 latency | under 1500 ms |
| Agent workflows | Success rate | 95% of runs |
| LLM call | P95 latency | under 8000 ms |

These targets are provisional and reviewed quarterly against real data. They are not contractual promises.

### Readiness checklist

- [x] Each step's latency is recorded via `latency_ms`.
- [x] Token usage and estimated cost recorded per model call.
- [x] Cost summary available per agent and workflow.
- [x] Model prices documented in `MODEL_PRICES` with a last-updated date.
- [ ] SLO targets reviewed and approved against real data.
- [ ] Error budget dashboard enabled.

### Metrics

- Model calls carrying an estimated cost: 100%.
- Cost estimation accuracy: prices refreshed at least quarterly.
- Cost summary computation time: under one second for the default window.
- Steps carrying `latency_ms`: 100% (target).

### Observability hooks

- Cost tracking via `dealix/observability/cost_tracker.py`.
- Agent summary via `api/routers/agent_observability.py`.
- Latency spans via `dealix/observability/otel.py`.
- Latency and error-rate alerts via `observability/alerts/`.

### Governance rules

- Every cost figure is shown labeled "estimated" (`is_estimate: true`), never presented as a verified number.
- Unknown models are priced at the most expensive model rate conservatively so spend is never under-reported.
- Metrics are not linked to real customer identifiers; `tenant_id` and `customer_handle` are used.
- Changing SLO targets requires a documented approval from the Platform Reliability Lead.

### Rollback procedure

1. If a metric source produces wrong numbers, exclude the source from dashboards until corrected.
2. When model prices change, update `MODEL_PRICES` and recompute the affected windows.
3. Revert to the previous SLO definition if a new one causes false alerts.
4. Record the rollback as an audit entry and notify the Platform Reliability Lead.

### Current readiness score

**Score: 77 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
