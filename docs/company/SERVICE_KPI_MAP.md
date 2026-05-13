---
doc_id: company.service_kpi_map
title: Service ↔ KPI Map — No KPI, Don't Sell
owner: CRO
status: approved
last_reviewed: 2026-05-13
audience: [internal, customer]
---

# Service ↔ KPI Map

> **Binding rule**: Dealix does not sell a service that cannot be tied
> to a measurable KPI with a defined baseline, target, and proof type.
> If a service has no KPI, it does not appear on the price list.

A service without a KPI is a deliverable; a service with a KPI is a
capability lift. Dealix sells capability lifts only.

## Phase-1 (Sellable) services

| Service | Primary KPI | Secondary KPI | Proof Type |
|---------|-------------|---------------|------------|
| Lead Intelligence Sprint | Ranked-A accounts produced (count) | % of accounts with cleaned firmographics | Before/After Account Quality Snapshot + ranked list export |
| AI Quick Win Sprint | Manual hours saved per week (delta) | Process error rate (delta) | Runbook + audit log + time-study comparison |
| Company Brain Sprint | % of answers with cited source (target ≥ 95%) | Median time-to-answer (delta) | Eval report + sample Q&A with citations |
| Data Cleanup Sprint | Data Readiness Score (delta 0–100) | % records with lawful basis recorded | DQ Report v1 vs v2 + PDPL register snippet |
| AI Ops Diagnostic | Capability levels assessed (7 of 7) | Top-3 prioritized opportunities | Diagnostic Report + Capability Roadmap |

## Phase-2 (Designed/Beta) services

| Service | Primary KPI | Secondary KPI | Proof Type |
|---------|-------------|---------------|------------|
| AI Support Desk Sprint | First-response time (delta) | Suggested-reply adoption rate | Before/after ticket-time histogram + reply eval |
| Workflow Automation Sprint | Recurring tasks automated (count) | Hours saved per automation | Runbook + run history + audit log |
| Executive Reporting Automation | Time from week-close to report delivered | Decision actions taken per report | Sample weekly pack + decision log |
| AI Governance Program | Risk events with full audit trail (%) | Approval-matrix coverage (%) | Governance dashboard + audit export |
| Monthly Retainers (RevOps / AI Ops) | Recurring capability score delta per month | Net Revenue Retention | Monthly Operating Review pack |

## Rule: KPI definition is part of the SOW

Every SOW (`templates/sow/*.md`) must contain:

1. **KPI name** and how it is measured.
2. **Baseline** captured during Stage-2 Diagnose (no baseline → no
   measurable proof at close → service blocked).
3. **Target** for end of engagement.
4. **Proof Type** that will be produced at Stage-7 Prove.
5. **Owner** for measurement (HoCS by default).

## Closure rule (binding)

A project may not be marked CLOSED in the Delivery Ledger if its
Primary KPI is missing a measured before/after entry in the Proof
Ledger and Value Ledger (`VALUE_REALIZATION_SYSTEM.md`).

## Why this matters

- Pricing power: a SAR 20,000 Company Brain Sprint that lifts cited-
  answer rate from 0% to 96% justifies its price; the same sprint
  without measurement is "another chatbot".
- Retainer conversion: every retainer pitch references the KPI moved
  in the previous Sprint.
- Marketing: Proof Packs are KPI-deltas, not testimonials.

## Cross-links

- `docs/company/SERVICE_REGISTRY.md` — service catalog
- `docs/company/SERVICE_CATALOG.md` — 5-pillar summary
- `docs/company/SELLABILITY_POLICY.md` — what makes a service Sellable
- `docs/company/VALUE_REALIZATION_SYSTEM.md` — 5 value categories
- `docs/PROOF_PACK_V6_STANDARD.md` — proof pack standard
- `docs/ledgers/PROOF_LEDGER.md` — measured outcomes
- `docs/company/SERVICE_KPI_MAP.md` (this file) is referenced from every SOW
