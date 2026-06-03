# طابور إنتاج المحتوى — Content Production Queue (قالب تقرير)

قالب تقرير لتتبّع مسودّات المحتوى حتى النشر. كل بند يمرّ ببوّابة الموافقة
(`approval_required=true`). قالب فارغ يُملأ بحقائق فقط — لا أرقام/إثبات مُختلَق.

## مفتاح الحالة
`draft` → `approved` → `published` → `archived`.
بوّابات إضافية لـ `proof_learning`/`case_style`: موافقة العميل + تعمية قبل الاعتماد.

## الطابور (قالب — استبدل الصفوف بمسودّات حقيقية)
| `idea_id` | `type` | `hook` (مختصر) | `evidence_level` | بوّابة الموافقة/التعمية | `status` | اعتماد المؤسّس |
|-----------|--------|----------------|------------------|--------------------------|----------|----------------|
| `[POST-xxx]` | `founder_insight` | `[الخطّاف]` | `[...]` | — | `draft` | ☐ |
| `[POST-xxx]` | `sector_pain` | `[الخطّاف]` | `observed` | — | `draft` | ☐ |
| `[POST-xxx]` | `proof_learning` | `[الخطّاف]` | `observed/verified` | موافقة+تعمية ☐ | `draft` | ☐ |
| `[POST-xxx]` | `case_style` | `[نمط عام «مثال توضيحي»]` | `assumed` | تعمية ☐ | `draft` | ☐ |

## قواعد التعبئة
- لا انتقال إلى `approved` إلا باعتماد المؤسّس الصريح؛ لا نشر قبله.
- `proof_learning` يتطلّب موافقة العميل وتعمية فعليّتين (مرجع `PROOF_TO_CONTENT_SYSTEM_AR.md`).
- `case_style` بأسماء افتراضية فقط موسومة «مثال توضيحي» — لا أسماء/نتائج عملاء.
- كل رقم حقيقي بمصدر و`evidence_level`، وإلا يُحذف.
- لا عبارات محظورة؛ الأفعال المسموحة فقط؛ لا PII (الأدوار فقط).

## الربط
- المحرّك: `docs/content/CONTENT_ENGINE_AR.md`.
- خط دراسات الحالة: `docs/content/CASE_STUDY_PIPELINE_AR.md`.
- التقويم: `reports/content/CONTENT_CALENDAR.md`.
