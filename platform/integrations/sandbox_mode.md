# العربية

## وضع Sandbox — الطبقة السادسة

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

قبل أن ينفّذ أي تكامل إجراءً حقيقياً على نظام عميل، يجب أن يكون قابلاً للاختبار في بيئة معزولة. وضع Sandbox يضمن أن كل تكامل يُختبَر دون لمس بيانات حقيقية ودون إرسال أي رسالة فعلية. القاعدة الثابتة: كل تكامل له وضع sandbox قبل ترقيته إلى `pilot` أو `live`.

### مبادئ وضع Sandbox

- **عزل تام:** نداءات sandbox تذهب إلى حسابات اختبار أو محاكيات، لا إلى أنظمة إنتاج العميل.
- **لا إرسال خارجي حقيقي:** في وضع sandbox، إرسال واتساب والبريد يُنتج مسودة فقط — لا رسالة فعلية للعميل.
- **بيانات صناعية:** يستخدم sandbox بيانات اختبار مُولّدة، لا بيانات شخصية حقيقية.
- **نفس المسار:** يمر اختبار sandbox عبر نفس واجهة الموصّلات ونفس قواعد الحوكمة كالإنتاج.

### آلية التبديل بين Sandbox والإنتاج

- إرسال واتساب الحي محكوم براية `whatsapp_allow_live_send` في `core.config.settings`؛ عندما تكون `false`، تُرجِع `send_text` و`send_template` في `integrations/whatsapp.py` `whatsapp_allow_live_send_false` دون أي إرسال.
- البريد في sandbox يُوجَّه إلى نطاق اختبار أو يُكتب كمسودة عبر مزوّد الاختبار.
- التقويم في sandbox يُنشئ مواعيد على تقويم اختبار مخصّص.
- Calend’ly في sandbox يستخدم رموز حساب اختبار.
- حالة كل تكامل (`sandbox_only` / `pilot` / `live`) مسجّلة في `platform/integrations/integration_registry.md`.

### معايير الترقية من Sandbox إلى Pilot

1. اجتياز كل حالات الاختبار في `platform/integrations/tests.md` المتعلقة بالتكامل.
2. إثبات أن كل إرسال خارجي يبقى مسودة حتى موافقة بشرية.
3. إثبات عدم التكرار: إعادة نفس النداء لا تُنتج أثراً مزدوجاً.
4. إثبات أن الفشل يُدفَع إلى DLQ ولا يكسر سير العمل.
5. موافقة موثّقة من مالك المنصة — وتُسجَّل كقيد تدقيق.

### قائمة تحقّق Sandbox لكل تكامل جديد

- [ ] يوجد حساب اختبار أو محاكي معزول.
- [ ] راية تبديل live/sandbox موجودة ومُوثّقة.
- [ ] لا بيانات شخصية حقيقية في مسار sandbox.
- [ ] الإرسال الخارجي في sandbox مسودة فقط.
- [ ] حالة التكامل مسجّلة في سجل التكاملات.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| راية إرسال واتساب الحي | `integrations/whatsapp.py` (`whatsapp_allow_live_send`) |
| إعدادات البيئة | `core.config.settings` |
| حالات التكامل | `platform/integrations/integration_registry.md` |
| حالات الاختبار | `platform/integrations/tests.md` |

---

# English

## Sandbox Mode — Layer 6

**Owner:** Integrations Platform Lead.

### Purpose

Before any integration runs a real action on a customer system, it must be testable in an isolated environment. Sandbox mode ensures every integration is tested without touching real data and without sending any actual message. The fixed rule: every integration has a sandbox mode before promotion to `pilot` or `live`.

### Sandbox principles

- **Full isolation:** sandbox calls go to test accounts or simulators, never to customer production systems.
- **No real external send:** in sandbox mode, WhatsApp and email sends produce a draft only — no actual customer message.
- **Synthetic data:** sandbox uses generated test data, not real personal data.
- **Same path:** a sandbox test runs through the same connector facade and the same governance rules as production.

### Sandbox/production switching

- Live WhatsApp sending is governed by the `whatsapp_allow_live_send` flag in `core.config.settings`; when `false`, `send_text` and `send_template` in `integrations/whatsapp.py` return `whatsapp_allow_live_send_false` with no send.
- Email in sandbox is routed to a test domain or written as a draft via the test provider.
- Calendar in sandbox creates events on a dedicated test calendar.
- Calendly in sandbox uses test account tokens.
- Each integration status (`sandbox_only` / `pilot` / `live`) is recorded in `platform/integrations/integration_registry.md`.

### Promotion criteria from Sandbox to Pilot

1. Pass all test cases in `platform/integrations/tests.md` related to the integration.
2. Prove that every external send stays a draft until human approval.
3. Prove idempotency: replaying the same call produces no double effect.
4. Prove failure is pushed to the DLQ and does not break the workflow.
5. Documented approval from the platform owner — recorded as an audit entry.

### Sandbox checklist for every new integration

- [ ] An isolated test account or simulator exists.
- [ ] A live/sandbox toggle flag exists and is documented.
- [ ] No real personal data in the sandbox path.
- [ ] External send in sandbox is draft-only.
- [ ] Integration status is recorded in the registry.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Live WhatsApp send flag | `integrations/whatsapp.py` (`whatsapp_allow_live_send`) |
| Environment settings | `core.config.settings` |
| Integration statuses | `platform/integrations/integration_registry.md` |
| Test cases | `platform/integrations/tests.md` |
