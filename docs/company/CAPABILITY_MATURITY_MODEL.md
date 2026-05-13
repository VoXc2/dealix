---
doc_id: company.capability_maturity_model
title: Capability Maturity Model — Levels 0 to 5 per Capability
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal, customer]
---

# Capability Maturity Model

> The 5-level model (plus L0) used to assess every customer's 7
> capabilities (`CAPABILITY_OPERATING_MODEL.md`). Each level has
> concrete examples per capability and explicit movement rules. No
> Sprint, retainer, or enterprise contract is sold without an
> assessment that uses this model.

## The 6 levels (L0 baseline + L1–L5)

| Level | Name | One-line definition |
|------:|------|---------------------|
| 0 | Absent | No owner, no process, no data, no metric. |
| 1 | Manual | Work happens, but inconsistently and tribally. |
| 2 | Structured | Owner + documented process + inputs / outputs + KPI. |
| 3 | AI-Assisted | AI produces drafts; humans review and approve. |
| 4 | Governed AI Workflow | AI embedded with approvals + QA + audit + recurring report. |
| 5 | Optimized Operating System | Recurring, measured, improving, partially self-serve. |

## Level examples per capability

| Capability | L1 (Manual) | L3 (AI-Assisted) | L5 (Optimized OS) |
|------------|-------------|------------------|-------------------|
| Revenue | Leads in Excel, no scoring | Top-50 ranked accounts + AI-drafted outreach (human approved) | Weekly auto-ranked accounts + KPI dashboard + monthly improvement backlog |
| Customer | Mailbox / WhatsApp tickets handled ad hoc | AI-suggested replies, agent approves | Tagged categories + monthly retainer + suggested-reply eval ≥ 85% adoption |
| Operations | Recurring tasks done by hand each week | One automated workflow with approval + audit | Workflow library + run history + SLA + monthly improvement |
| Knowledge | "Where is that PDF?" | Cited-answer assistant on top of indexed docs | Freshness report + 3-tier access + monthly content audit |
| Data | CRM has fields but no source / lawful basis | Data Readiness Score scored + PII redacted | Continuous DQ pipeline + PDPL register live |
| Governance | Approvals over email | Approval matrix + audit-event store | Governance dashboard + zero open incidents 90 days |
| Reporting | Founder asks "what happened?" on Monday | Weekly executive pack ships every Monday | Decision-log closed loop + report-to-action time < 24h |

## Movement rules (binding)

| From → To | Trigger | Evidence required |
|-----------|---------|-------------------|
| L0 → L1 | Customer commits an owner + budget | Owner named + first artifact shipped |
| L1 → L2 | Sprint or Diagnostic completed | Owner + process + I/O + KPI documented in writing |
| L2 → L3 | Sprint shipped + Proof Pack | AI output produced + human review + QA score ≥ 80 + Proof Pack filed |
| L3 → L4 | Pilot (30–60 days) completed | Governance embedded + audit log + approval matrix + recurring report |
| L4 → L5 | Retainer ≥ 90 days | Monthly cadence + KPI dashboard + improvement backlog + monthly proof + NRR ≥ 100% |

**Hard rule**: no level skip is allowed. A customer at L1 cannot buy
into L4 without passing through L2 and L3 first. Diagnostic (Tier 1,
`IMPLEMENTATION_TIERS.md`) is the only way to score baseline level.

## Why level skipping fails

| Attempted skip | What breaks |
|----------------|-------------|
| L1 → L3 | No documented process means AI automates chaos. QA scores collapse. |
| L2 → L4 | Governance bolted on after the fact. PDPL audit fails. |
| L3 → L5 | No retainer cadence means no improvement loop. Capability decays in 60 days. |

## How this maps to the commercial path

| Tier (`IMPLEMENTATION_TIERS.md`) | Level achieved | Proof produced |
|----------------------------------|----------------|----------------|
| Tier 1 — Diagnostic | Baseline scored (L0–L2) | Capability scorecard + roadmap |
| Tier 2 — Sprint | L1 → L3 in one capability | Sprint Proof Pack |
| Tier 3 — Pilot | L3 → L4 in one capability | Pilot Proof Pack + retainer proposal |
| Tier 4 — Managed OS | L4 stable, moving toward L5 | Monthly Operating Review pack |
| Tier 5 — Enterprise OS | L5 in 3+ capabilities | Enterprise governance + audit + dashboards |

## Acceptance criteria for "built"

See `docs/capabilities/CAPABILITY_ACCEPTANCE_CRITERIA.md` — concrete
what-counts-as-done at L2 / L3 / L4 / L5.

## Saudi / PDPL context

L4 (Governed AI Workflow) is the binding floor for any AI workload
involving personal data of Saudi residents. PDPL Art. 5 (lawful basis)
and Art. 13 (data-subject notice) cannot be satisfied at L3.

## Cross-links

- `docs/company/CAPABILITY_OPERATING_MODEL.md` — the 7 capabilities
- `docs/company/AI_CAPABILITY_FACTORY.md` — the factory flow
- `docs/company/CAPABILITY_FACTORY_MAP.md` — problem → capability summary
- `docs/company/IMPLEMENTATION_TIERS.md` — commercial tiers
- `docs/capabilities/CAPABILITY_ACCEPTANCE_CRITERIA.md` — built / not-built definitions
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability → value statement
- `docs/strategy/dealix_maturity_and_verification.md` — Dealix-side maturity
- `docs/company/MATURITY_BOARD.md` — board-level tracker
