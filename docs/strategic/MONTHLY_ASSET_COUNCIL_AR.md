# مجلس الأصول الشهري (Monthly Asset Council)

**الغرض:** مراجعة ما إذا كانت ذاكرة Dealix تتحوّل إلى **قيمة حقيقية**، لا مجرد حجم مجلدات.

**الإيقاع:** شهريًا — يمكن تنفيذه فرديًا (مؤسس) مع توثيق مخرجات في `docs/strategic/_generated/monthly_docs_review_YYYY_MM.json` لاحقًا إن رغبت.

## الأسئلة

1. ما **أكثر 5 أصول استخدامًا** (من `docs_asset_usage_log.json`)؟  
2. ما **أعلى 5 أصول قيمة لكن بلا استخدام** (انظر [_generated/asset_activation_priorities.json](_generated/asset_activation_priorities.json))؟  
3. ما الأصول التي **أُرسلت لشركاء**؟  
4. ما الأصول التي **ساهمت في meeting أو follow-up**؟  
5. ما الأصول التي **يجب أرشفتها** (انظر [ARCHIVE_REVIEW_QUEUE_AR.md](ARCHIVE_REVIEW_QUEUE_AR.md))؟  
6. هل وُجد **ملف أُرسل خارج الحزم المعتمدة**؟  
7. هل يوجد ملف **عالي القيمة بلا publication boundary** سليم؟  

## المخرجات المتوقعة

- تحديث [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md) (EvidenceLevel، LastUsed، UsageCount، Next Action).  
- تحديث [ARCHIVE_REVIEW_QUEUE_AR.md](ARCHIVE_REVIEW_QUEUE_AR.md) عند الحاجة.  
- تحديث [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md) عند إضافة حزمة جديدة.  
- إلحاق `entries` في [`../../data/docs_asset_usage_log.json`](../../data/docs_asset_usage_log.json).  

## الأدوات

- `py -3 scripts/generate_holding_value_summary.py` — ينتج `holding_value_summary.json` و`asset_activation_priorities.json`.  
- `py -3 scripts/validate_docs_governance.py`
