# Dealix — من الصفر إلى شركة قابضة

هذا المجلد يضم **الخريطة العليا الكاملة** لبناء Dealix كشركة تشغيل AI محكومة، قابلة للنمو حتى تصبح **شركة قابضة** — وليس كأداة أو وكالة أتمتة.

## المستند الرئيسي

- **[DEALIX_FROM_ZERO_TO_HOLDING_BLUEPRINT.md](DEALIX_FROM_ZERO_TO_HOLDING_BLUEPRINT.md)** — الفكرة الأم، المعادلة الكبرى، الطبقات 1–40، MVP الحقيقي، أول تجربة عملية، والخلاصة.

## روابط مرتبطة في الريبو

- [DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md) — فهرس الطبقات المرقّم `docs/00` … `docs/36`
- [SYSTEM_MAP.md](../enterprise_architecture/SYSTEM_MAP.md) — تعيين الطبقات إلى الحزم في `auto_client_acquisition/`
- `docs/00_constitution/` — دستور ومبادئ موجودة مسبقًا
- `docs/agentic_operations/` — وكلاء محكومون (MVP levels)

## كيف تستخدمها

1. اقرأ الـ Blueprint كاملاً مرة واحدة على الأقل (صورة ذهنية واحدة).
2. عند التنفيذ، ارجع إلى مجلد الطبقة المرقّم في `docs/NN_*` أو إلى الكود عبر `dealix_master_layers/registry.py`.
3. عند الطلب: «فصّل طبقة X» — ننزل من الخريطة العليا إلى تنفيذ واختبارات.
