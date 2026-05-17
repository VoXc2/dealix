# ضمان جودة التسليم / Delivery QA Scorecard

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `checklists/DELIVERY_LEAD_INTELLIGENCE_SPRINT.md` · `DEALIX_STANDARD.md`

---

## الغرض / Purpose

كل Proof Pack يمر على بطاقة جودة من 10 نقاط قبل التسليم النهائي. الهدف: تسليم متّسق، خالٍ من المبالغة، ومتوافق مع الـ non-negotiables.

Every Proof Pack passes a 10-point QA scorecard before final delivery. The goal: consistent delivery, free of exaggeration, and aligned with the non-negotiables.

## القاعدة الحاسمة / The hard rule

أي Proof Pack يسجّل أقل من **8/10** لا يُسلَّم كنسخة نهائية — يجب إصلاحه أولاً ثم إعادة التقييم.

Any Proof Pack scoring below **8/10** cannot be delivered as final — it must be fixed first, then re-scored.

## نقاط التقييم العشر / The 10 checks

| # | الفحص / Check | السؤال / Question | اجتياز / Pass |
|---|---|---|---|
| 1 | المصدر / Source | هل المصدر واضح؟ Is the data source clear and stated? | |
| 2 | المالك / Owner | هل مالك كل بند واضح؟ Is the owner of each item clear? | |
| 3 | حدود الموافقة / Approval | هل حد الموافقة واضح (ماذا يحتاج موافقة قبل أي إرسال)؟ Is the approval boundary clear? | |
| 4 | أثر الدليل / Evidence trail | هل أثر الدليل واضح (مرجع لكل ادعاء)؟ Is the evidence trail clear? | |
| 5 | الإجراءات التالية / Next actions | هل الإجراءات التالية واضحة وقابلة للتنفيذ؟ Are the next actions clear? | |
| 6 | المخاطر / Risks | هل المخاطر مذكورة صراحة؟ Are the risks stated explicitly? | |
| 7 | لا مبالغة / No exaggeration | هل خلا التقرير من أي ادعاء مبالغ فيه؟ Is there no exaggerated claim? | |
| 8 | الترقية / Upsell | هل توجد ترقية منطقية مرتبطة بالنتائج؟ Is there a logical upsell? | |
| 9 | اللغة / Language | هل اللغة مفهومة لغير المتخصص؟ Is the language understandable? | |
| 10 | قابلية التجهيل / Anonymizable | هل يمكن تحويله إلى insight مجهّل دون PII؟ Can it become an anonymized insight? | |

## بطاقة التقييم القابلة للتعبئة / Fill-in scorecard

| # | الفحص / Check | اجتياز؟ / Pass? (✅ / ❌) | ملاحظة الإصلاح / Fix note |
|---|---|---|---|
| 1 | المصدر / Source | | |
| 2 | المالك / Owner | | |
| 3 | حدود الموافقة / Approval | | |
| 4 | أثر الدليل / Evidence trail | | |
| 5 | الإجراءات التالية / Next actions | | |
| 6 | المخاطر / Risks | | |
| 7 | لا مبالغة / No exaggeration | | |
| 8 | الترقية / Upsell | | |
| 9 | اللغة / Language | | |
| 10 | قابلية التجهيل / Anonymizable | | |
| | **المجموع / Total** | **__ / 10** | |
| | **القرار / Decision** | يُسلَّم إذا ≥ 8 / Deliver if ≥ 8 | |

## كيفية الاستخدام / How to use

1. عبّئ بطاقة التقييم بعد إعداد الـ Proof Pack وقبل إرساله للعميل.
2. ضع ✅ أو ❌ لكل فحص، واكتب ملاحظة إصلاح لكل ❌.
3. اجمع النتيجة. إذا أقل من 8، أصلِح البنود الراسبة وأعد التقييم.
4. لا تُسلَّم النسخة النهائية حتى تصل إلى 8/10 على الأقل.

Fill the scorecard after preparing the Proof Pack and before sending it to the client. Mark ✅ or ❌ per check, write a fix note for each ❌, sum the score. If below 8, fix the failed items and re-score. Do not deliver the final version until it reaches at least 8/10.

## ملاحظات الانضباط / Discipline notes

- الفحص 7 يرفض أي رقم نتائج مضمون — النتائج تُوصف كـ `estimated` أو حسب تير `value_os`. راجع `REVENUE_TRUTH_LABELS.md`.
- الفحص 10 يضمن خلو أي insight منشور من PII (أسماء، بريد، هواتف، هويات).
- الفحص 3 يضمن عدم تضمين أي إرسال خارجي دون موافقة صريحة من العميل.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
