# محاذاة Wave 13 مع Landing وبوابة العميل

**التاريخ:** 2026-05-10  
**الغرض:** توثيق كيف تنعكس طبقة Full Ops (Wave 13) في الواجهات العامة دون ادّعاءات خارج `no_overclaim`.

## أين يظهر Wave 13 للعميل

| القدرة | مسار تقني | واجهة عميل |
|--------|-----------|-------------|
| كتالوج الخدمات السبع | `api/routers/service_catalog.py` + `registry.py` | صفحات تسعير/باقات إذا كانت تقرأ من API |
| تسليمات Deliverables | `api/routers/deliverables.py` | يمكن ربطها بالبوابة لاحقاً |
| مقاييس لوحة أعمال | `api/routers/business_metrics_board.py` | تقارير / ECC |
| اختناقات | `api/routers/bottleneck_radar.py` | لوحة تشغيل |
| درجات نجاح العميل (٥ درجات) | `api/routers/customer_success_scores.py` | قراءات تقديرية `is_estimate=True` |
| بوابة عميل | `GET /api/v1/customer-portal/{handle}` | [`landing/customer-portal.html`](../../landing/customer-portal.html) + [`landing/assets/js/customer-dashboard.js`](../../landing/assets/js/customer-dashboard.js) |

## سلوك الواجهة (customer-dashboard.js)

- **DEMO / PRE-LAUNCH / LIVE:** يُحدَّد بـ `?org=` و `?access=`.
- **LIVE:** يجلب البوابة ثم يملأ بطاقات التشغيل، الخط الزمني، الرادار، و**بطاقات Wave 13 الأربع** (`renderW13FourCards`) عند توفر الحقول.
- **تدهور البيانات:** أشرطة `cp-degraded-banner` و `w13-degraded-banner` عند `insufficient_data` — يجب ألا تُقرأ كفشل منتج بل كحاجة بيانات/تكامل.

## تدقيق نصوص (سلامة الحوكمة)

- تمت مراجعة نسخة DEMO في البوابة: أي ذكر لـ «تلقائي» يجب أن **لا يُفهم كإرسال خارجي بارد**. عند الحاجة تُستبدل الصياغة بـ: تأهيل **داخل النظام**، **مسودة للموافقة** على `/decisions.html`.
- ملفات أخرى (`trust.html`, `start.html`, `subprocessors.html`) تتسق عموماً مع `no_cold_whatsapp` وعدم الضمان المطلق.

## قائمة تحقق سريعة عند إضافة قسم جديد في Landing

1. هل النص يتوافق مع `hard_gates` لأقرب `service_id`؟
2. هل يُشار إلى **موافقة** قبل أي إرسال خارجي؟
3. هل الأرقام **تقديرية** أو مرتبطة بـ KPI مذكور في `registry.py`؟
4. هل يحتاج تحديث [no_overclaim.yaml](../../dealix/registers/no_overclaim.yaml)؟

## مراجع

- [docs/WAVE13_FULL_OPS_AUDIT.md](../WAVE13_FULL_OPS_AUDIT.md)
- [DEALIX_ROLE_SERVICE_LADDER_AR.md](DEALIX_ROLE_SERVICE_LADDER_AR.md)
