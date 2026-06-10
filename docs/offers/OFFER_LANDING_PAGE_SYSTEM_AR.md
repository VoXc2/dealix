# نظام صفحات العروض — Offer Landing Page System
<!-- Agent #33 — Owner: Marketing | Date: 2026-06-03 -->
<!-- Arabic primary — العربية أولاً | Internal reference, not a public page -->

> **الغرض:** توثيق الهيكل والأسلوب المشترك بين صفحات العروض الست الأساسية في Dealix، بحيث تكون الصفحات متّسقة بصرياً ونبرة ومحتوى، ويبقى تحديثها سهلاً.

> **النطاق:** هذا النظام يخصّ صفحات `docs/offers/*_PAGE_AR.md` فقط. صفحات المبيعات الداخلية في `docs/sales/*` و`docs/sales-kit/*` خارج النطاق، لكنها مرجع أسلوب.

---

## 1. المبادئ التأسيسية

### 1.1 القواعد الذهبية (Hard constraints)

| # | القاعدة | كيف نطبّقها |
|---|---------|-------------|
| 1 | **لا ادعاءات مضمونة** | كل عبارة نفعية تُسبق بمستوى دليل (`assumed` / `observed` / `validated` / `measured`) |
| 2 | **لا برهان مفبرك** | لا شعارات شركات، لا أرقام مبيعات، لا شهادات عملاء. placeholder صريح إذا لا يوجد دليل |
| 3 | **لا ROI مبالغ فيه** | لا "500%"، لا "10x"، لا "ضمان" |
| 4 | **Arabic-first** | كل المحتوى الأساسي بالعربية. النسخة الإنجليزية إن وُجدت مشتقة منها، لا العكس |
| 5 | **CTA واضح** | كل صفحة فيها CTA رئيسي + ثانوي + WhatsApp (بعد موافقة) |
| 6 | **تسعير نطاقي** | نطاقات فقط ("founder-confirmed band: X–Y SAR")، لا أسعار نهائية على الصفحة |

### 1.2 مستويات الأدلة (Evidence levels)

نستخدم نفس المستويات المعتمدة في `docs/EXECUTIVE_DECISION_PACK.md` و`docs/responsible_ai/`:

| المستوى | الرمز | المعنى | متى يُستخدم |
|---------|------|-------|--------------|
| **L0 — Assumed** | `assumed` | فرضية بدون تحقق | الافتراضات التشخيصية، تقديرات النطاق |
| **L1 — Observed** | `observed` | شوهد في السوق/قطاع | معطيات السوق العامة |
| **L2 — Validated** | `validated` | تحقّق منه مصدر مستقل | دراسة حالة، تقرير طرف ثالث |
| **L3 — Measured** | `measured` | تمّ قياسه منّا على عميل حقيقي | Proof Pack موثّق |

> **قاعدة:** أي ادّعاء عن نتيجة (>0) يجب أن يكون `measured`. أي ادعاء عن توفر ميزة (`assumed`/`observed`).

---

## 2. الهيكل الموحّد (13 قسم لكل عرض)

كل صفحة عرض تتبع نفس الترتيب. لا نحذف قسماً، ولا نضيف قسماً خارج هذه القائمة:

| # | القسم | الهدف | ملاحظات |
|---|-------|-------|---------|
| 1 | **Hero** | الجذب + CTA | headline, subheadline, primary CTA, secondary CTA |
| 2 | **المشكلة (Problem)** | إيضاح الألم | ليس تعريفاً بنا، بل تعريفاً بهم |
| 3 | **الحل (Solution)** | ماذا نفعل | بلغة العميل، لا jargon |
| 4 | **المخرجات (Deliverables)** | ماذا يحصل عليه | قائمة ملموسة + جهد/وقت |
| 5 | **العملية (Process)** | كيف نعمل | kickoff → discovery → pilot → delivery → handover |
| 6 | **الإثبات (Proof)** | ما يدعم الادعاءات | مع evidence_level؛ placeholder صريح إذا لا يوجد |
| 7 | **النطاق (Scope)** | ما هو مشمول | in scope فقط |
| 8 | **خارج النطاق (Out of scope)** | ما هو **غير** مشمول | كن صريحاً — هذا يبني ثقة |
| 9 | **نطاق التسعير (Pricing band)** | السعر كمدى | "founder-confirmed band: X–Y SAR" |
| 10 | **الأسئلة الشائعة (FAQ)** | 3–6 أسئلة | الأسئلة العامة تربط بـ `OFFER_FAQ_LIBRARY_AR.md` |
| 11 | **مسارات التحويل (CTA paths)** | 4 مسارات على الأقل | WhatsApp / Proposal / Booking / Pilot (للمؤسسات) |
| 12 | **ماذا بعد الموافقة (Next 24h / 7d / 30d)** | خطوات واضحة | يفك التردّد |
| 13 | **التجديد والتوسعة (Renewal narrative)** | القصة لما بعد التسليم | بدون أرقام صعبة |

