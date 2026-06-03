# Account Scoring Model — نموذج ترتيب الحسابات (Top 100)

> كل Account Pack يأخذ درجة من **100**. الترتيب يحدد أي الحسابات تدخل قائمة **Top 100** للمراجعة والاعتماد.

---

## 1. المعايير والأوزان

| المعيار | الوزن | ما الذي يقيسه |
|---------|------:|----------------|
| Pain clarity | 25 | وضوح الألم وارتباطه بنظام محدد |
| Contact availability | 20 | وجود قناة تواصل عامة وثقة بها |
| System fit | 20 | مدى ملاءمة النظام الموصى به للحالة |
| Ability-to-pay signal | 15 | إشارات عامة على القدرة على الدفع |
| Evidence level | 10 | مستوى الدليل (L0→L4) |
| Low risk | 10 | انخفاض مخاطر الحالة |
| **المجموع** | **100** | |

> المخطط: `schemas/account_scoring.schema.json` (مجموع المكوّنات يجب أن يساوي `total_score`).

---

## 2. الشرائح (Tiers)

| المجموع | الشريحة | الإجراء |
|--------:|---------|---------|
| **85+** | Top Priority | يدخل Top 100 + مرشح إرسال/اتصال |
| **75–84** | Approval Queue | مراجعة المؤسس قبل الإرسال |
| **65–74** | Rewrite / More Research | يحتاج بحثًا أو إعادة صياغة |
| **<65** | Reject / Nurture | لا يُرسل الآن؛ قائمة رعاية |

---

## 3. شروط الاستبعاد من Top 100 (Hard Gates)

لا يدخل الحساب Top 100 إذا تحقق أيٌّ مما يلي:

```
- لا يوجد recommended_system
- لا يوجد evidence_level
- لا يوجد contact route (best_contact_route)
- risk_level = high
- يوجد ادعاء غير مؤكد مكتوب كأنه حقيقة
- الشركة في suppression list (do_not_contact = true)
```

---

## 4. الترتيب الحالي للعيّنة (8 حسابات)

| الحساب | Pain | Contact | Fit | Pay | Evid | Risk | **المجموع** | الشريحة |
|--------|----:|-------:|---:|---:|----:|----:|----------:|---------|
| `ACC-005` Rased | 23 | 15 | 20 | 13 | 9 | 9 | **89** | Top Priority |
| `ACC-001` Madar | 23 | 15 | 19 | 13 | 8 | 9 | **87** | Top Priority |
| `ACC-002` Tadreeb Plus | 22 | 14 | 19 | 12 | 8 | 9 | **84** | Approval Queue |
| `ACC-007` BinaaPro | 22 | 14 | 19 | 12 | 8 | 9 | **84** | Approval Queue |
| `ACC-004` Noor Clinics | 21 | 15 | 18 | 12 | 8 | 9 | **83** | Approval Queue |
| `ACC-003` Afaq | 19 | 9 | 17 | 11 | 8 | 7 | **71** | Rewrite / Research |
| `ACC-006` Tawteen | 17 | 9 | 16 | 11 | 6 | 7 | **66** | Rewrite / Research |
| `ACC-008` Mohtawa | 15 | 9 | 15 | 10 | 5 | 7 | **61** | Reject / Nurture |

> ملاحظة: `ACC-003`/`ACC-006`/`ACC-008` خرجت من Top Priority بسبب ضعف قناة التواصل (C1) و/أو انخفاض الدليل (L0/L1) — وهذا بالضبط ما يجب أن يفعله النموذج: يفضّل الحسابات القابلة للتنفيذ فعليًا.

---

## 5. العلاقة مع Cash Priority

- **Account Score (100):** هل الحساب *مؤهل وجاهز*؟ (جودة الفرصة)
- **Cash Priority Score (100):** كم هو *سريع وسهل التحول إلى كاش*؟ (راجع `docs/finance/CASH_PRIORITY_SCORE_AR.md`)

القرار اليومي يستخدم الاثنين: نبدأ بحسابات عالية الجودة **و** عالية أولوية الكاش.

---

## 6. التقارير المرتبطة

- `reports/account_intelligence/TOP_100_ACCOUNT_QUEUE.md`
- `reports/account_intelligence/ACCOUNT_PACK_QUALITY_REVIEW.md`
- `reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md`

---

*Account Scoring Model | الإصدار 1.0 | آخر تحديث: 2026-06-03*
