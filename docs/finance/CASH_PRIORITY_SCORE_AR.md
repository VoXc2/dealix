# Cash Priority Score — درجة أولوية الكاش

> كم هذه الفرصة **سريعة وسهلة** التحوّل إلى نقد؟ درجة من 100 توجّه ترتيب العمل اليومي.

---

## 1. المعايير والأوزان

| المعيار | الوزن | يقيس |
|---------|------:|------|
| Ability to pay | 25 | إشارات عامة على القدرة المالية |
| Urgency | 25 | إلحاح الحاجة الآن |
| Ease of delivery | 20 | سهولة التسليم وقلّة التكاملات |
| Upsell potential | 15 | احتمال التوسّع لاحقًا |
| Contact availability | 15 | جاهزية قناة التواصل |
| **المجموع** | **100** | |

> المخطط: `schemas/cash_priority_score.schema.json` (مجموع المكوّنات = `total_score`).
> البيانات: `data/finance/cash_priority_scores.jsonl`.

---

## 2. النطاقات (Bands)

| المجموع | النطاق | المعنى |
|--------:|--------|--------|
| **80+** | `now` | ابدأ اليوم |
| **60–79** | `this_week` | هذا الأسبوع |
| **<60** | `nurture` | رعاية لاحقة |

---

## 3. ترتيب العيّنة

| الحساب | Pay | Urg | Ease | Upsell | Contact | **Total** | النطاق |
|--------|---:|---:|----:|------:|-------:|---------:|--------|
| `ACC-001` Madar | 19 | 18 | 16 | 12 | 9 | **74** | this_week |
| `ACC-005` Rased | 20 | 16 | 17 | 12 | 9 | **74** | this_week |
| `ACC-002` Tadreeb Plus | 17 | 17 | 18 | 10 | 10 | **72** | this_week |
| `ACC-004` Noor Clinics | 18 | 17 | 16 | 10 | 9 | **70** | this_week |
| `ACC-007` BinaaPro | 18 | 15 | 17 | 11 | 9 | **70** | this_week |
| `ACC-003` Afaq | 15 | 16 | 15 | 9 | 6 | **61** | this_week |
| `ACC-006` Tawteen | 16 | 14 | 14 | 9 | 6 | **59** | nurture |
| `ACC-008` Mohtawa | 12 | 14 | 16 | 10 | 6 | **58** | nurture |

---

## 4. أفضل أول بيع (Fastest Cash)

غالبًا الأسرع تسليمًا والأقل احتياجًا للتكاملات:

```
Proposal & Proof OS   (3,000 SAR)
Follow-up Recovery OS (3,500 SAR)
Executive Command OS  (5,500 SAR)
```

لأنها تعتمد على قوالب ومخرجات سريعة أكثر من تكاملات تقنية.

---

## 5. التحقق الآلي

`scripts/account-factory-check.mjs` يتحقق أن مجموع المكوّنات الخمسة يساوي `total_score` لكل سجل.

---

*Cash Priority Score | الإصدار 1.0 | آخر تحديث: 2026-06-03*
