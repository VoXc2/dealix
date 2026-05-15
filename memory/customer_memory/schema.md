# العربية

# مخطّط ذاكرة العميل — الطبقة الرابعة

> يصف هذا المستند مخطّط ذاكرة العميل في Dealix: ما يعرفه النظام عن كل عميل، وكيف يُربط بمصدره، ويُقيَّد بمستأجره، ويحترم الموافقة.

## 1. الغرض

ذاكرة العميل تحفظ سياق العميل: الحساب، المحادثات المعتمدة، الخطّ الزمني للتفاعلات. هي ذاكرة «ما تعرفه الشركة عن عملائها». تُبنى من مصادر مُسجَّلة فقط، وتحترم الموافقة وحجب البيانات الحسّاسة.

## 2. الحقول

| الحقل | النوع | الوصف |
|---|---|---|
| `customer_memory_id` | معرّف نصّي | معرّف فريد للمدخل. |
| `tenant_id` | معرّف نصّي | ربط المستأجر، إلزاميّ وثابت. |
| `account_ref` | مرجع | إشارة لسجلّ الحساب. |
| `source_ref` | مرجع | المحادثة أو الحدث أو المستند المصدر. |
| `content` | نصّ | نصّ السياق بعد حجب البيانات الحسّاسة. |
| `memory_type` | تعداد | `account_fact` / `conversation` / `interaction_event`. |
| `consent_status` | تعداد | حالة الموافقة من سجلّ الموافقات. |
| `permission_tags` | قائمة | وسوم الصلاحيّة على مستوى المستخدم. |
| `freshness` | تعداد | `fresh` / `aging` / `stale`. |
| `created_at` / `updated_at` | وقت | طوابع زمنيّة. |

## 3. النطاق وربط المستأجر

- كل مدخل مقيّد بمستأجر واحد؛ لا استرجاع عابر للمستأجرين.
- تُبنى حزمة سياق العميل عبر `auto_client_acquisition/customer_brain/context_pack.py` و `builder.py`.
- المحادثات تُضمَّن في `ConversationEmbeddingRecord` عبر `core/memory/embedding_service.py`.
- الموافقة وحجب البيانات يُداران عبر `auto_client_acquisition/customer_data_plane/` (`consent_registry.py` و `pii_redactor.py`).

## 4. الموافقة والخصوصيّة

- لا يُخزَّن سياق عميل بلا أساس قانوني مُسجَّل؛ التفاصيل في `privacy_policy.md`.
- البيانات الحسّاسة تُحجَب قبل التخزين والتضمين.
- لا يُرسِل Dealix رسائل خارجيّة نيابةً عن العميل دون موافقة صريحة، ولا تُجمع جهات اتصال من رسائل باردة أو أتمتة LinkedIn.

## 5. الحوكمة

- لا مدخل بلا `source_ref`؛ ذاكرة عميل بلا مصدر مرفوضة.
- سحب الموافقة يوقف استرجاع المدخلات المعتمدة عليها.
- حذف بيانات عميل إجراء مُصنَّف يترك أثر تدقيق.

روابط: `privacy_policy.md` · `../../platform/knowledge/hybrid_retrieval.md` · `../../platform/knowledge/source_lineage.md`

---

# English

# Customer Memory Schema — Layer 4

> This document describes Dealix's customer memory schema: what the system knows about each customer, how it is bound to its source, scoped to its tenant, and respects consent.

## 1. Purpose

Customer memory holds customer context: the account, approved conversations, the interaction timeline. It is the memory of "what the company knows about its customers." It is built only from recorded sources and respects consent and sensitive-data redaction.

## 2. Fields

| Field | Type | Description |
|---|---|---|
| `customer_memory_id` | string id | Unique identifier of the entry. |
| `tenant_id` | string id | Tenant binding, mandatory and immutable. |
| `account_ref` | reference | Pointer to the account record. |
| `source_ref` | reference | The source conversation, event, or document. |
| `content` | text | Context text after sensitive-data redaction. |
| `memory_type` | enum | `account_fact` / `conversation` / `interaction_event`. |
| `consent_status` | enum | Consent status from the consent registry. |
| `permission_tags` | list | Permission tags at the user level. |
| `freshness` | enum | `fresh` / `aging` / `stale`. |
| `created_at` / `updated_at` | timestamp | Timestamps. |

## 3. Scope and tenant binding

- Every entry is scoped to a single tenant; no cross-tenant retrieval.
- The customer context pack is built via `auto_client_acquisition/customer_brain/context_pack.py` and `builder.py`.
- Conversations are embedded in `ConversationEmbeddingRecord` via `core/memory/embedding_service.py`.
- Consent and redaction are managed via `auto_client_acquisition/customer_data_plane/` (`consent_registry.py` and `pii_redactor.py`).

## 4. Consent and privacy

- No customer context is stored without a recorded lawful basis; details in `privacy_policy.md`.
- Sensitive data is redacted before storage and embedding.
- Dealix does not send external messages on the customer's behalf without explicit approval, and contacts are not gathered from cold messages or LinkedIn automation.

## 5. Governance

- No entry without a `source_ref`; customer memory without a source is rejected.
- Withdrawal of consent stops retrieval of the entries that depend on it.
- Deleting customer data is a classified action that leaves an audit trail.

Links: `privacy_policy.md` · `../../platform/knowledge/hybrid_retrieval.md` · `../../platform/knowledge/source_lineage.md`
