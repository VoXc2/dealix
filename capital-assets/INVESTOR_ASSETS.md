# أصول المستثمر — Investor Assets

> النوع: `investor_asset` | آخر مراجعة: 2026-05-14
> مصدر: [`capital_asset_registry.py`](../auto_client_acquisition/capital_os/capital_asset_registry.py)

أصول المستثمر هي السرديّات والوثائق التي تُهيكل محادثة الجولة قبل الجولة — قبل أن يطلب صندوق Sanabil أو STV ورقة شروط. أصل واحد مُسجَّل: CAP-010 (الورقة الواحدة + مذكرة التمويل).

Investor assets are the narratives and documents that structure the pre-round conversation — before Sanabil or STV ask for a term sheet. One registered: CAP-010 (one-pager + funding memo).

---

## CAP-010 — Investor One-Pager + Funding Memo

**Maturity:** draft | **Proof level:** doc-backed | **Public:** False
**Files:**
- `docs/sales-kit/INVESTOR_ONE_PAGER.md`
- `docs/funding/FUNDING_MEMO.md`
- `docs/funding/USE_OF_FUNDS.md`
- `docs/funding/WHY_NOW_GCC_AI_OPS.md`

### الدور الاستراتيجي (AR)
سردية مستثمر من صفحة واحدة ثنائية اللغة + مذكرة تمويل + استخدام الأموال + ملف "لماذا الآن". أربع وثائق تُجيب على أربعة أسئلة يطرحها كل مستثمر في الدقائق العشر الأولى: ماذا تبنون؟ لماذا الآن؟ ماذا ستفعلون بالمال؟ كيف نخرج؟

### Strategic role (EN)
A bilingual single-page investor narrative + funding memo + use-of-funds + "why now" file. Four documents that answer the four questions every investor asks in the first ten minutes: what are you building? why now? what will you do with the money? how do we exit?

### Buyer relevance
Sanabil، STV، Wa'ed Ventures، Raed Ventures، ملاك سعوديون.

### استخدام تجاري (AR)
- فاتح محادثة ما قبل التأسيس.
- توظيف مستشار (المستشار يقرأ المذكرة قبل أن يقبل).

### Commercial use (EN)
- Pre-seed conversation starter.
- Advisor recruitment (an advisor reads the memo before saying yes).

### متى تُظهره (AR)
**ليس** في أول إيميل. السرديّة المختصرة (paragraph) أولاً عبر مقدّمة موثّقة، ثم الورقة الواحدة في الردّ. مذكرة التمويل بعد المكالمة الأولى، فقط لو طلبها المستثمر صراحة. هذا التسلسل يحترم وقت المستثمر ويبني الجاذبية تدريجياً.

### When to surface (EN)
**Not** in the first email. A one-paragraph narrative first via a documented introduction, then the one-pager in the reply. The funding memo *after* the first call, only if the investor explicitly requests it. This sequence respects the investor's time and builds pull gradually.

### الخطوط الحمراء المرتبطة (AR)
- `no_guaranteed_outcomes` — مذكرة التمويل لا تحتوي على أي أرقام إيرادات موعودة. كل توقّع مُحدَّد كـ "تقديري" مع منهجية واضحة.
- `no_unsourced_claims` — كل ادعاء حول حجم السوق أو نسبة النمو يُوصَل إلى مصدر منشور (Statista، PwC ME، تقرير GASTAT).

### Linked non-negotiables (EN)
- `no_guaranteed_outcomes` — the funding memo contains no promised revenue numbers. Every projection is labelled "estimated" with explicit methodology.
- `no_unsourced_claims` — every market-size or growth-rate claim wires to a published source (Statista, PwC ME, GASTAT report).

---

## السبب الذي يجعل النضوج "draft" (AR) / Why maturity is "draft" (EN)

- **AR:** الأصل في حالة `draft` لأنه يُختبر مع مستشار واحد في المرة قبل أن يخرج إلى مستثمر مؤسسي. حالة "live" تُمنح فقط بعد أن يقرأه ثلاثة مستشارين على الأقل ويُجمعوا أن السرديّة قابلة للدفاع. هذا انضباط يحفظ السمعة قبل الجولة.
- **EN:** The asset sits at `draft` because it is tested with one advisor at a time before going to an institutional investor. "Live" status is granted only after at least three advisors have read it and converged that the narrative is defensible. This discipline protects reputation before the round.

---

## الفرق بين الورقة الواحدة والمذكرة (AR) / Pager vs memo (EN)

| Document | Length | Audience | When |
|---|---|---|---|
| Investor One-Pager | 1 page | First investor read | Email reply after intro |
| Funding Memo | 5-7 pages | Investor + their analyst | After call 1, on request |
| Use of Funds | 2 pages | Investor + advisor | Diligence stage |
| Why Now (GCC AI Ops) | 3 pages | Investor + their LP | Diligence stage |

---

## مبدأ سرديّة الجولة (AR) / Narrative principle (EN)

- **AR:** Dealix لا تبيع نموّاً مُتوقَّعاً، تبيع عقيدة موثَّقة بكود وأصولاً رأسمالية قابلة للتدقيق. المستثمر يرى أن المُخاطرة التشغيلية مُدارة قبل أن يرى أن السوق كبير. هذا ترتيب مختلف، لكنه الترتيب الذي ينجح مع رأس المال السعودي.
- **EN:** Dealix does not sell projected growth; it sells documented doctrine and auditable capital assets. The investor sees that operational risk is managed before they see that the market is large. A different order — but the order that works with Saudi capital.

---

*Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.*
