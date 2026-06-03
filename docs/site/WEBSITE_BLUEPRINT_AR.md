# Website Blueprint — مخطط الموقع

*مواصفة بنية الموقع لتحويل الزائر إلى Mini Proposal. (مواصفة — لم تُطبَّق على تطبيق React بعد.)*
*آخر تحديث: 2026-06-03*

> ملاحظة صادقة: تطبيق الويب الحالي في `src/` (صفحات Landing/Dashboard/...). هذا
> المستند **مواصفة** للبنية المستهدفة؛ لم نعدّل كود React هنا لتجنّب كسر البناء.
> التنفيذ مهمة لاحقة منفصلة.

---

## المسار

```txt
Home → Systems → System Page → Diagnostic → Mini Proposal → Contact
```

## الصفحة الرئيسية

```txt
1. Hero قوي
2. مشكلة الشركات
3. الأنظمة الخمسة
4. كيف نشتغل
5. أسعار افتتاحية
6. Diagnostic CTA
7. أمثلة Outputs
8. FAQ
9. CTA نهائي
```

## صفحة كل نظام

```txt
Hero · Pain · Who it is for · When you need it · What you get ·
First Sprint · Delivery Pack · Required Inputs · Acceptance Criteria ·
Starter Price · FAQ · CTA
```

محتوى كل نظام يأتي من `docs/systems/DEALIX_FIVE_SYSTEMS_AR.md`.

## صفحة Diagnostic

تسأل:

```txt
ما نوع الشركة؟
أين أكبر تعطّل الآن؟
هل عندكم leads؟
هل واتساب قناة مهمة؟
هل العروض متكررة؟
هل الإدارة تحتاج تقرير يومي؟
ما هدفك خلال 14 يوم؟
```

وتُخرج:

```txt
Recommended System · Why · First Sprint · Starter Price ·
Required Inputs · Mini Proposal Draft
```

> منطق التوصية يطابق «قاعدة الاختيار» في وثيقة الأنظمة الخمسة.

---

## ربط الموقع بالمصنع (مستقبلي)

```txt
Diagnostic submission → website lead → يظهر في DAILY_SUPER_COMMAND (Website leads)
Contact form          → website lead → نفس المسار
```

الحالة الحالية في `reports/founder/DAILY_SUPER_COMMAND.md` تحت «Website leads» = 0
(غير مربوط بعد).
