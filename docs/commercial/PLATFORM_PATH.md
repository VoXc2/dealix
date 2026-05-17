# مسار المنصة / Platform Path
<!-- COMMERCIAL EMPIRE | Owner: Founder | Date: 2026-05-17 -->
> القانون / Canonical: see [docs/product/PLATFORM_PATH.md](../product/PLATFORM_PATH.md)

> **مستند خارطة طريق / Roadmap — not wired to checkout / خارطة طريق — غير مربوط بالدفع.**
> المراحل 4 و 5 تصميم مستقبلي. لا يُبنى أي منتج SaaS قبل اجتياز بوابة التكرار.
> Stages 4 and 5 are future design. No SaaS product is built before the Repeatability gate passes.

## 1. الغرض / Purpose

**العربية:** هذا المستند يرسم الطريق المرحلي من الأدوات الداخلية إلى منتج SaaS. القاعدة الأساسية: لا قفز إلى SaaS قبل ظهور إشارات حقيقية. القفز المبكر يحوّل دياليكس إلى شركة منتج بلا طلب مُثبت، ويستنزف رأس المال.

**English:** This document maps the staged path from internal tools to a SaaS product. The core rule: do not jump to SaaS before real signals appear. An early jump turns Dealix into a product company without proven demand and drains capital.

كل إشارة انتقال تحمل وسم حقيقة: Estimate / Observed / Client-confirmed / Payment-confirmed.
Every transition signal carries a truth label: Estimate / Observed / Client-confirmed / Payment-confirmed.

## 2. المراحل الخمس / The Five Stages

```text
STAGE 1  Internal tools          -> Dealix operators only
   |
STAGE 2  Client-visible reports  -> read-only outputs to the client
   |
STAGE 3  Client workspace        -> uploads, approvals, audit trail
   |
STAGE 4  Self-serve modules      -> guardrailed workflows, scored eligibility
   |
STAGE 5  SaaS                    -> subscription workspace + usage modules
```

| المرحلة / Stage | الوصف / Description | المالك / Who operates it |
|---|---|---|
| 1 — أدوات داخلية / Internal tools | أدوات يستخدمها مشغّلو دياليكس فقط / Tools used only by Dealix operators | دياليكس / Dealix |
| 2 — تقارير مرئية للعميل / Client-visible reports | مخرجات للقراءة فقط: PDF أو بوابة / Read-only outputs: PDF or portal | دياليكس / Dealix |
| 3 — مساحة عمل العميل / Client workspace | رفع ملفات، موافقات، أثر تدقيق / Uploads, approvals, audit trail | دياليكس + العميل / Dealix + client |
| 4 — وحدات الخدمة الذاتية / Self-serve modules | سير عمل مُحوكَم بأهلية مُقيَّمة / Guardrailed workflows, scored eligibility | العميل بإشراف / Client, supervised |
| 5 — SaaS | اشتراك + وحدات بالاستخدام / Subscription + usage-based modules | العميل / Client |

## 3. القاعدة الصارمة لتغيير المرحلة / The Hard Rule for Stage Change

**العربية:** لا تتحول دياليكس إلى SaaS حتى يتكرر سير العمل نفسه، ويفهم العميل القيمة، ولا يُرهق الدعمُ الفريقَ، وتكون الحوكمة قوية وقابلة للفرض داخل المنتج. الأربعة شروط معًا، لا أحدها.

**English:** Dealix does not convert to SaaS until the same workflow repeats, the client understands the value, support does not overwhelm the team, and governance is strong and enforceable inside the product. All four conditions, not one.

```text
STAGE TRANSITION GATE  (all required)
  [ ] same workflow shape repeats        truth label: Repeated workflow
  [ ] client understands value           truth label: Client-confirmed
  [ ] support load modeled, sustainable  truth label: Observed
  [ ] governance enforceable in-product  truth label: Observed
  ----------------------------------------------------------------
  missing any -> stay at current stage
```

## 4. الربط ببوابة التكرار / Link to the Repeatability Gate

**العربية:** بوابة الانتقال من المرحلة 3 إلى المرحلة 4، وكذلك من 4 إلى 5، مربوطة مباشرةً بالبوابة 5 (القابلية للتكرار) في [البوابات التجارية الخمس](COMMERCIAL_GATES.md). لا وحدة خدمة ذاتية ولا SaaS قبل اجتياز البوابة 5: ثلاثة سير عمل متكررة بنفس الألم والمشتري والشكل.

**English:** The transition from Stage 3 to Stage 4, and from Stage 4 to Stage 5, is tied directly to Gate 5 (Repeatability) in [The Five Commercial Gates](COMMERCIAL_GATES.md). No self-serve module and no SaaS before Gate 5 passes: three repeated workflows with the same pain, same buyer, same proof format.

| الانتقال / Transition | البوابة المطلوبة / Required gate | الدليل / Evidence |
|---|---|---|
| المرحلة 1 → 2 / Stage 1 → 2 | جودة تسليم ثابتة / Stable delivery QA | بطاقة QA بـ 8/10 / QA scorecard at 8/10 |
| المرحلة 2 → 3 / Stage 2 → 3 | عملاء توسّع / Expansion clients | Gate 4 مُجتاز / Gate 4 passed |
| المرحلة 3 → 4 / Stage 3 → 4 | القابلية للتكرار / Repeatability | Gate 5 مُجتاز / Gate 5 passed |
| المرحلة 4 → 5 / Stage 4 → 5 | تكرار + دعم مستدام / Repeat + sustainable support | Gate 5 + نموذج دعم موثّق / Gate 5 + documented support model |

## 5. الحوكمة داخل المنتج / In-Product Governance

**العربية:** كلما اقتربت دياليكس من المرحلة 5، يجب أن تنتقل الحوكمة من سياسة بشرية إلى ضابط مفروض في المنتج. كل إجراء خارجي يبقى draft_only حتى موافقة بشرية. لا تواصل بارد، لا كشط بيانات، لا إرسال جماعي. الوحدة التي لا تستطيع فرض هذه الحدود لا تُطلَق.

**English:** As Dealix nears Stage 5, governance must move from a human policy to an enforced in-product control. Every external action stays draft-only until human approval. No cold outreach, no scraping, no bulk sending. A module that cannot enforce these boundaries is not released.

## 6. الربط بالعروض المربوطة / Link to Wired Offers

**العربية:** المراحل 1–3 تُسلَّم عبر العروض المربوطة بالدفع الحالية. المرحلتان 4 و 5 ليستا مربوطتين بالدفع، وتبقيان خارطة طريق حتى تثبت بوابة التكرار.

**English:** Stages 1–3 are delivered through the current wired offers. Stages 4 and 5 are not wired to checkout and remain a roadmap until the Repeatability gate is proven.

| المرحلة / Stage | العرض الناقل / Carrying offer | الحالة / Status |
|---|---|---|
| 1–2 | Revenue Proof Sprint 499 / Data-to-Revenue Pack 1,500 | Wired |
| 3 | Growth Ops Monthly 2,999/mo / Executive Command Center 7,500/mo | Wired |
| 4–5 | وحدات الخدمة الذاتية وSaaS / Self-serve modules and SaaS | Roadmap — not wired to checkout / خارطة طريق — غير مربوط بالدفع |

## 7. مسؤولية المسار / Path Ownership

**العربية:** المؤسس يملك قرار الانتقال بين المراحل. لا انتقال دون تسجيل اجتياز البوابة في سجل القرارات، مع الأدلة الموسومة وتاريخها.

**English:** The Founder owns the stage-transition decision. No transition occurs without logging the gate pass in the decision ledger, with labelled evidence and a date.

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
