# قائمة مراجعة الأرشفة

**الغرض:** تحديد الملفات أو المجلدات التي تحتاج **مراجعة أرشفة** دون نقلها أو حذفها مباشرة.

## القاعدة

**Queue first. Move later. Delete almost never.**

## قائمة أولية

| الملف / المجلد | سبب المراجعة | الحالة المقترحة | لا يُنقل قبل | القرار |
|----------------|---------------|-------------------|----------------|--------|
| docs/26_human_amplified/ | رقم مكرر مع docs/26_service_catalog/ | SUPPORTING أو LEGACY | فحص الروابط والاعتماد | إبقاء مؤقت |
| docs/27_value_capture/ | رقم مكرر مع docs/27_delivery_playbooks/ | SUPPORTING | مراجعة علاقته بالتجاري | إبقاء |
| docs/30_standards/ | رقم مكرر مع docs/30_pricing/ | SUPPORTING | فحص standards و docs/23_standards | إبقاء |
| docs/35_tests/ | رقم مكرر مع docs/35_agent_iam/ | SUPPORTING | التأكد أن `tests/` هو المصدر التنفيذي | إبقاء |
| docs/29_enterprise_rollout | رقم مكرر مع docs/29_sales_os | SUPPORTING | محاذاة BU4 / موجات | إبقاء |
| docs/34_market_power | رقم مكرر مع docs/34_ai_estate | SUPPORTING | مراجعة canonical | إبقاء |
| أي مجلد wave قديم (wave6/, wave8/, …) | أرشيف تاريخي | ARCHIVED (تصنيف) | فحص ما إذا كان مستخدمًا في موجات حالية | انتظار |

## قرار الأرشفة

أي نقل أو حذف لاحق يحتاج:

1. فحص الروابط.  
2. فحص الاختبارات.  
3. تحديث [HOLDING_DOCS_HUB_AR.md](HOLDING_DOCS_HUB_AR.md) إن لزم.  
4. تحديث [DOCS_CANONICAL_REGISTRY_AR.md](DOCS_CANONICAL_REGISTRY_AR.md).  
5. إعادة توليد `_generated/docs_top_level_snapshot.json` عبر `py -3 scripts/generate_docs_hub_snapshot.py`.

مرجع السياسة: [DOCS_ARCHIVE_POLICY_AR.md](DOCS_ARCHIVE_POLICY_AR.md).
