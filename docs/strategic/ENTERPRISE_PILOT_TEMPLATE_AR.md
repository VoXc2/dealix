# قالب Pilot لمؤسسات Enterprise — Dealix

**الاستخدام:** املأ الأقسام قبل بدء العمل؛ يحدّ النطاق ويربط النتائج بـ Proof وقالب التعلّم الأسبوعي في المنتج.

## 1. تعريف العميل والنطاق

| الحقل | القيمة |
|--------|--------|
| اسم الحساب | |
| القطاع / المدينة | |
| جهة اتخاذ القرار (DM) | |
| شرائح الطبقات المباعة | A فقط / A+B / A+B+C (راجع [ENTERPRISE_OFFER_POSITIONING_AR.md](ENTERPRISE_OFFER_POSITIONING_AR.md)) |
| تاريخ بداية Pilot | |
| تاريخ مراجعة نصف المدة | |
| تاريخ قرار التوسعة | |

**نطاق مقصود (Anti-Waste):** عرض واحد أو مسار واحد واضح؛ لا توسيع صناعات متعددة داخل نفس الـ Pilot إلا بموافقة صريحة.

## 2. KPI واحد رئيسي للإثبات (North Star للـ Pilot)

| KPI | تعريف قابل للقياس | خط الأساس | الهدف | مصدر البيانات (مخطط) |
|-----|-------------------|-----------|--------|----------------------|
| | مثال: «عدد الليدات ذات جواز قرار صالح» أو «زمن أول Proof مسجّل» | | | proof_ledger / CRM / جداول تشغيل |

## 3. بوابات Proof (L0–L5)

- مرجع المستويات: `GET /api/v1/decision-passport/evidence-levels` و [DEALIX_MASTER_OPERATING_MODEL_AR.md](DEALIX_MASTER_OPERATING_MODEL_AR.md) (قسم Proof).
- **بوابة ما قبل التوسعة:** لا upsell عام تحت L4؛ لا إجراء خارجي بدون Decision Passport / موافقة حسب `anti-waste`.

| البوابة | مستوى الأدلة المستهدف | موافقة نشر (إن وُجدت) | مسؤول |
|---------|------------------------|------------------------|--------|
| أول دليل داخلي (L2–L3) | | | |
| نشر عام (L4) | | | |
| توسعة إيراد (L5) | | | |

## 4. مسار التشغيل الأسبوعي (ربط بـ API)

هيكل JSON المرجعي من `GET /api/v1/revenue-os/learning/weekly-template` ووحدة [auto_client_acquisition/revenue_os/learning_weekly.py](../../auto_client_acquisition/revenue_os/learning_weekly.py) (`weekly_learning_report_skeleton`).

املأ أثناء الـ Pilot:

| مفتاح الهيكل | ماذا تسجّل هذا الأسبوع |
|--------------|-------------------------|
| `what_worked_ar` | |
| `what_failed_ar` | |
| `segments_to_stop_ar` | |
| `offer_price_signals_ar` | |
| `repeated_feature_requests_ar` | |
| `workflow_simplifications_ar` | |
| `funnel_metrics.*` | اربط بأرقام: signal→lead→passport→approved→delivery→proof→expansion |

**ملاحظة:** الحقول التلقائية الكاملة تتطلب ربط أحداث وتحليلات لاحقاً؛ حتى ذلك الحين يُعتمد التعبئة اليدوية من هذا القالب.

## 5. مخاطر واعتمادات

| المخاطر | تخفيف | مالك |
|---------|--------|------|
| غياب مفاتيح تكامل (CRM/…) | تفعيل مسار degrades بشكل واضح للعميل | |
| طلبات خارج السلسلة الذهبية | إعادة التوجيه إلى Decision Passport | |

## 6. قرار نهاية الـ Pilot

- [ ] تحقق KPI الرئيسي
- [ ] Proof مسجّل وفق البوابات
- [ ] تحديث [dealix/registers/no_overclaim.yaml](../../dealix/registers/no_overclaim.yaml) إن تغيّر أي ادّعاء عام
- [ ] قرار: توسعة / تمديد / إيقاف (مع سبب مسجّل)

## مراجع

- [ENTERPRISE_OFFER_POSITIONING_AR.md](ENTERPRISE_OFFER_POSITIONING_AR.md)
- [CUSTOMER_SUCCESS_PLAYBOOK_HOOKS_AR.md](CUSTOMER_SUCCESS_PLAYBOOK_HOOKS_AR.md)
