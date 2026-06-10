# Deliverables Library — مكتبة المخرجات
**Dealix — Agent #3**

> **الغرض:** قائمة موحدة بكل المخرجات (deliverables) التي يمكن أن تقدمها Dealix. كل عميل يجب أن يعرف بالضبط ماذا سيستلم، بأي format، ومتى.

---

## 1. Deliverable Categories

### 1.1 Reports (تقارير)
- Diagnostic Report
- Leakage Map
- Workflow Design Doc
- Implementation Plan
- Delivery Status Report
- Weekly Value Report
- Monthly Performance Report
- Renewal Health Report

### 1.2 Workflows (تدفقات عمل)
- Follow-up Workflow
- Lead Nurture Workflow
- Proposal Workflow
- Onboarding Workflow
- Renewal Workflow
- Support Triage Workflow
- Reporting Workflow

### 1.3 Dashboards (لوحات)
- Pipeline Dashboard
- Lead Quality Dashboard
- Conversion Dashboard
- Revenue Dashboard
- Client Health Dashboard
- Channel ROI Dashboard

### 1.4 Templates (قوالب)
- Email Templates
- WhatsApp Templates
- Proposal Templates
- Discovery Question Templates
- Objection Response Templates
- Case Study Templates
- Invoice Templates (per ZATCA)

### 1.5 Playbooks (أدلة)
- Sales Playbook
- Discovery Playbook
- Objection Playbook
- Renewal Playbook
- Onboarding Playbook

### 1.6 Integrations & Configs
- CRM Setup
- HubSpot Config
- Calendly Setup
- Email Warmup Config
- WhatsApp Templates
- Reporting Tools

### 1.7 Training Materials
- Workflow Training Deck
- Team Training Session
- Video Walkthroughs
- FAQ Docs

### 1.8 Evidence & Proof
- Proof Pack
- Case Study (anonymized)
- ROI Estimate (with `is_estimate` label)
- Before/After Workflow
- Data Insights Report

---

## 2. Format Standards

### 2.1 Documents
- **Format:** Markdown (AR) or PDF (final)
- **Language:** Arabic primary, English secondary
- **Length:** depends on package, but no fluff
- **Source citation:** every claim has source or `is_estimate`

### 2.2 Reports
- **Header:** client, date, version, approval
- **Sections:** executive summary, findings, recommendations, next steps
- **Footer:** evidence level, founder approval, dry-run note

### 2.3 Dashboards
- **Tool:** Looker, Metabase, or custom (per stack)
- **Refresh:** daily/weekly as agreed
- **Access:** client + Dealix team
- **Branding:** white-label option (partner)

### 2.4 Templates
- **Format:** copy-paste ready
- **Variables:** clearly marked
- **Approval required:** yes, if customer-facing
- **Versioning:** tracked

### 2.5 Playbooks
- **Format:** step-by-step with screenshots
- **Owner:** who does what
- **Approval:** who approves
- **Evidence:** who checks
- **Update:** quarterly

### 2.6 Proof Packs
- **Format:** PDF + supporting data
- **Evidence level:** labeled (L0-L5)
- **Approval:** founder for L4-L5
- **Disclaimer:** clearly stated

---

## 3. Per-Product Deliverables (Quick Reference)

| Product | Key Deliverables |
|---------|------------------|
| Readiness Scan | 1-page report + top 3 priorities |
| Diagnostic | Leakage map + 1 report + recommendations |
| Workflow | 1 workflow + templates + 2-week support + weekly report |
| Starter | 3-5 workflows + 1 dashboard + weekly review |
| Full OS | 5-10 workflows + 2-3 dashboards + 60-day support |
| Retainer | Weekly review + monthly report + experiments |
| Custom | Per SOW |

---

## 4. Acceptance Criteria

لكل deliverable:
- **Definition of Done (DoD):** what makes it "ready"
- **Approval Required:** yes/no
- **Client Sign-off:** required
- **Evidence Level:** labeled
- **Source:** if applicable
- **Issue Window:** X days for revisions

---

## 5. Delivery Cadence

| Deliverable | Cadence | Owner |
|-------------|---------|-------|
| Diagnostic Report | one-time | Proposal Agent |
| Weekly Value Report | weekly | CS Agent |
| Monthly Performance | monthly | CS Agent |
| Renewal Health | monthly | Renewal Agent |
| Ad-hoc Reports | on request | Sales/CS |
| Status Updates | daily/weekly | Delivery OS |

---

## 6. Quality Standards

### 6.1 Every Deliverable Must
- ✅ Have evidence level labeled
- ✅ Have approval before send
- ✅ Be free of guaranteed claims
- ✅ Have source citation
- ✅ Be relevant to client's pain
- ✅ Be in client's language

### 6.2 Quality Red Flags
- ⚠️ No source for numbers
- ⚠️ Vague recommendations
- ⚠️ Off-topic to pain
- ⚠️ Too long / padding
- ⚠️ Not actionable

---

## 7. Deliverable Storage

### 7.1 Where
- Reports: `data/commercial/{client_id}/reports/`
- Workflows: `data/commercial/{client_id}/workflows/`
- Templates: `data/commercial/{client_id}/templates/`
- Dashboards: external tool (Metabase, etc.) with client access
- Proof Packs: `data/commercial/{client_id}/proof/`

### 7.2 Naming Convention
- `{date}_{type}_{version}_{client_slug}.{ext}`
- Example: `2026-06-03_diagnostic_v1_acme-agency.md`

---

## 8. Versioning

- **v1, v2, v3...** for each version
- **draft, review, approved, sent** for status
- **All versions stored** (for audit)

---

## 9. Client-Side Acceptance

### 9.1 For Each Deliverable
- Client reviews within X days
- Client accepts or requests changes
- Founder approves final
- Sent to client with delivery note

### 9.2 Acceptance Slip
- Sign-off document
- Tracks revision count
- Locks in acceptance
- Stored for audit

---

## 10. Companion Files

- Catalog: `PRODUCT_CATALOG_AR.md`
- Packaging: `PACKAGING_STRATEGY_AR.md`
- Scope: `SCOPE_AND_OUT_OF_SCOPE_AR.md`
- Customer Success: `CUSTOMER_SUCCESS_OS_AR.md` (PHASE 11)

---

**Deliverables = promise. كل واحد يجب أن يكون واضح، قابل للقياس، قابل للتسليم، قابل للقبول. لا "extra mile" — في نطاق، أو change order.**
