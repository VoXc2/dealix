# مكتبة أزرار الحثّ على اتخاذ إجراء — Offer CTA Library
<!-- Agent #33 — Owner: Marketing | Date: 2026-06-03 -->
<!-- Arabic primary — العربية أولاً | Shared CTA library for all 6 offer pages -->

> **الغرض:** مكتبة أزرار CTA (Call-to-Action) موحّدة لـ 6 صفحات عروض + قنوات التحويل الخارجية. كل CTA يُستخدم في السياق المناسب، بنفس النبرة، بنفس التصميم.

> **القاعدة:** الأزرار تتبع التسلسل: Primary (نيّة عالية) → Secondary (نيّة متوسطة) → Soft (نيّة منخفضة). WhatsApp يأتي بعد موافقة صريحة فقط.

---

## 1. CTAs رئيسية (Primary — أعلى نيّة)

> تُستخدم في الـ Hero وفي آخر الصفحة. زر أخضر داكن `#0A4D3F`، نص أبيض، حجم 16–18px.

| # | النص (AR) | الترجمة (EN hint) | متى يُستخدم | الـ Link template |
|---|-----------|-------------------|-------------|-------------------|
| P1 | **احجز تشخيص تسرب الإيرادات** | Book Revenue Leakage Diagnostic | تشخيص تسرب الإيرادات | `/ar/diagnostic?source=offer-rev-leak` |
| P2 | **ابدأ سباق استرجاع المتابعة** | Start Followup Recovery Workflow | سباق المتابعة | `/ar/pilot/followup?source=offer-followup` |
| P3 | **شغّل بداية عمليات الإيرادات بالذكاء الاصطناعي** | Start AI Revenue Ops Starter | بداية AI Ops | `/ar/pilot/ai-ops-starter?source=offer-ai-ops` |
| P4 | **فعّل نظام الإيرادات الكامل** | Activate Full Revenue OS | النظام الكامل | `/ar/contact/enterprise?source=offer-full-os` |
| P5 | **ابدأ خطة التحسين الشهري** | Start Monthly Optimization Plan | التحسين الشهري | `/ar/contact/renewal?source=offer-monthly` |
| P6 | **اطلب نظام الشركة المخصّص** | Request Custom Company OS | نظام مخصّص | `/ar/contact/enterprise?source=offer-custom` |

---

## 2. CTAs ثانوية (Secondary — نيّة متوسطة)

> تُستخدم تحت الـ primary أو في وسط الصفحة. شفّاف، حدود خضراء داكنة.

| # | النص (AR) | EN hint | متى يُستخدم |
|---|-----------|---------|-------------|
| S1 | **تعرّف على نظام Dealix** | See the Dealix System | Hero — بديل عن التشخيص |
| S2 | **احجز اجتماع اكتشاف (30 دقيقة)** | Book 30-min Discovery Call | التشخيص + السباق |
| S3 | **اطلب مقترحاً مكتوباً** | Request a Written Proposal | العروض الشهرية / المؤسسية |
| S4 | **شاهد كيف نعمل (عرض توضيحي)** | Watch a Walkthrough | كل العروض |
| S5 | **قارن العروض جنباً إلى جنب** | Compare Offers Side-by-Side | لقرّاء المقارنة |
| S6 | **تحدّث مع المؤسّس مباشرة** | Talk to the Founder | العروض المؤسسية |

---

## 3. CTAs خفيفة (Soft — نيّة منخفضة)

> للمتعلّمين، في المقالات، في الـ footer. لون رمادي دافئ `#6B6B6B`.

| # | النص (AR) | EN hint | متى يُستخدم |
|---|-----------|---------|-------------|
| SO1 | **اقرأ دليل التشخيص** | Read the Diagnostic Guide | صفحات المحتوى |
| SO2 | **نزّل دليل نظام الإيرادات** | Download the Revenue OS Guide | Lead magnet |
| SO3 | **اشترك في الموجز الأسبوعي** | Subscribe to the Weekly Brief | Newsletter |
| SO4 | **تابعنا على LinkedIn** | Follow us on LinkedIn | Social |
| SO5 | **اقرأ الأسئلة الشائعة** | Read the FAQ | تعلّم |
| SO6 | **تصفّح دراسات الحالة (قريباً)** | Browse Case Studies (coming soon) | Proof |

---

## 4. WhatsApp CTAs (بعد موافقة صريحة)

