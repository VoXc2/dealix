# عرض ما قبل التأسيس — Pre-Seed Pitch
## ديلكس · Dealix — Governed AI Operations for Saudi B2B services

> **Audience / الجمهور:** Sanabil, STV, Wa'ed, Raed — and the strategic advisors who travel with them.
> صناديق سنابل، STV، وعد، رائد — والمستشارون الاستراتيجيون المرتبطون بهم.
> **Status / الحالة:** Pre-revenue. Conversation opener, not a term sheet.
> ما قبل الإيراد. هذا فاتحة حوار، ليس term sheet.
> **Reads alongside / يُقرأ مع:** `docs/sales-kit/INVESTOR_ONE_PAGER.md` (positioning), `docs/strategic/GCC_EXPANSION_STRATEGY.md` (geographic plan), `docs/THE_DEALIX_PROMISE.md` (doctrine).

---

## ١. السطر الرئيسي · Headline

### العربية

ديلكس هو طبقة عمليات الذكاء الاصطناعي المحوكمة التي تتبنّاها شركات الخدمات السعودية B2B لأن البديل هو شراء أداة ذكاء اصطناعي لن يوافق عليها أي مدير أمن معلومات. النموذج هو سلعة. الحوكمة العلنية المفروضة برمجيًا هي الخندق.

### English

Dealix is the Governed AI Operations layer Saudi B2B services adopts because the alternative is buying an AI tool no CISO will approve. The model is a commodity. Publicly committed, code-enforced governance is the moat.

---

## ٢. المشكلة · Problem

### العربية

شركات الخدمات السعودية في الشريحة الوسطى (٥٠–٥٠٠ موظف) عندها مشكلتان متشابكتان لا أحد يحلّهما معًا. الأولى: ألم ذكاء الإيرادات. مصادر حقيقة متفرّقة (CRM، مالي، عمليات)، توقّعات إيراد غير دقيقة، تقارير شهرية للمجلس مبنية على Excel هش. الثانية: فجوة حوكمة PDPL/NDMO. المادة ١٨ سارية، NDMO يفرض نضج بيانات، ومدير أمن المعلومات يرفض أي أداة لا تكشف محيطها للجمهور.

الاستشارات الكبرى تبيع وثائق بميزانية ربع ١٠٠–٣٠٠ ألف ريال وزمن تسليم ربع كامل. أدوات SaaS الأجنبية لا تقرأ اللائحة العربية، لا تتكامل مع ZATCA، ولا تُجيب على سؤال CISO عن المحيط. البناء الداخلي يستغرق ١٨ شهرًا قبل أول مخرج. النتيجة: السوق يَشتري شيئًا لا يحلّ المشكلة، أو لا يَشتري شيئًا أصلًا.

### English

Saudi mid-market B2B services (50–500 employees) carries two intertwined pains no vendor solves together. First, revenue intelligence pain: scattered sources of truth (CRM, finance, ops), inaccurate forecasts, monthly board reports stitched in fragile Excel. Second, the PDPL/NDMO governance gap: Article 18 is live, NDMO mandates data maturity, and the CISO rejects any tool that does not expose its perimeter publicly.

Big advisory sells documents at 100–300K SAR per quarter with quarter-long delivery cycles. Foreign SaaS does not read the Arabic regulation, does not integrate with ZATCA, and cannot answer the CISO's perimeter question. An internal build takes 18 months before the first deliverable. The market either buys something that does not solve the problem, or does not buy at all.

---

## ٣. القناعة · Insight

### العربية

الخندق ليس النموذج. الخندق هو العقيدة. ١١ بندًا غير قابلة للتفاوض (`auto_client_acquisition/governance_os/non_negotiables.py`) منشورة علنيًا، مفروضة باختبارات CI تمر في كل push، يمكن لأي CISO التحقق منها في ثوانٍ:

```bash
curl https://api.dealix.me/api/v1/dealix-promise/markdown
```

النموذج التنبؤي يُستنسخ في ربع. واجهة المستخدم تُستنسخ في شهر. التزام عام مفروض كودًا — لا يُستنسخ دون إعادة بناء ثقافة التسليم بالكامل، وهذا قرار يستغرق سنين.

### English

The moat is not the model. The moat is the doctrine. 11 non-negotiables (`auto_client_acquisition/governance_os/non_negotiables.py`) published publicly, enforced by CI tests that must pass on every push, verifiable by any CISO in seconds via the public manifesto endpoint. A forecast model is cloned in a quarter. A UI is cloned in a month. A public commitment enforced in code is not cloned without rebuilding an entire delivery culture — a multi-year decision.

---

## ٤. المنتج · Product

### العربية

سُلَّم العروض ٢٠٢٦-Q2 يتألف من ثلاثة عناصر فقط، كل واحد مُسجَّل في `auto_client_acquisition/service_catalog/registry.py`:

