# العربية

# مخطّط ذاكرة السياسات — الطبقة الرابعة

> يصف هذا المستند مخطّط ذاكرة السياسات في Dealix: قواعد المؤسسة وضوابطها، وكيف تُربط بمصدرها وتُقيَّد بمستأجرها وتُحدَّث دون كسر القرارات السابقة.

## 1. الغرض

ذاكرة السياسات تحفظ قواعد المؤسسة: سياسات الحوكمة، الضوابط، حدود الإجراءات. هي ذاكرة «ما تعرفه الشركة عن قواعدها». كل قاعدة تُربط بملف سياسة مصدر، فيمكن للنظام أن يجيب «ما السياسة هنا؟» مع استشهاد.

## 2. الحقول

| الحقل | النوع | الوصف |
|---|---|---|
| `policy_memory_id` | معرّف نصّي | معرّف فريد للمدخل. |
| `tenant_id` | معرّف نصّي | ربط المستأجر، إلزاميّ وثابت. |
| `policy_source_ref` | مرجع | ملف السياسة الأمّ ونسخته. |
| `rule_id` | معرّف نصّي | القاعدة المعرّفة (مثل قاعدة في `governance_os/rules/`). |
| `statement` | نصّ | نصّ القاعدة. |
| `scope` | تعداد | `tenant` / `role` / `action`. |
| `status` | تعداد | `active` / `superseded` / `retired`. |
| `effective_from` | وقت | تاريخ السريان. |
| `freshness` | تعداد | `fresh` / `aging` / `stale`. |

## 3. النطاق وربط المستأجر

- كل قاعدة مقيّدة بمستأجر واحد؛ لا استرجاع عابر للمستأجرين.
- القواعد العامّة المعرّفة في `auto_client_acquisition/governance_os/rules/` تُرجَع كمراجع، مثل `no_source_no_answer.yaml`.
- السجلّات القانونيّة المرجعيّة تُربط بـ `dealix/masters/` (مثل `constitution.md`).

## 4. التحديث دون كسر القرارات السابقة

- عند تغيّر سياسة، تُنشأ نسخة جديدة بحالة `active` وتُنقَل القديمة إلى `superseded`، لا تُمحى.
- القرارات المتّخذة وفق نسخة سابقة تظل تشير إليها، فيبقى التدقيق ممكنًا.
- `effective_from` يحدّد أي نسخة كانت سارية وقت أي قرار.

## 5. الحوكمة

- لا قاعدة بلا `policy_source_ref`؛ سياسة بلا مصدر مرفوضة.
- إجابة عن «ما السياسة؟» تستشهد بالنسخة السارية، وتذكر صراحةً إن كانت السياسة `superseded`.
- تعديل ذاكرة السياسات إجراء مُصنَّف يتطلب موافقة موثَّقة وأثر تدقيق.

روابط: `../organizational_memory/schema.md` · `../../platform/knowledge/citations.md` · `../../platform/knowledge/readiness.md`

---

# English

# Policy Memory Schema — Layer 4

> This document describes Dealix's policy memory schema: the organization's rules and controls, and how they are bound to their source, scoped to their tenant, and updated without breaking prior decisions.

## 1. Purpose

Policy memory holds the organization's rules: governance policies, controls, action limits. It is the memory of "what the company knows about its rules." Every rule is bound to a source policy file, so the system can answer "what is the policy here?" with a citation.

## 2. Fields

| Field | Type | Description |
|---|---|---|
| `policy_memory_id` | string id | Unique identifier of the entry. |
| `tenant_id` | string id | Tenant binding, mandatory and immutable. |
| `policy_source_ref` | reference | The parent policy file and its version. |
| `rule_id` | string id | The defined rule (e.g. a rule in `governance_os/rules/`). |
| `statement` | text | The text of the rule. |
| `scope` | enum | `tenant` / `role` / `action`. |
| `status` | enum | `active` / `superseded` / `retired`. |
| `effective_from` | timestamp | Effective date. |
| `freshness` | enum | `fresh` / `aging` / `stale`. |

## 3. Scope and tenant binding

- Every rule is scoped to a single tenant; no cross-tenant retrieval.
- Platform rules defined in `auto_client_acquisition/governance_os/rules/` are returned as references, such as `no_source_no_answer.yaml`.
- Reference legal records are linked to `dealix/masters/` (such as `constitution.md`).

## 4. Updating without breaking prior decisions

- When a policy changes, a new version is created with status `active` and the old one moves to `superseded`, not erased.
- Decisions made under a prior version still point to it, so audit remains possible.
- `effective_from` determines which version was in force at the time of any decision.

## 5. Governance

- No rule without a `policy_source_ref`; a policy without a source is rejected.
- An answer to "what is the policy?" cites the active version and explicitly notes if the policy is `superseded`.
- Editing policy memory is a classified action requiring documented approval and an audit trail.

Links: `../organizational_memory/schema.md` · `../../platform/knowledge/citations.md` · `../../platform/knowledge/readiness.md`
