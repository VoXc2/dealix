# Proposal Approval Gate — بوابة اعتماد العروض

العرض المصغّر **يفشل** ولا يدخل طابور الإرسال إذا تحقق أي مما يلي.

---

## 1. شروط الفشل

```
لا يوجد starter_price
لا يوجد deliverables (أو أقل من 3)
لا يوجد timeline
لا يوجد required_inputs
approval_required ≠ true
يوجد ادعاء مضمون (نضمن/نضاعف/100%/guarantee…)
```

---

## 2. مسار الاعتماد

```
عرض مولّد (draft)
   → يجتاز البوابة؟ لا  → يُعاد للصياغة/يُرفض
   → نعم → approval_queue
        → مراجعة المؤسس
             → موافقة → approved → (إرسال يدوي/معتمد) → sent
             → رفض   → rejected (مع سبب)
```

يتوافق هذا مع `company_os/governance/agent_permissions.md`: الوكلاء يصيغون، والمؤسس يعتمد التسعير والإرسال.

---

## 3. التحقق الآلي

`validate_account_intelligence.py` يفحص لكل 400 عرض:
- وجود `starter_price_sar` صحيح (> 0).
- `approval_required === true`.
- `deliverables.length ≥ 3`.
- خلو `why_this_system` والمخرجات من ادعاءات مضمونة.

أي مخالفة = فشل التحقق وكود خروج ≠ 0.

---

## 4. التسعير

- الأسعار الافتتاحية ثابتة لكل نظام (3,000–5,500 ريال) وتأتي من `dealix_account_lib.SYSTEMS`.
- أي تعديل سعري قرار بشري (Founder)، ولا يتخذه وكيل.

---

*Version 1.0*
