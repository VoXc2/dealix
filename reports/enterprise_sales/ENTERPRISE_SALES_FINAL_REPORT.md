# Enterprise Sales OS — التقرير النهائي

> **Agent 29 — Dealix Enterprise Sales Motion & ABM**
> **Generated:** 2026-06-03 · v0.1 (Final Report)
> **Owner:** المؤسس · Sales Lead · CS Lead

---

## 1. ملخص تنفيذي

بُني **Enterprise Sales OS** كمجموعة متكاملة من الوثائق التشغيلية والتقنية لإدارة حركة مبيعات المؤسسات الكبيرة (B2B Enterprise) في السوق السعودي. الـ OS يمتدّ من ABM واختيار الحسابات إلى Expansion بعد التسليم، ويتكامل مع الأنظمة القائمة في Dealix (Commercial, Enterprise, Enterprise Rollout, Governance, Legal) دون تكرار.

> **Status الإجمالي:** Design Draft — جميع البنية مُنجزة. يحتاج تأكيد Founder لإكمال الأرقام النهائية (placeholders فقط للأمان).

---

## 2. ما تمّ بناؤه

### 2.1 الوثائق (`docs/enterprise_sales/`) — 11 ملف، جميعها Arabic-first

| # | الملف | الحالة | الغرض |
|---|--------|--------|-------|
| 1 | ENTERPRISE_SALES_OS_AR.md | READY (structure) | الفهرس الرئيسي والربط |
| 2 | ACCOUNT_BASED_SELLING_AR.md | PARTIAL (Tier-1 actual) | ABM + Tier-1/2/3 + Scoring |
| 3 | TARGET_ACCOUNT_PROFILE_AR.md | READY (structure) | TAP بقالب 18 حقل + worked example |
| 4 | STAKEHOLDER_MAPPING_AR.md | READY (structure) | 10 أدوار معيارية + رسائل عربية |
| 5 | BUYING_COMMITTEE_PLAYBOOK_AR.md | READY (structure) | Workshop + Power/Interest + Scripts |
| 6 | ENTERPRISE_DISCOVERY_AR.md | READY (structure) | 90-min agenda + بنك أسئلة |
| 7 | MUTUAL_ACTION_PLAN_AR.md | READY (structure) | 10 مراحل من Discovery إلى Expansion |
| 8 | EXECUTIVE_BUSINESS_CASE_AR.md | READY (structure) | 1-page template + worked example |
| 9 | PILOT_TO_EXPANSION_PLAYBOOK_AR.md | READY (structure) | 4 نماذج + سلّم توسّع + SOW template |
| 10 | PROCUREMENT_SALES_PLAYBOOK_AR.md | READY (structure) | RFP/RFI/RFQ + بنود placeholders |
| 11 | ENTERPRISE_DEAL_RISK_REVIEW_AR.md | READY (structure) | 9 فئات + Weekly Review template |

### 2.2 الـ Schemas (`schemas/`) — 4 JSON Schema (Draft 2020-12)

- `enterprise_account.schema.json` — TAP مع 18 حقل required.
- `stakeholder.schema.json` — Stakeholder مع 10 أدوار.
- `mutual_action_plan.schema.json` — MAP مع 10 مراحل.
- `enterprise_deal_risk.schema.json` — Deal Risk مع 9 فئات.

### 2.3 البيانات (`data/enterprise_sales/`) — 4 JSONL

- `accounts.jsonl` — 3 حسابات (industrial, healthcare, retail).
- `stakeholders.jsonl` — 12 stakeholder موزّعين على الحسابات.
- `mutual_action_plans.jsonl` — 2 MAPs في مراحل مختلفة.
- `deal_risks.jsonl` — 7 مخاطر موزّعة بـ severity mix.

### 2.4 التقارير (`reports/enterprise_sales/`) — 3 + 1 Final

- `ENTERPRISE_PIPELINE_REVIEW.md` — حالة الـ Pipeline لـ 3 حسابات.
- `ACCOUNT_PLAN_REVIEW.md` — مراجعة TAPs + completeness check.
- `ENTERPRISE_DEAL_RISK_REVIEW.md` — توزيع المخاطر + Top 5.
- `ENTERPRISE_SALES_FINAL_REPORT.md` — هذا الملف.

---

## 3. حالة READY / PARTIAL / NEEDS_REVIEW

### 3.1 READY (البنية الأساسية مكتملة)

- ✅ جميع الـ 11 وثيقة (structure مكتمل، sections موجودة، content Arabic-first).
- ✅ جميع الـ 4 schemas (JSON Schema 2020-12 valid، `type/properties/required` valid).
- ✅ جميع الـ 4 JSONL (rows valid، evidence_level marked، anonymized placeholders).
- ✅ جميع الـ 3 reports.
- ✅ Final Report (هذا).

