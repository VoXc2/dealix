# Dealix — النزول للسوق بخمسة أنظمة (Focus 5)

> القرار التنفيذي: ينزل Dealix السوق بـ **خمسة أنظمة فقط**. كل نظام له صفحة واضحة في
> الفرونت، سعر افتتاحي واضح، خدمة قابلة للتسليم، واستهداف يومي يولّد **400 مسودة مخصصة**.
>
> القاعدة: لا نعرض «كل شيء» للعميل. نعرض **5 أنظمة قوية** تغطي أهم آلام الشركات.
> داخليًا يقدر Dealix يقدّم خدمات كثيرة، لكن خارجيًا لازم يكون واضحًا جدًا.

**مصدر الحقيقة (Source of truth):** `src/data/systems.ts` — أي تعديل على الأسماء أو
الأسعار أو محتوى الأنظمة يتم هناك أولًا، والصفحات والاختبارات تقرأ منه.

---

## 1. الأنظمة الخمسة النهائية

```txt
1. Revenue Operating System   — نظام تشغيل الإيرادات
2. Executive Command OS       — لوحة القرار التنفيذي
3. Follow-up Recovery OS      — نظام استرجاع المتابعات
4. WhatsApp Client OS         — نظام تشغيل العملاء على واتساب
5. Proposal & Proof OS        — نظام العروض والإثبات
```

### لماذا هذه الخمسة؟

لأنها تغطي رحلة الشركة كاملة:

```txt
Lead يظهر
→ يحتاج متابعة
→ يحتاج قرار إداري
→ يدخل واتساب/قناة عميل
→ يحتاج عرضًا مقنعًا ودليلًا
```

| النظام | الألم الأساسي | من نبيعه له؟ | أول نتيجة ملموسة |
| --- | --- | --- | --- |
| **Revenue Operating System** | الفرص تضيع ولا يوجد نظام next action | وكالات، تدريب، خدمات، عقار، توظيف | خريطة تسرب + pipeline متابعة |
| **Executive Command OS** | الإدارة لا ترى القرار اليومي بوضوح | مؤسس، CEO، GM، مالك وكالة/عيادة/شركة خدمات | لوحة قرار يومية |
| **Follow-up Recovery OS** | المتابعة تضيع بعد أول رسالة | تدريب، عقار، عيادات، وكالات، استشارات | follow-up queue + رسائل |
| **WhatsApp Client OS** | واتساب مليان محادثات بدون نظام | عيادات، عقار، تدريب، خدمات محلية | flows + action cards + handoff |
| **Proposal & Proof OS** | العروض ضعيفة أو بطيئة أو بلا دليل | استشارات، وكالات، B2B services | proposal + proof pack |

---

## 2. السعر في الفرونت

نعم نعرض السعر — لكن بذكاء: **أسعار افتتاحية واضحة** وليس «اتصل بنا» فقط.

السبب: في البداية نحتاج تقليل الاحتكاك وبناء الثقة. السعر الواضح يُظهر الجدية ويقلل
الرسائل غير المناسبة. لكن لا نضع سعرًا نهائيًا لكل الحالات؛ نكتب **«يبدأ من»**.

| النظام | السعر الافتتاحي | مدة أول Sprint |
| --- | ---: | ---: |
| Revenue Operating System | يبدأ من **4,500 SAR** | 7–10 أيام |
| Executive Command OS | يبدأ من **5,500 SAR** | 7–14 يوم |
| Follow-up Recovery OS | يبدأ من **3,500 SAR** | 7 أيام |
| WhatsApp Client OS | يبدأ من **4,500 SAR** | 7–10 أيام |
| Proposal & Proof OS | يبدأ من **3,000 SAR** | 5–7 أيام |

صيغة السعر داخل الصفحة:

```txt
يبدأ من 3,500 ريال
Sprint أولي لمدة 7 أيام
يشمل التشخيص + أول workflow + تقرير تنفيذي
```

وتحتها مباشرة:

