# العربية

# مخطّط ذاكرة سير العمل — الطبقة الرابعة

> يصف هذا المستند مخطّط ذاكرة سير العمل في Dealix: ما يعرفه النظام عن العمليّات والخطوات والأحداث التشغيليّة، وكيف يُربط بمصدره ويُقيَّد بمستأجره.

## 1. الغرض

ذاكرة سير العمل تحفظ كيف تعمل المؤسسة فعليًّا: خطوات العمليّات، الأحداث التشغيليّة، الخطوط الزمنيّة. هي ذاكرة «ما تعرفه الشركة عن عمليّاتها». تُبنى من أحداث مُسجَّلة، فيمكن إعادة تشغيلها وتدقيقها.

## 2. الحقول

| الحقل | النوع | الوصف |
|---|---|---|
| `workflow_memory_id` | معرّف نصّي | معرّف فريد للمدخل. |
| `tenant_id` | معرّف نصّي | ربط المستأجر، إلزاميّ وثابت. |
| `workflow_ref` | مرجع | إشارة للعمليّة أو سير العمل الأمّ. |
| `event_ref` | مرجع | الحدث المصدر في سجلّ الأحداث. |
| `step_name` | نصّ | اسم الخطوة التشغيليّة. |
| `outcome` | تعداد | `completed` / `failed` / `pending`. |
| `permission_tags` | قائمة | وسوم الصلاحيّة على مستوى المستخدم. |
| `freshness` | تعداد | `fresh` / `aging` / `stale`. |
| `created_at` | وقت | طابع زمنيّ للحدث. |

## 3. النطاق وربط المستأجر

- كل مدخل مقيّد بمستأجر واحد؛ لا استرجاع عابر للمستأجرين.
- الأحداث تُخزَّن في سجلّ الأحداث `auto_client_acquisition/revenue_memory/` (`event_store.py` و `events.py`).
- إعادة التشغيل عبر `auto_client_acquisition/revenue_memory/replay.py` والإسقاطات عبر `projections.py`.
- الخطّ الزمني عبر `auto_client_acquisition/revenue_memory/timeline.py`.

## 4. إعادة التشغيل والتدقيق

- ذاكرة سير العمل قائمة على مصدر أحداث؛ يمكن إعادة بناء الحالة بإعادة تشغيل الأحداث.
- كل حدث غير قابل للتعديل بعد كتابته؛ التصحيح يكون بحدث جديد لا بمحو.
- الاحتفاظ يتبع `auto_client_acquisition/revenue_memory/retention.py`.

## 5. الحوكمة

- لا مدخل بلا `event_ref`؛ ذاكرة سير عمل بلا مصدر مرفوضة.
- إجابة عن «ماذا حدث في هذه العمليّة؟» تستشهد بأحداث حقيقيّة، لا بسرد مُختلَق.
- لا تُختلَق نتائج خطوات؛ تُذكر الحالة كما هي مُسجَّلة.

روابط: `../../platform/knowledge/source_lineage.md` · `../executive_memory/schema.md` · `../organizational_memory/schema.md`

---

# English

# Workflow Memory Schema — Layer 4

> This document describes Dealix's workflow memory schema: what the system knows about processes, steps, and operational events, and how it is bound to its source and scoped to its tenant.

## 1. Purpose

Workflow memory holds how the organization actually operates: process steps, operational events, timelines. It is the memory of "what the company knows about its operations." It is built from recorded events, so it can be replayed and audited.

## 2. Fields

| Field | Type | Description |
|---|---|---|
| `workflow_memory_id` | string id | Unique identifier of the entry. |
| `tenant_id` | string id | Tenant binding, mandatory and immutable. |
| `workflow_ref` | reference | Pointer to the parent process or workflow. |
| `event_ref` | reference | The source event in the event store. |
| `step_name` | text | Name of the operational step. |
| `outcome` | enum | `completed` / `failed` / `pending`. |
| `permission_tags` | list | Permission tags at the user level. |
| `freshness` | enum | `fresh` / `aging` / `stale`. |
| `created_at` | timestamp | Event timestamp. |

## 3. Scope and tenant binding

- Every entry is scoped to a single tenant; no cross-tenant retrieval.
- Events are stored in the event store `auto_client_acquisition/revenue_memory/` (`event_store.py` and `events.py`).
- Replay via `auto_client_acquisition/revenue_memory/replay.py` and projections via `projections.py`.
- Timeline via `auto_client_acquisition/revenue_memory/timeline.py`.

## 4. Replay and audit

- Workflow memory is event-sourced; state can be rebuilt by replaying events.
- Every event is immutable once written; correction is a new event, not an erasure.
- Retention follows `auto_client_acquisition/revenue_memory/retention.py`.

## 5. Governance

- No entry without an `event_ref`; workflow memory without a source is rejected.
- An answer to "what happened in this process?" cites real events, not a fabricated narrative.
- Step outcomes are not fabricated; the state is reported as recorded.

Links: `../../platform/knowledge/source_lineage.md` · `../executive_memory/schema.md` · `../organizational_memory/schema.md`
