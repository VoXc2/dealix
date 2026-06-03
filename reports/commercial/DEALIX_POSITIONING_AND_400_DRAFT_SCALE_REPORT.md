# Dealix Positioning & 400-Draft Scale Report

*Date: 2026-06-03 · Author: Positioning, Mission Packaging & GCC Draft Scale audit · Status: Draft for founder approval*

---

## 0. Executive summary

```txt
أقوى تموضع لـ Dealix ليس "منتج واحد" ولا "وكالة خدمات كثيرة"، بل:
مظلّة تشغيل واحدة (Dealix) → 4 أعمدة → 8 Operating Missions → services.
نبيع مهمة واحدة تعطي أسرع دليل قيمة، ثم نوسّعها إلى نظام تشغيل إيرادات.
السعودية أولاً، الخليج جاهز ثانياً.
400 drafts/day ✅ — 400 sends/day ❌ افتراضياً (يتطلب جاهزية تسليم وموافقة).
```

---

## 1. Current repo alignment (الواقع، بصراحة)

> **تنبيه مهم:** البرومبت الأصلي (Agent #4) كُتب لحالة ريبو مختلفة (`Dealix-sa/dealix`) وأشار إلى ملفات **غير موجودة** في هذا الريبو (`voxc2/dealix`).

| الملف المُشار إليه في البرومبت                          | الحالة الفعلية |
| ------------------------------------------------------- | -------------- |
| `docs/DEALIX_PRODUCT_SIMPLIFICATION_MAP.md`             | ❌ غير موجود   |
| `docs/strategic/CATEGORY_DESIGN_AND_MASTER_OPERATING_SYSTEM_AR.md` | ❌ غير موجود |
| `docs/commercial/` `docs/gtm/` `docs/outreach/` `docs/sectors/` `docs/whatsapp/` | ❌ غير موجودة (أُنشئت الآن) |
| `AGENTS.md`                                             | ❌ غير موجود   |

**أين توجد الاستراتيجية فعلاً في هذا الريبو؟**

| القدرة            | الملف الفعلي                                                |
| ----------------- | ---------------------------------------------------------- |
| التموضع/العرض      | `company_os/marketing/one_pagers/one_pager_arabic.md` · `company_os/marketing/pitch_deck/outline.md` |
| المنتجات/التسليم   | `company_os/delivery/p1_delivery_sop.md` · `proof_pack_template.md` · `client_success_plan.md` |
| الإيراد/الـ outreach | `company_os/revenue/{prospects.csv, outreach_queue.json, followups.json, proposals.json, objections.json}` |
| الحوكمة            | `company_os/governance/{agent_permissions.md, pdpl_checklist.md, data_handling_checklist.md}` |
| الواجهة (العميل)   | `src/pages/LandingPage.tsx` · `src/pages/Dashboard.tsx`     |
| الاقتصاد           | `company_os/finance/unit_economics.md`                      |

**القرار المنهجي:** بما أن "Product Simplification Map" **غير موجود**، لم نخترع تصنيفاً موازياً عشوائياً؛ بل بنينا التموضع على القدرات الموجودة فعلاً وربطنا كل طبقة جديدة بملفاتها الحقيقية (`MISSION_TO_PILLAR_MAP_AR.md`).

---

## 2. Recommended customer-facing architecture

```txt
البراند:  Dealix — نظام تشغيل الإيرادات للشركات السعودية (Saudi-first) · GCC-ready

الأعمدة الأربعة (يراها العميل):
   Dealix Radar · Dealix AI Team · Dealix Portal · Dealix Proof

الطبقة الجديدة: Dealix Operating Missions (8 مهام) تحت الأعمدة.

عمود الحوكمة: Observe→Advise→Draft→Act-with-Approval (Autonomous ممنوع) · PDPL/SDAIA · ai_action_ledger.
```

- الأعمدة الأربعة **متوافقة** مع بطاقات الموقع الحالي (`LandingPage.tsx`): "كشف تسرب الإيرادات/War Room" ≈ Radar، "تدقيق المتابعات/تحسين مستمر" ≈ AI Team، "لوحة التحكم" ≈ Portal، "Proof Pack" ≈ Proof.
- **لكنها غير مُفعّلة بالاسم في `src/` بعد** — هذا قرار براند مؤسس (راجع §6).

---

## 3. Mission packaging

8 مهام، كل منها مخرج واضح + عمود قائد + منتج دخول (تفصيل في `docs/commercial/DEALIX_OPERATING_MISSIONS_AR.md`):

| Mission | Entry product | عمود قائد |
| ------- | ------------- | --------- |
| M1 Revenue Leakage     | P1 Sprint     | Radar |
| M2 Follow-up Recovery  | P1 → P2       | AI Team |
| M3 Sales Draft Factory | P2            | AI Team |
| M4 WhatsApp Client OS  | P1 → P2       | AI Team/Portal |
| M5 Proposal & Proof    | P1 → P2       | AI Team/Proof |
| M6 Customer Success    | P2            | Portal/Proof |
| M7 GTM Expansion       | P2            | Radar/AI Team |
| M8 Full Revenue OS     | P2 Enterprise | الأربعة |

- التغليف عبر منتجي الريبو الحاليين (P1 2,500–7,500 ر.س / P2 3,000–20,000 ر.س/شهر) — لا أسعار جديدة مخترعة، فقط anchors (`unit_economics.md`).
- مهمة الدخول الموصى بها للسوق الحالي: **M2 Follow-up Recovery** (6/15 من الـ prospects الحاليين — `CLIENT_NEED_CARDS.md`).

---

## 4. 400-draft production plan

```txt
التوزيع: 150 first-touch · 100 follow-up1 · 75 follow-up2 · 35 proposal/proof · 20 close-loop · 20 partner/press = 400
الفصل:   400 drafts/day ✅  ≠  400 sends/day ❌ (افتراضياً)
الترتيب: Top-100 آلياً → موافقة مؤسس على 20–80 → إرسال بشري ضمن الـ ramp
```

| المرحلة       | Drafts/day | Sends/day |
| ------------- | ---------: | --------: |
| Day 1–7       |        400 |     20–40 |
| Week 2        |        400 |    50–100 |
| Week 3        |        400 |   100–200 |
| Week 4        |        400 |   200–300 |
| بعد الاستقرار |    400–800 |   300–400 |

شرط الرفع: SPF/DKIM/DMARC · one-click unsubscribe · suppression list · bounce handling · spam rate < 0.3% · domain health (Postmaster). تفصيل في `docs/outreach/DAILY_400_DRAFT_FACTORY_AR.md` و`GCC_OUTREACH_POLICY_AR.md`.

> **التوصية الصريحة:** لا تبدأ بـ 400 sends/day. الإرسال المتدرّج المراقَب يحمي الدومين والـ deliverability.

---

## 5. Saudi-first / GCC-ready expansion

```txt
Phase 1 KSA:  Riyadh · Jeddah · Eastern Province        ← الآن
Phase 2 UAE:  Dubai · Abu Dhabi · Sharjah               ← بعد أول Proof Pack
Phase 3:      Qatar · Kuwait
Phase 4:      Bahrain · Oman
```

- لا تبديل هوية: "Saudi-first, GCC-ready". (الموقع يقول بالفعل "للسعودية والخليج".)
- استهداف بمنطق **Sector × City × Signal × Mission × Channel** (`GCC_TARGETING_REVIEW.md`).
- email-first؛ لا cold WhatsApp/LinkedIn automation؛ امتثال لكل دولة قرار مؤسس.

---

## 6. Required founder decisions

| # | القرار                                                              | التوصية                          |
| - | ------------------------------------------------------------------- | -------------------------------- |
| 1 | اعتماد الأعمدة الأربعة كأسماء خارجية رسمية                          | ✅ اعتماد (يطابق الموقع الحالي)   |
| 2 | تفعيل الأعمدة + Missions في `src/pages/LandingPage.tsx`             | مرحلة لاحقة بعد الاعتماد (قرار براند مواجه للعميل) |
| 3 | مهمة الدخول الأساسية للسوق السعودي                                  | M2 Follow-up Recovery            |
| 4 | تثبيت anchors التسعير لكل Mission                                   | كما في `MISSION_PACKAGING_MAP_AR.md` |
| 5 | بدء الإرسال (الكمية والدومين)                                       | Day1–7: 20–40 send بعد فحص الجاهزية |
| 6 | موعد فتح Phase 2 (UAE)                                              | بعد أول Proof Pack من KSA        |
| 7 | إثراء `prospects.csv` بحقل المدينة (حالياً `City: confirm`)         | نعم                              |

---

## 7. Risks

| المخاطرة                                   | التخفيف                                              |
| ------------------------------------------ | --------------------------------------------------- |
| حرق الدومين عند الإرسال الكبير المبكر       | ramp متدرّج + الفصل draft/send + Postmaster monitoring |
| ظهور البراند مشتّتاً ("كل الخدمات")         | البيع كـ Mission واحدة تحت 4 أعمدة                   |
| تصنيف موازٍ يفصل الوثائق عن الكود           | ربط كل طبقة بملفات `company_os/` و`src/`             |
| كسر الحوكمة (إرسال آلي/PII/تسعير)           | احترام الخطوط الحمراء في `agent_permissions.md`      |
| توسّع GCC قبل الدليل                        | بوابة Proof Pack بين المراحل                         |
| ادعاءات نتائج مضمونة                        | سياسة No guaranteed claims في القوالب وبوابات الجودة |

---

## 8. Files created / modified

**Docs (created):**
- `docs/commercial/DEALIX_OPERATING_MISSIONS_AR.md`
- `docs/commercial/MISSION_PACKAGING_MAP_AR.md`
- `docs/commercial/MISSION_TO_PILLAR_MAP_AR.md`
- `docs/commercial/GCC_EXPANSION_STRATEGY_AR.md`
- `docs/outreach/DAILY_400_DRAFT_FACTORY_AR.md`
- `docs/outreach/CLIENT_NEED_CARD_SYSTEM_AR.md`
- `docs/outreach/GCC_OUTREACH_POLICY_AR.md`

**Reports (created):**
- `reports/commercial/MISSION_PACKAGING_REVIEW.md`
- `reports/commercial/DEALIX_POSITIONING_AND_400_DRAFT_SCALE_REPORT.md` (هذا الملف)
- `reports/outreach/DAILY_400_DRAFT_PRODUCTION.md`
- `reports/outreach/CLIENT_NEED_CARDS.md`
- `reports/outreach/GCC_TARGETING_REVIEW.md`

**Code modified:** لا شيء. لم نغيّر `src/` ولا `company_os/` — تغيير الواجهة المواجهة للعميل قرار براند مؤسس (§6 #2). وثائق فقط في هذه الدُفعة.

---

## 9. Tests / checks run

| Check | النتيجة |
| ----- | ------- |
| البحث عن الملفات المُشار إليها في البرومبت | ❌ غير موجودة — موثّق في §1 |
| تحديد مصدر الاستراتيجية الفعلي (`company_os/`, `src/`) | ✅ |
| ربط كل عمود/مهمة بملف حقيقي في الريبو | ✅ `MISSION_TO_PILLAR_MAP_AR.md` |
| تطابق التوزيع 150+100+75+35+20+20 = 400 | ✅ |
| تطابق الأسعار مع `unit_economics.md` | ✅ anchors فقط |
| تطابق إيقاع المتابعة 3/7/14 مع `followups.json` | ✅ |
| احترام الخطوط الحمراء في `agent_permissions.md` | ✅ (لا send آلي، لا PII، لا تسعير AI) |
| Need Cards مبنية على `prospects.csv` الفعلي (15) | ✅ |
| `npm run lint` (لم نلمس الكود) | ⏳ غير مطلوب — لا تغييرات كود |

---

## 10. الخلاصة التنفيذية (10 قواعد)

```txt
1. Dealix اسم واحد.
2. العميل يرى 4 أعمدة: Radar, AI Team, Portal, Proof.
3. الخدمات تُباع كـ Operating Missions.
4. كل prospect له Client Need Card.
5. 400 drafts/day هدف ممتاز.
6. 400 sends/day لا يبدأ إلا بعد الجاهزية.
7. السعودية أولاً، الخليج جاهز ثانياً.
8. لا تبع "كل شيء" — بِع أول Mission مناسبة.
9. كل Mission تقود إلى Mission أكبر.
10. كل شيء ينتهي بـ Proof و Renewal.
```

*كل قرارات الإرسال/التسعير/التحقق القانوني تبقى بشرية (founder-approved).*
