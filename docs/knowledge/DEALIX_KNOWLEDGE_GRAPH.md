---
doc_id: knowledge.dealix_graph
title: Dealix Knowledge Graph — Sector to Service to Proof
owner: HoCS
status: approved
last_reviewed: 2026-05-13
audience: [internal]
---

# Dealix Knowledge Graph

> Dealix's operating knowledge lives across many files. This graph
> defines how the entities relate so that any rep, CSM, partner, or
> agent can trace a customer problem from sector to proof. Phase 2,
> this graph becomes a recommendation engine inside Dealix.

## The entity relationship

```
Sector ──► Problems ──► Services ──► Inputs
                                       │
                                       ▼
                                    Outputs ──► KPIs ──► Risks ──► Playbooks
```

| Entity | Definition | Canonical source |
|--------|------------|------------------|
| Sector | A Saudi B2B vertical Dealix targets | `docs/strategy/VERTICAL_PLAYBOOKS.md` |
| Problems | The specific pains the sector experiences | `docs/playbooks/<sector>.md` |
| Services | Dealix services that build the capability to solve the problem | `docs/company/SERVICE_REGISTRY.md` |
| Inputs | What the customer must provide for the service to work | `docs/capabilities/<capability>.md` |
| Outputs | What the service ships | `docs/services/<service>/offer.md` |
| KPIs | The measurable lift the service produces | `docs/company/SERVICE_KPI_MAP.md` |
| Risks | What can go wrong; governance posture | `docs/governance/RUNTIME_GOVERNANCE.md` + `docs/playbooks/<sector>.md` |
| Playbooks | Sector-specific operating instructions | `docs/playbooks/<sector>.md` |

## Example trace — B2B Services

```
Sector:    B2B Services (Saudi small/mid-cap B2B consultancies, agencies)
   │
   ▼
Problems:  Leads scattered, ICP unclear, no prioritization, sales cycles
           long, retention low.
   │
   ▼
Services:  Lead Intelligence Sprint → Pilot Conversion → Monthly RevOps
   │
   ▼
Inputs:    Account/lead CSV, ICP description, service offer doc, source
           attribution, prior outcomes (won/lost).
   │
   ▼
Outputs:   Data quality report · cleaned account list · top-50 ranked
           accounts · top-10 next actions · outreach draft pack · Mini
           CRM board · executive report · Proof Pack.
   │
   ▼
KPIs:      Primary: Ranked-A accounts produced (count).
           Secondary: % accounts with cleaned firmographics.
   │
   ▼
Risks:     No cold WhatsApp/SMS/LinkedIn automation.
           Source required for every record.
           PDPL Art. 13 notice in every outreach draft.
           Per-message human approval before external send.
   │
   ▼
Playbook:  docs/playbooks/b2b_services.md (sector-specific scoring,
           outreach norms, common objections, Saudi-context outreach
           windows).
```

## How the graph is used

- **Sales call**: rep starts at Sector, walks down to Playbook;
  the conversation is sector-anchored, not service-anchored.
- **Proposal**: CRO ensures the SOW names entities at every level
  (sector, problem, service, inputs, outputs, KPI, risks).
- **Delivery**: CSM uses the Outputs row as the Stage 7 Prove
  checklist.
- **Governance**: HoLegal uses the Risks row as the PDPL audit
  surface for the project.
- **Compounding**: every project produces a Playbook update
  (per `COMPOUNDING_SYSTEM.md`); the graph gets denser over time.

## Phase 2 — recommendation engine

Once the graph reaches a critical density (≥ 25 paid customers, ≥ 5
sectors, ≥ 8 services live), it becomes a recommendation engine
inside Dealix:

- **For sales**: given a sector + 1-line problem, recommend the
  Service + KPI + Risks to discuss.
- **For delivery**: given a service + customer's input quality,
  predict QA score and time-to-value.
- **For product**: given a recurring missing Output, recommend the
  next feature to productize (per `FEATURE_PRIORITIZATION.md`).

Implementation candidate: `dealix/knowledge_os/graph.py` (Phase 2,
gated by 25-customer threshold).

## Anti-patterns

- Maintaining the graph in slide decks (it must live in the docs).
- Letting the graph diverge from the underlying files (the files are
  truth; the graph is a view).
- Adding sectors before Dealix has 2+ paid customers in them.

## Saudi / PDPL context

The Risks node for any sector with personal data always includes the
PDPL register check. The graph makes this hard to forget — every
trace surfaces the same row.

## Cross-links

- `docs/strategy/VERTICAL_PLAYBOOKS.md` — sector list
- `docs/playbooks/` — playbooks (Risks + Sector node sources)
- `docs/company/SERVICE_REGISTRY.md` — services
- `docs/company/SERVICE_KPI_MAP.md` — KPIs
- `docs/company/CAPABILITY_FACTORY_MAP.md` — capability framing
- `docs/capabilities/` — per-capability blueprints
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime checks
- `docs/company/COMPOUNDING_SYSTEM.md` — playbook updates
- `docs/product/FEATURE_PRIORITIZATION.md` — productization triggers
