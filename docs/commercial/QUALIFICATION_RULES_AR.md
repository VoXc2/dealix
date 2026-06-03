# قواعد التأهيل — Dealix

> الحقيقة المرجعية: rubric التقييم في [`MARKET_PRODUCTION_NAMING_CONVENTIONS.md`](../gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md)
> (Prospect score rubric) · بوابة الاستبعاد [`DISQUALIFICATION_RULES_AR.md`](./DISQUALIFICATION_RULES_AR.md) ·
> حقل `qualified` في [`opportunity.schema.json`](../../schemas/opportunity.schema.json).

المبدأ: نؤهّل لنحمي وقت الطرفين. الفرصة **مؤهَّلة** (`qualified=true`) فقط بعد المرور من بوابة الانسحاب
أولاً، ثم استيفاء الأركان الأربعة. التأهيل شرط مسبق لأي عرض.

---

## 1) بوابة الانسحاب أولاً

قبل أي تأهيل، تمرّ الفرصة على بوابة `evaluate_fit` (القواعد D1–D10 في
[`WALK_AWAY_RULES_AR.md`](./WALK_AWAY_RULES_AR.md)). أي تحقّق لقاعدة استبعاد واحدة ⇐ لا تأهيل.

---

## 2) الأركان الأربعة للتأهيل

| الركن | السؤال | معيار النجاح | الوزن (rubric) |
|-------|--------|---------------|-----------------|
| **تدفّق leads** | هل عندهم استفسارات متكرّرة نرتّبها ونقيسها؟ | تدفّق منتظم موجود | `likely_lead_flow` 15 |
| **صاحب القرار** | هل نصل لمن يعتمد القرار والدفع؟ | وصول واضح لصاحب القرار | `decision_maker_clarity` 15 |
| **القدرة على الدفع** | هل الميزانية ضمن أدنى نطاق `DLX-L1` فأعلى؟ | قدرة دفع مؤكّدة | `payment_ability` 15 |
| **الملاءمة (Fit)** | هل القطاع وفئة الألم ضمن ICP والسلّم؟ | ملاءمة قطاع + ألم واضح | `sector_fit` 20 + `buying_signal` 20 |

عناصر مكمّلة في الـ rubric: `personalization_signal` 10 · `risk_low` 5 (المجموع 100).

---

## 3) عتبة التأهيل

- **مؤهَّل (`qualified=true`):** مرّ بوابة الانسحاب + الأركان الأربعة محقّقة + فئة ألم واحدة محدّدة + إثبات ≥ `observed` لأي ادّعاء كمّي.
- **غير مؤهَّل بعد:** نقص في ركن واحد ⇐ يبقى `qualified=false`، والإجراء التالي عادةً `book_discovery` لإكمال الصورة.
- **التخصيص:** أرضية طابور الموافقة `P1` (شركة + قطاع) على الأقل.

> مثال توضيحي «مثال توضيحي»: في [`opportunities.jsonl`](../../data/commercial/opportunities.jsonl) الفرصة
> `OPP-003` (TrainMe KSA) ما زالت `qualified=false` و`product_match=null` — تحتاج discovery قبل أي مطابقة عرض.

---

## 4) من الإشارة إلى مؤهَّل

```
signal_detected → researched → فحص بوابة الانسحاب
   ├─ مرّ + الأركان الأربعة محقّقة → qualified=true → مطابقة العرض
   └─ نقص ركن → qualified=false → book_discovery أو nurture
```

---

## 5) ربط بالمطابقة والعرض

- بعد التأهيل: مطابقة الألم بالعرض عبر [`OFFER_MATCHING_RULES_AR.md`](./OFFER_MATCHING_RULES_AR.md) و[`PAIN_TO_OFFER_MATRIX_AR.md`](./PAIN_TO_OFFER_MATRIX_AR.md).
- لا عرض دون فرصة مؤهَّلة — راجع [`PROPOSAL_APPROVAL_POLICY_AR.md`](./PROPOSAL_APPROVAL_POLICY_AR.md).

## 6) السلامة عند التأهيل

- لا ادّعاءات ممنوعة في أي ملخّص تأهيل (لا «نضمن»، لا «نضاعف الإيرادات»، لا «بدون مخاطرة»).
- لا بيانات شخصية — أدوار فقط. أي مثال يُوسم «مثال توضيحي».
- كل ادّعاء كمّي يحمل `evidence_level`.

> سطر واحد: بوابة انسحاب أولاً، ثم أربعة أركان (تدفّق leads، صاحب قرار، قدرة دفع، ملاءمة) — وبدونها لا تأهيل ولا عرض.
