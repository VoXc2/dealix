# Platform Path — From Services to a Platform / مسار المنصة

> Dealix may one day be a platform. The mistake is to jump there early. This
> doc records the **disciplined six-stage path** from internal tooling to a
> self-serve product, and the build rules that decide when each step is
> earned. It is explicitly **not a signal to start building SaaS now**.
>
> قد تصبح Dealix منصة يوماً ما. الخطأ هو القفز إلى ذلك مبكراً. تسجّل هذه
> الوثيقة **المسار المنضبط من ست مراحل** من الأدوات الداخلية إلى منتج
> ذاتي الخدمة، وقواعد البناء التي تقرر متى تُستحَق كل خطوة. وهي صراحةً
> **ليست إشارة لبدء بناء SaaS الآن**.

**Date opened / تاريخ الفتح:** 2026-05-17
**Owner / المالك:** Founder
**Status / الحالة:** Strategic narrative — not a binding spec.

---

## 1. Do not jump to SaaS early / لا تقفز إلى SaaS مبكراً

A platform built before the workflow is proven is a product with no users and
no proof. The path is sequential: each stage exists only because the stage
before it created real, repeated demand.

المنصة المبنية قبل إثبات سير العمل هي منتج بلا مستخدمين وبلا إثبات. المسار
تسلسلي: كل مرحلة توجد فقط لأن المرحلة التي قبلها صنعت طلباً حقيقياً متكرراً.

> **Rule / القاعدة:** the platform is earned, not chosen. Build the next stage
> only when the current one repeats with real customers.
> المنصة تُستحَق ولا تُختار. ابنِ المرحلة التالية فقط حين تتكرر الحالية مع
> عملاء حقيقيين.

---

## 2. The six stages / المراحل الست

Each stage is a different surface, with a different audience and a higher bar
to enter.

كل مرحلة سطح مختلف، بجمهور مختلف وعتبة دخول أعلى.

| Stage / المرحلة | Surface / السطح | Who uses it / من يستخدمها |
|---|---|---|
| 1 — Internal tools / أدوات داخلية | Founder-only scripts and modules | Delivery team / فريق التسليم |
| 2 — Client-visible reports / تقارير مرئية للعميل | Proof Packs and read-only outputs | One customer / عميل واحد |
| 3 — Client workspace / مساحة عمل العميل | A shared, customer-facing view | Active customers / عملاء نشطون |
| 4 — Partner portal / بوابة الشركاء | A surface for partners to manage referrals and delivery | Partners / الشركاء |
| 5 — Self-serve modules / وحدات ذاتية الخدمة | Specific modules a customer runs without the founder | Repeat customers / عملاء متكررون |
| 6 — SaaS / منتج SaaS | A standalone, self-serve product | The market / السوق |

Stages 5 and 6 are **later** initiatives. Stages 1–4 are the realistic horizon
of current work.

المرحلتان 5 و6 مبادرتان **لاحقتان**. المراحل 1–4 هي الأفق الواقعي للعمل
الحالي.

---

## 3. The build rule / قاعدة البناء

Nothing is built ahead of demand. Each artifact is promoted only when
repetition proves it is worth the next level of investment.

لا شيء يُبنى قبل الطلب. كل مُخرَج يُرقَّى فقط حين يثبت التكرار أنه يستحق
المستوى التالي من الاستثمار.

| Trigger / المُحفّز | Build / ما يُبنى |
|---|---|
| A new workflow / سير عمل جديد | A checklist / قائمة تحقق |
| Repeated twice / تكرر مرتين | A template / قالب |
| Repeated three times / تكرر ثلاث مرات | An automation / أتمتة |
| Repeated with two customers / تكرر مع عميلين | An internal module / وحدة داخلية |
| Repeated with three customers + retainers / تكرر مع ثلاثة عملاء + احتفاظ | A product feature / ميزة منتج |

A workflow that has not repeated does not get a tool. Effort follows evidence
of demand, never a hunch.

سير العمل الذي لم يتكرر لا يحصل على أداة. الجهد يتبع دليل الطلب، لا الحدس.

---

## 4. The proof gates / بوابات الإثبات

Beyond the build rule, four gates protect the path from premature leaps. None
may be skipped.

إلى جانب قاعدة البناء، أربع بوابات تحمي المسار من القفزات المبكرة. لا يجوز
تخطّي أي منها.

| Gate / البوابة | Rule / القاعدة |
|---|---|
| Revenue gate / بوابة الإيراد | No revenue before payment / لا إيراد قبل الدفع |
| Rung gate / بوابة الدرجة | No advanced rung before a meeting / لا درجة متقدمة قبل اجتماع |
| Scope gate / بوابة النطاق | No top rung before a signed scope / لا درجة عليا قبل نطاق موقّع |
| Repetition gate / بوابة التكرار | No building before a workflow actually repeats / لا بناء قبل تكرار سير العمل فعلياً |

These gates make the platform path a consequence of proven work, not a bet on
future work.

هذه البوابات تجعل مسار المنصة نتيجة لعمل مُثبَت، لا رهاناً على عمل مستقبلي.

---

## Doctrine alignment / المواءمة مع الدستور

- The platform is a **later** outcome — preparing for it never displaces
  delivery and proof now. / المنصة نتيجة لاحقة لا تُزيح التسليم والإثبات الآن.
- Pricing of any platform tier follows
  [`../COMPANY_SERVICE_LADDER.md`](../COMPANY_SERVICE_LADDER.md). Only the
  **499 SAR** Sprint is firm; every higher tier is a `recommended_draft` until
  paid pilots inform a real number.
- The path is built on **proof gates and repeated evidence**, never on
  guaranteed revenue or promised platform growth.
- Client-visible and self-serve surfaces keep the evidence trail and human
  approval for external actions intact at every stage.

## Related docs / مراجع ذات صلة

- [`CAPITAL_MODEL.md`](CAPITAL_MODEL.md) — Product Capital is what becomes the platform
- [`ACADEMY_PATH.md`](ACADEMY_PATH.md) — the other later initiative
- [`OFFER_LADDER.md`](OFFER_LADDER.md) — the rungs the rung gate protects
- [`PROOF_PACK_STANDARD.md`](PROOF_PACK_STANDARD.md) — the Stage 2 client-visible report
- [`../COMPANY_SERVICE_LADDER.md`](../COMPANY_SERVICE_LADDER.md) — canonical pricing
- [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) — hard limits
