# العربية

# مخطّط الذاكرة التنفيذيّة — الطبقة الرابعة

> يصف هذا المستند مخطّط الذاكرة التنفيذيّة في Dealix: القرارات والسياق الاستراتيجي، وكيف تُربط بمصدرها وتُقيَّد بمستأجرها وتبقى قابلة للتدقيق.

## 1. الغرض

الذاكرة التنفيذيّة تحفظ القرارات: ما الذي تقرّر، ولماذا، وعلى أي أساس، ومن أقرّه. هي ذاكرة «ما تعرفه الشركة عن قراراتها». تُبنى من قرارات مُسجَّلة بمصادرها، فلا تُختلَق مبرّرات بأثر رجعي.

## 2. الحقول

| الحقل | النوع | الوصف |
|---|---|---|
| `executive_memory_id` | معرّف نصّي | معرّف فريد للمدخل. |
| `tenant_id` | معرّف نصّي | ربط المستأجر، إلزاميّ وثابت. |
| `decision_ref` | مرجع | القرار المسجَّل المصدر. |
| `rationale` | نصّ | مبرّر القرار كما سُجِّل وقت اتّخاذه. |
| `evidence_refs` | قائمة مراجع | المصادر التي استند إليها القرار. |
| `decided_by` | دور | الدور الذي أقرّ القرار. |
| `decision_type` | تعداد | `strategic` / `operational` / `governance`. |
| `freshness` | تعداد | `fresh` / `aging` / `stale`. |
| `decided_at` | وقت | طابع زمنيّ للقرار. |

## 3. النطاق وربط المستأجر

- كل مدخل مقيّد بمستأجر واحد؛ لا استرجاع عابر للمستأجرين.
- الذاكرة الاستراتيجيّة والدروس تُسجَّل عبر `auto_client_acquisition/intelligence_os/strategic_memory.py`.
- محرّكات القرار والاستراتيجيّة في `auto_client_acquisition/intelligence_os/` (`decision_engine.py` و `strategy_decision.py`).
- السجلّات المرجعيّة الحاكمة في `dealix/masters/` (مثل `constitution.md`).

## 4. التدقيق والاحتفاظ

- كل قرار يحمل `evidence_refs`؛ قرار بلا أدلّة لا يُسجَّل كقرار مُسنَد.
- المبرّر يُحفَظ كما كان وقت القرار، ولا يُعاد كتابته بأثر رجعي.
- القرارات تُحفَظ لقيمتها التاريخيّة ولا تُوسَم `stale` لمجرّد قدمها؛ الحداثة تشير لمدى سريان القرار لا لقيمته كسجلّ.

## 5. الحوكمة

- إجابة عن «لماذا اتُّخذ هذا القرار؟» تستشهد بـ `rationale` و `evidence_refs`، لا بسرد مُختلَق.
- لا تُقدَّم القيمة التقديريّة في القرار كقيمة مُتحقَّقة.
- تعديل سجلّ قرار إجراء مُصنَّف يترك أثر تدقيق؛ التصحيح بإضافة سجلّ لا بمحو.

روابط: `../workflow_memory/schema.md` · `../policy_memory/schema.md` · `../../platform/knowledge/source_lineage.md`

---

# English

# Executive Memory Schema — Layer 4

> This document describes Dealix's executive memory schema: decisions and strategic context, how they are bound to their source, scoped to their tenant, and kept auditable.

## 1. Purpose

Executive memory holds decisions: what was decided, why, on what basis, and who approved it. It is the memory of "what the company knows about its decisions." It is built from decisions recorded with their sources, so rationales are not fabricated retroactively.

## 2. Fields

| Field | Type | Description |
|---|---|---|
| `executive_memory_id` | string id | Unique identifier of the entry. |
| `tenant_id` | string id | Tenant binding, mandatory and immutable. |
| `decision_ref` | reference | The source recorded decision. |
| `rationale` | text | The decision's rationale as recorded at the time it was made. |
| `evidence_refs` | list of references | The sources the decision rested on. |
| `decided_by` | role | The role that approved the decision. |
| `decision_type` | enum | `strategic` / `operational` / `governance`. |
| `freshness` | enum | `fresh` / `aging` / `stale`. |
| `decided_at` | timestamp | Decision timestamp. |

## 3. Scope and tenant binding

- Every entry is scoped to a single tenant; no cross-tenant retrieval.
- Strategic memory and lessons are recorded via `auto_client_acquisition/intelligence_os/strategic_memory.py`.
- Decision and strategy engines are in `auto_client_acquisition/intelligence_os/` (`decision_engine.py` and `strategy_decision.py`).
- Governing reference records are in `dealix/masters/` (such as `constitution.md`).

## 4. Audit and retention

- Every decision carries `evidence_refs`; a decision without evidence is not recorded as an evidenced decision.
- The rationale is kept as it was at decision time and is not rewritten retroactively.
- Decisions are retained for their historical value and are not flagged `stale` merely for age; freshness indicates whether the decision is still in force, not its value as a record.

## 5. Governance

- An answer to "why was this decision made?" cites the `rationale` and `evidence_refs`, not a fabricated narrative.
- An estimated value within a decision is not presented as a verified value.
- Editing a decision record is a classified action that leaves an audit trail; correction is by adding a record, not by erasure.

Links: `../workflow_memory/schema.md` · `../policy_memory/schema.md` · `../../platform/knowledge/source_lineage.md`
