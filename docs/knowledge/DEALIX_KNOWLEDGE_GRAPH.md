# Dealix Knowledge Graph — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DEALIX_KNOWLEDGE_GRAPH_AR.md](./DEALIX_KNOWLEDGE_GRAPH_AR.md)

## Context
The Knowledge Graph is the conceptual map that connects sectors,
problems, services, inputs, outputs, KPIs, proofs, risks, governance,
and playbooks. It is the structure that prevents the company from
solving the same problem twice and ensures every new project plugs
into accumulated knowledge. It complements
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` by making strategy
machine-readable, and supports the observability stance defined in
`docs/AI_OBSERVABILITY_AND_EVALS.md`.

## Core relationships

- A **Sector** has **Problems**.
- **Problems** map to **Services**.
- **Services** require **Inputs**.
- **Services** produce **Outputs**.
- **Outputs** map to **KPIs**.
- **KPIs** create **Proof**.
- **Risks** require **Governance Controls**.
- Repeated patterns become **Playbooks**.

## Example chain

> B2B Services → messy leads → Lead Intelligence Sprint → CSV / CRM
> export → top 50 accounts + drafts → pipeline clarity → source /
> consent risk → B2B Services Playbook.

Read end-to-end: a sector (B2B Services) carries a recurring problem
(messy leads). That problem maps to a service (Lead Intelligence
Sprint). The service consumes an input (CSV / CRM export) and produces
an output (top 50 accounts + drafts). The output is measured by a KPI
(pipeline clarity). The KPI generates proof. Along the way a risk
emerges (source / consent), which requires a governance control. When
this pattern repeats across three or more clients, it becomes a
playbook.

## Node types

| Node | Examples |
|---|---|
| Sector | B2B Services, Clinics, Retail, Manufacturing, Finance |
| Problem | Messy leads, slow support, lost knowledge, manual reporting |
| Service | Lead Intelligence Sprint, Company Brain Sprint, Support Desk Sprint |
| Input | CRM export, support tickets, internal documents, financial logs |
| Output | Ranked accounts, indexed answers, automated replies |
| KPI | Hours saved, qualified accounts, response time, error rate |
| Proof | Proof pack, case study, audit log, benchmark snapshot |
| Risk | Source quality, consent, PII exposure, vendor lock-in |
| Governance | Approval gates, retention rules, audit logging |
| Playbook | Sector-specific operational guide |

## Edge rules

- Every Service node must have at least one outgoing edge to an Output.
- Every Output node must have at least one outgoing edge to a KPI.
- Every Risk node must have at least one outgoing edge to a Governance
  control.
- A Playbook node is created automatically when a Sector → Service →
  Output chain repeats successfully across three or more projects.

## Storage and tooling

The graph lives initially as a structured table in the internal
workspace. It is exported quarterly into a queryable representation
(JSON / graph DB) once the volume justifies engineering effort. Until
then it serves as a shared mental model and a feeder for the IP
Registry.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Project intake brief | New Sector / Problem nodes | Founder | Per project |
| Closure report | New Output / KPI / Proof nodes | Delivery lead | Per project |
| Governance review | New Risk / Control nodes | Founder | Per project |
| Pattern review | New Playbook nodes | Founder | Quarterly |

## Metrics
- Node growth — new nodes added per quarter; target ≥ 20.
- Coverage — share of active services with full Sector → Problem → Service → Output → KPI → Proof chain; target ≥ 80%.
- Playbook conversion — share of repeated Sector→Service patterns that produced a Playbook; target ≥ 70%.
- Risk coverage — share of Risk nodes with at least one Governance control; target 100%.

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability data that becomes proof nodes.
- `docs/AI_STACK_DECISIONS.md` — AI stack the graph leans on for retrieval.
- `docs/COMPETITIVE_POSITIONING.md` — the graph differentiates Dealix from generic AI vendors.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — knowledge capital this graph instantiates.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
