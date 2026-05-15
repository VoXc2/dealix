# العربية

# سياسة الخصوصيّة — ذاكرة العميل (الطبقة الرابعة)

> كيف يحمي Dealix بيانات العملاء في ذاكرته: الأساس القانوني، الموافقة، حجب البيانات الحسّاسة، وحقوق العميل.

## 1. الغرض

تحدّد هذه السياسة كيف تدخل بيانات العميل ذاكرة Dealix وكيف تُحمى. المبدأ: لا تُخزَّن بيانات شخصيّة بلا أساس قانوني، ولا تُستخدَم خارج الغرض المعلَن.

## 2. الأساس القانوني والموافقة

- كل مدخل في ذاكرة العميل يحمل `consent_status` من سجلّ الموافقات `auto_client_acquisition/customer_data_plane/consent_registry.py`.
- محتوى بلا أساس قانوني واضح يدخل قائمة مراجعة بشريّة، لا الفهرسة.
- سحب الموافقة يوقف فورًا استرجاع المدخلات المعتمدة عليها.

## 3. حجب البيانات الحسّاسة

- تمرّ كل وحدة محتوى عبر `auto_client_acquisition/customer_data_plane/pii_redactor.py` قبل التخزين والتضمين.
- لا تُكتب بيانات شخصيّة في السجلّات (`no_pii_in_logs`).
- المعرّفات الوطنيّة وأرقام الهواتف والبريد لا تُخزَّن في الذاكرة القابلة للاسترجاع إلا بأساس قانوني صريح.

## 4. حدود الاستخدام

- لا يُرسِل Dealix رسائل خارجيّة نيابةً عن العميل دون موافقة صريحة موثَّقة.
- لا تُجمع جهات اتصال عبر رسائل واتساب باردة أو أتمتة LinkedIn أو كسح المواقع.
- بيانات العميل لا تُستخدَم لتدريب نماذج عامّة خارج نطاق المستأجر.
- لا استرجاع عابر للمستأجرين تحت أي ظرف.

## 5. حقوق العميل

- حق الوصول: يمكن للعميل الاطّلاع على ما هو مُسجَّل عنه.
- حق التصحيح: يُحدَّث المدخل غير الدقيق مع أثر تدقيق.
- حق الحذف: حذف بيانات العميل إجراء مُصنَّف يترك قيد تدقيق، ضمن حدود الالتزامات القانونيّة.

## 6. الحوكمة

- كل وصول لبيانات عميل حسّاسة يُسجَّل عبر `auto_client_acquisition/revenue_memory/audit.py`.
- تصدير بيانات عميل حسّاسة يتطلب موافقة مُصنَّفة.
- القيمة التقديريّة عن العميل تُوسَم صراحةً؛ القيمة التقديريّة ليست قيمة مُتحقَّقة.

روابط: `schema.md` · `../organizational_memory/retention_policy.md` · `../../platform/knowledge/citations.md`

---

# English

# Privacy Policy — Customer Memory (Layer 4)

> How Dealix protects customer data in its memory: lawful basis, consent, sensitive-data redaction, and customer rights.

## 1. Purpose

This policy defines how customer data enters Dealix memory and how it is protected. The principle: no personal data is stored without a lawful basis, and none is used outside the stated purpose.

## 2. Lawful basis and consent

- Every customer-memory entry carries a `consent_status` from the consent registry `auto_client_acquisition/customer_data_plane/consent_registry.py`.
- Content without a clear lawful basis enters a human review queue, not indexing.
- Withdrawal of consent immediately stops retrieval of the entries that depend on it.

## 3. Sensitive-data redaction

- Every content unit passes through `auto_client_acquisition/customer_data_plane/pii_redactor.py` before storage and embedding.
- Personal data is never written to logs (`no_pii_in_logs`).
- National IDs, phone numbers, and email are not stored in retrievable memory except under an explicit lawful basis.

## 4. Usage boundaries

- Dealix does not send external messages on the customer's behalf without explicit, documented approval.
- Contacts are not gathered through cold WhatsApp messages, LinkedIn automation, or site scraping.
- Customer data is not used to train general models outside the tenant scope.
- No cross-tenant retrieval under any condition.

## 5. Customer rights

- Right of access: a customer can see what is recorded about them.
- Right of rectification: an inaccurate entry is corrected with an audit trail.
- Right of erasure: deleting customer data is a classified action that leaves an audit entry, within legal-obligation limits.

## 6. Governance

- Every access to sensitive customer data is logged via `auto_client_acquisition/revenue_memory/audit.py`.
- Exporting sensitive customer data requires classified approval.
- An estimated value about a customer is labeled explicitly; an estimated value is not a verified value.

Links: `schema.md` · `../organizational_memory/retention_policy.md` · `../../platform/knowledge/citations.md`
