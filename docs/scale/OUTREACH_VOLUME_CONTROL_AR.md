# Outreach Volume Control — التحكم في حجم التواصل

> الإرسال ليس مجرد رقم. هو محكوم بصحة الدومين، جودة الردود، ومعدل السبام.
> هذا الملف يحكم **كم نرسل فعليًا** بعد أن ينتج النظام الـ drafts.

---

## مبدأ الفصل

```txt
الإنتاج (Drafts) → يمكن أن يصل 400/يوم من اليوم الأول.
الإرسال (Sends) → يبدأ صغيرًا ويرتفع فقط مع إثبات الجودة و deliverability.
```

---

## سقوف الإرسال حسب الوضع

| Mode | Sends/day | طريقة الإرسال |
|------|----------:|----------------|
| Dry Run | 0 | لا إرسال |
| Soft Launch | 10–25 | يدوي بموافقة |
| Controlled Launch | 25–75 | محكوم بموافقة دفعات |
| Full Launch | controlled only | دفعات محكومة فقط |
| Scale | حسب deliverability | فريق تشغيل + مراقبة |

المصدر: `company_os/scale/scale_state.json` و `company_os/deliverability/deliverability_state.json`.

---

## قواعد رفع الحجم

```txt
1. لا قفزة مفاجئة في الحجم (no sudden volume spike).
2. ارفع تدريجيًا (مثال: +20% كل 3 أيام بحد أقصى).
3. لا ترفع إذا spam rate >= الحد التحذيري.
4. لا ترفع إذا bounce rate مرتفع.
5. لا ترفع إذا Delivery Capacity Utilization > 80%.
```

---

## بوابة الإرسال (Send Gate)

كل دفعة إرسال تحتاج:

```txt
1. SPF / DKIM / DMARC جاهزة.
2. unsubscribe / suppression فعّالة.
3. do-not-contact محترم.
4. لا purchased lists.
5. لا fake Re/Fwd.
6. لا claims مضمونة.
7. موافقة المؤسس على الدفعة.
```

يتحقق منها `python dealix.py deliverability-check`.

---

## التصعيد عند الخطر

| الإشارة | الإجراء |
|---------|---------|
| spam rate ≥ تحذيري | ثبّت الحجم، راجع المحتوى |
| spam rate ≥ الحد الصلب | أوقف الإرسال فورًا |
| ردود سلبية مرتفعة | راجع الزاوية والقائمة |
| bounce مرتفع | نظّف القائمة، تحقق من المصدر |

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
