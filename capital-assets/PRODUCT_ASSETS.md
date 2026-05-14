# أصول المنتج — Product Assets

> النوع: `product_asset` | آخر مراجعة: 2026-05-14
> مصدر: [`capital_asset_registry.py`](../auto_client_acquisition/capital_os/capital_asset_registry.py)

أصول المنتج هي الأسطح التشغيلية التي يستخدمها المؤسس يومياً — ليست شرائح، ليست تقارير، بل لوحات تحكّم حية متّصلة بمصادر الحقيقة. أصل واحد مُسجَّل: CAP-014 (Founder Command Center).

Product assets are the live operational surfaces the founder uses daily — not slides, not reports, but live dashboards wired to the sources of truth. One registered: CAP-014 (Founder Command Center).

---

## CAP-014 — Founder Command Center

**Maturity:** live | **Proof level:** test-backed | **Public:** False
**Files:**
- `api/routers/founder_command_center.py`
- `landing/founder-command-center.html`
- `tests/test_founder_command_center.py`

### الدور الاستراتيجي (AR)
لوحة زجاج واحدة — تجمع: حالة النشر، حالة العقيدة، درجات سُلَّم العروض الثلاث، روتين المؤسس اليومي، ARR الجاري، وسِجِل الأصول الرأسمالية. مكان واحد يفتحه المؤسس صباحاً ليرى الحالة الكلّية للشركة بدون التنقّل بين عشر أدوات.

### Strategic role (EN)
A single pane of glass — combining: deploy status, doctrine status, the three ladder rungs, founder daily routine, live ARR, and the Capital Asset registry. One surface the founder opens in the morning to see the whole-company state without rotating through ten tools.

### Buyer relevance
مؤسس، مستشار.

### استخدام تجاري (AR)
- انضباط تشغيلي للمؤسس — كل صباح، فتح Command Center قبل أي شيء آخر.
- سطح عرض للمستشار — في الاجتماع الأسبوعي مع المستشار، الـCommand Center هو الشاشة المشتركة.

### Commercial use (EN)
- Founder operational discipline — every morning, open Command Center before anything else.
- Advisor demo surface — in the weekly advisor sync, the Command Center is the shared screen.

### متى تُظهره (AR)
**ليس** للمشتري. **ليس** للمستثمر في الاجتماع الأول. هذا أصل داخلي (`public=False`) — يُفتح فقط في:

1. الاجتماع الأسبوعي مع المستشار التشغيلي.
2. مكالمة "افتح الكابوت" مع شريك راسٍ بعد توقيع NDA.
3. عرض "اليوم في حياة المؤسس" لمرشّح أول ٣ تعيينات (CAP-011).

### When to surface (EN)
**Not** to the buyer. **Not** to the investor in the first meeting. This is an internal asset (`public=False`) — it surfaces only in:

1. The weekly sync with the operational advisor.
2. An "open-the-hood" call with an anchor partner after NDA.
3. The "day in the life of the founder" demo to a candidate for one of the first 3 hires (CAP-011).

### الخطوط الحمراء المرتبطة
`no_unsourced_claims` — كل عدّاد على Command Center متّصل بمصدر حقيقة في الكود؛ لا توجد أرقام مرسومة يدوياً، ولا "تقديرات تقديم العرض".

### Linked non-negotiables (EN)
`no_unsourced_claims` — every counter on the Command Center wires to a source of truth in code; no hand-drawn numbers, no "pitch-time estimates".

---

## لماذا أصل واحد فقط؟ (AR) / Why only one? (EN)

- **AR:** فلسفة Dealix هي أن المنتج الحقيقي قليل وعميق، لا كثير وسطحي. واجهة المؤسس الواحدة المتقنة أفضل من خمس لوحات نصف-جاهزة. الـCommand Center سيُولِّد منتجات فرعية مع نضوج كل سطح — في تلك اللحظة، تُسجَّل كأصول رأسمالية مستقلة.
- **EN:** The Dealix doctrine is that real product is few and deep, not many and shallow. One polished founder surface beats five half-built dashboards. The Command Center will spawn child products as each surface matures — at that moment, they get registered as independent Capital Assets.

---

## المسار التالي (AR) / Roadmap (EN)

- **AR:** أصول المنتج المخطّط لها (غير مُسجَّلة بعد): لوحة المشتري المؤسسي، لوحة الشريك الراسي، لوحة المستثمر الحيّة. كل واحدة ستدخل المكتبة عندما تجتاز مدقّق Wave.
- **EN:** Planned product assets (not yet registered): enterprise-buyer surface, anchor-partner surface, live investor surface. Each enters the library when it passes the wave validator.

---

*Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.*
