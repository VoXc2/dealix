# Sector Testing Matrix — مصفوفة اختبار القطاعات

> قبل التوسع الكامل في قطاع، نختبره في دفعة محدودة. القطاع يثبت نفسه بالردود،
> لا بالافتراض.

---

## المصفوفة

| القطاع | الاحتياج المرشّح | الزاوية | حجم الاختبار | المقياس |
|--------|------------------|---------|-------------:|---------|
| Training Companies | فقدان استفسارات واتساب | Loss framing | 20 | reply_rate |
| Marketing Agencies | ضعف المتابعة | Proof/stat | 20 | reply_rate |
| Clinics | حجوزات ضائعة | Speed | 20 | reply_rate |
| Professional Services | بطء إغلاق الصفقات | Outcome | 20 | reply_rate |

---

## قاعدة الاختبار

```txt
- غيّر القطاع فقط (variables_changed = ["sector"]).
- ثبّت الزاوية والعرض أثناء اختبار القطاع.
- 20 شركة لكل قطاع كحد أدنى للحكم الأولي.
```

---

## الربط بسياسة التوسع

نتيجة الاختبار تُغذّي `reports/scale/SECTOR_EXPANSION_DECISION.md`. لا يُدخل
القطاع في التوسع الكامل إلا إذا:

```txt
1. حقّق النقاط السبع في SECTOR_EXPANSION_POLICY_AR.md.
2. أعطت تجربته المحدودة reply_rate مقبولًا.
```

---

## الحكم

| النتيجة | القرار |
|---------|--------|
| reply_rate قوي | توسّع تدريجيًا |
| متوسط | كرّر بزاوية مختلفة |
| ضعيف | أجّل القطاع |

تُوثّق في `reports/experiments/WEEKLY_REVENUE_EXPERIMENTS.md`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
