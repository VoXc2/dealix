# Mission → Pillar Map — خريطة ربط المهام بالأعمدة الأربعة

> الغرض: إثبات أن طبقة **Operating Missions** ليست تصنيفاً موازياً، بل تعيد استخدام **الأعمدة الأربعة** والقدرات الموجودة فعلاً في الريبو. كل عمود مربوط بملفات حقيقية في `company_os/` و`src/`.

---

## 1. الأعمدة الأربعة ← مصدرها في الريبو

| العمود (خارجي)     | ماذا يعني للعميل                | يُبنى من القدرات الموجودة فعلاً في الريبو                                                                                                                | الاسم الحالي في الموقع `src/pages/LandingPage.tsx` |
| ------------------ | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Dealix Radar**   | يرى أين المشكلة وماذا يفعل      | Revenue Leakage Map · Lead Response Audit · Follow-up Gap Report (`delivery/p1_delivery_sop.md`) · War Room (`war_room/REVENUE_WAR_ROOM_TODAY.md`, `war_room/SCORECARD_REPORT.md`) | بطاقة "كشف تسرب الإيرادات" + "Executive War Room"   |
| **Dealix AI Team** | فريق AI يجهّز العمل اليومي      | outreach drafts (`revenue/outreach_queue.json`) · follow-ups (`revenue/followups.json`) · objections (`revenue/objections.json`) · proposals (`revenue/proposals.json`) · prospect_research agent (`governance/agent_permissions.md`) | بطاقة "تدقيق المتابعات" + "تحسين مستمر"             |
| **Dealix Portal**  | واجهة العميل والتسليم           | intake/onboarding (`delivery/p1_intake_template.md`) · delivery SOP (`delivery/p1_delivery_sop.md`) · client success (`delivery/client_success_plan.md`) · approval queue (`governance/approval_queue.json`) · لوحات `src/pages/Dashboard.tsx` | روابط "لوحة التحكم / العملاء / الحوكمة / المالية"   |
| **Dealix Proof**   | دليل ونتائج وشفافية             | Proof Pack (`delivery/proof_pack_template.md`) · CEO Brief (`war_room/WEEKLY_CEO_BRIEF.md`) · case studies (template في `company_os/company_os/marketing/case_studies/`) · audit ledger (`governance/ai_action_ledger.jsonl`) | بطاقة "Proof Pack شهري"                             |

> **عمود الحوكمة (Governance Spine)** يخترق الأربعة جميعاً: مستويات الصلاحية الخمسة + الخطوط الحمراء في `governance/agent_permissions.md`، وقائمة PDPL في `governance/pdpl_checklist.md`.

---

## 2. المصفوفة: Mission × Pillar

`●` = عمود قائد · `○` = عمود داعم

| Mission                       | Radar | AI Team | Portal | Proof | التغليف التجاري       |
| ----------------------------- | :---: | :-----: | :----: | :---: | --------------------- |
| M1 Revenue Leakage            |   ●   |    ○    |        |   ○   | P1 Sprint             |
| M2 Follow-up Recovery         |   ○   |    ●    |        |   ○   | P1 → P2               |
| M3 Sales Draft Factory        |       |    ●    |   ○    |   ○   | P2 Retainer           |
| M4 WhatsApp Client OS         |       |    ●    |   ●    |   ○   | P1 → P2               |
| M5 Proposal & Proof           |       |    ●    |        |   ●   | P1 → P2               |
| M6 Customer Success           |   ○   |    ○    |   ●    |   ●   | P2 Retainer           |
| M7 GTM Expansion              |   ●   |    ●    |        |   ○   | P2 Retainer           |
| M8 Full Revenue OS            |   ●   |    ●    |   ●    |   ●   | P2 Enterprise         |

**ملاحظة قراءة:** لا توجد Mission "بلا عمود". كل مهمة تُسلَّم عبر واحد أو أكثر من الأعمدة الأربعة فقط — لا أسماء داخلية تظهر للعميل.

---

## 3. Mission × المخرجات الفعلية في الريبو

| Mission                | يستهلك / ينتج هذه الملفات الحقيقية                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| M1 Revenue Leakage     | `delivery/p1_delivery_sop.md` (Day 1) · `delivery/proof_pack_template.md` §2 · `war_room/SCORECARD_REPORT.md` |
| M2 Follow-up Recovery  | `delivery/p1_delivery_sop.md` (Day 2) · `revenue/followups.json` · `proof_pack_template.md` §4    |
| M3 Sales Draft Factory | `revenue/outreach_queue.json` · `reports/outreach/DAILY_400_DRAFT_PRODUCTION.md`                  |
| M4 WhatsApp Client OS  | `revenue/followups.json` (قناة) · `governance/data_handling_checklist.md`                         |
| M5 Proposal & Proof    | `revenue/proposals.json` · `revenue/objections.json` · `proof_pack_template.md` §5                |
| M6 Customer Success    | `delivery/client_success_plan.md` · `war_room/WEEKLY_CEO_BRIEF.md`                                |
| M7 GTM Expansion       | `reports/outreach/GCC_TARGETING_REVIEW.md` · `revenue/prospects.csv`                              |
| M8 Full Revenue OS     | كل ما سبق + `finance/unit_economics.md` (Enterprise tier)                                         |

---

## 4. ربط الأعمدة بالأسعار الحالية (`finance/unit_economics.md`)

| العمود/المهمة الداخلة             | المنتج             | السعر المرجعي         |
| --------------------------------- | ------------------ | --------------------- |
| Radar (تشخيص) — M1/M5             | P1 Sprint          | 2,500–7,500 ر.س (5 أيام) |
| AI Team + Portal (تشغيل) — M2/M3/M4 | P2 Small/Medium    | 3,000–8,000 ر.س/شهر    |
| الأعمدة الأربعة — M6/M7/M8        | P2 Enterprise      | 20,000 ر.س/شهر         |

> **قاعدة هامش الربح** (من `unit_economics.md`): يجب بقاء gross margin فوق 60%؛ المهام لا تكسر هذه القاعدة لأنها تعيد استخدام نفس خطوط التسليم الحالية.

---

## 5. خلاصة الربط

```txt
1 براند → 4 أعمدة → 8 missions → services داخلية
كل طبقة تستند إلى ملفات موجودة فعلاً في company_os/ و src/.
لا تصنيف موازٍ. لا أسماء داخلية للعميل. لا كسر لهامش الربح أو الحوكمة.
```

*راجع أيضاً: `DEALIX_OPERATING_MISSIONS_AR.md` و `MISSION_PACKAGING_MAP_AR.md`.*
