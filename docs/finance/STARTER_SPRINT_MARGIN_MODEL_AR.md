# Starter Sprint Margin Model — نموذج هامش الـ Sprint الافتتاحي

> لا تتوسّع بلا هامش. كل فرصة تُقدّر بسعرها الافتتاحي، وتعقيد تسليمها، وساعاتها، وتلميح هامشها.

---

## 1. حقول الاقتصاد لكل فرصة

```
expected_starter_price        السعر الافتتاحي المتوقع (SAR)
delivery_complexity           low / medium / high
estimated_delivery_hours      ساعات تقديرية لأول Sprint
gross_margin_hint             تلميح هامش إجمالي
upsell_potential              احتمال التوسّع
cash_priority                 درجة أولوية الكاش (راجع CASH_PRIORITY_SCORE_AR.md)
```

---

## 2. الأنظمة الخمسة — سعر/تعقيد/هامش

| النظام | السعر الافتتاحي | تعقيد التسليم | ساعات تقديرية | تلميح الهامش |
|--------|---------------:|:-------------:|:-------------:|:------------:|
| Proposal & Proof OS | 3,000 | منخفض | 10–16 | مرتفع |
| Follow-up Recovery OS | 3,500 | منخفض–متوسط | 14–22 | مرتفع |
| Revenue Operating System | 4,500 | متوسط | 18–28 | متوسط–مرتفع |
| WhatsApp Client OS | 4,500 | متوسط | 18–30 | متوسط |
| Executive Command OS | 5,500 | متوسط | 20–32 | متوسط–مرتفع |

> القيم تقديرية للتخطيط. التسعير النهائي **قرار بشري**.

---

## 3. قاعدة الهامش (Margin Rule)

```
gross_margin_hint = (starter_price − (estimated_hours × blended_rate)) / starter_price
```

- إن نزل التلميح تحت العتبة المقبولة → الفرصة تُراجَع قبل الالتزام.
- نُفضّل في البداية الأنظمة **منخفضة التعقيد** (Proposal & Proof، Follow‑up) لتسريع الكاش وبناء الإثباتات.

---

## 4. أولوية البدء (Sequencing)

```
1) فرص this_week / now في Cash Priority
2) أنظمة منخفضة التعقيد أولاً
3) حسابات Top 100 ذات قناة تواصل C2+
```

التقرير اليومي: `reports/finance/DAILY_REVENUE_OPPORTUNITY_REPORT.md`.

---

## 5. الارتباط بالاقتصاد القائم

يتكامل هذا النموذج مع `company_os/finance/unit_economics.md` و`revenue_scorecard.csv` الموجودين، فيضيف طبقة **تقدير الفرصة قبل البيع** فوق طبقة **قياس الأداء بعد البيع**.

---

*Starter Sprint Margin Model | الإصدار 1.0 | آخر تحديث: 2026-06-03*
