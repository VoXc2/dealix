# Controlled Launch Plan

**الهدف:** تشغيل يومي مضبوط مع بوابات جودة تنفيذية تعمل آليًا قبل أي إرسال.

> شرط الدخول: Launch Score ≥ 85 + كل بوابات الجودة تعمل. الحالة الحالية: **غير مؤهّل**.

---

## شروط الدخول

- [ ] Launch Score ≥ 85
- [ ] Top 100 Account Queue يعمل ويُحدَّث يوميًا
- [ ] Contact Discovery لا يخترع (confidence + source مطلوبان)
- [ ] Email Quality Gate تنفيذي (يرفض الادعاءات + يفرض unsubscribe)
- [ ] Call Brief Queue يعمل
- [ ] Delivery Pipeline يعمل مع Acceptance Gates

## التشغيل اليومي

```txt
1. Founder Daily Command يصدر صباحًا (mode + score + blockers + candidates)
2. Top 100 Queue → اختيار المرشّحين
3. Email Quality Gate يمر على كل مسودّة آليًا
4. المؤسس يوافق على دفعة الإرسال
5. Call Briefs تُجهّز للمرشّحين الساخنين
6. Mini Proposals → بوابة موافقة → إرسال يدوي
7. Delivery يبدأ فقط بعد اكتمال inputs
```

## البوابات الإلزامية

| البوابة | الشرط |
|---------|-------|
| Email Quality Gate | لا guaranteed claims · unsubscribe موجود · suppression نظيف |
| Contact Discovery Gate | كل contact له مصدر عام + درجة ثقة |
| Proposal Gate | موافقة المؤسس قبل أي عرض/تسعير |
| Delivery Gate | inputs مكتملة + acceptance criteria واضحة |

## Deliverability (بريد بارد)

- SPF + DKIM مضبوطة، و DMARC للمرسلين بحجم أكبر.
- one-click unsubscribe للرسائل التسويقية.
- مراقبة spam rate والإبقاء عليه منخفضًا.
- حجم تدريجي (warm-up) — لا دفعات كبيرة فجأة.

## Exit Criteria للانتقال إلى Full Launch

- [ ] Launch Score ≥ 90
- [ ] كل الفحوصات خضراء في GitHub Actions
- [ ] security/privacy + delivery gates تمر
- [ ] استقرار المقاييس على أسبوع كامل

راجع `docs/launch/FULL_LAUNCH_PLAN_AR.md`.
