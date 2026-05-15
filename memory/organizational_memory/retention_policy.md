# العربية

# سياسة الاحتفاظ — الذاكرة التنظيميّة (الطبقة الرابعة)

> كيف يحتفظ Dealix بالذاكرة التنظيميّة، ومتى تتقادم، ومتى تُحذف، ومن يقرّر.

## 1. الغرض

تحدّد هذه السياسة دورة حياة المدخل في الذاكرة التنظيميّة: من الإنشاء إلى التقادم إلى الحذف المنضبط. الهدف ذاكرة محدَّثة وقابلة للتدقيق، بلا حذف صامت وبلا تضخّم بمحتوى قديم.

## 2. حالات الحداثة

| الحالة | المعنى | الأثر على الاسترجاع |
|---|---|---|
| `fresh` | حديث ضمن نافذة الصلاحيّة | يُسترجَع بأولويّة طبيعيّة. |
| `aging` | تجاوز نافذة الحداثة الأوّليّة | يُسترجَع مع وسم تنبيه على الحداثة. |
| `stale` | تجاوز حدّ التقادم | يُسترجَع فقط مع إشارة صريحة لقدمه، أو يُستبعَد حسب نوع السؤال. |

## 3. مدد الاحتفاظ

- المستندات وأدلّة التشغيل: تُحفَظ ما دامت سارية؛ تُراجَع حداثتها دوريًّا.
- مراجع السياسات: تتبع دورة حياة السياسة الأمّ في `../policy_memory/schema.md`.
- الدروس الاستراتيجيّة: تُحفَظ لقيمتها التاريخيّة ولا تُوسَم `stale` لمجرّد قدمها.
- أحداث الأعمال المرتبطة: تتبع سياسة الاحتفاظ في `auto_client_acquisition/revenue_memory/retention.py`.

## 4. الحذف

- الحذف لا يكون صامتًا أبدًا؛ كل حذف يترك قيد تدقيق.
- حذف مدخل إجراء مُصنَّف يتطلب موافقة موثَّقة.
- عند حذف مصدر، تُحدَّث الاستشهادات المعتمدة عليه لتعكس فقدان المصدر، فلا تظهر إجابة بمصدر مفقود.

## 5. الحوكمة

- لا تُحذف بيانات يلزم الاحتفاظ بها لأساس قانوني أو تعاقدي قبل انقضاء المدّة.
- مراجعة الحداثة عمليّة دوريّة مجدولة، مالكها قائد المعرفة.
- القيمة التقديريّة المبنيّة على مصدر `stale` تُوسَم صراحةً بقدم مصدرها.

روابط: `schema.md` · `../../platform/knowledge/source_lineage.md` · `../policy_memory/schema.md`

---

# English

# Retention Policy — Organizational Memory (Layer 4)

> How Dealix retains organizational memory, when it ages, when it is deleted, and who decides.

## 1. Purpose

This policy defines the lifecycle of an organizational-memory entry: from creation, to aging, to disciplined deletion. The goal is a current, auditable memory with no silent deletion and no bloat from stale content.

## 2. Freshness states

| State | Meaning | Effect on retrieval |
|---|---|---|
| `fresh` | Recent, within the validity window | Retrieved at normal priority. |
| `aging` | Past the initial freshness window | Retrieved with a freshness-warning tag. |
| `stale` | Past the staleness threshold | Retrieved only with an explicit "old" marker, or excluded depending on the question. |

## 3. Retention durations

- Documents and runbooks: retained while in force; freshness reviewed periodically.
- Policy references: follow the lifecycle of the parent policy in `../policy_memory/schema.md`.
- Strategic lessons: retained for their historical value and are not flagged `stale` merely for age.
- Associated business events: follow the retention policy in `auto_client_acquisition/revenue_memory/retention.py`.

## 4. Deletion

- Deletion is never silent; every deletion leaves an audit entry.
- Deleting an entry is a classified action requiring documented approval.
- When a source is deleted, citations that depended on it are updated to reflect the lost source, so no answer shows a missing source.

## 5. Governance

- Data required for a lawful or contractual basis is not deleted before its retention period ends.
- Freshness review is a scheduled periodic process, owned by the Knowledge Lead.
- An estimated value built on a `stale` source is explicitly labeled with its source's age.

Links: `schema.md` · `../../platform/knowledge/source_lineage.md` · `../policy_memory/schema.md`
