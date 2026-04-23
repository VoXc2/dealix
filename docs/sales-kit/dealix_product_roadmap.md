# Dealix — Product Roadmap

## Q2 2026 → Q4 2027

**Principle:** "Feature freeze until first 10 paying customers." كل feature بعد ذلك = feedback-driven.

---

## الوضع الحالي — Q2 2026 (Now)

### ما موجود ✅
- FastAPI backend + 9 routers
- Moyasar checkout + webhooks
- Landing page + demo request form
- Basic pipeline view (Starter tier)
- Admin dashboard (approvals, audit)
- Saudi Arabic UI (RTL)
- PDPL/GDPR-ready architecture
- PostHog analytics
- Sentry error tracking
- Railway deployment
- Public /health + public endpoints

### ما ناقص ❌ (Priority 0 — قبل أي feature جديدة)
- [ ] **Complete Railway deployment** — manual user step
- [ ] **Moyasar webhook setup** — manual user step
- [ ] **First paid customer** — no features until then

---

## Q2 2026 (الشهر الحالي + القادم)

### Theme: "Sell + Measure ONLY"

**من الـ user instructions:** "Feature freeze 14 يوم — Operation + Sell + Measure فقط"

### Tasks (NOT features):
- [x] Sales kit (36 ملف)
- [x] Legal docs (privacy, terms)
- [x] Financial model
- [ ] Deploy Railway + Moyasar webhook
- [ ] Close first 5 customers
- [ ] Collect 5 NPS scores
- [ ] 3 case studies drafted

### KPI Gate لـ Q3:
- **10 paying customers** — هذا الـ gate الوحيد
- NPS > 40
- 1 case study live

---

## Q3 2026 (Jul-Sep)

### Theme: "Stabilize + Hire"

### Product Features (بعد الـ gate)

#### P1 — Must Have
1. **Bulk import wizard** — CSV/Excel → Dealix
   - Trigger: من feedback أول 5 عملاء
   - Effort: 2 أسابيع
   
2. **Mobile app (iOS + Android)** — React Native
   - 80% feature parity مع web
   - Effort: 6 أسابيع (part-time)

3. **Email sync (Gmail + Outlook)**
   - Thread tracking per lead
   - Auto-log مكالمات
   - Effort: 3 أسابيع

4. **Workflow automation (v1)** — 5 triggers فقط
   - Lead stuck > X يوم → alert
   - New lead → assign by territory
   - Deal closed → Slack notification
   - Effort: 2 أسابيع

#### P2 — Nice to Have
5. **Custom fields** — حتى 10 fields
6. **Email templates** — Arabic + English
7. **Reports builder (basic)** — 5 report types

### Hires
- Senior Full-stack Engineer (Sep)
- CSM / Customer Success (Oct)

### KPI Gate لـ Q4:
- 45 paying customers
- MRR 45K SAR
- Churn < 7% monthly
- 5 case studies live

---

## Q4 2026 (Oct-Dec)

### Theme: "Scale + Raise"

### Product Features

#### P1
1. **Scale tier launch**
   - SSO (Google, Microsoft, SAML)
   - Advanced RBAC
   - Audit logs exportable
   - Custom domains
   - Effort: 4 أسابيع

2. **AI Lead Scoring v1**
   - مدعوم بـ Claude/GPT-4
   - Arabic + English signal
   - ROI: +20% conversion expected
   - Effort: 3 أسابيع

3. **WhatsApp Business API (direct integration)**
   - Meta-approved templates (Arabic)
   - Two-way sync
   - Auto-log responses
   - Effort: 6 أسابيع (depends on Meta approval 2-4 أسابيع)

4. **Pipeline Forecasting**
   - Weighted pipeline value
   - Close probability (AI-enhanced)
   - Effort: 2 أسابيع

#### P2
5. **Integrations marketplace (v0)**
   - Zapier support
   - Salesforce import (one-way)
   - 3-5 most-requested integrations
   
6. **Advanced reports**
   - Cohort analysis
   - Pipeline velocity
   - Team performance dashboards

### Funding
- **Seed round** — Oct/Nov
- Target: 1-2M SAR
- 10-15% dilution

### KPI Gate لـ 2027:
- 100 paying customers
- ARR 1.5M SAR
- NRR > 110%
- 3 reference customers للـ VC calls

---

## Q1 2027 (Jan-Mar)

### Theme: "UAE Expansion Prep"

### Product
1. **Multi-currency support**
   - SAR, AED, QAR, BHD, KWD, OMR
   - Auto-detect by customer location
   
2. **VAT handling per GCC country**
   - KSA 15%, UAE 5%, etc.
   - Invoicing compliance per country
   
3. **Multi-language (English alongside Arabic)**
   - Full translation (not just UI)
   - For UAE market (more English-speaking)

