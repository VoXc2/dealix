# أصول المبيعات — Sales Assets

> النوع: `sales_asset` | آخر مراجعة: 2026-05-14
> مصدر: [`capital_asset_registry.py`](../auto_client_acquisition/capital_os/capital_asset_registry.py)

أصول المبيعات هي الأسطح التي تُحوِّل المحادثة من "ما هذا؟" إلى "كيف نبدأ؟". أصلان مُسجَّلان: CAP-004 (سُلَّم العروض)، CAP-005 (خريطة التوصيل التجاري).

Sales assets are the surfaces that convert the conversation from "what is this?" to "how do we start?". Two registered: CAP-004 (offer ladder), CAP-005 (commercial map).

---

## CAP-004 — 3-Offer Commercial Ladder

**Maturity:** live | **Proof level:** test-backed | **Public:** True
**Files:**
- `auto_client_acquisition/service_catalog/registry.py`
- `api/routers/commercial_map.py`
- `docs/OFFER_LADDER_AND_PRICING.md`
- `docs/COMMERCIAL_WIRING_MAP.md`
- `docs/sales-kit/PRICING_REFRAME_2026Q2.md`
- `landing/pricing.html`

### الدور الاستراتيجي (AR)
إعادة صياغة الربع الثاني ٢٠٢٦: تشخيص مجاني / ريتينر ٤٬٩٩٩ ريال / Sprint بـ٢٥٬٠٠٠ ريال. ثلاث درجات لا أكثر — كل درجة لها مُحفِّز قرار مختلف، وكل واحدة تُوصِّل إلى الدرجة التالية تلقائياً.

### Strategic role (EN)
The 2026-Q2 reframe: Free Diagnostic / 4,999 SAR Retainer / 25,000 SAR Sprint. Three rungs, no more — each rung has a different decision trigger and routes to the next automatically.

### Buyer relevance
مؤسس خدمات B2B سعودي، COO خدمات B2B سعودي، CFO.

### متى تُظهره في محادثة المبيعات (AR)
في الدقيقة الأولى من المكالمة الأولى. سُلَّم العروض هو محرّك تأهيل: المؤسس الذي يرفض التشخيص المجاني ليس عميلاً. المشتري الذي يقفز مباشرة إلى Sprint بدون ريتينر يحتاج تشخيصاً قبل أي شيء.

### When to surface in sales (EN)
First minute of the first call. The ladder is a qualification engine: a founder who refuses the free diagnostic is not a customer. A buyer who jumps straight to Sprint without a Retainer needs a diagnostic before anything else.

### استخدام تجاري (AR) / Commercial use (EN)
- **AR:** مرساة تسعير، توليد مقترح آلي، محرّك تأهيل.
- **EN:** Pricing anchor, automated proposal generation, qualification engine.

### الخطوط الحمراء المرتبطة
`no_guaranteed_outcomes`، `no_unsourced_claims` — السُلَّم لا يَعِد بأرقام مبيعات، يَعِد بنطاق محدّد ومخرجات قابلة للمراجعة.

---

## CAP-005 — Commercial Map API

**Maturity:** live | **Proof level:** test-backed | **Public:** True
**Files:**
- `api/routers/commercial_map.py`
- `tests/test_commercial_map.py`
- `docs/COMMERCIAL_WIRING_MAP.md`

### الدور الاستراتيجي (AR)
خريطة سلكية تجارية عامة — كل عرض موصول علناً بصفحة الهبوط الخاصة به، نقطة النهاية الـ API، وسطح التسليم. لا توجد ادعاءات تجارية بدون ملف يُنفِّذها.

### Strategic role (EN)
Public commercial wiring map — every offer is publicly wired to its landing page, API endpoint, and delivery surface. There is no commercial claim without a file that enforces it.

### Buyer relevance
شريك، مشتريات، استشارات Big 4.

### متى تُظهره في محادثة المبيعات (AR)
في محادثة الشراكة، عندما يسأل الشريك الراسي "كيف نعرف أن عروضكم حقيقية وليست شرائح؟". الإجابة: `curl /api/v1/commercial-map`. كل سطر في الاستجابة يُوصِّل إلى ملف يُنفّذه.

### When to surface in sales (EN)
In a partner conversation, when the anchor partner asks "how do we know your offers are real, not slides?". The answer: `curl /api/v1/commercial-map`. Every line of the response wires to a file that enforces it.

### استخدام تجاري (AR) / Commercial use (EN)
- **AR:** عناية واجبة للشريك، شفافية تشغيلية.
- **EN:** Partner diligence, operational transparency.

### الخطوط الحمراء المرتبطة
`no_unsourced_claims` — كل عرض يجب أن يُوصَل إلى ملف يُنفِّذه؛ الخريطة هي الدليل.

---

## استخدام مُجمَّع (AR) / Combined use (EN)

- **AR:** CAP-004 يُعطي المشتري سعراً واضحاً ونطاقاً محدّداً. CAP-005 يُعطي الشريك وفريق المشتريات سطحاً للتحقق من أن كل عرض موصول بملف حقيقي. معاً، يُسقطان الاحتكاك التجاري في خطوتين: التأهيل ثم التحقق.
- **EN:** CAP-004 gives the buyer a clear price and a defined scope. CAP-005 gives the partner and procurement a surface to verify that every offer wires to a real file. Together they collapse commercial friction into two steps: qualification, then verification.

---

*Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.*
