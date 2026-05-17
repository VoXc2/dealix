# Dealix — تجارب التسعير · Pricing Experiments

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `COMMERCIAL_CONTROL_TOWER.md` · `OFFER_MATRIX.md` · `../PRICING_STRATEGY.md` · `../OFFER_LADDER_AND_PRICING.md` · `../COMMERCIAL_WIRING_MAP.md`

---

> **تنبيه · Banner:** تجارب التسعير **داخلية**. الأسعار المنشورة تبقى شفّافة وقانونية وثابتة. السجل الرسمي في [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) يحكم كل الأسعار المنشورة — هذا هو المصدر الوحيد للحقيقة، وأي اختبار يحترم `no_hidden_pricing`.
>
> **Banner:** pricing experiments are **INTERNAL**. Published prices stay transparent, lawful, and stable. The authoritative registry in [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) governs all published prices — it is the single source of truth, and every experiment respects `no_hidden_pricing`.

---

## الغرض · Purpose

تختبر هذه الوثيقة كيف يُقدَّم العرض — لا كم يكلّف. التجارب تدور حول **النطاق، والتأهيل، والتموضع، والتغليف** — وليس خصومات غير معلنة أو أسعار مخترعة.

This document tests how an offer is presented — not what it costs. Experiments revolve around **scope, qualification, positioning, and packaging** — not undisclosed discounts or invented prices.

ما **لا** يُختبَر أبداً:

What is **never** tested:

- خصومات سرّية لمشترٍ دون آخر · secret discounts for one buyer over another.
- أرقام خارج السجل الرسمي · numbers outside the authoritative registry.
- تسعير مخفي أو مشروط بشكل غير معلن · hidden or undisclosed conditional pricing.

كل التجارب تتمركز حول درجتَي الدخول في السجل: `free_mini_diagnostic` (0 SAR) و`revenue_proof_sprint_499` (499 SAR).

All experiments center on the registry's entry rungs: `free_mini_diagnostic` (0 SAR) and `revenue_proof_sprint_499` (499 SAR).

---

## بروتوكول التجربة — 30 يوماً · 30-Day Experiment Protocol

| اليوم · Day | النشاط · Activity |
|---|---|
| 1–3 | حدّد متغيّراً واحداً للاختبار: نطاق، أو تأهيل، أو تموضع، أو تغليف. · pick one variable: scope, qualification, positioning, or packaging. |
| 4–20 | شغّل الصيغة على مجموعة محادثات حقيقية، وسجّل الاستجابة في الـscorecard. · run the variant on real conversations, log response in the scorecard. |
| 21–25 | اقرأ النتائج: جودة الاهتمام، سرعة الإغلاق، وضوح النطاق. · read results: interest quality, closing speed, scope clarity. |
| 26–30 | قرّر: ثبّت الصيغة، أو عدّلها، أو ارجع للأصل. وثّق القرار. · decide: lock, adjust, or revert. Document the decision. |

**قاعدة · Rule:** متغيّر واحد فقط لكل دورة. تغيير متغيّرين معاً يجعل النتيجة غير قابلة للقراءة.

**Rule:** one variable per cycle. Changing two variables together makes the result unreadable.

---

## أمثلة المتغيّرات · Example Variables

| المتغيّر · Variable | مثال اختبار · Example test |
|---|---|
| النطاق · Scope | 10 leads مقابل 15 lead في `free_mini_diagnostic`. · 10 vs 15 leads in the mini diagnostic. |
| التأهيل · Qualification | إضافة سؤال "من يملك قرار المتابعة؟" قبل العرض. · add "who owns the follow-up decision?" before the offer. |
| التموضع · Positioning | "تدقيق متابعة الـleads" مقابل "إثبات ما بعد الحملة". · "lead follow-up audit" vs "post-campaign proof". |
| التغليف · Packaging | تقديم `revenue_proof_sprint_499` كخطوة تالية تلقائية للتشخيص المجاني. · framing the sprint as the automatic next step after the free diagnostic. |

---

## قواعد القرار · Decision Rules

| الملاحظة · Observation | التفسير · Reading | الإجراء · Action |
|---|---|---|
| عرض الدخول يجذب اهتماماً منخفض الجودة فقط · the entry offer attracts low-quality interest only | النطاق فضفاض أو التأهيل ضعيف · scope too loose or qualification weak | شدّ النطاق وأضف سؤال تأهيل · tighten scope, add a qualification question. |
| عرض الدخول يُغلق بسهولة مفرطة · the entry offer closes too easily | قد يكون منقوص النطاق · it may be underscoped | راجع ما يشمله العرض، لا سعره · review what the offer includes, not its price. |
| درجة أعلى لا تُغلق · a higher rung does not close | غالباً المشكلة proof أو buyer-fit · usually a proof or buyer-fit problem | راجع جودة الـProof وملاءمة المشتري قبل لمس السعر · review proof quality and buyer fit before touching price. |

**مبدأ حاكم · Governing principle:** السعر ليس أول مشتبه به. حين لا تُغلق درجة أعلى، النقص عادةً في الدليل أو في ملاءمة المشتري — لا في الرقم.

**Governing principle:** price is not the first suspect. When a higher rung does not close, the gap is usually in the proof or in buyer fit — not in the number.

---

## ما تخرج به التجربة · Experiment Output

- قرار مكتوب: ثبّت / عدّل / ارجع.
- إن أدّت التجربة إلى تغيير سعر منشور، يُحدَّث السجل في `registry.py` أولاً، ثم [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) — لا سعر منشور يتغيّر خارج هذا المسار (`no_unaudited_changes`).
- مرجع للسياق الأوسع: [`../PRICING_STRATEGY.md`](../PRICING_STRATEGY.md) و[`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).

- A written decision: lock / adjust / revert.
- If an experiment leads to a published price change, the registry in `registry.py` is updated first, then [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) — no published price changes outside this path (`no_unaudited_changes`).
- Wider context: [`../PRICING_STRATEGY.md`](../PRICING_STRATEGY.md) and [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
