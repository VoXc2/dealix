---
title: Dealix Maturity Model and Verification System
doc_id: W6.T37.maturity-verification
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: docs/strategy/dealix_maturity_and_verification.ar.md
related: [W0.T00, W6.T32, W6.T33, W6.T34, W6.T35, W6.T36]
kpi:
  metric: dealix_company_maturity_level
  target: 3
  window: 12m
rice:
  reach: 0
  impact: 3
  confidence: 0.95
  effort: 1
  score: governance-anchor
---

# Dealix Maturity Model and Verification System

## 1. Context

A vision is only real when it is **operationally verifiable**. This document
defines (a) the 5-level Maturity Model that grades Dealix's company state at
any moment, (b) the 7-Test arrival framework, (c) four enforceable Readiness
Gates that determine whether a service can be sold, delivered, or shipped to
production, and (d) the canonical Dealix Operating Scorecard that the CEO
reviews weekly.

It is the answer to the question: *"How do I know Dealix has arrived?"*

## 2. Audience

CEO, CTO, HoCS, HoP. Used in the weekly operating cadence (W5.T30) and the
monthly board review.

## 3. The 5-Level Maturity Model

| Level | Name | Required state |
|-------|------|----------------|
| **0** | Idea | Vision and service catalog in words only — not a company yet. |
| **1** | Productized Services | 3 starting offers (W6.T35) with scope, price, template, report, demo. |
| **2** | Repeatable Delivery | 3–5 paying customers, same service delivered twice with consistent quality, Quality Score floor 80 enforced. |
| **3** | Platform-Assisted Delivery | Dealix itself helps deliver: import, scoring, reports, drafts, approvals, audit, proof packs. Move from service → service-assisted software. |
| **4** | Retainer Machine | Predictable MRR from monthly retainers; renewal process exists; customer health score live; usage metrics tracked. |
| **5** | Enterprise AI OS | Multi-tenant, RBAC, integrations, SLA, governance dashboard, audit exports, enterprise onboarding. |

**Promotion rule:** a level is only achieved when ALL its required states are
in evidence (not aspiration). HoCS gates level promotion; CEO ratifies. We
publicly claim only the level we have evidence for.

## 4. The 7-Test Arrival Framework

Dealix has "arrived" only when all seven tests pass simultaneously.

### 4.1 Market Test
- ≥ 3 paying customers (target ≥ 10).
- ≥ 1 retainer (target ≥ 5).
- Sprint → Retainer conversion ≥ 20% (target ≥ 40%).
- Average first-90-day customer value 9.5K–25K SAR (target 45K+).
- Gross margin ≥ 50% (target ≥ 70%).
- ≥ 1 real case study (target ≥ 5).
- **Real signal:** the customer pays a second time without being re-convinced.

### 4.2 Product Test
Every service in the catalog has:
- Service page, intake form, scope template, delivery checklist, QA checklist,
  report template, demo, pricing, upsell path, supporting OS module.
- Anything without these is *not a product yet — it is manual work*.

### 4.3 Repeatability Test
The same service can be delivered to two different customers within the
documented duration without regressions in Quality Score.

### 4.4 Impact Test
Every project demonstrates at least one of:
hours saved · data cleaned · errors reduced · response speed improved ·
pipeline organized · opportunities generated · reports produced ·
knowledge made searchable · AI risk reduced.
If impact is not measurable, it is not a product.

### 4.5 Governance Test
Every project ships with source attribution, lawful basis, PII redaction,
approval workflow, audit logs, no unsafe automation, no fake claims, no
unsourced AI answers.

### 4.6 Data Test
A Data Readiness Gate runs before any AI implementation — refusing projects
where data sources are unknown, PII is unmanaged, lawful basis is missing,
or quality is below floor.

### 4.7 Team Test
Every operation has Template → Checklist → Tool → QA → Report → Playbook.
Anyone on the team can deliver the service by following the checklist — work
does not depend on a single person.

## 5. Four Enforceable Readiness Gates

### 5.1 Service Readiness Score (0–100)

A service is sold only at score ≥ 80. Below 80 = beta only.

| Criterion | Weight |
|-----------|------:|
| Clear offer + price | 10 |
| Intake form ready | 10 |
| Scope template ready | 10 |
| Supporting module/tool | 15 |
| Report template ready | 10 |
| QA checklist ready | 15 |
| Demo / sample output | 10 |
| Compliance checks defined | 10 |
| Upsell path defined | 10 |
| **Total** | **100** |

### 5.2 Delivery Readiness Gate

Before accepting a customer, all answers must be "yes":
- Required inputs known?
- Outputs defined?
- Out-of-scope items documented?
- Timeline fixed?
- Report template ready?
- QA checklist ready?
- Impact measurable?
- Next offer prepared?

### 5.3 AI Readiness Gate

Before building any AI feature for a customer:
- Is data available?
- Is its source documented?
- Is data valid?
- Is PII handled (detected + redacted)?
- Is the use case allowed under PDPL?
- Is human approval modeled?
- Is the impact metric defined?

If data is not ready → start with a Data Readiness or Data Cleanup engagement,
not an AI build.

### 5.4 Production Readiness Gate

Any feature inside Dealix enters production only when:
- Has tests · has logging · has error handling · has audit events.
- No PII leakage · output schema defined · fallback path defined.
- Cost-guard wired if LLM-backed · documentation exists.

