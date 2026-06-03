# قائمة تكرار بايلوت المؤسسة — مصغّرة

استخدم هذا الملف مع [PILOT_EXECUTION_RUNBOOK_AR.md](PILOT_EXECUTION_RUNBOOK_AR.md) بعد كل بايلوت لتكرار التشغيل دون إعادة اختراع العملية.

## قبل البدء

- [ ] النطاق معبّأ من [pilot_scope_template.md](pilot_scope_template.md)
- [ ] `tenant_id` واضح وليس `default` في الإنتاج
- [ ] Decision Passport: تم الاطلاع على `golden-chain` و`evidence-levels` (انظر الدليل الرئيسي)

## أثناء البايلوت

- [ ] كل إجراء خارجي أو عالي المخاطر: مسودة أو موافقة مسجّلة
- [ ] أي قيمة مقاسة: مرجع مصدر `source_ref`

## بعد البايلوت

- [ ] Proof Pack أو ما يعادله موثّق للمرحلة
- [ ] تصنيف الحدث الخارجي (`follow_up_sent`, `scope_requested`, إلخ) في سجل التشغيل الأسبوعي
- [ ] تشغيل بوابة التحقق عند أي تغيير في الريبو: `bash scripts/verify_global_ai_transformation.sh`

## تكرار البايلوت التالي

انسخ مجلد الأدلة مع تاريخ جديد؛ لا تمس القوالب المرجعية إلا عبر PR موافَق عليه.
