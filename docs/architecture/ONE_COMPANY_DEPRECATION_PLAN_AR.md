# Dealix — خطة توحيد One Company (193 مسار → 1 نظام)

## التشخيص
- `auto_client_acquisition/` يحتوي 193 مجلدًا فرعيًا — كل مجلد يمثل قدرة أو طبقة تاريخية (data_os, proof_os, governance_os, etc.)
- `dealix/commercial/` الآن هو النظام الأساسي الموحد (22 محركًا، 44 ذراع، 20 قطاع) — `One Company` الحقيقي
- `core/agents`, `autonomous_growth/agents`, `integrations/` — طبقات قديمة مكررة

## الحل — ترحيل مرحلي بأفضل فكر بعد بحث عميق
1. **تجميد**: لا إنشاء قدرات جديدة في `auto_client_acquisition` — كل جديد في `dealix/commercial`
2. **تصنيف**: كل من 193 مسارًا يصنف `CANONICAL` (يبقى), `LEGACY` (مهجور), `DUPLICATE` (مكرر), `RETIRED` (محذوف)
3. **محولات**: لكل `LEGACY` مفيد، إنشاء `adapter` في `dealix/commercial` يعيد استخدام المنطق دون نسخه
4. **اختبارات**: `import-linter` يمنع استيراد `auto_client_acquisition` الجديد بعد `2026-10-01`
5. **حذف تدريجي**: كل شهر، حذف 10 `RETIRED` بعد 3 اختبارات خضراء + نسخة احتياطية

## الفائدة
- تقليل `One-Company` من `HIGH` إلى `PASS` في 90 يومًا بدون تعطيل الإنتاج
- كل الأذرع الـ 44 تبقى مفعلة عبر `dealix/commercial/arm_registry` — لا 44 مشروع

## الحفظ
كلشي في `main` عبر PRs، `origin/main` متزامن
