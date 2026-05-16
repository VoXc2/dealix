# 📨 Dealix — Today Warm Queue (First 5)

**Goal:** تنفيذ أول 5 تواصلات دافئة بصيغة **manual send + approval-first + evidence logging**.

## قواعد التنفيذ

- لا يوجد أي إرسال تلقائي.
- قبل الإرسال: الحالة `prepared_not_sent` (L2).
- بعد الإرسال اليدوي: الحالة `sent` (L4) مع timestamp ومصدر القناة.
- الردود تُصنّف يدويًا (`replied_interested` أو غيره).
- أي خطوة scope/invoice يجب أن تمر عبر موافقة صريحة.

---

## Message 1/5 — Abdullah Al-Assiri (Lucidya)

**Platform:** LinkedIn DM  
**State now:** `prepared_not_sent`

```
السلام عليكم عبدالله،

أنا سامي وأبني Dealix كتشغيل محكوم للإيراد والذكاء الاصطناعي للشركات السعودية.

نساعد الفرق التي تستخدم AI أو RevOps بدون حدود واضحة للمصدر والموافقة والإثبات،
ثم نحول ذلك إلى قرارات قابلة للقياس (وليس أتمتة عشوائية).

إذا مناسب لك، أحب آخذ 20 دقيقة وأعرض عليك نموذج Diagnostic سريع على حالة قريبة من واقعكم.
```

---

## Message 2/5 — Ahmad Al-Zaini (Foodics)

**Platform:** LinkedIn DM  
**State now:** `prepared_not_sent`

```
الله يسعدك أحمد،

أنا سامي من Dealix. تموضعنا: Governed Revenue & AI Operations.

التركيز عندنا ليس "AI automation" فقط، بل تشغيل الإيراد عبر:
مصدر واضح + موافقة + دليل + قرار + أثر قابل للقياس.

هل يناسبك 20 دقيقة لنقارن هذا الإطار على سيناريو نمو B2B قريب من Foodics؟
```

---

## Message 3/5 — Nawaf Hariri (Salla)

**Platform:** X DM أو LinkedIn  
**State now:** `prepared_not_sent`

```
أستاذ نواف،

أبني Dealix كطبقة تشغيل محكومة لفرق الإيراد والـ AI:
Decision passports + approval boundaries + proof packs.

الفكرة: قبل أي تنفيذ خارجي، نضمن وضوح المصدر والحوكمة ثم نقيس القيمة الفعلية.

إذا مناسب، 20 دقيقة لمراجعة Diagnostic زاويته B2B service teams داخل منظومة سلة.
```

---

## Message 4/5 — Hisham Al-Falih (Lean)

**Platform:** LinkedIn DM  
**State now:** `prepared_not_sent`

```
هشام السلام عليكم،

أنا سامي من Dealix. نشتغل على Governed Revenue & AI Operations للفرق التي تحتاج:
ضبط قرارات الإيراد + AI governance + evidence trail قابل للتدقيق.

أحب أشاركك إطار تشخيص سريع يوضح كيف نغلق فجوة "التنفيذ السريع بدون حوكمة".
هل يناسبك لقاء 20 دقيقة هذا الأسبوع؟
```

---

## Message 5/5 — Ibrahim Manna (BRKZ)

**Platform:** LinkedIn DM  
**State now:** `prepared_not_sent`

```
إبراهيم مرحبًا،

أنا سامي وأبني Dealix: تشغيل إيراد وذكاء اصطناعي بحوكمة وموافقات وأدلة.

نشتغل مع الفرق التي لديها pipeline/AI activity لكن ينقصها:
source clarity + approval boundaries + proof of value.

إذا مناسب، 20 دقيقة أعرض عليك Diagnostic framework ونرى هل يناسب سياق BRKZ.
```

---

## Evidence Logging Template (بعد كل إرسال)

حدّث السجل الداخلي لكل جهة:

- `state`: `sent`
- `sent_at`: `YYYY-MM-DD HH:MM`
- `channel`: `linkedin_dm` أو `x_dm`
- `founder_confirmed`: `true`
- `next_followup_at`: `+2 days`

## Follow-up cadence

| Day | State target | Action |
|-----|--------------|--------|
| +2 | `sent` | bump محترم |
| +5 | `replied_interested` أو `sent` | value-add مختصر |
| +10 | `sent` | close-loop محترم |

## منع الحوادث

- لا claim revenue قبل `invoice_paid`.
- لا نشر case study أو proof خارجي بدون موافقة.
- لا رفع مستوى evidence دون حدث فعلي موثق.
