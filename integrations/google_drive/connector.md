# العربية

## موصّل Google Drive — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل Google Drive يربط Dealix بمساحة ملفات العميل على Drive لقراءة وكتابة المستندات (مثل المقترحات والتقارير). حالته الحالية **نموذج أولي** — قيد التطوير، لا يُستخدَم مع بيانات عميل حقيقية. القاعدة الثابتة: لا حذف ملفات، ولا مشاركة عامة دون موافقة.

### النطاق

- **مخطّط له (بعد الترقية):** قراءة ملفات من مجلد محدّد، رفع/تحديث مستندات يولّدها Dealix، قراءة بيانات وصفية.
- **غير مدعوم:** حذف الملفات، تغيير صلاحيات المشاركة لتصبح عامة، الوصول خارج المجلد المصرّح به.

### التنفيذ

- يُستخدَم Google Drive عبر محوّل مزوّد يمر بواجهة الموصّلات الموحّدة في `dealix/connectors/connector_facade.py`.
- لا سياسة صريحة للموصّل `google_drive` في `DEFAULT_POLICIES`؛ يأخذ الافتراضية حتى تُضاف سياسة مخصّصة.

### المصادقة والنطاقات

- المصادقة عبر OAuth 2.0 أو حساب خدمة، بنفس نمط Google Calendar في `integrations/calendar.py`.
- نطاق Drive يُقيَّد إلى الحد الأدنى: `drive.file` (وصول للملفات التي ينشئها Dealix فقط) بدل `drive` الكامل حيثما أمكن.
- بيانات الاعتماد تُقرأ كقيم سرّية ولا تُطبع في أي سجل.

### الموثوقية والحوكمة

- العمليات قابلة للإعادة عبر مفتاح عدم التكرار من واجهة الموصّلات؛ رفع نفس الملف بنفس المفتاح لا يُنشئ نسخة مزدوجة.
- الفشل النهائي يُدفَع إلى DLQ ولا يكسر سير العمل.
- لا يُكشَط محتوى Drive — يُقرأ فقط ما صرّح به العميل ضمن المجلد المحدّد.
- أي مشاركة ملف خارج المؤسسة إجراء يمر عبر `external_action_requires_approval`.

### معايير الترقية إلى Pilot

1. سياسة صريحة لـ `google_drive` في `DEFAULT_POLICIES`.
2. نطاق `drive.file` بالحد الأدنى من الصلاحيات.
3. وضع sandbox مُثبَت بمجلد Drive اختبار.
4. اجتياز حالات الاختبار ذات الصلة في `platform/integrations/tests.md`.
5. موافقة موثّقة من مالك المنصة.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| واجهة الموصّلات | `dealix/connectors/connector_facade.py` |
| نمط مصادقة Google | `integrations/calendar.py` |
| سجل التكاملات | `platform/integrations/integration_registry.md` |
| تدفّقات المصادقة | `platform/integrations/auth_flows.md` |

---

# English

## Google Drive Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The Google Drive connector links Dealix to a customer's Drive file space to read and write documents (such as proposals and reports). Its current status is **prototype** — under development, not used with real customer data. The fixed rule: no file deletion, and no public sharing without approval.

### Scope

- **Planned (after promotion):** read files from a specified folder, upload/update documents Dealix generates, read metadata.
- **Not supported:** deleting files, changing share permissions to public, accessing outside the authorized folder.

### Implementation

- Google Drive is used via a provider adapter that passes through the unified connector facade in `dealix/connectors/connector_facade.py`.
- There is no explicit policy for the `google_drive` connector in `DEFAULT_POLICIES`; it takes the default until a custom policy is added.

### Authentication and scopes

- Authentication is via OAuth 2.0 or a service account, in the same pattern as Google Calendar in `integrations/calendar.py`.
- The Drive scope is restricted to the minimum: `drive.file` (access only to files Dealix creates) rather than full `drive` wherever possible.
- Credentials are read as secret values and never printed to any log.

### Reliability and governance

- Operations are idempotent via the idempotency key from the connector facade; uploading the same file with the same key creates no duplicate copy.
- Final failure is pushed to the DLQ and does not break the workflow.
- Drive content is not scraped — only what the customer authorized within the specified folder is read.
- Any file sharing outside the organization is an action that passes `external_action_requires_approval`.

### Promotion criteria to Pilot

1. An explicit `google_drive` policy in `DEFAULT_POLICIES`.
2. The minimum-privilege `drive.file` scope.
3. A sandbox mode proven with a test Drive folder.
4. Passing the relevant test cases in `platform/integrations/tests.md`.
5. Documented approval from the platform owner.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Connector facade | `dealix/connectors/connector_facade.py` |
| Google authentication pattern | `integrations/calendar.py` |
| Integration registry | `platform/integrations/integration_registry.md` |
| Authentication flows | `platform/integrations/auth_flows.md` |