## 6. Dealix Operating Scorecard

Single dashboard reviewed weekly in the operating cadence (W5.T30). Every
metric has an owner and a freshness requirement (≤ 7 days).

### Revenue
- MRR · new project revenue · gross margin · sprint → retainer conversion ·
  expansion revenue.

### Delivery
- On-time delivery · QA score average · rework rate · client satisfaction ·
  proof packs completed.

### Product
- Services supported by platform · manual steps automated · reusable templates ·
  active client workspaces · feature usage.

### AI Quality
- Hallucination incidents · citation coverage · eval pass rate · cost per project ·
  model failure rate.

### Governance
- PII incidents (target zero) · approval completion · audit log coverage ·
  forbidden-action blocks · source attribution coverage.

## 7. "Build Only After Repetition" Rule

A feature is added to the platform only after the underlying need has occurred
≥ 2 times in real delivery. Examples:

- Wrote 3 executive reports by hand → build the report generator.
- Cleaned 3 CSVs → build the import preview.
- Ran the same scoring 3 times → build the scoring engine.
- Delivered 3 Company Brain demos → build the RAG module.
- Manually reviewed 5 outputs → build the QA evaluator.

This rule prevents premature engineering and ensures every feature is paid for
in real delivery time before its build cost is incurred.

## 8. Weekly Decision Loop (CEO Checklist)

Every Monday, the CEO answers:

1. Which service generated revenue this week?
2. Which process repeated this week?
3. What was the biggest delay cause?
4. What did customers ask for most?
5. What took the most time?
6. What is the biggest open risk?
7. Which feature would most reduce delivery time?
8. Which service deserves to become a retainer?
9. Which vertical was most responsive?
10. Which evidence converts to a case study?

Decisions: at most three commits — one feature to build, one process to
template, one experiment to run. Output is captured into the Operating
Scorecard.

## 9. Dependencies

- W6.T34 internal OS modules — capability surface against which gates score.
- W6.T35 three starting offers — the products being graded.
- W6.T36 Delivery Standard + Quality System — Quality Score floor of 80 used here.
- W4.T13 Executive KPI spec — Scorecard wiring.
- W5.T30 Executive Operating Cadence — when this doc is reviewed.

## 10. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Operating Partner positioning: `docs/strategy/dealix_operating_partner_positioning.md`
- Service portfolio: `docs/strategy/service_portfolio_catalog.md`
- OS modules: `docs/product/internal_os_modules.md`
- Three starting offers: `docs/strategy/three_starting_offers.md`
- Delivery Standard + QA: `docs/strategy/dealix_delivery_standard_and_quality_system.md`
- KPI spec: `docs/analytics/executive_kpi_spec.md`
- Ops cadence: `docs/operations/executive_operating_cadence.md`

## 11. Owner & Review Cadence

- **Owner**: CEO. CTO + HoCS contribute on gates 5.3 + 5.4.
- **Review**: weekly Scorecard refresh; monthly Maturity-level review; quarterly
  gate-criteria revision.

## 12. The 5-Layer Architecture (canonical company structure)

Dealix as a real company stacks into exactly five layers. Every code module,
every doc, every offering must belong to one of these layers.

```
┌────────────────────────────────────────────────┐
│ 1. Service Catalog                             │  Offers, prices, scopes, outcomes
│    (W6.T33 service_portfolio_catalog.md)       │
├────────────────────────────────────────────────┤
│ 2. Delivery OS                                 │  Intake, checklist, QA, report, proof,
│    (W6.T34 §3.9 + W6.T36 + delivery_factory/)  │  handoff, renewal
├────────────────────────────────────────────────┤
│ 3. Product OS                                  │  Data / Revenue / Customer / Operations
│    (revenue_os, customer_data_plane,           │  / Knowledge OS modules
│     orchestrator, knowledge_v10, etc.)         │
├────────────────────────────────────────────────┤
│ 4. Trust OS                                    │  Governance, approvals, redaction,
│    (dealix/trust/)                             │  audit, event store, decision passport
├────────────────────────────────────────────────┤
│ 5. AI Platform                                 │  LLM gateway, agents, evals, observability
│    (dealix/llm_gateway/, ai_workforce/)        │
└────────────────────────────────────────────────┘
```

This layered view subsumes the 11-module catalog (W6.T34) and the 5 customer
pillars (W6.T32). Layers 3 and 4 power Layer 2; Layer 2 productizes Layer 1;
Layer 5 is the AI substrate beneath everything.

## 13. The Final Test Question

The single binary test that determines whether a Dealix service has reached
production-grade:

> **"Can I hand this service to a new customer at the same quality, in the
> same timebox, with the same report / proof / QA, without the founder being
> the bottleneck?"**

- Answer **yes** → the service is real.
- Answer **no** → it is still a manual project; productize before scaling.

This question is asked weekly in the operating cadence (W5.T30) for every
service the company is currently selling.

## 14. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CEO | Initial 5-level Maturity Model + 7 Tests + 4 Readiness Gates + Operating Scorecard + "Build only after repetition" rule + weekly CEO checklist |
| 2026-05-13 | CEO | Added §12 (5-Layer Architecture: Service Catalog / Delivery OS / Product OS / Trust OS / AI Platform) and §13 (Final Test Question) |