### 2.1 ترتيب الأقسام — لماذا؟

- **Hero → Problem → Solution**: يطابق رحلة القارئ (هل هذا لي؟ هل يحلّ مشكلتي؟).
- **Deliverables + Process → Proof**: يعطي تفاصيل قبل أن يطلب "أرني دليل".
- **Scope + Out of scope → Pricing**: "ما ستحصل عليه" قبل "كم سيكلف" يخفّف حساسية السعر.
- **FAQ → CTA paths → Next → Renewal**: يختم بالـ action والـ future، لا بالمخاوف.

> **التنازل الوحيد:** CTA قد يتكرّر بعد Hero وآخر الصفحة (sticky CTA). لكن CTA الأول في Hero يبقى ثابت.

---

## 3. دليل الأسلوب (Style Guide)

### 3.1 النبرة والصوت (Voice & Tone)

> من `docs/sales-kit/dealix_brand_guidelines.md`، مُلخّص:

| البُعد | كيف نتكلم |
|--------|------------|
| **الصوت** | واثق بدون غرور. صادق. مباشر. محترم. |
| **العامية/الفصحى** | عربي فصيح مبسّط مع قبول كلمات سوقية شائعة. لا شامي، لا خليجي ثقيل. |
| **النبرة** | حماسية واثقة على الـ landing، دافئة على WhatsApp، صبّورة على الدعم. |
| **المباشرة** | جملة واحدة بدل فقرة. ابدأ بالفعل. |

### 3.2 الكلمات المحظورة (Forbidden vocabulary)

نحظر هذه الكلمات في كل صفحات العروض:

| الممنوع | البديل |
|---------|--------|
| "ثوري" / "Revolutionary" | "مُحَقَّق" / "قابل للقياس" |
| "الأفضل" / "Best" | "نساعدك على" / "نقدّم" |
| "Disruptive" | (احذف) |
| "AI-powered" لحالها | "ذكاء اصطناعي يفهم السياق السعودي" |
| "100%" (للنتائج) | "نقيس" / "نسجّل" |
| "مضمون" / "Guaranteed" | "نلتزم بـ ..." / "بالإثبات" |
| "ROI 500%" / "10x" | "تقدير نطاقات" + evidence_level |
| "حققنا لعميلنا X..." (بدون proof) | "Proof pending — first pilot will land here" |

### 3.3 القواعد التحريرية

1. **جملة قصيرة** (< 18 كلمة في المتوسط)
2. **لا تكرار**: لا تكرّر نفس الصفة في الـ H1 + subtitle + Hero
3. **ابدأ بالفعل**: "احجز تشخيص" بدل "يمكنك حجز"
4. **أرقام محدّدة بشكل حذر**: "خلال 7 أيام" ✅، "نصف ساعة بالضبط" ❌ (إلا إذا L3)
5. **لا كليشيهات**: احذف "في عصر التكنولوجيا"، "في عالم سريع التغيّر"
6. **RTL دائماً** للعربي (`direction: rtl`)

---

## 4. متطلبات الأصول البصرية (Visual asset requirements)

> صفحات العروض حالياً **محتوى** (Markdown). متى تحوّلت لـ HTML/Next.js، تطبَّق هذه المتطلبات.

### 4.1 الأيقونات (Iconography)

