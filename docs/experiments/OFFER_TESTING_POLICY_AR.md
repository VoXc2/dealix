# Offer Testing Policy — سياسة اختبار العروض

> العرض هو ما نبيعه وكيف نسعّره ونؤطّره. نختبر عنصرًا واحدًا من العرض في كل
> تجربة (الشكل أو السعر أو الإثبات أو الـ CTA).

---

## ما الذي نختبره؟

| العنصر | مثال control | مثال variant |
|--------|--------------|--------------|
| Offer shape | diagnostic first | Sprint 7 days |
| Price | 3,000 starter | 4,500 starter |
| CTA | "مكالمة 15 دقيقة؟" | "أرسل Mini Proposal؟" |
| Proof | checklist | sample output |
| Buyer | Marketing Manager | Founder |

---

## قاعدة الاختبار

```txt
- غيّر عنصرًا واحدًا من العرض فقط.
- ثبّت القطاع والزاوية أثناء اختبار العرض.
- المقياس الأساسي: close_rate (أو positive_reply_rate للـ CTA).
```

---

## ضوابط التسعير

```txt
- التسعير ضمن نطاق معتمد فقط.
- لا وكيل يغيّر السعر (can_change_price = false).
- تغيير السعر في التجربة = قرار مؤسس موثّق.
```

---

## بنية تجربة العرض

```txt
type: "offer" | "price" | "cta" | "proof" | "buyer"
control: <العنصر الحالي>
variants: <عنصر واحد جديد>
metric: close_rate | positive_reply_rate
requires_approval_for_send: true
```

---

## الحكم والتوثيق

| النتيجة | القرار |
|---------|--------|
| variant أفضل بوضوح | حدّث العرض الافتراضي |
| لا فرق واضح | أبقِ control، جرّب عنصرًا آخر |
| variant أسوأ | تراجع وثبّت control |

تُوثّق في `reports/experiments/OFFER_CONVERSION_REVIEW.md`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