4. **Team territories**
   - Geographic routing
   - Per-country pipeline views

### Operations
- UAE legal entity setup (Dubai/ADGM)
- UAE bank account
- UAE VAT registration
- 2 Sales reps hired (KSA + UAE)

### KPI Gate Q2:
- 180 customers total
- 20 UAE customers
- MRR 250K SAR

---

## Q2 2027 (Apr-Jun)

### Theme: "UAE Launch"

### Product
1. **Enterprise features**
   - Data residency options (KSA vs UAE)
   - Advanced audit (SOC 2 prep)
   - Custom SLAs per customer
   - White-label option (agency partners)

2. **AI Assistant (chat-based)**
   - "Ask Dealix" — natural language queries
   - Auto-summarize long threads
   - Suggest next actions
   - Arabic-first

3. **Mobile app v2**
   - Offline mode
   - Voice-to-text (Saudi dialect)
   - Biometric login

### GTM
- UAE launch event (Dubai)
- Arabic Content calendar expansion (UAE dialect)
- UAE-specific case studies

### KPI Gate Q3:
- 280 customers
- 45 UAE
- 5K NPS responses
- Series A readiness

---

## Q3 2027 (Jul-Sep)

### Theme: "Platform Maturation"

### Product
1. **Dealix Intelligence** — Analytics suite
   - Cross-tenant benchmarking (anonymous)
   - Industry reports
   - Competitive intel

2. **Sales enablement**
   - Content library
   - Training modules
   - Certification program

3. **Partner marketplace**
   - System integrators
   - Consultants
   - Add-on developers

### Operations
- Qatar + Bahrain research
- SOC 2 Type I audit (October)
- ISO 27001 audit

### KPI Gate Q4:
- 350 customers
- ARR 7M SAR
- 3 mature markets (KSA/UAE) + 1 pilot (Qatar)

---

## Q4 2027 (Oct-Dec)

### Theme: "Series A + Regional Leadership"

### Product
1. **Enterprise platform**
   - Multi-org support (for consultancies)
   - Advanced workflow engine (complex automations)
   - Custom integrations framework
   - API marketplace

2. **Dealix Mobile v3**
   - AR visualization (meeting prep)
   - Voice assistant
   - Offline-first architecture

3. **Industry verticals**
   - Dealix for Logistics
   - Dealix for Real Estate
   - Dealix for F&B

### GTM
- Qatar launch
- Bahrain launch
- Regional events (Web Summit, STEP)

### Funding
- Series A: 10-20M SAR
- Target valuation: 80-120M SAR
- Lead: regional VC (STV, Raed, or similar)

### End-of-Year Targets:
- 480 customers
- ARR 12M SAR
- 4 markets (KSA, UAE, Qatar, Bahrain)
- Series A closed

---

## Long-term Vision (2028-2030)

### 2028
- 1,200 customers
- 5 markets (+ Kuwait)
- Dealix Intelligence as separate product
- ARR 30M+ SAR

### 2029
- 3,500 customers
- Launch Dealix AI (proprietary LLM sales-tuned)
- Acquisition opportunities (smaller competitors)
- ARR 90M+ SAR

### 2030 (Vision 2030 alignment)
- 8,000+ customers
- Pan-Arab leader
- IPO or strategic acquisition
- ARR 200M+ SAR

---

## قواعد الـ Roadmap

### ما يدخل الـ roadmap
- ✅ > 3 عملاء طلبوه
- ✅ يحل ألم محدد + measurable
- ✅ ROI واضح (revenue أو retention)
- ✅ technical feasibility محققة
- ✅ strategic alignment

### ما لا يدخل
- ❌ "يعجبني لو نضيف"
- ❌ عميل واحد طلبه
- ❌ ما نقدر نقيسه
- ❌ Big tech-debt accumulation
- ❌ Ops-heavy features بدون ROI

---

## آلية التحديث

- **أسبوعي:** mini-review (30 دقيقة)
- **شهري:** user feedback synthesis
- **ربع سنوي:** roadmap revision + communication للعملاء
- **نصف سنوي:** strategic overhaul + market validation

**الشفافية:** public roadmap على dealix.sa/roadmap (بدون تواريخ تفصيلية — أرقام ربعية فقط).

---

## Risk Mitigation

| المخاطرة | الأثر | Mitigation |
|---------|------|-----------|
| Meta WhatsApp approval delay | عالي | Fallback: Twilio integration |
| Hires يتأخرون | متوسط | Network pipeline + remote-friendly |
| UAE launch faces regulatory issues | متوسط | ADGM zone + legal partner early |
| Funding market يتدهور | متوسط | Bootstrap-able — لسنا dependent |
| Tech debt accumulation | منخفض | 20% effort reserved للـ refactoring |

---

*آخر تحديث: 2026-04-23 | Next review: 2026-07-23*