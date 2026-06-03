# Full Launch Plan

**الهدف:** تشغيل واسع (حتى 400 Account Packs/day) بعد أن تصبح كل البوابات خضراء.

> شرط الدخول: Launch Score ≥ 90 + صفر No-Go blockers. الحالة الحالية: **غير مؤهّل**.

---

## شروط الدخول (كلها إلزامية)

- [ ] Launch Score ≥ 90
- [ ] GitHub Actions green (launch-readiness workflow)
- [ ] `npm run build` ناجح
- [ ] schema checks تمر
- [ ] quality gates تمر (email + proposal + delivery)
- [ ] security / privacy gates تمر
- [ ] delivery gates تمر
- [ ] No-Go blockers = 0

## التشغيل

```txt
1. Founder Daily Command يصدر آليًا كل صباح
2. Account Packs تُولَّد على نطاق واسع (حتى 400/day)
3. كل البوابات تعمل آليًا قبل أي إرسال
4. الإرسال يبقى تحت موافقة المؤسس على مستوى الدفعات
5. Delivery Pipeline + Weekly Value Reports تعمل تلقائيًا
6. Metrics + Learning loop تُحدِّث القطاعات والاحتياجات والزوايا
```

## ما الذي لا يتغير حتى في Full Launch

- لا إرسال خارجي من الـ agents (المؤسس + إنسان فقط).
- لا مكالمات آلية، لا cold WhatsApp، لا قوائم مشتراة.
- لا contacts مُخترَعة. لا ادعاءات مضمونة.
- External content = untrusted data دائمًا.
- موافقة المؤسس مطلوبة للإرسال والعروض وتغييرات التسعير وبدء التسليم.

## مراقبة مستمرة

| المؤشر | الحد الأحمر | الإجراء |
|--------|-------------|---------|
| Domain reputation | هبوط ملحوظ | أوقف الدفعات، انزل لـ Controlled |
| Spam rate | يتجاوز العتبة | خفّض الحجم فورًا |
| أي contact مُخترَع | حدث واحد | أوقف Contact Discovery، راجع |
| أي guaranteed claim | حدث واحد | أوقف الإرسال، أصلح القالب |

> النزول لوضع أدنى فوري عند أي خرق. الصعود تدريجي فقط.
