# Dealix — Offer Ladder & Pricing
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-16 | Version: v2 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** كل درجة تُفتح فقط بعد إثبات حقيقي من الدرجة السابقة.
> لا ترقية قبل نتيجة موثقة. لا ضمانات. لا ادعاءات مبالغ فيها.

> **إفصاح نمط التسليم — Delivery-mode disclosure.** الدرجة 0 (تشخيص عمليات
> الإيراد المحكوم) مُسلَّمة عبر **منتج مُتحقَّق منه** يُنتج مُخرجاً حقيقياً
> جاهزاً للعميل. أمّا الدرجات 1–6 فهي اليوم **بقيادة المؤسس / شبه-مؤتمتة**
> (founder-assisted / semi-automated): الأدوات موجودة لكن التسليم يتطلّب
> تشغيلاً يدوياً من المؤسس، ولكل إجراء خارجي موافقة. لا تُعرض كخدمات مُدارة
> بالكامل، ولا تُفتح إلا بعد استيفاء شروط الدخول المذكورة لكل درجة. الأتمتة
> الكاملة لا تُبنى إلا عند ظهور طلب حقيقي — انظر
> `docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`.
>
> Rung 0 ships a verified product deliverable. Rungs 1–6 are
> **founder-assisted / semi-automated** today — not full managed services —
> and unlock only on the stated entry conditions. Every external action
> requires founder approval; there is no autonomous external send.

> **بوابة الأدلة — Evidence gate.** لا رقم بلا `source_ref`. مخرج الذكاء
> الاصطناعي ليس دليلاً. كل قرار يحصل على Decision Passport، وكل ارتباط يُنتج
> Proof Pack. التموضع الكامل في
> `docs/strategy/GOVERNED_REVENUE_AI_OPERATIONS.md`.

---

## سلم الخدمات — نظرة عامة

```
[0] Governed Revenue Ops Diagnostic   مجاني ← باب الدخول
[1] Revenue Intelligence Sprint       25,000 SAR ← العرض المدفوع الأساسي
[2] Governed Ops Retainer             4,999–35,000 SAR/شهر ← بعد Sprint
[3] AI Governance for Revenue Teams   حسب النطاق
[4] CRM / Data Readiness for AI       حسب النطاق
[5] Board Decision Memo               حسب النطاق
[6] Trust Pack Lite                   حسب النطاق ← فقط عند إشارة asks_for_security
```

تسلسل البيع: التشخيص → السبرنت → الاشتراك → حزمة الثقة المختصرة عند الطلب →
مذكرة المجلس للقيادة. **لا تُعرض كل الخدمات دفعة واحدة.**

---

## الخدمة 0: Governed Revenue Ops Diagnostic
**تشخيص عمليات الإيراد المحكوم**

| العنصر | التفاصيل |
|--------|----------|
| **السعر** | **مجاني** (باب الدخول) |
| **العميل المستهدف** | أي مؤسس B2B سعودي مهتم باستكشاف Dealix |
| **المشكلة التي يحلها** | "لا أعرف أين تكمن الفجوات في عمليات الإيراد وحوكمة الذكاء الاصطناعي عندي" |
| **المخرجات** | تقرير تشخيصي 1 صفحة + 3 أولويات + توصية الخطوة التالية |
| **مقاييس الإثبات** | هل أوصلنا لـ Revenue Intelligence Sprint؟ |
| **المدخلات المطلوبة** | 6 أسئلة عبر `/diagnostic.html` (15 دقيقة) |
| **الاستثناءات** | لا وعود ROI، لا تقارير متقدمة، لا وصول للمنصة |
| **مسار الترقية** | → Revenue Intelligence Sprint |
| **الهامش** | 0 SAR تكلفة مباشرة (API تكلفة < 2 SAR) |
| **وقت التسليم** | فوري (API + مراجعة يدوية 30 دقيقة) |
| **نمط التسليم اليوم** | منتج مُتحقَّق منه |
| **وضع الإجراء** | `approved_manual` |

---

## الخدمة 1: Revenue Intelligence Sprint
**سبرنت ذكاء الإيراد**

