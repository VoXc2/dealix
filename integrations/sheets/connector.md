# العربية

## موصّل Google Sheets — Dealix

**Owner:** مالك منصة التكاملات (Integrations Platform Lead).

### الغرض

موصّل Google Sheets يربط Dealix بجداول العميل لقراءة وكتابة الصفوف (مثل قوائم العملاء المحتملين أو تقارير الحالة). حالته الحالية **نموذج أولي** — قيد التطوير، لا يُستخدَم مع بيانات عميل حقيقية. القاعدة الثابتة: لا كشط، ولا حذف نطاقات بالجملة.

### النطاق

- **مخطّط له (بعد الترقية):** قراءة صفوف من نطاق محدّد، إلحاق صفوف جديدة، تحديث خلايا محدّدة.
- **غير مدعوم:** حذف الأوراق أو النطاقات بالجملة، الوصول إلى جداول خارج الجدول المصرّح به، استيراد بيانات لم يوافق العميل على معالجتها.

### التنفيذ

- يُستخدَم Google Sheets عبر محوّل مزوّد يمر بواجهة الموصّلات الموحّدة في `dealix/connectors/connector_facade.py`.
- لا سياسة صريحة للموصّل `google_sheets` في `DEFAULT_POLICIES`؛ يأخذ الافتراضية حتى تُضاف سياسة مخصّصة.
- Sheets يفرض حدود قراءة/كتابة لكل دقيقة — تُضاف سياسة محافظة عند الترقية.

### المصادقة والنطاقات

- المصادقة عبر OAuth 2.0 أو حساب خدمة، بنفس نمط Google Calendar في `integrations/calendar.py`.
- النطاق يُقيَّد إلى `spreadsheets` للجدول المحدّد فقط.
- بيانات الاعتماد تُقرأ كقيم سرّية ولا تُطبع.

### الموثوقية والحوكمة

- الكتابة قابلة للإعادة عبر مفتاح عدم التكرار؛ إلحاق نفس الصف بنفس المفتاح لا يُنتج صفاً مكرراً.
- الفشل النهائي يُدفَع إلى DLQ ولا يكسر سير العمل.
- لا يُكشَط محتوى الجدول — يُقرأ فقط النطاق المصرّح به.
- البيانات الشخصية في الجداول تخضع لقاعدة `pii_requires_review` قبل أي معالجة لاحقة.
- لا تُكتب محتويات الخلايا في قيد التدقيق — يُسجَّل المعرّف والنتيجة فقط.

### معايير الترقية إلى Pilot

1. سياسة صريحة محافظة لـ `google_sheets` في `DEFAULT_POLICIES`.
2. نطاق `spreadsheets` بالحد الأدنى من الصلاحيات.
3. وضع sandbox مُثبَت بجدول اختبار.
4. اجتياز حالات الاختبار ذات الصلة في `platform/integrations/tests.md`.
5. موافقة موثّقة من مالك المنصة.

### الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي |
|---|---|
| واجهة الموصّلات | `dealix/connectors/connector_facade.py` |
| نمط مصادقة Google | `integrations/calendar.py` |
| مراجعة البيانات الشخصية | `auto_client_acquisition/governance_os/rules/pii_requires_review.py` |
| سجل التكاملات | `platform/integrations/integration_registry.md` |

---

# English

## Google Sheets Connector — Dealix

**Owner:** Integrations Platform Lead.

### Purpose

The Google Sheets connector links Dealix to a customer's spreadsheets to read and write rows (such as lead lists or status reports). Its current status is **prototype** — under development, not used with real customer data. The fixed rule: no scraping, and no bulk range deletion.

### Scope

- **Planned (after promotion):** read rows from a specified range, append new rows, update specific cells.
- **Not supported:** bulk deletion of sheets or ranges, accessing spreadsheets outside the authorized one, importing data the customer did not consent to process.

### Implementation

- Google Sheets is used via a provider adapter that passes through the unified connector facade in `dealix/connectors/connector_facade.py`.
- There is no explicit policy for the `google_sheets` connector in `DEFAULT_POLICIES`; it takes the default until a custom policy is added.
- Sheets enforces per-minute read/write limits — a conservative policy is added on promotion.

### Authentication and scopes

- Authentication is via OAuth 2.0 or a service account, in the same pattern as Google Calendar in `integrations/calendar.py`.
- The scope is restricted to `spreadsheets` for the specified spreadsheet only.
- Credentials are read as secret values and never printed.

### Reliability and governance

- Writes are idempotent via the idempotency key; appending the same row with the same key produces no duplicate row.
- Final failure is pushed to the DLQ and does not break the workflow.
- Spreadsheet content is not scraped — only the authorized range is read.
- Personal data in spreadsheets is subject to the `pii_requires_review` rule before any downstream processing.
- Cell contents are not written to the audit log — only the ID and result are recorded.

### Promotion criteria to Pilot

1. An explicit conservative `google_sheets` policy in `DEFAULT_POLICIES`.
2. The minimum-privilege `spreadsheets` scope.
3. A sandbox mode proven with a test spreadsheet.
4. Passing the relevant test cases in `platform/integrations/tests.md`.
5. Documented approval from the platform owner.

### Mapping to existing code

| Component | Real repo path |
|---|---|
| Connector facade | `dealix/connectors/connector_facade.py` |
| Google authentication pattern | `integrations/calendar.py` |
| PII review rule | `auto_client_acquisition/governance_os/rules/pii_requires_review.py` |
| Integration registry | `platform/integrations/integration_registry.md` |
