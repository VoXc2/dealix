---
title: Dealix Delivery Standard and Quality System
doc_id: W6.T36.delivery-quality
owner: HoCS
status: approved
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: docs/strategy/dealix_delivery_standard_and_quality_system.ar.md
related: [W0.T00, W6.T32, W6.T33, W6.T34, W6.T35, W5.T10, W5.T18]
kpi:
  metric: project_quality_score_floor
  target: 80
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.9
  effort: 2
  score: delivery-foundation
---

# Dealix Delivery Standard and Quality System

## 1. Context

Selling well is not enough. Dealix's defensible moat is the **consistency and quality of delivery** across every customer. This document defines (a) the eight-stage Dealix Delivery Standard every project follows, (b) the five-gate Quality System every project passes through, (c) the project Quality Score (0–100) that gates handoff, and (d) the five competitive advantages we operationalize to be uncopyable in the Saudi market.

It is the document that turns Dealix from a freelance-style AI shop into a productized AI Operating Partner.

## 2. Audience

CS, Delivery, Engineering, CRO. Customers receive a customer-facing version (the AR companion) as the standard SOW addendum.

## 3. The Eight-Stage Delivery Standard

Every Dealix project — Sprint, Pilot, Retainer, Enterprise — follows the same eight stages:

```
Discover → Diagnose → Design → Build → Validate → Deliver → Prove → Expand
```

### 3.1 Discover

Understand the company.
- Sector, team size, revenue band, sales channels, current tools.
- Where time is wasted, where money is lost, where risk lives.
- Available data, file inventory, system access.

**Output**: completed intake form (Delivery OS), discovery summary.

### 3.2 Diagnose

Score the situation.
- Data readiness score.
- Process maturity score.
- AI use-case score.
- Risk score (PDPL, operational, brand).
- ROI estimate (low / mid / high).
- Quick-win identification.

**Output**: diagnostic report; top-3 recommended use cases with scoring rationale.

### 3.3 Design

Architect the solution.
- Workflow design.
- Data schema and source map.
- Prompts, approvals, escalations.
- Dashboard wireframe.
- Output specifications.
- Success metrics (numeric, dated).

**Output**: design document signed by customer.

### 3.4 Build

Execute with minimum complexity.
- Reuse existing OS modules (no bespoke code where composition works).
- Human-in-the-loop by default.
- Audit logs from day 1.
- Templates over custom UIs.
- Test cases written before code.

**Output**: working build in customer environment.

### 3.5 Validate

Stress-test before handoff.
- Quality / safety / accuracy / speed.
- Edge cases (empty input, foreign characters, malformed records).
- Arabic and English tone validation.
- PII / PDPL red-team.
- Customer UAT.

**Output**: validation report with pass/fail per criterion.

### 3.6 Deliver

Hand over with discipline.
- Dashboard or workflow live in customer environment.
- Executive report.
- SOP / runbook.
- Training session (recorded).
- Handoff document.

**Output**: handoff packet acknowledged by customer.

### 3.7 Prove

Quantify the impact (within 14 days of delivery).
- Hours saved per week.
- Qualified leads generated.
- Tickets classified / response time delta.
- Pipeline value created.
- Data quality before/after.
- Customer feedback rating.

**Output**: proof pack added to Proof Ledger (`docs/revenue/PROOF_LEDGER*` family).

### 3.8 Expand

Open the next conversation.
- Retainer.
- Additional workflow.
- New pillar (Brain after Grow, Govern after Brain, etc.).
- Enterprise upgrade.

**Output**: signed renewal or next-sprint scope, or documented "no" with reason.

## 4. The Five-Gate Quality System

Every project passes through five QA gates before handoff. Any FAIL blocks delivery.

### 4.1 Business QA

- Is the problem statement explicit?
- Does the output matter to executive decision-makers?
- Is there a numeric KPI?
- Is there a clear next action?
- Is there an upsell path?

### 4.2 Data QA

- Is every data source attributed?
- Are duplicates handled?
- Are missing fields documented?
- Is PII detected and (where required) redacted?
- Is lawful basis (PDPL Art. 5) documented?
- Is data quality score calculated and shared?

### 4.3 AI QA

- Are outputs accurate (sampled against truth set)?
- Are hallucinations caught (citation-grounded where applicable)?
- Are sources cited?
- Is Arabic tone appropriate for sector and buyer level?
- Are edge cases tested?

### 4.4 Compliance QA

- Are there exaggerated claims or unverifiable benefits?
- Is cold outreach PDPL-compliant (Art. 13 notice / Art. 14 consent)?
- Is PII absent from reports?
- Is human approval logged where required?
- Is the audit trail complete and queryable?

### 4.5 Delivery QA