| العنصر | التفاصيل |
|--------|----------|
| **السعر** | **25,000 SAR** (دفع واحد مسبق) |
| **العميل المستهدف** | مؤسس B2B أو قائد إيراد يريد قرارات إيراد محكومة ومدعومة بالأدلة |
| **المشكلة التي يحلها** | "pipeline مشوّش، متابعة ضعيفة، ذكاء اصطناعي غير مُدار — أحتاج قرارات بمصدر وموافقة وأثر" |
| **المخرجات** | ترتيب أولوية الحسابات، تقييم مخاطر الصفقات، مسودات الإجراء التالي الأفضل، قوالب متابعة، سجل فرص الإيراد، Decision Passport، Proof Pack |
| **مقاييس الإثبات** | فرص مُثبتة بأدلة موثّقة، Proof Pack مُسلَّم، Decision Passport لكل قرار |
| **المدخلات المطلوبة** | وصول للـ pipeline الحالي، قائمة الحسابات، حالة 3 صفقات حالية |
| **الاستثناءات** | لا إرسال خارجي ذاتي (draft_only)، لا فرص مضمونة، لا وصول للأنظمة الداخلية بلا موافقة |
| **مسار الترقية** | → Governed Ops Retainer |
| **الهامش** | مرتفع (تكلفة تسليم: ساعات مؤسس + < 50 SAR LLM) |
| **وقت التسليم** | حسب النطاق المتفق عليه |
| **نمط التسليم اليوم** | بقيادة المؤسس / شبه-مؤتمت |
| **وضع الإجراء** | `approval_required` |

---

## الخدمة 2: Governed Ops Retainer
**اشتراك العمليات المحكومة**

| العنصر | التفاصيل |
|--------|----------|
| **السعر** | **4,999–35,000 SAR/شهر** (اشتراك شهري) |
| **العميل المستهدف** | شركة B2B أتمت Sprint ناجحاً وتريد قيمة متكررة |
| **المشكلة التي يحلها** | "نريد مراجعة إيراد ومراجعة ذكاء اصطناعي محكومة بشكل مستمر شهرياً" |
| **المخرجات** | مراجعة إيراد شهرية، مراجعة جودة pipeline، مراجعة قرارات الذكاء الاصطناعي، طابور متابعة موافَق عليه، سجل مخاطر، تقرير قيمة، مذكرة مجلس |
| **مقاييس الإثبات** | قيمة شهرية متكررة، فرص اشتراك موثّقة، Proof Pack شهري |
| **المدخلات المطلوبة** | وصول Dealix Portal، تحديثات pipeline دورية، موافقة على كل إجراء خارجي |
| **الاستثناءات** | لا إرسال خارجي ذاتي، لا مشورة قانونية، لا تمثيل خارجي |
| **مسار الترقية** | → AI Governance / Board Decision Memo |
| **الهامش** | مرتفع (تكلفة: ساعات مؤسس شهرياً + LLM) |
| **وقت التسليم** | تسليم مستمر شهري |
| **نمط التسليم اليوم** | بقيادة المؤسس / شبه-مؤتمت — تشغيل يدوي شهري |
| **وضع الإجراء** | `approval_required` لكل إجراء خارجي |

---

## الخدمة 3: AI Governance for Revenue Teams
**حوكمة الذكاء الاصطناعي لفرق الإيراد**

| العنصر | التفاصيل |
|--------|----------|
| **السعر** | **حسب النطاق** |
| **العميل المستهدف** | فريق إيراد يستخدم الذكاء الاصطناعي بلا حدود أو سياسة واضحة |
| **المشكلة التي يحلها** | "الفريق يستخدم الذكاء الاصطناعي بسرعة وبلا حوكمة — نحتاج حدوداً وقواعد" |
| **المخرجات** | إجراءات ذكاء اصطناعي مسموحة/ممنوعة، حدود الموافقات، قواعد المصادر، سياسة منع الإرسال الخارجي الذاتي، تسجيل الأدلة |
| **مقاييس الإثبات** | سياسة موافَق عليها ومطبَّقة، حدود موافقات موثّقة |
| **المدخلات المطلوبة** | جرد استخدام الذكاء الاصطناعي الحالي، تدفّقات الإيراد، أصحاب القرار |
| **الاستثناءات** | لا مشورة قانونية، لا تدقيق امتثال رسمي |
| **مسار الترقية** | → Governed Ops Retainer / Trust Pack Lite |
| **الهامش** | مرتفع |
| **وقت التسليم** | حسب النطاق المتفق عليه |
| **نمط التسليم اليوم** | بقيادة المؤسس / شبه-مؤتمت |
| **وضع الإجراء** | `approval_required` |

---

## الخدمة 4: CRM / Data Readiness for AI
**جاهزية CRM/البيانات للذكاء الاصطناعي**