| العرض | السعر | المدة | المخرج المحوري |
|---|---|---|---|
| التشخيص الاستراتيجي | ٠ ر.س | يوم عمل واحد | تقرير وضع PDPL + خطة ٩٠ يومًا |
| ريتينر العمليات المحوكمة | ٤٬٩٩٩ ر.س / شهر | حد أدنى ٣ أشهر | تقرير قيمة شهري قابل للتدقيق |
| سبرنت ذكاء الإيرادات | ٢٥٬٠٠٠ ر.س | ٣٠ يومًا | Capital Asset مُسجَّل + Proof Pack موقَّع |

كل ارتباط مغلق يودع Capital Asset واحدًا على الأقل في `capital_ledger`. الأصل يبقى ملك العميل بعد انتهاء التعاقد. الارتباط القادم يبدأ متقدّمًا بسبب الارتباط السابق. هذه ليست استراتيجية — هذه بنية اقتصادية: هامش يَتراكم لأن المخرَج يَتراكم.

### English

The 2026-Q2 ladder has exactly three offerings, each registered in `auto_client_acquisition/service_catalog/registry.py`:

| Offering | Price | Duration | Core deliverable |
|---|---|---|---|
| Strategic Diagnostic | 0 SAR | 1 working day | PDPL posture report + 90-day plan |
| Governed Ops Retainer | 4,999 SAR / month | 3-month minimum | Audit-ready monthly Value Report |
| Revenue Intelligence Sprint | 25,000 SAR | 30 fixed days | Registered Capital Asset + signed Proof Pack |

Every closed engagement deposits at least one Capital Asset in `capital_ledger`. The asset remains the customer's property after the contract ends. The next engagement starts ahead because of the prior one. This is not strategy — it is an economic structure: margin compounds because deliverables compound.

---

## ٥. لماذا الآن · Why now

### العربية

النافذة التنظيمية مفتوحة الآن. تطبيق PDPL مع المادة ١٨ سارٍ، NDMO يطلب نضج بيانات، رؤية ٢٠٣٠ تَدفع نحو السيادة الرقمية، والهيجان حول الذكاء الاصطناعي خَلق طلبًا من المشتري على عمليات محوكمة — لا أدوات لامعة. النافذة محدودة بـ ٢٤ شهرًا قبل أن يَتشكّل سوق ناضج وتنخفض هامش الأول-للسوق.

ديلكس دخل بعقيدة أولًا، لا منتج أولًا. هذا قرار غير عادي. الشركات الأخرى تَبني المنتج وتُلصق الحوكمة لاحقًا. ديلكس بَنى الحوكمة (١١ اختبار CI) قبل أن يَكتب صف منتج واحد لعميل. هذا الترتيب يَنعكس على الخندق.

### English

The regulatory window is open now. PDPL enforcement with Article 18 is live, NDMO mandates data maturity, Vision 2030 pushes digital sovereignty, and AI hype has created buyer demand for governed operations — not shiny tools. The window is bounded at ~24 months before a mature market forms and first-mover margin compresses.

Dealix entered doctrine-first, not product-first. That is an unusual decision. Most companies build the product and bolt governance on later. Dealix built the governance (11 CI tests) before it shipped a single customer-facing product line. That ordering shows up in the moat.

---

## ٦. وضع الجذب · Traction posture

### العربية

سنكون صادقين: قبل الإيراد. ما هو في الإنتاج اليوم على `api.dealix.me`: نقطة نهاية Promise العامة، الخريطة التجارية، Founder Command Center العام. سُلَّم العروض الثلاثة فُعِّل في الكود، الأرضية ٤٬٩٩٩ ر.س / شهر مَكتوبة (`registry.py` — السطر ٩١)، Moyasar متكامل في وضع الاختبار جاهز للقطع الحي، ZATCA Phase 2 مُختبَر.

ما ليس في الإنتاج: فاتورة رقم ١. لن نتظاهر بعكس ذلك. خط أنابيب الشركاء المرتكزين مَزروع — Big 4 advisory، مزوّدو دفع مرخّصون من ساما. القناة المُختصرة للثقة في السوق السعودي هي ما نَطلب الحوار حوله، لا التمويل.

كل رقم في هذه الصفحة قابل للإرجاع إلى ملف في المستودع. لا ادعاء إيراد افتراضي. لا نسبة تحويل بدون مرجع. لا حجم سوق بدون مصدر عام.

### English

We will be direct: pre-revenue. In production today on `api.dealix.me`: the public Promise endpoint, the commercial map, the public Founder Command Center. The 3-offer ladder is live in code, the 4,999 SAR/month floor is written into `registry.py` (line 91), Moyasar is integrated in test mode and ready for live cutover, ZATCA Phase 2 is tested.

