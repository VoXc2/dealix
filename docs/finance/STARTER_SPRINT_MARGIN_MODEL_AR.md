# Starter Sprint Margin Model — نموذج هامش الـ Sprints الافتتاحية

*كم يكلّف كل Sprint وكم يربح، لاتخاذ قرار تسعير واعٍ.*
*آخر تحديث: 2026-06-03 · العملة: SAR*

> ملاحظة: الأرقام أدناه **افتراضات تخطيطية** (assumptions) لاتخاذ القرار، وليست
> التزامًا ماليًا. القرار النهائي للتسعير بشري دائمًا (راجع مصفوفة الصلاحيات).

---

## الأسعار الافتتاحية (Starter Prices)

| النظام | First Sprint | السعر | المدة |
|--------|--------------|------:|------:|
| Revenue OS | Revenue Leakage Sprint | 4,500 | 5 أيام |
| Executive Command OS | Daily Command Sprint | 5,500 | 7 أيام |
| Follow-up Recovery OS | 7-Day Follow-up Recovery Sprint | 3,500 | 7 أيام |
| WhatsApp Client OS | WhatsApp Flow Sprint | 4,500 | 7 أيام |
| Proposal & Proof OS | Proposal & Proof Sprint | 3,000 | 5 أيام |

---

## نموذج التكلفة (Assumptions)

```txt
تكلفة التسليم المتغيّرة لكل Sprint  ≈ 20%–35% من السعر (وقت + أدوات)
الهامش الإجمالي المستهدف             ≈ 65%–80%
```

| النظام | السعر | تكلفة تقديرية (30%) | هامش تقديري |
|--------|------:|--------------------:|------------:|
| Revenue OS | 4,500 | ~1,350 | ~3,150 |
| Executive Command OS | 5,500 | ~1,650 | ~3,850 |
| Follow-up Recovery OS | 3,500 | ~1,050 | ~2,450 |
| WhatsApp Client OS | 4,500 | ~1,350 | ~3,150 |
| Proposal & Proof OS | 3,000 | ~900 | ~2,100 |

---

## فرصة اليوم (من التشغيل الحالي)

Top 20 send candidates (5 حسابات) — قيمة pipeline لأول Sprint:

```txt
TrainMe 4,500 + BrightSmile 4,500 + TechVenture 5,500 + LegalEdge 3,000 + Digital Rise 4,500
= 22,000 SAR
```

بافتراض هامش 70%: **~15,400 SAR** هامش محتمل إذا تحوّلت الخمسة.

> هذه قيمة *فرصة* وليست إيرادًا محقّقًا. التحقّق اليومي في
> `reports/finance/DAILY_REVENUE_OPPORTUNITY_REPORT.md`.

---

## مبادئ مالية

```txt
- لا قرار تسعير آلي — موافقة المؤسس إلزامية.
- السعر الافتتاحي مدخل للعلاقة، والقيمة الأكبر في retainer/renewal بعد الإثبات.
- كل Sprint له acceptance gate قبل اعتباره مكتملًا (راجع جاهزية التسليم).
```
