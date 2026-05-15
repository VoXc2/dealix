# العربية

## جاهزية الطبقة السادسة — التنفيذ والتكاملات

**Owner:** مالك منصة التكاملات (Integrations Platform Lead) — قسم هندسة المنصة.

### 1. الغرض

تقيس هذه الوثيقة جاهزية الطبقة 6: قدرة Dealix على الاتصال بأنظمة العميل وتشغيل إجراءات حقيقية بأمان — CRM، واتساب، البريد، التقويم، Google Drive، Sheets، Slack/Teams، التذاكر، خطافات الويب — دون كسر سير العمل ودون تجاوز الحوكمة.

### 2. قائمة الجاهزية

- [x] لكل تكامل وضع sandbox معزول قبل الترقية إلى pilot.
- [x] كل إجراء قابل للإعادة (idempotent) عبر `dealix/reliability/idempotency.py`.
- [x] فشل أي تكامل لا يكسر سير العمل — يُدفَع إلى DLQ في `dealix/reliability/dlq.py`.
- [x] الرموز والمفاتيح مشفّرة وتُقرأ كقيم سرّية عبر `core.config.settings`.
- [x] خطافات الويب موقّعة ويُتحقَّق منها (`verify_signature` في `integrations/whatsapp.py`).
- [x] لكل تكامل حد معدّل صريح في `DEFAULT_POLICIES`.
- [x] كل إرسال خارجي يواجه العميل مسودة + موافقة بشرية أولاً.
- [x] قاطع دائرة لكل موصّل (`BreakerState`).
- [ ] لوحة صحة التكاملات تعرض كل فشل تكامل بصورة آنية كاملة.
- [ ] تتبّع 99% من الإجراءات مُثبَت بقياس مستقل.
- [ ] اختبار تدوير المفاتيح الربعي موثّق بجدول دوري.

### 3. المقاييس

- نسبة الإجراءات القابلة للتتبّع: الهدف ≥ 99%.
- نسبة نجاح الإجراءات بعد إعادة المحاولة.
- عمق DLQ لكل طابور (`outbound`, `webhooks`, `crm_sync`, `enrichment`).
- عدد المرات التي فُتح فيها قاطع كل موصّل.
- زمن الاستجابة الوسيط لكل موصّل (`duration_ms`).
- نسبة الخطافات المرفوضة لفشل التوقيع.

### 4. خطافات المراقبة

- قيد تدقيق لكل نداء في جدول `connector_audit` (`_persist` في `connector_facade.py`).
- `audit_tail()` يعرض آخر النداءات للوحة الصحة.
- `DLQ.stats()` و`DLQ.depth()` يغذيان مؤشرات الطوابير الفاشلة.
- سجلات منظّمة: `connector_retry`, `circuit_open`, `dlq_push`.
- تنبيه عند بقاء قاطع مفتوحاً أو عمق DLQ متزايد.

### 5. قواعد الحوكمة

- كل إجراء `external_send` يمر عبر `external_action_requires_approval.yaml`.
- واتساب البارد ممنوع عبر `no_cold_whatsapp.yaml`.
- لا كشط (`no_scraping`) ولا أتمتة LinkedIn (`no_linkedin_automation`).
- لا أرقام مبيعات مضمونة ولا إثبات مزيّف في أي محتوى تكامل.
- الأسرار لا تُكتب في السجلات أو سجل التدقيق.
- تغيير حالة تكامل أو إبطال مفتاح إجراء A2 مُسجَّل.

### 6. إجراء التراجع

1. ضبط `ConnectorPolicy.allow = false` للموصّل المتأثّر — يوقف كل نداءاته فوراً.
2. أو ضبط راية البيئة (مثل `whatsapp_allow_live_send=false`) لإيقاف الإرسال الحي.
3. الأحداث الواردة المعلّقة تبقى آمنة في `WEBHOOKS_DLQ` لإعادة التشغيل لاحقاً.
4. تخفيض حالة التكامل إلى `sandbox_only` في سجل التكاملات.
5. بعد الإصلاح: إعادة تشغيل DLQ يدوياً — عدم التكرار يضمن أمان الإعادة.
6. تسجيل التراجع كقيد تدقيق وإخطار المالك.