- Are all deliverables in the handoff packet?
- Is the executive report clear to a non-technical reader?
- Does the customer know what to do next?
- Is the handoff session scheduled / completed?
- Is the renewal / next-step proposal drafted?

## 5. Project Quality Score (0–100)

Every project is scored against seven weighted criteria. Floor for handoff: **80**.

| Criterion | Weight |
|-----------|-------:|
| Business impact clarity | 20 |
| Data quality | 15 |
| AR/EN output quality | 15 |
| Customer usability | 10 |
| Safety & compliance | 15 |
| Productization potential (reusable as template) | 15 |
| Upgradeability to retainer | 10 |
| **Total** | **100** |

Projects below 80 do not ship until improved. Scoring lives in Delivery OS (`dealix/delivery/qa_review.py`) and is reviewed weekly by HoCS.

## 6. Five Competitive Advantages (Operationalized)

These are not slogans — each one ties to a specific operational mechanism.

| Advantage | What it means | How we operationalize it |
|-----------|---------------|--------------------------|
| **Outcome-first** | Every service has a numeric outcome | KPI per offering in W6.T33; outcome captured in Proof Ledger |
| **Saudi-localized** | AR/EN, sectors, cities, local context | Bilingual outputs (W3.T20 index); vertical playbooks (W1.T01); ZATCA / PDPL gates baked in |
| **Proof-backed** | Every project produces evidence | Proof pack mandatory in stage 7; Proof Ledger appendable, citable in sales |
| **Governed AI** | Source attribution, PII, approvals, audit | Governance OS gates every action (W4.T14); Decision Passport stamped on every outbound action |
| **Productized delivery** | Same quality repeats per customer | Delivery OS (W6.T34 §3.9) + this Quality System; no bespoke without ≥3 reuse candidates |

## 7. Vertical Playbooks

Per sector (BFSI, Retail/eComm, Healthcare, Education, Real Estate, Logistics, Restaurants, Construction, Clinics, Professional Services), each playbook contains:

- Top 5 pains.
- ICP refinement.
- Recommended offerings (from W6.T33 catalog).
- Top 5 objections + counters.
- Scoring rules tweaks.
- Outreach templates.
- KPIs.
- Compliance notes (sector-specific, e.g., SAMA for BFSI, SFDA for Healthcare, NUPCO for procurement).

Initial playbooks are W1.T01 (BFSI, Retail, Healthcare). Phase 2 adds Education, Real Estate, Logistics. Phase 3 adds the rest.

## 8. Proof Ledger

A repository where every project's before/after evidence lives. For each project:

- Records cleaned (n, %).
- Hours saved per week.
- Messages drafted / sent / replied.
- Tickets classified.
- Pipeline value created.
- Customer feedback rating.

Surfaced in `docs/revenue/PROOF_LEDGER*` family (and existing files). Sales reps cite Ledger entries by ID in proposals — turns Dealix's own delivery into the most credible reference customer.

## 9. KPIs

- Average Quality Score across projects: ≥ 85.
- % of projects passing all 5 gates first-time: ≥ 70%.
- Stage 7 (Prove) completion rate within 14 days: ≥ 95%.
- Stage 8 (Expand) opens a documented next conversation: 100% of projects.
- Mean time from "Diagnose" to "Deliver" for Sprint offerings: ≤ planned duration (7 / 10 / 14 / 21 / 30 days per offering).

## 10. Dependencies

- W6.T34 Delivery OS module (this doc operates the OS).
- W6.T33 service portfolio (each catalog offering applies this Standard).
- W3.T07 trust pack (Compliance QA references Trust).
- W4.T14 policy rules (Compliance QA references rules).
- W4.T25 data quality gates (Data QA references gates).
- W5.T10 CS framework (handoff to CS uses this Standard).
- W5.T18 pilot framework (paid pilots use this Standard with extended scope).

## 11. Cross-links

- Positioning: `docs/strategy/dealix_operating_partner_positioning.md`
- Portfolio: `docs/strategy/service_portfolio_catalog.md`
- OS modules: `docs/product/internal_os_modules.md`
- Starting offers: `docs/strategy/three_starting_offers.md`
- Trust pack: `docs/trust/`
- Policy rules: `docs/policy/revenue_os_policy_rules.md`
- Data quality gates: `docs/data/data_quality_gates.md`
- CS framework: `docs/customer-success/cs_framework.md`

## 12. Owner & Review Cadence

- **Owner**: HoCS (delivery side) + HoP (productization side).
- **Review**: weekly QA scoreboard review in operating cadence (W5.T30); monthly Standard refresh; quarterly retro on which gates caught the most issues.

## 13. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial 8-stage Delivery Standard, 5-gate QA, Quality Score, 5 advantages, vertical playbooks, Proof Ledger |