- **المكتبة**: Lucide (الأساسية) + أيقونات ZATCA/Saudi مخصّصة
- **النمط**: line icons (stroke 2px)، زوايا مدوّرة (2px radius)
- **الحجم**: 16/20/24px فقط (لا أحجام فردية)
- **اللون**: `#0A4D3F` للنصوص، `#C9A961` للـ CTAs

### 4.2 الصور (Imagery)

| ✅ مسموح | ❌ ممنوع |
|---------|---------|
| شركات سعودية حقيقية (بعد إذن) | Stock photos عامة |
| مكاتب بسيطة | مكاتب أجنبية (Europe/US) |
| أيادي سعودية تستخدم Dealix | صور "business people shaking hands" |
| لقطات شاشة Dealix | لقطات من منتجات منافسة |
| فواتير ZATCA، لوحات مفاتيح عربية | صور نمطية مكررة |

### 4.3 الألوان (Color tokens)

من `docs/sales-kit/dealix_brand_guidelines.md`:

```
Primary:    Dealix Deep Green  #0A4D3F
Accent:     Dealix Gold        #C9A961
Surface:    Dealix Sand        #F4F0E8
Text:       Deep Charcoal      #1A1A1A
Muted:      Warm Gray          #6B6B6B
Border:     Cool Gray          #E5E5E5
Success:    #2D7A4F
Warning:    #E8A33D
Error:      #C73E3E
Info:       #3B6B8C
```

**قاعدة 60-30-10**: 60% Sand/أبيض + 30% Deep Green + 10% Gold.

### 4.4 الخطوط (Typography)

- **عربي**: IBM Plex Sans Arabic (Bold 700 للعناوين / Regular 400 للنص / Light 300 للـ captions)
- **Fallback عربي**: Tajawal
- **English**: Inter

---

## 5. كيف نحافظ على تزامن الصفحات الست

### 5.1 القواعد التشغيلية

1. **تعديل قسم واحد = تعديل 6 صفحات** إذا كان القسم مشتركاً (Hero, FAQ, Scope, Pricing).
2. **المحتوى الفريد** يبقى محلياً في كل صفحة (Hero headline, Problem, Solution).
3. **CTA + FAQ pointer** دائماً يربطان بـ `OFFER_CTA_LIBRARY_AR.md` و`OFFER_FAQ_LIBRARY_AR.md`.
4. **مستوى الدليل** على كل ادعاء — لا "نتائج مبهرة" بدون L3.

### 5.2 كيف نعدّل قسماً مشتركاً

> مثلاً: تحديث بند في الـ Out-of-scope.

1. حدّث النص في `OFFER_LANDING_PAGE_SYSTEM_AR.md` أولاً (إن كان قاعدة عامة).
2. حدّث كل صفحات العروض الست التي تحتاج.
3. سجّل في changelog القسم 7.

### 5.3 مصادر الحقيقة (Source-of-truth rules)

| البُعد | المرجع |
|--------|--------|
| الأسلوب/العلامة التجارية | `docs/sales-kit/dealix_brand_guidelines.md` |
| التسعير (نطاقات) | `docs/OFFER_LADDER_AND_PRICING.md` (canonical) |
| سياسة الممنوعات | `docs/EXECUTIVE_DECISION_PACK.md` + `docs/responsible_ai/*` |
| WhatsApp flow | `docs/WHATSAPP_OPERATOR_FLOW.md` (لا نُكرّر) |
| Discovery script | `docs/sales/DISCOVERY_SCRIPT.md` (لا نُكرّر) |
| Objection handler | `docs/sales-kit/dealix_objection_handler.md` (لا نُكرّر) |
| Price lock (Pilot 499 SAR) | `docs/PRICING_AND_PACKAGING_V6.md` (locked حتى 5 عملاء) |

> **مبدأ:** صفحات العروض تُشير إلى المصادر بـ link، ولا تنسخها.

---

## 6. نقاط الربط بين الصفحات (Cross-offer links)

كل صفحة عرض تحتوي على روابط لصفحات أخرى حسب المنطق:

