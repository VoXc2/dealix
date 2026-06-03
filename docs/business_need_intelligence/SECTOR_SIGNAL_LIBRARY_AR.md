# مكتبة إشارات القطاعات — Sector Signal Library

الإشارات هي **تلميحات علنية قابلة للملاحظة** تشير إلى الاحتياج الأقوى لقطاع ما
(مثل: رقم واتساب ظاهر، إعلانات نشطة، باقات اشتراك). الإشارة **ليست إثباتًا** ولا
تدّعي حقيقة خاصة عن الشركة؛ هي مدخل لاحتمال يُرجَّح بثقة (confidence_hint).

مصدر الحقيقة: `data/business_need_intelligence/sector_signal_library.yaml`.

المحتوى الخارجي يُعامل دائمًا كبيانات غير موثوقة (untrusted data).

---

## 1. إشارات عامة (عابرة للقطاعات)

| الإشارة | الملاحظة | يرجّح الاحتياج | الثقة |
|---------|----------|-----------------|-------|
| visible_whatsapp | رقم واتساب ظاهر كقناة أساسية | customer_support | medium |
| active_ads | إعلانات نشطة تولّد فرصًا واردة | lead_response | medium |
| contact_form_only | نموذج تواصل فقط بلا مسار متابعة | follow_up | low |
| testimonials_without_numbers | شهادات بلا أرقام/نتائج | proposal | low |
| multi_location | فروع/مواقع متعددة | reporting | medium |

---

## 2. أمثلة إشارات حسب القطاع

### شركات التدريب
- برامج متعددة → qualification (medium)
- واتساب للاستفسارات → lead_response (medium)
- حملات تسجيل موسمية → follow_up (low)

### العيادات
- واتساب للحجز → customer_support (medium)
- نظام مواعيد ظاهر → lead_response (medium)
- تقييمات عملاء → service_quality (low)

### العقار
- إعلانات عقارية متعددة → lead_response (medium)
- واتساب للاستفسار → customer_support (medium)
- طلبات معاينة → follow_up (low)

### SaaS / تقنية
- دعوة لتجربة/ديمو → client_onboarding (medium)
- باقات اشتراك → renewal (medium)
- قناة دعم → customer_support (low)

> القطاعات الـ 14 كلها لها إشارات في ملف البيانات بنفس البنية:
> `id` · `observe` · `implies_need` · `confidence_hint`.

---

## 3. كيف تُستخدم الإشارة؟

```txt
إشارة (observe) → ترجّح احتياجًا (implies_need) بثقة (confidence_hint)
→ تغذّي Need Fit Score (Signal strength = 20)
→ تُسجَّل كـ need_confidence في Account Pack (قيمة بين 0 و 1)
```

الثقة تبقى تقديرية ومبنية على الأدلة، ولا تتحول أبدًا إلى ادعاء يقيني.