| العنصر | التفاصيل |
|--------|----------|
| **السعر** | **حسب النطاق** |
| **العميل المستهدف** | شركة B2B تريد استخدام الذكاء الاصطناعي لكن بياناتها غير جاهزة |
| **المشكلة التي يحلها** | "بياناتنا مشوّشة — لا نثق بها كمصدر لقرار محكوم" |
| **المخرجات** | تقرير نظافة CRM، خريطة المصادر، الحقول الناقصة، الحسابات المكررة، مشاكل مراحل دورة الحياة، درجة جاهزية البيانات، توصية جاهزية الذكاء الاصطناعي |
| **مقاييس الإثبات** | درجة جاهزية بيانات موثّقة، خريطة مصادر مُسلَّمة |
| **المدخلات المطلوبة** | CRM export أو قائمة حسابات، وصف ICP الحالي |
| **الاستثناءات** | لا استخراج بيانات (no scraping)، لا تكامل مباشر مع أنظمة CRM بلا موافقة |
| **مسار الترقية** | → Revenue Intelligence Sprint / Governed Ops Retainer |
| **الهامش** | مرتفع |
| **وقت التسليم** | حسب النطاق المتفق عليه |
| **نمط التسليم اليوم** | بقيادة المؤسس / شبه-مؤتمت |
| **وضع الإجراء** | `approval_required` |

---

## الخدمة 5: Board Decision Memo
**مذكرة قرار مجلس الإدارة**

| العنصر | التفاصيل |
|--------|----------|
| **السعر** | **حسب النطاق** |
| **العميل المستهدف** | مؤسس/C-Suite/مجلس إدارة يحتاج قرارات إيراد ورأس مال محكومة |
| **المشكلة التي يحلها** | "نحتاج مذكرة قرار واضحة بمصادر وأدلة، لا dashboards فارغة" |
| **المخرجات** | أهم قرارات الإيراد، مخاطر pipeline، مخاطر حوكمة الذكاء الاصطناعي، تخصيص رأس المال، توصيات بناء/تثبيت/إيقاف |
| **مقاييس الإثبات** | مذكرة مُستخدَمة في اجتماع قيادة، Decision Passport لكل توصية |
| **المدخلات المطلوبة** | بيانات pipeline، أولويات القيادة، قيود رأس المال |
| **الاستثناءات** | لا مشورة استثمارية، لا توقّعات مضمونة |
| **مسار الترقية** | → Governed Ops Retainer |
| **الهامش** | مرتفع |
| **وقت التسليم** | حسب النطاق المتفق عليه |
| **نمط التسليم اليوم** | بقيادة المؤسس / شبه-مؤتمت |
| **وضع الإجراء** | `approval_required` |

---

## الخدمة 6: Trust Pack Lite
**حزمة الثقة المختصرة**

| العنصر | التفاصيل |
|--------|----------|
| **السعر** | **حسب النطاق** |
| **العميل المستهدف** | عميل أبدى إشارة `asks_for_security` صراحةً |
| **المشكلة التي يحلها** | "نحتاج دليلاً على حدود الأمان والثقة قبل أن نوسّع الذكاء الاصطناعي" |
| **المخرجات** | سياسة إجراءات الذكاء الاصطناعي، مصفوفة الموافقات، التعامل مع الأدلة، الإجراءات الممنوعة، قواعد سلامة الوكلاء، حدود الثقة |
| **مقاييس الإثبات** | حزمة ثقة مُسلَّمة ومراجَعة، حدود ثقة موثّقة |
| **المدخلات المطلوبة** | نطاق استخدام الذكاء الاصطناعي، متطلبات الأمان لدى العميل |
| **الاستثناءات** | تُعرض **فقط** عند إشارة `asks_for_security` — لا تُعرض استباقياً |
| **مسار الترقية** | → AI Governance / Governed Ops Retainer |
| **الهامش** | مرتفع |
| **وقت التسليم** | حسب النطاق المتفق عليه |
| **نمط التسليم اليوم** | بقيادة المؤسس / شبه-مؤتمت |
| **وضع الإجراء** | `approval_required` |

---

## ملخص الأسعار السريع

| # | الخدمة | السعر | الوضع | نمط التسليم |
|---|--------|-------|-------|------------|
| 0 | Governed Revenue Ops Diagnostic | مجاني | متاح الآن | منتج مُتحقَّق منه |
| 1 | Revenue Intelligence Sprint | 25,000 SAR | بعد تشخيص | بقيادة المؤسس |
| 2 | Governed Ops Retainer | 4,999–35,000 SAR/شهر | بعد Sprint | بقيادة المؤسس / شبه-مؤتمت |
| 3 | AI Governance for Revenue Teams | حسب النطاق | بعد تأهيل | بقيادة المؤسس / شبه-مؤتمت |
| 4 | CRM / Data Readiness for AI | حسب النطاق | بعد تأهيل | بقيادة المؤسس / شبه-مؤتمت |
| 5 | Board Decision Memo | حسب النطاق | بعد تأهيل | بقيادة المؤسس / شبه-مؤتمت |
| 6 | Trust Pack Lite | حسب النطاق | عند إشارة `asks_for_security` | بقيادة المؤسس / شبه-مؤتمت |

