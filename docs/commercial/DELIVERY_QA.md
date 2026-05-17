# ضمان جودة التسليم / Delivery QA
<!-- COMMERCIAL EMPIRE | Owner: Founder | Date: 2026-05-17 -->
> القانون / Canonical: see [docs/27_delivery_playbooks/DELIVERY_QA_CHECKLIST.md](../27_delivery_playbooks/DELIVERY_QA_CHECKLIST.md)

## 1. الغرض / Purpose

**العربية:** هذا المستند هو بوابة الجودة الأخيرة قبل تسليم أي Proof Pack للعميل. لا يخرج أي حزمة إثبات نهائية قبل أن تحصل على 8/10 على الأقل في بطاقة التقييم العشرية. الهدف ليس الكمال، بل ضمان أن كل تسليم واضح المصدر والمالك والحدود والأدلة.

**English:** This document is the final quality gate before any Proof Pack reaches a client. No final Proof Pack ships before it scores at least 8/10 on the ten-point scorecard. The goal is not perfection; it is a delivery with a clear source, owner, boundary, and evidence trail.

## 2. بطاقة التقييم العشرية / The 10-Point Scorecard

كل نقطة قيمتها درجة واحدة. الحد الأدنى للإرسال كنسخة نهائية: 8/10.
Each point is worth one point. Minimum to ship as final: 8/10.

| # | البند / Item | السؤال / Question | درجة / Score |
|---|---|---|---|
| 1 | المصدر / Source | هل مصدر كل رقم وملاحظة واضح؟ / Is the source of every number and note clear? | 0 / 1 |
| 2 | المالك / Owner | هل المسؤول عن كل إجراء واضح بالاسم؟ / Is the owner of each action named? | 0 / 1 |
| 3 | حد الموافقة / Approval boundary | هل حدود ما يحتاج موافقة بشرية واضحة؟ / Is the human-approval boundary clear? | 0 / 1 |
| 4 | أثر الأدلة / Evidence trail | هل يمكن تتبّع كل استنتاج إلى دليله؟ / Can each conclusion be traced to its evidence? | 0 / 1 |
| 5 | الخطوات التالية / Next actions | هل الخطوات التالية محددة وقابلة للتنفيذ؟ / Are next actions specific and actionable? | 0 / 1 |
| 6 | المخاطر / Risks | هل المخاطر والافتراضات مذكورة صراحةً؟ / Are risks and assumptions stated explicitly? | 0 / 1 |
| 7 | لا مبالغة / No exaggeration | هل خلا التسليم من أي ادعاء مبالغ فيه؟ / Is the delivery free of any exaggerated claim? | 0 / 1 |
| 8 | ترقية منطقية / Logical upsell | هل توجد توصية ترقية منطقية ومبنية على الأدلة؟ / Is there a logical, evidence-based upsell? | 0 / 1 |
| 9 | وضوح اللغة / Language clarity | هل اللغة مفهومة لصاحب القرار غير التقني؟ / Is the language clear to a non-technical decision-maker? | 0 / 1 |
| 10 | قابلية الرؤية / Insight-ready | هل يمكن تحويله إلى رؤية مجهّلة الهوية؟ / Can it become an anonymized insight? | 0 / 1 |

```text
SCORING RULE
  10/10  -> ship as final + tag as case-safe candidate
  8-9/10 -> ship as final, log gaps for next delivery
  6-7/10 -> ship as DRAFT ONLY, founder review required
  < 6/10 -> do not ship, rework
```

## 3. معايير سرعة مصنع التسليم / Delivery Factory Speed Standard

**العربية:** أول 48 ساعة هي التي تبني الثقة. السرعة هنا ليست تسرّعًا، بل إيقاع منضبط يثبت للعميل أن دياليكس منظّمة. كل مخرج في هذه المرحلة هو مسودة حتى الموافقة (draft_only).

**English:** The first 48 hours build trust. Speed here is not haste; it is a disciplined cadence proving to the client that Dealix is organized. Every output in this phase is draft-only until approved.

| النافذة / Window | المخرجات / Deliverables |
|---|---|
| خلال 10 دقائق / Within 10 min | رسالة شكر، نموذج onboarding، قائمة المطلوب، تاريخ التسليم / Thank-you message, onboarding form, list of what's needed, delivery date |
| خلال 24 ساعة / Within 24 h | لوحة العملاء/الفرص، الأسئلة الناقصة، النتائج الأولية / Lead/opportunity board, missing questions, initial findings |
| خلال 48 ساعة / Within 48 h | Proof Pack v1، مسودات المتابعة، ملاحظات المخاطر، الخطوات التالية / Proof Pack v1, follow-up drafts, risk notes, next actions |
| خلال 7 أيام / Within 7 days | مكالمة التسليم، تأكيد القيمة، توصية Sprint/Retainer، طلب الإحالة / Delivery call, value confirmation, Sprint/Retainer recommendation, referral ask |

**الهدف / Target:** Time-to-Proof < 48h للمشاريع التجريبية / for pilots. تصنيف الحقيقة: Observed عند القياس الفعلي، Estimate قبل التسليم. / Truth label: Observed when measured, Estimate before delivery.

## 4. حدود السرعة / Speed Boundaries

**العربية:** السرعة لا تلغي الموافقة. كل رسالة متابعة أو إجراء خارجي يبقى مسودة حتى يوافق عليه إنسان من جانب العميل أو المؤسس. لا إرسال تلقائي، لا واتساب بارد، لا سحب بيانات. السرعة تخصّ التجهيز الداخلي، لا الإرسال الخارجي.

**English:** Speed never bypasses approval. Every follow-up message or external action stays draft-only until a human — client-side or founder — approves it. No automated sending, no cold WhatsApp, no scraping. Speed applies to internal preparation, not external dispatch.

## 5. ربط الترقية / Upsell Linkage

**العربية:** البند 8 في بطاقة التقييم يربط الجودة بالنمو التجاري. الترقية المنطقية تعني توصية مبنية على فجوة موثّقة في التسليم نفسه — مثل ثغرة متابعة متكررة تبرّر Revenue Proof Sprint أو Growth Ops Monthly.

**English:** Scorecard point 8 links quality to commercial growth. A logical upsell means a recommendation grounded in a documented gap inside the delivery itself — e.g., a recurring follow-up gap that justifies a Revenue Proof Sprint or Growth Ops Monthly.

| العرض / Offer | السعر / Price | الحالة / Status |
|---|---|---|
| Free Mini Diagnostic | 0 | Wired |
| Revenue Proof Sprint | 499 one-time | Wired |
| Data-to-Revenue Pack | 1,500 one-time | Wired |
| Growth Ops Monthly | 2,999/mo | Wired |
| Support OS Add-on | 1,500/mo | Wired |
| Executive Command Center | 7,500/mo | Wired |
| Agency Partner OS | custom | Wired |

أي طبقة أكبر: Roadmap — not wired to checkout / خارطة طريق — غير مربوط بالدفع.

## 6. مسؤولية البوابة / Gate Ownership

**العربية:** المؤسس هو مالك بوابة الجودة. لا يُحوّل أي تسليم من مسودة إلى نهائي إلا بعد تسجيل درجة البطاقة في سجل التسليم، مع توقيع المراجع وتاريخه.

**English:** The Founder owns the quality gate. No delivery moves from draft to final until the scorecard result is logged in the delivery record, with the reviewer's sign-off and date.

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