```txt
السعر النهائي يعتمد على حجم البيانات، عدد القنوات، التكاملات، وعدد workflows المطلوبة.
```

تفاصيل التسعير الكاملة في: [`SYSTEM_PRICING_STARTER_AR.md`](./SYSTEM_PRICING_STARTER_AR.md).

---

## 3. بنية صفحات الفرونت

> ملاحظة معمارية: واجهة Dealix الحالية هي تطبيق **Vite + React (SPA)** عربي RTL،
> وليست Next.js متعدد اللغات. لذلك نُفّذت المسارات بدون بادئة `/[locale]`، والموقع
> عربي افتراضيًا. الخريطة المنطقية المطلوبة تبقى كما هي:

| المسار المنطقي | التنفيذ الفعلي (SPA) |
| --- | --- |
| `/[locale]/systems` | `/systems` → `src/pages/Systems.tsx` |
| `/[locale]/systems/revenue-operating-system` | `/systems/revenue-operating-system` |
| `/[locale]/systems/executive-command-os` | `/systems/executive-command-os` |
| `/[locale]/systems/follow-up-recovery-os` | `/systems/follow-up-recovery-os` |
| `/[locale]/systems/whatsapp-client-os` | `/systems/whatsapp-client-os` |
| `/[locale]/systems/proposal-proof-os` | `/systems/proposal-proof-os` |
| `/[locale]/pricing` | `/pricing` → `src/pages/Pricing.tsx` |

صفحات النظام تُبنى بمكونات قابلة لإعادة الاستخدام في `src/components/systems/`:
`SystemHero`, `SystemBenefits`, `SystemDeliveryPack`, `SystemPricing`, `SystemFAQ`,
`SystemCard` — وكلها مدفوعة ببيانات `src/data/systems.ts`.

### كل صفحة نظام تحتوي على

- Hero (اسم + tagline + سعر افتتاحي + مدة Sprint)
- Pain statement (الألم الذي يحله)
- Benefits (ماذا تستفيد الشركة؟)
- Who it is for (لمن هذا النظام؟)
- ماذا تحصل عليه خلال أول Sprint
- Delivery Pack
- Starting price + ملاحظة التسعير
- CTA
- FAQ
- **بدون أي وعود نتائج مضمونة، وبدون أسماء وحدات داخلية في النص الموجّه للعميل**

---

## 4. الرسالة للعميل

```txt
اختر النظام المناسب لمشكلتك الآن، أو ابدأ بتشخيص سريع ونقترح لك الأفضل.
```

داخليًا يشتغل Dealix كمنظومة كاملة: يستهدف، يحلل، يكتب، يجهّز، يراجع، ويسلّم — مع
حوكمة واضحة (AI drafts → Human approves → System logs).

---

## 5. مستندات مرتبطة

- التسعير الافتتاحي: [`SYSTEM_PRICING_STARTER_AR.md`](./SYSTEM_PRICING_STARTER_AR.md)
- حزم التسليم: [`SYSTEM_DELIVERY_PACKS_AR.md`](./SYSTEM_DELIVERY_PACKS_AR.md)
- مصنع الـ 400 مسودة: [`../outreach/DAILY_400_SYSTEM_DRAFT_FACTORY_AR.md`](../outreach/DAILY_400_SYSTEM_DRAFT_FACTORY_AR.md)
- بطاقة احتياج العميل: [`../outreach/SYSTEM_BASED_CLIENT_NEED_CARD_AR.md`](../outreach/SYSTEM_BASED_CLIENT_NEED_CARD_AR.md)
- مكتبة الإيميلات: [`../outreach/FOCUS_5_COLD_EMAIL_LIBRARY_AR.md`](../outreach/FOCUS_5_COLD_EMAIL_LIBRARY_AR.md)
- خطة الإطلاق: [`../gtm/FOCUS_5_SAUDI_LAUNCH_PLAN_AR.md`](../gtm/FOCUS_5_SAUDI_LAUNCH_PLAN_AR.md)
