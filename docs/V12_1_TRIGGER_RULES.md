# قواعد تفعيل V12.1 (بدون V13)

**V13 ممنوع** حتى يوجد إثبات إيراد وتشغيل حقيقي — راجع [`V13_NOT_ALLOWED_REVENUE_FIRST_REALITY.md`](V13_NOT_ALLOWED_REVENUE_FIRST_REALITY.md).

## يُسمح ببدء V12.1 عند تحقق واحد على الأقل

- `payment_received` موثّق خارج الريبو، أو
- `written_commitment_received` موثّق، أو
- `delivery_session_started` (خطة تسليم مفعّلة مع العميل)، أو
- `proof_event` من عميل حقيقي (غير تجريبي داخلي)

## نطاق V12.1 المسموح

- سجلات دورة حياة عميل (خارج الريبو أو عبر واجهات موجودة بدون PII في git)
- تأكيد دفع يدوي
- قوالب case study **بعد موافقة عميل**
- تقرير أسبوعي للمؤسس من بيانات حقيقية

## ممنوع في V12.1

- بوابات إرسال حي جديدة
- شحن Moyasar live بدون PR وسياسة صريحة
- أتمتة LinkedIn أو scraping
- تسمية الإصدار V13
