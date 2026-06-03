# بوابة جودة الإيميل — Email Quality Gate

كل draft يُسجَّل من 100 ويمر على شروط رفض صارمة. المنطق منفّذ في
`scripts/lib/commercial.js` (`scoreTotal`, `band`, `emailGate`) ويُشغَّل عبر
`npm run commercial:quality`. التقرير: `reports/quality/DAILY_QUALITY_GATE_REVIEW.md`.

---

## نموذج النقاط (100)

| البند | النقاط |
|-------|------:|
| Personalization | 25 |
| Pain clarity | 20 |
| System fit | 20 |
| CTA clarity | 15 |
| Risk safety | 10 |
| Tone quality | 10 |

## النطاقات (Bands)

```
< 65        = rejected
65 – 74     = needs_rewrite
75 – 84     = approval_queue
85+         = top_priority
```

---

## شروط الرفض الصارمة (Hard Fail)

تُرفض المسودة فورًا — مهما كانت نقاطها — إذا تحقق أي شرط:

| السبب (reason) | الوصف |
|----------------|-------|
| `no_need_card` | لا توجد Client Need Card |
| `no_recommended_system` | لا يوجد نظام موصى به |
| `no_cta` | لا يوجد CTA واضح |
| `no_evidence_level` | لا يوجد مستوى دليل |
| `guaranteed_claim` | ادعاء مضمون (نضمن / 100% / guaranteed) |
| `fake_re_fwd` | عنوان Re:/Fwd: مزيّف بلا محادثة سابقة |
| `unverified_pain_as_fact` | ألم مكتوب كحقيقة مع دليل L0/L1 |
| `internal_module_name_leaked` | تسريب اسم نظام داخلي (id) في النص |
| `suppression_hit` | الشركة/النطاق في قائمة الحجب |
| `prompt_injection_in_source` | حقن تعليمات في نص خارجي مرفق |

---

## شرط دخول Top 100

يدخل draft قائمة الـ Top 100 فقط إذا:

```
score >= 75
AND recommended_system موجود
AND Client Need Card موجودة
AND risk_level != high
AND evidence_level موجود
AND CTA موجود
```

---

## قاعدة اللغة المحترمة

عند L0/L1 نكتب «غالبًا / قد يكون / في هذا النوع من الشركات». لا نكتب «أنتم تعانون
من...» أو «واضح أنكم تخسرون...». الرسالة الأولى يجب أن تكون محترمة وذكية لا مدّعية.
