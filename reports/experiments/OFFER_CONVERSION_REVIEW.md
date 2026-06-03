# Offer Conversion Review — مراجعة تحويل العروض

*Date: 2026-06-03 | Policy: `docs/experiments/OFFER_TESTING_POLICY_AR.md`*

---

## العروض المختبَرة

| العنصر | Control | Variant | المقياس | الحالة |
|--------|---------|---------|---------|--------|
| Offer shape | diagnostic first | Sprint 7 days | close_rate | قيد الاختبار (EXP-003) |
| Price | 3,000 starter | 4,500 starter | close_rate | مخطّط |
| CTA | مكالمة 15 دقيقة؟ | أرسل Mini Proposal؟ | positive_reply_rate | قيد الاختبار (EXP-002) |
| Proof | checklist | sample output | positive_reply_rate | مخطّط |

---

## النتائج (تُحدَّث)

| العرض | عروض مُرسلة | مغلقة | close_rate | الحكم |
|-------|-----------:|------:|----------:|-------|
| Sprint 7 days | — | — | — | قيد الجريان |
| diagnostic first | — | — | — | control |

> القيم الحالية في السعر: Revenue Intelligence Sprint = 2,500 SAR (مبدئي
> للحصول على شهادات)، مع اختبار نطاقات أعلى لاحقًا ضمن قرار المؤسس.

---

## ضوابط التسعير

```txt
- التسعير ضمن نطاق معتمد فقط.
- لا وكيل يغيّر السعر (can_change_price = false).
- تغيير السعر في التجربة = قرار مؤسس موثّق.
```

---

## الحكم

```txt
- ثبّت العرض الذي يرفع close_rate بوضوح.
- لا تغيّر أكثر من عنصر واحد في العرض في تجربة واحدة.
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