| من/إلى | Diagnostic | Followup Workflow | AI Ops Starter | Full Revenue OS | Monthly Optimization | Custom Company OS |
|--------|------------|-------------------|----------------|-----------------|----------------------|-------------------|
| **Diagnostic** | — | upgrade | upgrade | upgrade | upgrade | upgrade |
| **Followup Workflow** | entry | — | upgrade | upgrade | — | upgrade |
| **AI Ops Starter** | entry | cross-sell | — | upgrade | upgrade | upgrade |
| **Full Revenue OS** | entry | cross-sell | downgrade-if-needed | — | upgrade | upgrade |
| **Monthly Optimization** | — | — | cross-sell | prerequisite | — | upgrade |
| **Custom Company OS** | — | — | — | prerequisite | prerequisite | — |

> **القاعدة:** نُشير إلى الـ upgrade path بوضوح في كل صفحة ("بعد هذا العرض، الخطوة التالية هي X"). هذا يبني السُلّم.

---

## 7. إدارة الإصدارات (Versioning & change control)

- **كل صفحة** تبدأ بـ Frontmatter: `<!-- Agent #33 | Version: 1.0 | Last updated: YYYY-MM-DD -->`
- **التغييرات الجوهرية** (نطاق، تسعير، ممنوعات) تذهب عبر PR بفحص من المؤسس.
- **التغييرات الطفيفة** (نص، تنسيق) مباشرة، لكن يُسجَّل التاريخ.
- **Changelog القسم 7** يُحدَّث مع كل تعديل.

### 7.1 سجل الإصدارات

| Version | Date | التغيير | من |
|---------|------|---------|-----|
| 1.0 | 2026-06-03 | إنشاء النظام والصفحات الست | Agent #33 |

---

## 8. استخدام الأصول الموجودة (Link-only, do not duplicate)

> صفحات العروض **تستفيد** من هذه الأصول، لا **تكرّر**ها:

- `docs/sales-kit/dealix_onepager.md` — يُشار إليه كـ "ملخص العرض"
- `docs/sales-kit/dealix_pitch_deck.md` — يُشار إليه كـ "العرض التقديمي"
- `docs/sales-kit/dealix_objection_handler.md` — يُشار إليه في FAQ
- `docs/sales/DISCOVERY_SCRIPT.md` — يُشار إليه في CTA paths
- `docs/WHATSAPP_OPERATOR_FLOW.md` — يُشار إليه في WhatsApp path
- `docs/sales-kit/dealix_brand_guidelines.md` — يُشار إليه للأسلوب البصري
- `docs/PROOF_AND_CASE_STUDY_SYSTEM.md` — يُشار إليه لقسم Proof
- `docs/PRICING_AND_PACKAGING_V6.md` — يُشار إليه لـ pricing band

---

## 9. قائمة فحص (Definition-of-done checklist) لكل صفحة عرض

قبل اعتبار الصفحة "done"، نتحقق من:

- [ ] الـ 13 قسم كلها موجودة (لا قسم مفقود)
- [ ] Arabic-first (لا نسخة إنجليزية أولية)
- [ ] CTA رئيسي + ثانوي في Hero
- [ ] WhatsApp path مذكور مع reminder للموافقة (لا cold)
- [ ] Out-of-scope صريح ومفصّل (ليس بند واحد عام)
- [ ] Pricing كـ **نطاق** لا سعر نهائي
- [ ] كل ادعاء له evidence_level (L0–L3)
- [ ] لا ممنوعات (شركة X حققت، ROI 500%، مضمون، 100%)
- [ ] FAQ يربط بـ `OFFER_FAQ_LIBRARY_AR.md`
- [ ] CTA يربط بـ `OFFER_CTA_LIBRARY_AR.md`
- [ ] Next 24h / 7d / 30d كلها مذكورة
- [ ] Renewal narrative بدون أرقام صعبة

---

## 10. ملخّص

> **هذا النظام هو العقد بين صفحات العروض الست والعميل.** كل صفحة تلتزم بـ 13 قسم، نفس النبرة، نفس مستوى الأدلة، نفس رابط الممنوعات. التعديل في قسم مشترك = تعديل في 6 صفحات، لا أكثر، ولا أقل.

*Version 1.0 · 2026-06-03 · Agent #33 · Dealix Offer Pages System*
