# ضمان جودة المبيعات / Sales Quality Assurance
<!-- COMMERCIAL EMPIRE | Owner: Founder | Date: 2026-05-17 -->
> القانون / Canonical: see [docs/quality/QA_DELIVERY_RUBRIC_AR.md](../quality/QA_DELIVERY_RUBRIC_AR.md)

## 1. المبدأ / Principle

**العربية:** جودة المبيعات تُقاس أسبوعيًا، لا تُفترَض. كل أسبوع نراجع **5 محادثات بيع** مقابل معايير ثابتة. الهدف ليس معاقبة البائع — بل حماية العميل والعلامة من وعد خطير أو ادعاء غير مدعوم. كل رقم يحمل تصنيف حقيقة: تقدير / ملحوظ / مؤكَّد من العميل / مؤكَّد بالدفع.

**English:** Sales quality is measured weekly, not assumed. Each week we review **5 sales conversations** against fixed criteria. The goal is not to punish the salesperson — it is to protect the customer and the brand from a dangerous promise or an unsupported claim. Every metric carries a truth label: Estimate / Observed / Client-confirmed / Payment-confirmed.

## 2. المعايير الأسبوعية / Weekly Criteria

**العربية:** لكل محادثة نسأل:
- هل بدأنا بالألم؟
- هل عرضنا إثباتًا (Proof)؟
- هل خفّضنا النطاق — لا السعر؟
- هل طرحنا سؤال إغلاق؟
- هل سجّلنا خطوة تالية؟
- هل وعدنا بشيء خطير؟

**English:** For each conversation we ask:
- Did we start with the pain?
- Did we show Proof?
- Did we reduce the scope — not the price?
- Did we ask a closing question?
- Did we record a next action?
- Did we promise anything dangerous?

## 3. الروبرِك المُقيَّم / The Scored Rubric

| # | المعيار / Criterion | 2 — كامل / Full | 1 — جزئي / Partial | 0 — غائب / Absent |
|---|---|---|---|---|
| 1 | البدء بالألم / start with pain | فُتحت المحادثة بمشكلة العميل / opened on the buyer's problem | ذُكر الألم متأخرًا / pain mentioned late | بدأنا بالعرض أو السعر / opened on offer or price |
| 2 | عرض الإثبات / show Proof | عُرض Proof Pack أو عيّنة حقيقية / showed a Proof Pack or real sample | إشارة عامة للإثبات / vague reference to proof | لا إثبات / no proof |
| 3 | خفض النطاق لا السعر / reduce scope not price | عُرض نطاق مصغّر بسعر معلن ثابت / offered a reduced scope at the posted price | تردّد بين الاثنين / wavered between the two | عُرض خصم على السعر / offered a price discount |
| 4 | سؤال الإغلاق / closing question | طُرح سؤال إغلاق واضح / asked a clear closing question | سؤال غامض / a vague question | لا سؤال إغلاق / no closing question |
| 5 | الخطوة التالية / next action | خطوة محددة بمالك وتاريخ / a specific step with owner and date | خطوة مبهمة / a fuzzy step | لا خطوة / no next action |
| 6 | سلامة الوعود / promise safety | لا وعد خطير إطلاقًا / no dangerous promise at all | تأطير مبالغ فيه / overstated framing | وعد بعائد أو نسبة كحقيقة / promised ROI or a rate as fact |

**العربية:** الدرجة القصوى 12. المعيار 6 خاص: أي 0 فيه يجعل المحادثة **فاشلة فورًا** بغض النظر عن المجموع.

**English:** Maximum score is 12. Criterion 6 is special: any 0 there makes the conversation an **automatic fail** regardless of the total.

## 4. عتبات الدرجة / Score Thresholds

| المجموع / Total | الحالة / Status | الإجراء / Action |
|---|---|---|
| 10–12 | نظيف / Clean | لا إجراء، يُسجَّل كنموذج جيد / no action, logged as a good example |
| 7–9 | يحتاج تحسين / Needs improvement | ملاحظات مكتوبة + متابعة الأسبوع التالي / written notes + next-week follow-up |
| 0–6 أو فشل تلقائي / or auto-fail | يحتاج تصحيح / Needs correction | حلقة تصحيح إلزامية / mandatory correction loop |

## 5. ما يستوجب التصحيح دائمًا / Always Triggers Correction

**العربية:** أي محادثة تحتوي على واحد مما يلي تدخل حلقة التصحيح فورًا، مهما كانت درجتها:
- وعد بعائد مضمون.
- ادعاء غير مدعوم بدليل.
- إثبات مُختلَق أو اسم عميل بلا موافقة.
- خطوة تالية غير واضحة أو غائبة.

**English:** Any conversation containing one of the following enters the correction loop immediately, whatever its score:
- a guaranteed ROI promise.
- an unsupported claim.
- fabricated proof or a client name without consent.
- an unclear or absent next action.

## 6. حلقة التصحيح / The Correction Loop

```text
flagged_conversation
   -> founder_review            ← مراجعة المؤسس للمحادثة كاملة
   -> root_cause_named          ← تسمية السبب الجذري (نص، تدريب، ضغط)
   -> correction_message        ← إن خرج وعد خطير للعميل: رسالة تصحيح
                                  (draft_only حتى موافقة المؤسس)
   -> coaching_note_logged      ← ملاحظة تدريب للبائع
   -> rechecked_next_week       ← إعادة فحص محادثة جديدة الأسبوع التالي
```

**العربية:** إذا وصل وعد خطير إلى العميل فعلًا، تُصاغ رسالة تصحيح تُعيد ضبط التوقّع — وتبقى `draft_only` حتى موافقة المؤسس قبل الإرسال. لا إجراء خارجي بلا موافقة بشرية.

**English:** If a dangerous promise actually reached the customer, a correction message is drafted to reset the expectation — and it stays `draft_only` until founder approval before sending. No external action without human approval.

## 7. الإيقاع الأسبوعي / Weekly Cadence

```text
كل اثنين / every Monday:
  [ ] اختيار 5 محادثات من الأسبوع السابق / pick 5 conversations from last week
  [ ] تطبيق الروبرِك على كل محادثة / score each with the rubric
  [ ] تسجيل المجموع وتصنيف الحقيقة / log total + truth label
  [ ] فتح حلقة تصحيح لكل محادثة دون 7 أو فاشلة / open a correction loop for any < 7 or failed
  [ ] تحديث متوسط الجودة الأسبوعي (Observed) / update the weekly quality average (Observed)
```

## 8. التصعيد / Escalation

**العربية:** ثلاث محادثات فاشلة لنفس البائع خلال 4 أسابيع تستوجب مراجعة مباشرة مع المؤسس وإعادة تدريب على النصوص المعتمدة. النمط المتكرر مشكلة نظام — لا مشكلة فرد.

**English:** Three failed conversations for the same salesperson within 4 weeks require a direct review with the founder and retraining on the approved scripts. A repeated pattern is a system problem — not an individual one.

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