### 3.2 PARTIAL (هيكل مكتمل + placeholders)

- ⚠️ Account Selection Scoring Weights في `ACCOUNT_BASED_SELLING_AR.md` — w1..w8 placeholders.
- ⚠️ Tier-1 Actual List — غير منشور لأسباب سرية.
- ⚠️ Pilot prices و Annual Contract prices — جميعها `founder-confirmed range — placeholder`.
- ⚠️ KPIs والـ targets — جميعها placeholders حتى أول Closed-Won.
- ⚠️ Expansion timeline windows — placeholders.

### 3.3 NEEDS_REVIEW (يحتاج Owner ثانوي أو Founder)

- ❌ Account Selection Weights النهائية (يحتاج Founder + Sales Lead).
- ❌ Tier-1 actual list (يحتاج Founder فقط — سري).
- ❌ Pricing bands النهائية (يحتاج Founder).
- ❌ Champion Strength Score formula (placeholder).
- ❌ جدول المدفوعات (placeholder).
- ❌ Liability Cap values (placeholder).

---

## 4. الربط مع الأنظمة الأخرى في Dealix

| النظام | كيف يُستخدم | الوثائق المرتبطة |
|--------|--------------|-----------------|
| `docs/commercial/` | حركة SMB/Commercial | يستخدم `SALES_PLAYBOOK.md` و `OFFER_LADDER.md` |
| `docs/enterprise/` | Enterprise Readiness | `VENDOR_PROFILE_AR.md`, `DPA_DEALIX_FULL.md`, `SLA_SLO_DRAFT_AR.md`, `PROCUREMENT_FAQ_AR.md` |
| `docs/enterprise_rollout/` | Department Rollout | `ENTERPRISE_ENTRY_STRATEGY.md`, `DEPARTMENT_ROLLOUT_MODEL.md`, `ENTERPRISE_ROLES.md` |
| `docs/governance/` | AI Governance | `AI_CONTROL_PLANE.md`, `CONTROLS_MATRIX.md` |
| `docs/legal/` | Legal Foundation | `DPA_DEALIX_FULL.md`, `LEGAL_FOUNDER_SELF_EXECUTION.md` |
| `docs/security/` | Security Foundation | `SECURITY_GUIDE.md`, `SECURITY_RUNBOOK.md` |
| `data/enterprise/` | Enterprise data | نمط `questionnaires.jsonl` و `risks.jsonl` (مُتّبَع) |
| `data/customer_success/` | QBR & Adoption | Customer Success Playbook |

> **هذا الـ OS لا يُكرّر أي ملف من القائمة. كل ملف يُشير إلى المصدر الأصلي.**

---

## 5. Open Questions للمؤسس

1. **Tier-1 actual list:** 5–10 حسابات سعودية مستهدفة بالاسم. (سرّي.)
2. **Account Selection Weights:** w1..w8 — أيها أكثر أهمية؟ (Strategic Fit غالبًا الأعلى، لكن يحتاج تأكيد.)
3. **Pricing Bands:** Founder-confirmed range لـ Pilot، Annual Contract، Multi-department Rollout.
4. **Champion Strength Score formula:** كيف نُوزّع الـ 5 نقاط؟ (الـ current مقترح 1 نقطة لكل بُعد من 5.)
5. **جدول المدفوعات:** Default = quarterly متساوية؟ أم شهري + setup fee؟
6. **Liability Cap values:** النطاق المسموح به (عادةً يُحدّد بـ 12 شهر من Fees).
7. **ABM Specialist:** تعيين داخلي أم outsourcing للـ campaign execution؟
8. **CRM:** HubSpot ABM أم نظام محلي؟ (يؤثّر على JSONL → CRM integration.)
9. **Procurement template:** هل MSA / SOW / NDA مكتملة في `docs/enterprise/` و `docs/legal/`؟ (يحتاج مراجعة.)
10. **Security Review SLA:** الزمن المستهدف لإجابة Security Questionnaire (مؤسسيًا 5–10 أيام).

---

## 6. أولويات 7 أيام

| # | المهمة | المالك | الإجراء |
|---|--------|--------|---------|
| 1 | تأكيد Tier-1 actual list (سرّي) | Founder | قائمة 5–10 أسماء + درجات ABM مبدئية |
| 2 | تحديد Account Selection Weights | Founder + Sales Lead | جلسة 60 دقيقة لتثبيت w1..w8 |
| 3 | ACC-001: 7-Day Actions | Sales Lead | 3 إجراءات (CRO, CFO إحالة, Comparison Sheet) |
| 4 | ACC-002: فتح EB Channel | Sales Lead + Founder | مكالمة Founder + CEO خلال 48 ساعة |
| 5 | ACC-002: إرسال DPA موقّع | Founder | مُسبّقًا قبل CISO يطلبه |
| 6 | ACC-003: إضافة 2 stakeholders | Sales Lead | Procurement + Legal → Multi-Threading = 5 |
| 7 | تحديث board.md | Sales Lead | done-status entry بعد إكمال OS |

