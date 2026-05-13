# 12-Month Company Roadmap — Build & Target by Phase

**Layer:** L7 · Execution Engine
**Owner:** Founder / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [12_MONTH_COMPANY_ROADMAP_AR.md](./12_MONTH_COMPANY_ROADMAP_AR.md)

## Context
This is the company-level twelve-month roadmap — the build, sell, and
target plan that the entire company runs against, phase by phase. It is
distinct from `docs/growth/12_MONTH_ROADMAP.md` (Growth Machine) and
`docs/PRODUCT_ROADMAP.md` (product surface). This file removes the
ambiguity about *which build is allowed when*, and gates each phase on
revenue, proof, and retainer count. It plugs into the operating doctrine
in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the 90-day overlay in
`docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`.

## Phase Map

| Phase | Window | Theme | Exit Gate |
|---|---|---|---|
| 1 | Days 1-30 | Sellable Core | 1-3 paid customers, 1 proof pack |
| 2 | Days 31-60 | Repeatable Delivery | 3-5 customers, 1 retainer, QA ≥ 85 |
| 3 | Days 61-90 | Retainer Machine | 5-8 customers, 2 retainers, MRR floor |
| 4 | Months 3-6 | Product-Assisted Services | 10+ clients, 3-5 retainers, SAR 50k+ MRR |
| 5 | Months 6-12 | Managed AI Ops Platform | 25+ clients, 8-12 retainers, SAR 150k+ MRR |

## Phase 1 — Days 1-30: Sellable Core

**Build (engineering + ops spine):**
- Service catalog (public 5-door).
- Lead Intelligence offer (scoped, priced).
- AI Quick Win offer (scoped, priced).
- Company Brain offer (scoped, priced).
- Proof pack template (anonymizable).
- Governance rules baseline.
- Quality standard v1.

**Code spine:**
- `data_os.import_preview`
- `data_os.data_quality_score`
- `governance_os.policy_check`
- `revenue_os.scoring`
- `reporting_os.proof_pack`

**Sell:** Lead Intelligence Sprint, AI Quick Win Sprint.

**Target:** 1-3 paid customers · SAR 10k-40k revenue · 1 proof pack ·
0 PII incidents.

## Phase 2 — Days 31-60: Repeatable Delivery

**Build:**
- `delivery_os` — intake form, scope builder, QA checklist, handoff
  procedure, renewal recommendation.
- `reporting_os` — executive report, proof pack, weekly summary.

**Sell:** Lead Intelligence Sprint, Company Brain pilot, AI Quick Win
Sprint.

**Target:** 3-5 paid customers · 1 retainer · 2 proof packs ·
1 vertical playbook · QA average ≥ 85.

## Phase 3 — Days 61-90: Retainer Machine

**Build:**
- Client Workspace v1 — overview, data quality, top actions, reports,
  approvals, proof pack.
- Founder Command Center v1 — revenue, delivery, proof, governance,
  product backlog.

**Sell:** Monthly RevOps OS, Monthly AI Ops, Monthly Company Brain.

**Target:** 5-8 paid customers · 2 retainers · SAR 20k-50k MRR ·
3 reusable playbooks.

## Phase 4 — Months 3-6: Product-Assisted Services

**Build:**
- LLM Gateway.
- Prompt Registry.
- Capital Ledger.
- Proof Ledger.
- Client Health Score.
- Capability Backlog.
- Basic Company Brain RAG.
- Support Desk suggested replies.

**Sell:** Continue all retainers; add Workflow Pilot and Support Desk
Pilot.

**Target:** 10+ paid clients · 3-5 retainers · SAR 50k+ MRR ·
5 proof packs · 3 case studies.

## Phase 5 — Months 6-12: Managed AI Ops Platform

**Build:**
- Multi-client workspace.
- Role permissions v1.
- Workflow runtime.
- Eval runner.
- AI run ledger.
- Audit exports.
- Integrations v1.
- Enterprise governance pack.

**Sell:** Enterprise AI OS pilots; expansion within retainer base.

**Target:** 25+ clients served · 8-12 retainers · SAR 150k+ MRR ·
1 enterprise pilot · Dealix Method published as public standard.

## Gate Discipline

A phase does not end on a date. It ends when the exit gate is met.
Building Phase 4 modules while Phase 2 gate (QA ≥ 85) is unmet is
explicitly forbidden — that is the `STOP_DOING` rule operationalized.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Strategic plan, pipeline, capacity | Phase plan and exit gates | Founder | Quarterly review |
| Phase plan | Weekly build/sell/target | Founder | Weekly |
| Phase exit evidence | Gate decision | Founder | Per phase |

## Metrics
- Phase exit gate pass — boolean per phase.
- MRR trajectory — month-over-month SAR.
- Retainer count — total active monthly contracts.
- Proof pack count — cumulative anonymized packs published.
- Case study count — cumulative named customer stories.

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan the roadmap executes.
- `docs/V5_COMPLETION_ROADMAP.md` — V5 completion track running in parallel.
- `docs/PRODUCT_ROADMAP.md` — product surface that backs phases 4-5.
- `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` — 90-day overlay onto phases 1-3.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