---

# English Section — القسم الإنجليزي

## Ladder Overview

```
[0] Governed Revenue Ops Diagnostic   Free ← entry door
[1] Revenue Intelligence Sprint       25,000 SAR ← core paid offer
[2] Governed Ops Retainer             4,999–35,000 SAR/mo ← after Sprint
[3] AI Governance for Revenue Teams   Scoped
[4] CRM / Data Readiness for AI       Scoped
[5] Board Decision Memo               Scoped
[6] Trust Pack Lite                   Scoped ← only on an asks_for_security signal
```

Sell sequence: Diagnostic → Sprint → Retainer → Trust Pack Lite on demand →
Board Decision Memo for leadership. **Never present all services at once.**

## Service 0: Governed Revenue Ops Diagnostic

| Item | Detail |
|------|--------|
| **Price** | **Free** (entry door) |
| **Target customer** | Any Saudi B2B founder exploring Dealix |
| **Problem solved** | "I do not know where the gaps are in my revenue ops and AI governance" |
| **Deliverables** | 1-page diagnostic report + 3 priorities + next-step recommendation |
| **Proof metric** | Did it lead to a Revenue Intelligence Sprint? |
| **Inputs required** | 6 questions via `/diagnostic.html` (15 minutes) |
| **Exclusions** | No ROI promises, no advanced reports, no platform access |
| **Upgrade path** | → Revenue Intelligence Sprint |
| **Delivery mode today** | Verified product |
| **Action mode** | `approved_manual` |

## Service 1: Revenue Intelligence Sprint

| Item | Detail |
|------|--------|
| **Price** | **25,000 SAR** (single upfront payment) |
| **Target customer** | B2B founder or revenue leader who wants governed, evidence-backed revenue decisions |
| **Problem solved** | "Messy pipeline, weak follow-up, unmanaged AI — I need decisions with a source, an approval, and a documented impact" |
| **Deliverables** | Account prioritization, deal risk scoring, next-best-action drafts, follow-up templates, revenue opportunity ledger, Decision Passport, Proof Pack |
| **Proof metric** | Evidenced opportunities with documented sources, Proof Pack delivered, a Decision Passport per decision |
| **Inputs required** | Access to current pipeline, account list, status of 3 live deals |
| **Exclusions** | No autonomous external send (draft_only), no guaranteed opportunities, no internal-system access without approval |
| **Upgrade path** | → Governed Ops Retainer |
| **Delivery mode today** | Founder-assisted / semi-automated |
| **Action mode** | `approval_required` |

## Service 2: Governed Ops Retainer

| Item | Detail |
|------|--------|
| **Price** | **4,999–35,000 SAR/mo** (monthly subscription) |
| **Target customer** | A B2B company that completed a successful Sprint and wants recurring value |
| **Problem solved** | "We want a continuous, governed monthly revenue review and AI decision review" |
| **Deliverables** | Monthly revenue review, pipeline quality review, AI decision review, approved follow-up queue, risk register, value report, board memo |
| **Proof metric** | Recurring monthly value, documented retainer opportunities, monthly Proof Pack |
| **Inputs required** | Dealix Portal access, regular pipeline updates, approval on every external action |
| **Exclusions** | No autonomous external send, no legal advice, no external representation |
| **Upgrade path** | → AI Governance / Board Decision Memo |
| **Delivery mode today** | Founder-assisted / semi-automated — manual monthly operation |
| **Action mode** | `approval_required` per external action |

## Service 3: AI Governance for Revenue Teams

| Item | Detail |
|------|--------|
| **Price** | **Scoped** |
| **Target customer** | A revenue team using AI without clear boundaries or policy |
| **Problem solved** | "The team uses AI fast and without governance — we need boundaries and rules" |
| **Deliverables** | Allowed / forbidden AI actions, approval boundaries, source rules, no-autonomous-external-send policy, evidence logging |
| **Proof metric** | An approved and applied policy, documented approval boundaries |
| **Inputs required** | Inventory of current AI use, revenue workflows, decision owners |
| **Exclusions** | No legal advice, no formal compliance audit |
| **Upgrade path** | → Governed Ops Retainer / Trust Pack Lite |
| **Delivery mode today** | Founder-assisted / semi-automated |
| **Action mode** | `approval_required` |