> **القاعدة:** لا cold WhatsApp. كل CTA يسبقه reminder للموافقة. الزرين يستخدمان نفس رقم الواتساب (المؤسّس) ولكن بـ template مختلف.

### 4.1 W1 — التشخيص
> **النص الكامل على الصفحة (مع reminder):**
> "بموافقتك، أرسل لنا رسالة واتساب على +9665XXXXXXX لتأكيد التشخيص المجاني. (نحترم خصوصيتك: لاcold، لا قوائم، لا بيع بيانات.)"
> **الـ button:** "أرسل رسالة واتساب (بعد موافقتك)"
> **الـ deep link:** `https://wa.me/9665XXXXXXX?text=أرغب%20في%20حجز%20تشخيص%20تسرب%20الإيرادات`

### 4.2 W2 — السباق / البداية
> **النص:** "بموافقتك، راسلنا واتساب لبدء السباق. (بموافقتك فقط — نلتزم بـ[WHATSAPP_OPERATOR_FLOW.md](../WHATSAPP_OPERATOR_FLOW.md).)"
> **الـ button:** "راسلنا واتساب لبدء السباق"
> **الـ deep link:** `https://wa.me/9665XXXXXXX?text=أرغب%20في%20بدء%20سباق%20استرجاع%20المتابعة`

### 4.3 W3 — الدعم التشغيلي (للعملاء الحاليين)
> **النص:** "أنت عميل حالي؟ راسلنا واتساب لطلب دعم تشغيلي."
> **الـ button:** "دعم تشغيلي (عملاء حاليين)"
> **الـ deep link:** `https://wa.me/9665XXXXXXX?text=عميل%20حالي%20—%20أحتاج%20دعماً%20تشغيلياً`

### 4.4 W4 — رابط التدفّق التشغيلي
> كل CTA واتساب يربط بـ `docs/WHATSAPP_OPERATOR_FLOW.md` (لا نُكرّر البايز في المكتبة، فقط نُشير).

---

## 5. Booking CTAs (حجز اجتماع)

> تُستخدم عبر Calendly (يفضّل) أو نموذج ويب. **بدون إرسال رسائل cold قبل الاجتماع.**

| # | النص (AR) | EN hint | الـ Link template |
|---|-----------|---------|-------------------|
| B1 | **احجز اجتماع اكتشاف 30 دقيقة** | Book 30-min Discovery | `/ar/booking/discovery?source={offer}` |
| B2 | **احجز مراجعة عرض (45 دقيقة)** | Book 45-min Offer Review | `/ar/booking/offer-review?source={offer}` |
| B3 | **احجز kickoff لمشروع (60 دقيقة)** | Book 60-min Project Kickoff | `/ar/booking/kickoff?source={offer}` |
| B4 | **احجز مراجعة تجديد (ربع سنوية)** | Book Quarterly Renewal Review | `/ar/booking/renewal?source={offer}` (للعملاء فقط) |

---

## 6. Proposal Request CTAs (طلب مقترح مكتوب)

| # | النص (AR) | EN hint | الـ Link template |
|---|-----------|---------|-------------------|
| PR1 | **اطلب مقترحاً مكتوباً خلال 48 ساعة** | Request a Written Proposal in 48h | `/ar/proposal/request?source={offer}` |
| PR2 | **اطلب SOW مخصّصاً (3–5 أيام)** | Request Custom SOW (3–5 days) | `/ar/proposal/sow?source={offer}` |
| PR3 | **احصل على تقدير نطاق سريع (بدون التزام)** | Get a Quick Range Estimate | `/ar/proposal/range?source={offer}` |

---

## 7. Pilot CTAs (للعروض التجريبية المدفوعة)

> Pilot = عروض قصيرة (5–14 يوم) بأسعار ثابتة (499 SAR) أو نطاق مخصّص. **مغلق لـ 5 عملاء** — انظر `docs/PRICING_AND_PACKAGING_V6.md`.

| # | النص (AR) | EN hint | الـ Link template |
|---|-----------|---------|-------------------|
| PI1 | **جرّب Pilot 7 أيام بـ 499 ر.س** | Try 7-day Pilot for 499 SAR | `/ar/pilot/499?source={offer}` |
| PI2 | **ابدأ Pilot مخصّصاً (نطاق مؤسسي)** | Start Custom Pilot (Enterprise Band) | `/ar/pilot/custom?source={offer}` |
| PI3 | **احجز عرضاً توضيحياً مباشراً** | Book Live Demo | `/ar/booking/demo?source={offer}` |

