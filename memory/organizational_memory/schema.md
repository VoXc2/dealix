# العربية

# مخطّط الذاكرة التنظيميّة — الطبقة الرابعة

> يصف هذا المستند مخطّط الذاكرة التنظيميّة في Dealix: ملفّات المؤسسة وسياساتها وأدلّتها التشغيليّة ودروسها، وكيف تُخزَّن وتُربط بمصدرها وتُقيَّد بمستأجرها.

## 1. الغرض

الذاكرة التنظيميّة تحفظ معرفة المؤسسة المستقرّة: المستندات، أدلّة التشغيل، الدروس المستفادة. هي ذاكرة «ما تعرفه الشركة عن نفسها». تربط كل مدخل بملفّه الأصلي ولا تُنتج معرفة بلا مصدر.

## 2. الحقول

| الحقل | النوع | الوصف |
|---|---|---|
| `memory_id` | معرّف نصّي | معرّف فريد للمدخل. |
| `tenant_id` | معرّف نصّي | ربط المستأجر، إلزاميّ وثابت. |
| `source_file_ref` | مرجع | إشارة للملف الأصلي ونسخته. |
| `chunk_id` | معرّف نصّي | المقطع المشتقّ منه المدخل. |
| `content` | نصّ | نصّ المقطع بعد حجب البيانات الحسّاسة. |
| `content_hash` | بصمة | بصمة لكشف التغيير. |
| `memory_type` | تعداد | `document` / `policy_ref` / `runbook` / `lesson`. |
| `permission_tags` | قائمة | وسوم الصلاحيّة الموروثة من المصدر. |
| `freshness` | تعداد | `fresh` / `aging` / `stale`. |
| `created_at` / `updated_at` | وقت | طوابع زمنيّة. |

## 3. النطاق وربط المستأجر

- كل مدخل مقيّد بمستأجر واحد عبر `tenant_id`؛ لا مدخل مشترك بين مستأجرين.
- الاسترجاع من الذاكرة التنظيميّة مقيّد بالمستأجر وبصلاحيّة المستخدم.
- الدروس الاستراتيجيّة تُسجَّل عبر `auto_client_acquisition/intelligence_os/strategic_memory.py` ودماغ الشركة عبر `auto_client_acquisition/company_brain/brain.py`.

## 4. الاحتفاظ والحداثة

- لكل مدخل حالة حداثة تتبع `retention_policy.md`.
- المدخل القديم يُوسَم `stale` ولا يُحذف بصمت.
- تحديث المصدر يُنشئ نسخة جديدة ويبقي القديمة مرجعًا تاريخيًّا.

## 5. الحوكمة

- لا مدخل بلا `source_file_ref`؛ ذاكرة بلا مصدر مرفوضة.
- لا يدخل محتوى من كسح مواقع أو رسائل باردة.
- حذف مدخل إجراء مُصنَّف يتطلب موافقة موثَّقة وأثر تدقيق.

روابط: `retention_policy.md` · `../../platform/knowledge/architecture.md` · `../../platform/knowledge/source_lineage.md`

---

# English

# Organizational Memory Schema — Layer 4

> This document describes Dealix's organizational memory schema: the organization's files, policies, runbooks, and lessons, and how they are stored, bound to their source, and scoped to their tenant.

## 1. Purpose

Organizational memory holds the organization's stable knowledge: documents, runbooks, lessons learned. It is the memory of "what the company knows about itself." It binds every entry to its origin file and produces no knowledge without a source.

## 2. Fields

| Field | Type | Description |
|---|---|---|
| `memory_id` | string id | Unique identifier of the entry. |
| `tenant_id` | string id | Tenant binding, mandatory and immutable. |
| `source_file_ref` | reference | Pointer to the origin file and its version. |
| `chunk_id` | string id | The chunk the entry was derived from. |
| `content` | text | Chunk text after sensitive-data redaction. |
| `content_hash` | hash | Hash for change detection. |
| `memory_type` | enum | `document` / `policy_ref` / `runbook` / `lesson`. |
| `permission_tags` | list | Permission tags inherited from the source. |
| `freshness` | enum | `fresh` / `aging` / `stale`. |
| `created_at` / `updated_at` | timestamp | Timestamps. |

## 3. Scope and tenant binding

- Every entry is scoped to a single tenant via `tenant_id`; no entry is shared across tenants.
- Retrieval from organizational memory is scoped by tenant and by user permission.
- Strategic lessons are recorded via `auto_client_acquisition/intelligence_os/strategic_memory.py` and company knowledge via `auto_client_acquisition/company_brain/brain.py`.

## 4. Retention and freshness

- Every entry has a freshness status that follows `retention_policy.md`.
- An aging entry is flagged `stale` and is never silently deleted.
- A source update creates a new version and keeps the old one as a historical reference.

## 5. Governance

- No entry without a `source_file_ref`; memory without a source is rejected.
- No content from scraping or cold messages enters memory.
- Deleting an entry is a classified action requiring documented approval and an audit trail.

Links: `retention_policy.md` · `../../platform/knowledge/architecture.md` · `../../platform/knowledge/source_lineage.md`