## Service 4: CRM / Data Readiness for AI

| Item | Detail |
|------|--------|
| **Price** | **Scoped** |
| **Target customer** | A B2B company that wants to use AI but whose data is not ready |
| **Problem solved** | "Our data is messy — we cannot trust it as a source for a governed decision" |
| **Deliverables** | CRM hygiene report, source mapping, missing fields, duplicate accounts, lifecycle stage issues, data readiness score, AI readiness recommendation |
| **Proof metric** | A documented data readiness score, delivered source map |
| **Inputs required** | CRM export or account list, current ICP description |
| **Exclusions** | No data scraping, no direct CRM integration without approval |
| **Upgrade path** | → Revenue Intelligence Sprint / Governed Ops Retainer |
| **Delivery mode today** | Founder-assisted / semi-automated |
| **Action mode** | `approval_required` |

## Service 5: Board Decision Memo

| Item | Detail |
|------|--------|
| **Price** | **Scoped** |
| **Target customer** | A founder / C-Suite / board needing governed revenue and capital decisions |
| **Problem solved** | "We need a clear decision memo with sources and evidence, not empty dashboards" |
| **Deliverables** | Top revenue decisions, pipeline risks, AI governance risks, capital allocation, build / hold / kill recommendations |
| **Proof metric** | A memo used in a leadership meeting, a Decision Passport per recommendation |
| **Inputs required** | Pipeline data, leadership priorities, capital constraints |
| **Exclusions** | No investment advice, no guaranteed forecasts |
| **Upgrade path** | → Governed Ops Retainer |
| **Delivery mode today** | Founder-assisted / semi-automated |
| **Action mode** | `approval_required` |

## Service 6: Trust Pack Lite

| Item | Detail |
|------|--------|
| **Price** | **Scoped** |
| **Target customer** | A customer who explicitly raised an `asks_for_security` signal |
| **Problem solved** | "We need evidence of safety and trust boundaries before we expand AI use" |
| **Deliverables** | AI action policy, approval matrix, evidence handling, forbidden actions, agent safety rules, trust boundaries |
| **Proof metric** | A delivered and reviewed trust pack, documented trust boundaries |
| **Inputs required** | AI use scope, the customer's security requirements |
| **Exclusions** | Offered **only** on an `asks_for_security` signal — never presented proactively |
| **Upgrade path** | → AI Governance / Governed Ops Retainer |
| **Delivery mode today** | Founder-assisted / semi-automated |
| **Action mode** | `approval_required` |

## Quick Price Summary

| # | Service | Price | Status | Delivery mode |
|---|---------|-------|--------|---------------|
| 0 | Governed Revenue Ops Diagnostic | Free | Available now | Verified product |
| 1 | Revenue Intelligence Sprint | 25,000 SAR | After diagnostic | Founder-assisted |
| 2 | Governed Ops Retainer | 4,999–35,000 SAR/mo | After Sprint | Founder-assisted / semi-automated |
| 3 | AI Governance for Revenue Teams | Scoped | After qualification | Founder-assisted / semi-automated |
| 4 | CRM / Data Readiness for AI | Scoped | After qualification | Founder-assisted / semi-automated |
| 5 | Board Decision Memo | Scoped | After qualification | Founder-assisted / semi-automated |
| 6 | Trust Pack Lite | Scoped | On `asks_for_security` signal | Founder-assisted / semi-automated |

---

## Related documents — وثائق ذات صلة

- `docs/strategy/GOVERNED_REVENUE_AI_OPERATIONS.md` — canonical positioning and strategy.
- `docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md` — build triggers.
- `docs/COMPANY_SERVICE_LADDER.md` — prior ladder (superseded by this v2).

---

## Changelog

- **v2 — 2026-05-16.** Supersedes the v1.1 ladder (Free Diagnostic →
  499 SAR 7-Day Sprint → 1,500 SAR Pack → 2,999–4,999 SAR/mo Managed Ops →
  7,500–15,000 SAR/mo Command Center → Agency Partner OS). Replaced with the
  7-service Governed Revenue & AI Operations catalog per the founder's
  strategy refresh — see `docs/strategy/GOVERNED_REVENUE_AI_OPERATIONS.md`.
  Core paid offer moves from 499 SAR to the 25,000 SAR Revenue Intelligence
  Sprint; the recurring tier becomes the 4,999–35,000 SAR/mo Governed Ops
  Retainer.
- **v1.1 — 2026-05-16.** Delivery-mode disclosure added (now retired with v2).

---

*Version 2 | No guaranteed claims | Missing data = insufficient_data.*

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
