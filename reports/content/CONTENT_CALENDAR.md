# تقويم المحتوى — Content Calendar (قالب تقرير)

قالب تقرير لجدولة المحتوى اليومي لـ Dealix. المخرج اليومي ثابت: **4 أنواع**
(`founder_insight` · `sector_pain` · `proof_learning` · `case_style`)، وكلّها
`approval_required=true` قبل النشر. هذا قالب فارغ يُملأ بحقائق فقط — لا أرقام/إثبات مُختلَق.

## مفتاح الحالة (`status`)
`draft` → `approved` → `published` → `archived` (لا قفز فوق الموافقة).

## الجدول الأسبوعي (قالب — استبدل الصفوف بمسودّات حقيقية)
| اليوم | `idea_id` | `type` | `sector` | `evidence_level` | `status` | اعتماد المؤسّس |
|-------|-----------|--------|----------|------------------|----------|----------------|
| الأحد | `[POST-xxx]` | `founder_insight` | `[sector]` | `[none..verified]` | `draft` | ☐ |
| الإثنين | `[POST-xxx]` | `sector_pain` | `[sector]` | `[observed]` | `draft` | ☐ |
| الثلاثاء | `[POST-xxx]` | `proof_learning` | `[sector]` | `[observed/verified]` | `draft` | ☐ |
| الأربعاء | `[POST-xxx]` | `case_style` | `[sector]` | `assumed` | `draft` | ☐ |
| الخميس | `[POST-xxx]` | `[type]` | `[sector]` | `[...]` | `draft` | ☐ |

ملاحظة: `case_style` نمط عام «مثال توضيحي» بأسماء افتراضية فقط
(Digital Rise Agency · CloudShift Consulting · Horizon Realty Team) — لا نتائج عملاء.

## قواعد التعبئة
- لا يُجدوَل بند بلا موافقة مخطّطة؛ لا نشر قبل `approved`.
- كل رقم في أي بند حقيقي بمصدر و`evidence_level`، وإلا يُحذف.
- لا عبارات محظورة (نضمن/نضاعف الإيرادات/نتائج مضمونة/بدون مخاطرة/10x/
  guaranteed revenue/no risk)؛ الأفعال المسموحة فقط.
- لا PII (الأدوار فقط)؛ لا أسماء عملاء حقيقيين.

## الربط
- المحرّك: `docs/content/CONTENT_ENGINE_AR.md`.
- طابور الإنتاج: `reports/content/CONTENT_PRODUCTION_QUEUE.md`.
- مصدر الأفكار: `data/content/post_ideas.jsonl`.