### 7. درجة الجاهزية الحالية

**الدرجة: 79 / 100 — نطاق "تجريبي مع عميل" (client pilot).**

مقياس النطاقات: 0–59 نموذج أولي / 60–74 تجريبي داخلي / 75–84 تجريبي مع عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

البنود المتبقّية التي تحدّ من الدرجة: لوحة صحة التكاملات الآنية الكاملة، إثبات تتبّع 99% بقياس مستقل، وجدول تدوير المفاتيح الدوري الموثّق.

---

# English

## Layer 6 Readiness — Execution and Integrations

**Owner:** Integrations Platform Lead — Platform Engineering.

### 1. Purpose

This document measures Layer 6 readiness: Dealix's ability to connect to customer systems and run real actions safely — CRM, WhatsApp, email, calendar, Google Drive, Sheets, Slack/Teams, ticketing, webhooks — without breaking workflows and without bypassing governance.

### 2. Readiness checklist

- [x] Every integration has an isolated sandbox before promotion to pilot.
- [x] Every action is idempotent via `dealix/reliability/idempotency.py`.
- [x] Any integration failure does not break the workflow — it is pushed to the DLQ in `dealix/reliability/dlq.py`.
- [x] Tokens and keys are encrypted and read as secret values via `core.config.settings`.
- [x] Webhooks are signed and verified (`verify_signature` in `integrations/whatsapp.py`).
- [x] Every integration has an explicit rate limit in `DEFAULT_POLICIES`.
- [x] Every customer-facing external send is draft + human approval first.
- [x] A circuit breaker exists per connector (`BreakerState`).
- [ ] An integration health dashboard surfaces every integration failure fully in real time.
- [ ] 99% of actions traceable is proven by an independent measurement.
- [ ] A quarterly key rotation drill is documented on a periodic schedule.

### 3. Metrics

- Share of traceable actions: target >= 99%.
- Action success rate after retry.
- DLQ depth per queue (`outbound`, `webhooks`, `crm_sync`, `enrichment`).
- Number of times each connector breaker opened.
- Median latency per connector (`duration_ms`).
- Share of webhooks rejected for signature failure.

### 4. Observability hooks

- An audit entry per call in the `connector_audit` table (`_persist` in `connector_facade.py`).
- `audit_tail()` exposes recent calls for the health dashboard.
- `DLQ.stats()` and `DLQ.depth()` feed failed-queue indicators.
- Structured logs: `connector_retry`, `circuit_open`, `dlq_push`.
- Alert when a breaker stays open or DLQ depth grows.

### 5. Governance rules

- Every `external_send` action passes `external_action_requires_approval.yaml`.
- Cold WhatsApp is blocked via `no_cold_whatsapp.yaml`.
- No scraping (`no_scraping`) and no LinkedIn automation (`no_linkedin_automation`).
- No guaranteed sales numbers and no fake proof in any integration content.
- Secrets are never written to logs or the audit log.
- Changing an integration status or revoking a key is a recorded A2-class action.

### 6. Rollback procedure

1. Set `ConnectorPolicy.allow = false` for the affected connector — halts all its calls immediately.
2. Or set an environment flag (e.g. `whatsapp_allow_live_send=false`) to stop live sending.
3. Pending inbound events stay safe in `WEBHOOKS_DLQ` for later replay.
4. Downgrade the integration status to `sandbox_only` in the registry.
5. After the fix: replay the DLQ manually — idempotency keeps replay safe.
6. Record the rollback as an audit entry and notify the owner.

### 7. Current readiness score

**Score: 79 / 100 — "client pilot" band.**

Band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

Remaining items capping the score: a full real-time integration health dashboard, an independent proof of 99% traceability, and a documented periodic key rotation schedule.
