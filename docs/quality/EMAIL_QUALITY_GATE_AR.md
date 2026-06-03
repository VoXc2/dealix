# بوابة جودة الإيميل (Email Quality Gate)

> لا يدخل إيميل إلى قائمة الاعتماد إلا بعد تقييم وبوابة. الـ AI يقيّم، المؤسس يعتمد.
> الكود: `scripts/draft-quality-gate.js` + `scripts/commercial-lib.js` · الرُّبريك: `company_os/commercial/draft_scoring_rubric.json`

---

## 1. التقييم (من ١٠٠)

| البند | النقاط |
|-------|------:|
| Personalization | 25 |
| Pain clarity | 20 |
| System fit | 20 |
| CTA clarity | 15 |
| Risk safety | 10 |
| Tone quality | 10 |

---

## 2. الحالات حسب الدرجة

```txt
أقل من 65  = rejected
65–74      = needs_rewrite
75–84      = approval_queue
85+        = top_priority
```

---

## 3. شروط دخول Top 100

يدخل فقط إذا:

```txt
score >= 75
recommended_system واضح
Client Need Card موجود
risk_level ليس high
evidence_level موجود
CTA واضح
```

---

## 4. متى تفشل البوابة (Gate fails if)

البوابة **تفشل** إذا تحقق أي مما يلي (fail conditions):

```txt
لا يوجد Client Need Card
لا يوجد recommended_system
لا يوجد CTA
يوجد ادعاء مضمون (guaranteed claim)
يوجد Re/Fwd مزيّف (fake thread)
ألم مكتوب كحقيقة بدون دليل (pain written as fact)
تسريب اسم وحدة داخلية (internal module name)
الشركة ضمن suppression
```

> أي فشل = المسودة لا تُرسل، ولا تدخل Top Queue.

---

## 5. مستويات الدليل والصياغة

| المستوى | المصدر |
|---------|--------|
| L0 | تخمين قطاعي |
| L1 | موقع الشركة |
| L2 | صفحة خدمة/وظيفة/خبر |
| L3 | أكثر من مصدر عام متوافق |
| L4 | بيانات من الشركة نفسها |

إذا كان الدليل L0 أو L1 → استخدم الصياغة الاحترازية: «غالبًا / قد يكون / في هذا النوع من الشركات». لا تكتب «أنتم تعانون / عندكم مشكلة».

**صحيح:** «في شركات التدريب، غالبًا جزء من الاستفسارات يحتاج متابعة منظمة بعد أول تواصل.»
**خطأ:** «واضح أنكم تخسرون تسجيلات بسبب ضعف المتابعة.»

---

## 6. المخرج

`reports/quality/DAILY_QUALITY_GATE_REVIEW.md` + `company_os/commercial/draft_scores.json`.

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03*