What is not yet shipped: invoice #1. We will not pretend otherwise. The anchor partner pipeline is seeded — Big 4 advisory, SAMA-licensed processors. The trusted channel that compresses six months of trust-building in the Saudi market is what we are asking about, not capital.

Every number on this page resolves to a file in the repository. No hypothetical revenue claim. No conversion rate without a code reference. No market size without a public source.

---

## ٧. اقتصاديات الوحدة · Unit economics

### العربية

أرقام تقديرية صريحة. مَوسومة `is_estimate=True` في الكود.

- **ريتينر LTV (حد أدنى):** ٤٬٩٩٩ × ٣ أشهر = **١٤٬٩٩٧ ر.س** أرضية لكل عميل ريتينر.
- **سبرنت:** ٢٥٬٠٠٠ ر.س لمرة واحدة، ٣٠ يومًا.
- **هامش إجمالي مستهدف:** ~٨٥٪ على السبرنت، ~٧٠٪ على الريتينر (المرجع: نموذج التسعير في `api/routers/cost_tracking.py`).
- **تركّب Capital Asset:** كل سبرنت يَودع أصلًا قابلًا لإعادة الاستخدام في السبرنت التالي → التكلفة الحديّة تَنخفض بَعد كل ارتباط.

### English

Estimated numbers, explicitly flagged. Marked `is_estimate=True` in code.

- **Retainer LTV floor:** 4,999 × 3 months = **14,997 SAR** floor per retainer customer.
- **Sprint:** 25,000 SAR one-time, 30 days.
- **Target gross margin:** ~85% on Sprint, ~70% on Retainer (reference: tier model in `api/routers/cost_tracking.py`).
- **Capital Asset compounding:** every Sprint deposits a reusable asset for the next Sprint → marginal cost falls after each engagement.

---

## ٨. الطلب · The ask

### العربية

نَطلب حوار ما قبل تأسيس، لا term sheet اليوم. ثلاثة مخرجات من هذه المحادثة:

1. **مقدمة شريك مرتكز واحد** — Big 4 advisory أو مزوّد دفع مرخّص من ساما.
2. **التزام مستشار استراتيجي واحد** — ساعتان / شهر، خبرة قطاع.
3. **تاريخ نَعود فيه** — بعد ما تَهبط فاتورة رقم ٢، نَعود بوضع جذب موثَّق ومحادثة تسعير حقيقية.

نحن لسنا في عَجَلة لإغلاق جولة. نحن في عَجَلة لإغلاق أول فاتورتين بالطريقة الصحيحة، ثم بعدها نَتحدّث.

### English

We are asking for a pre-seed conversation, not a term sheet today. Three outcomes from this meeting:

1. **One anchor partner introduction** — Big 4 advisory or SAMA-licensed processor.
2. **One strategic advisor commitment** — 2 hours / month, sector experience.
3. **A date to revisit** — once invoice #2 lands, we come back with documented traction and a real pricing conversation.

We are not in a rush to close a round. We are in a rush to close the first two invoices the right way, and only then talk valuation.

---

## ٩. ثلاثة أشياء لن نفعلها · Three things we will never do

### العربية

1. **لا أتمتة outreach بارد.** لا WhatsApp بلا إذن، لا LinkedIn آلي، لا قوائم مسروقة، لا blast.
2. **لا ذكاء اصطناعي بلا مصدر.** كل ادعاء يَحمل Source Passport.
3. **لا إغلاق مشروع بدون Capital Asset.** كل ارتباط يَنتهي بأصل مُسجَّل في `capital_ledger`.

هذه ليست تَفضيلات تجارية. هي بنود يَفشل CI عند انتهاكها. المرجع الكامل: `docs/THE_DEALIX_PROMISE.md`.

### English

1. **No cold outreach automation.** No unconsented WhatsApp, no LinkedIn automation, no scraped lists, no blasts.
2. **No AI without source.** Every claim carries a Source Passport.
3. **No project close without a Capital Asset.** Every engagement ends with an asset registered in `capital_ledger`.

These are not commercial preferences. They are clauses that fail CI when violated. Full reference: `docs/THE_DEALIX_PROMISE.md`.

---

## ١٠. مراجع · Cross-links

- `docs/sales-kit/INVESTOR_ONE_PAGER.md` — anchor-partner positioning (this pitch extends it).
- `docs/sales-kit/PRICING_REFRAME_2026Q2.md` — pricing decisions + KPIs.
- `docs/strategic/GCC_EXPANSION_STRATEGY.md` — 12-month regional plan.
- `docs/THE_DEALIX_PROMISE.md` — 11 non-negotiables.
- `docs/funding/SAFE_NOTE_TEMPLATE.md` — convertible note placeholder (lawyer to finalize).
- `auto_client_acquisition/service_catalog/registry.py` — pricing source of truth.

---

> **Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
