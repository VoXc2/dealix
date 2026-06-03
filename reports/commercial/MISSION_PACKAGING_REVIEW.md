# Mission Packaging Review

*Date: 2026-06-03 · Owner: Founder · Status: Draft for approval*

---

## 1. Purpose

مراجعة جاهزية تغليف **Dealix Operating Missions** ومدى توافقها مع الريبو الحالي، قبل تفعيلها في الواجهة المواجهة للعميل (`src/`).

---

## 2. Architecture confirmed

| السؤال                                                | الإجابة                                                                 |
| ----------------------------------------------------- | ---------------------------------------------------------------------- |
| هل يبقى Dealix برانداً واحداً؟                          | ✅ نعم                                                                  |
| هل يبقى 4 أعمدة مواجهة للعميل؟                          | ✅ نعم — Radar, AI Team, Portal, Proof (أسماء مُقترحة، غير مفعّلة في `src` بعد) |
| هل تُضاف طبقة Operating Missions تحت الأعمدة؟           | ✅ نعم — 8 مهام                                                          |
| هل تظهر الأسماء الداخلية للعميل؟                        | ❌ لا — تُربط دائماً تحت أحد الأعمدة الأربعة                              |

---

## 3. Repo alignment

| العنصر                | الحالة في الريبو                                                                 |
| --------------------- | ------------------------------------------------------------------------------- |
| 4 pillar names        | ⚠️ **غير موجودة بالاسم** في `src/` أو `company_os/` — مُقترحة في هذه الدُفعة     |
| Underlying capabilities | ✅ موجودة كلها (Radar←leakage/war room، AI Team←outreach/followups، Portal←delivery، Proof←proof pack) |
| Products P1/P2        | ✅ موجودة (`one_pager_arabic.md`، `unit_economics.md`، `LandingPage.tsx`)        |
| Governance red-lines  | ✅ موجودة (`agent_permissions.md`) — المهام لا تكسرها                             |
| Referenced prompt files (`DEALIX_PRODUCT_SIMPLIFICATION_MAP.md`, `CATEGORY_DESIGN_*`, `AGENTS.md`, `docs/sectors|gtm|whatsapp/`) | ❌ **غير موجودة** في هذا الريبو — كانت تخص حالة ريبو مختلفة |

---

## 4. The 8 Missions — packaging status

| Mission                | منتج الدخول   | عمود قائد | جاهزية التسليم (SOP موجود؟)          |
| ---------------------- | ------------- | --------- | ----------------------------------- |
| M1 Revenue Leakage     | P1 Sprint     | Radar     | ✅ `p1_delivery_sop.md` Day 1        |
| M2 Follow-up Recovery  | P1 → P2       | AI Team   | ✅ Day 2 + `followups.json`          |
| M3 Sales Draft Factory | P2            | AI Team   | ⚠️ يحتاج تشغيل المصنع (drafts فقط)   |
| M4 WhatsApp Client OS  | P1 → P2       | AI Team/Portal | ⚠️ تشخيص جاهز، تشغيل يحتاج SOP خاص |
| M5 Proposal & Proof    | P1 → P2       | AI Team/Proof | ✅ Day 3 + `proof_pack_template.md` |
| M6 Customer Success    | P2            | Portal/Proof | ✅ `client_success_plan.md`        |
| M7 GTM Expansion       | P2            | Radar/AI Team | ⚠️ يحتاج مصفوفة استهداف (تم: `GCC_TARGETING_REVIEW.md`) |
| M8 Full Revenue OS     | P2 Enterprise | الأربعة   | ⚠️ تجميع المهام أعلاه               |

---

## 5. Gaps / risks

1. **أسماء الأعمدة غير مفعّلة في الواجهة** — الموقع الحالي يستخدم بطاقات features + أسماء منتجات (Sprint/Retainer/War Room/Proof Pack). تفعيل الأعمدة الأربعة في `src/pages/LandingPage.tsx` قرار براند مؤسس.
2. **M3/M4 يحتاجان SOP تشغيلي** مماثل لـ `p1_delivery_sop.md`.
3. **التسعير anchors فقط** — التسعير النهائي قرار مؤسس (خط أحمر #3).

---

## 6. Founder decisions required

| # | القرار                                                              | التوصية                          |
| - | ------------------------------------------------------------------- | -------------------------------- |
| 1 | اعتماد أسماء الأعمدة الأربعة كأسماء خارجية رسمية                     | اعتماد (يطابق الـ Landing الحالي) |
| 2 | تفعيل الأعمدة/المهام في `src/pages/LandingPage.tsx`                  | مرحلة لاحقة بعد الاعتماد          |
| 3 | اعتماد مهمة الدخول الأساسية للسوق السعودي                            | M2 Follow-up Recovery (أسرع دليل) |
| 4 | تثبيت anchors التسعير لكل Mission                                    | كما في `MISSION_PACKAGING_MAP_AR.md` |

---

## 7. Files produced this round

- `docs/commercial/DEALIX_OPERATING_MISSIONS_AR.md`
- `docs/commercial/MISSION_PACKAGING_MAP_AR.md`
- `docs/commercial/MISSION_TO_PILLAR_MAP_AR.md`
- `docs/commercial/GCC_EXPANSION_STRATEGY_AR.md`
- `docs/outreach/DAILY_400_DRAFT_FACTORY_AR.md`
- `docs/outreach/CLIENT_NEED_CARD_SYSTEM_AR.md`
- `docs/outreach/GCC_OUTREACH_POLICY_AR.md`

---

*Next: راجع `reports/commercial/DEALIX_POSITIONING_AND_400_DRAFT_SCALE_REPORT.md` للتقرير الكامل.*