---

## 7. أولويات 30 يوم

| # | المهمة | المالك | الإجراء |
|---|--------|--------|---------|
| 1 | تثبيت Pricing Bands | Founder | announcement رسمي + تحديث docs |
| 2 | تعيين ABM Specialist أو outsourcing | Founder + Sales Lead | قرار Hire/Outsource |
| 3 | تشغيل 3 حسابات إلى Pilot SOW موقّع | Sales Lead | ACC-002 → SOW; ACC-001/003 → Discovery |
| 4 | تكامل JSONL → CRM | Founder + Engineering | HubSpot sync أو جداول داخلية |
| 5 | Quarterly Business Review template | CS Lead | للتجديدات في الشهر 9 |
| 6 | تدريب Sales Lead على 11 وثيقة | Founder | walkthrough كامل + Q&A |
| 7 | تشغيل أول Weekly Deal Risk Review | Sales Lead | كل إثنين 30 دقيقة |
| 8 | أول MAP مع عميل حقيقي (ليس placeholder) | Sales Lead | ACC-002 الأوفر حظًا |
| 9 | تحديث ENTERPRISE_SALES_FINAL_REPORT (V2) | Founder | بعد أول Closed-Won |
| 10 | إضافة Reference anonymized واحد | Sales Lead + Founder | ضروري قبل أي Proposal |

---

## 8. تعريف النجاح (KPIs — Placeholders)

| المؤشر | الهدف (placeholder) | القياس |
|--------|---------------------|--------|
| عدد Tier-1 النشطة | 3–5 | شهري |
| Pipeline Coverage | ≥ 3× | شهري |
| Multi-Threading Index | ≥ 4 | شهري |
| متوسط زمن Discovery → Closed-Won | founder-confirmed range | ربع سنوي |
| Pilot-to-Close ratio | founder-confirmed range | ربع سنوي |
| مخاطر high مفتوحة / صفقة | < 0.5 | أسبوعي |
| Expansion rate (year 1) | founder-confirmed range | سنوي |

> **جميع الأرقام placeholders. تُعاير بعد أول Closed-Won.**

---

## 9. خريطة الـ OS (Index)

```
ENTERPRISE_SALES_OS_AR.md (هذا هو الفهرس)
│
├── ABM + TAP ─────────────── ACCOUNT_BASED_SELLING_AR.md
│                            TARGET_ACCOUNT_PROFILE_AR.md
│
├── Multi-Stakeholder ─────── STAKEHOLDER_MAPPING_AR.md
│                            BUYING_COMMITTEE_PLAYBOOK_AR.md
│                            ENTERPRISE_DISCOVERY_AR.md
│
├── Deal Process ──────────── MUTUAL_ACTION_PLAN_AR.md
│                            EXECUTIVE_BUSINESS_CASE_AR.md
│                            PILOT_TO_EXPANSION_PLAYBOOK_AR.md
│
├── Procurement & Risk ────── PROCUREMENT_SALES_PLAYBOOK_AR.md
│                            ENTERPRISE_DEAL_RISK_REVIEW_AR.md
│
└── Reports ───────────────── ENTERPRISE_PIPELINE_REVIEW.md
                             ACCOUNT_PLAN_REVIEW.md
                             ENTERPRISE_DEAL_RISK_REVIEW.md
                             ENTERPRISE_SALES_FINAL_REPORT.md (هذا)
```

---

## 10. Change Log

| التاريخ | الإصدار | التغيير |
|---------|---------|---------|
| 2026-06-03 | v0.1 | إنشاء Enterprise Sales OS (11 docs + 4 schemas + 4 data + 3 reports + final report) |

---

## 11. Conclusion

**Enterprise Sales OS v0.1** يضع Dealix في موقع تشغيلي واضح لإدارة حركة مبيعات المؤسسات في السوق السعودي. الـ OS:
- **مُتّسق** مع الأنظمة القائمة (لا تكرار).
- **آمن** (placeholders فقط للأرقام، anonymization كامل، Arabic-first).
- **قابل للتنفيذ** (4 نماذج Pilots، 10 مراحل MAP، 9 فئات مخاطر).
- **قابل للتوسّع** (Tiers، Expansion Ladder، Renewal motion).

**المطلوب الآن:** تأكيد Founder لـ Tier-1 list + Account Selection Weights + Pricing Bands.

> **آخر تحديث:** 2026-06-03 · v0.1