---

## 8. Enterprise CTAs (المؤسسات)

| # | النص (AR) | EN hint | الـ Link template |
|---|-----------|---------|-------------------|
| E1 | **تواصل مع مبيعات المؤسسات** | Contact Enterprise Sales | `/ar/contact/enterprise?source={offer}` |
| E2 | **اطلب وثائق المناقصة (RFP)** | Request RFP Documentation | `/ar/contact/rfp?source={offer}` |
| E3 | **ناقش MSA و DPA مخصّصاً** | Discuss Custom MSA and DPA | `/ar/contact/legal?source={offer}` |
| E4 | **ابدأ تقييم أمني (security review)** | Start Security Review | `/ar/contact/security?source={offer}` |

---

## 9. Renewal CTAs (للعملاء الحاليين)

> هذه الأزرار تختفي عن الزوّار الجدد وتظهر فقط عند تسجيل الدخول.

| # | النص (AR) | EN hint | الـ Link template |
|---|-----------|---------|-------------------|
| R1 | **احجز مراجعة تجديد ربع سنوية** | Book Quarterly Renewal Review | `/ar/account/renewal/book` |
| R2 | **ناقش توسيع النطاق** | Discuss Scope Expansion | `/ar/account/expand` |
| R3 | **اطلب ترقية إلى طبقة أعلى** | Request Tier Upgrade | `/ar/account/upgrade` |
| R4 | **قدّم ملاحظات للتجديد القادم** | Submit Renewal Feedback | `/ar/account/feedback` |

---

## 10. Anti-Pattern (ممنوعات)

> هذه العبارات **ممنوعة** في CTAs لأنها تنتهك قواعد Dealix:

| ❌ ممنوع | البديل الصحيح |
|---------|---------------|
| "احصل على ROI مضمون" | "احجز تشخيص وابدأ بقياس" |
| "100% نجاح" | "نقيس ونُوثّق" |
| "ابدأ مجاناً للأبد" | "ابدأ بتشخيص مجاني" (لا وعود أبدية) |
| "AI سيحلّ مشكلتك" | "نساعدك على حلّ المشكلة" |
| "تواصل معنا الآن" (بدون موافقة) | "بموافقتك، تواصل معنا" |

---

## 11. Placement Matrix (أين يظهر كل CTA)

| CTA Type | Hero | Mid-page | Sticky | Footer | After Pricing | After FAQ |
|----------|------|----------|--------|--------|---------------|-----------|
| Primary | ✅ | — | ✅ | — | ✅ | ✅ |
| Secondary | ✅ | ✅ | — | — | — | ✅ |
| Soft | — | ✅ | — | ✅ | — | ✅ |
| WhatsApp | — | ✅ (after consent) | — | ✅ | ✅ | ✅ |
| Booking | — | ✅ | — | — | ✅ | ✅ |
| Proposal | — | — | — | — | ✅ | — |
| Pilot | ✅ (لـ Pilot) | — | ✅ | — | — | — |
| Enterprise | — | ✅ (enterprise offer) | — | ✅ | ✅ | — |
| Renewal | — | — | — | — | — | — (auth) |

---

## 12. A/B Test Ideas (مفتوحة للمراجعة)

| الفرضية | الـ Variant A | الـ Variant B | المقياس |
|---------|---------------|---------------|---------|
| Primary أوضح | "احجز تشخيص" | "احجز تشخيص تسرب الإيرادات" | click-through |
| WhatsApp vs Booking | "راسلنا واتساب" | "احجز اجتماع 30 دقيقة" | conversion rate |
| Tone of Soft | "اقرأ الدليل" | "اقرأ قبل أن تتّخذ قرارك" | dwell time |

> **ما لم نقِسه بعد** (proof pending): لا A/B testing فعلي بعد. كل الفرضيات `assumed` (L0).

---

## 13. سجل الإصدارات

| Version | Date | التغيير | من |
|---------|------|---------|-----|
| 1.0 | 2026-06-03 | إنشاء مكتبة CTA الأولى (30+ CTA) | Agent #33 |

---

*Version 1.0 · 2026-06-03 · Agent #33 · Dealix Offer CTA Library*
