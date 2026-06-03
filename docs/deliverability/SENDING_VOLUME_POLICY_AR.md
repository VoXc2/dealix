# Sending Volume Policy — سياسة حجم الإرسال

> الحجم يرتفع بإثبات الجودة و deliverability، لا بالحماس. القفزة المفاجئة في
> الحجم من أسرع طرق حرق الدومين.

---

## سقوف الحجم حسب الوضع

| Mode | Sends/day |
|------|----------:|
| Dry Run | 0 |
| Soft Launch | 10–25 |
| Controlled Launch | 25–75 |
| Full Launch | controlled only |
| Scale | حسب deliverability |

المصدر: `company_os/scale/scale_state.json`.

---

## قواعد الرفع التدريجي (Warm-up)

```txt
1. ابدأ صغيرًا (10–25/يوم) حتى مع دومين جاهز.
2. ارفع تدريجيًا فقط بعد استقرار spam/bounce تحت الحدود.
3. حد أقصى للزيادة: ~+20% كل 3 أيام (لا قفزات).
4. أي يوم يتجاوز فيه السبام التحذير → ثبّت ولا ترفع.
```

---

## بوابة الدفعة (Batch Gate)

كل دفعة إرسال:

```txt
- ضمن سقف الوضع الحالي.
- بعد فحص deliverability ناجح.
- بموافقة المؤسس على الدفعة.
- مع احترام suppression / do-not-contact.
```

يتحقق `check_deliverability_readiness.py` أن `current_daily_volume ≤ max_daily_volume_for_mode`.

---

## التصعيد

| الإشارة | الإجراء |
|---------|---------|
| سبام ≥ تحذيري | ثبّت الحجم |
| سبام ≥ صلب | أوقف الإرسال |
| bounce مرتفع | نظّف القائمة |
| قفزة مفاجئة مكتشفة | ارجع لآخر حجم آمن |

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
