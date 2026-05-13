# Dealix Holding OS — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** CEO / Group Strategy
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DEALIX_HOLDING_OS_AR.md](./DEALIX_HOLDING_OS_AR.md)

## Context
Dealix is not one product, one agency, or one SaaS. It is an **AI Operations Holding Company** that owns the operating system, the methods, the playbooks, the products, the proof, and the delivery companies for AI-enabled business capabilities across Saudi Arabia and MENA. This file is the umbrella definition of the holding shape — every other doc in `docs/holding/`, `docs/business_units/`, `docs/standards/`, and `docs/product/` plugs into the structure described here. It implements the strategic intent set in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and operates under the rules of `docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Why a holding, not a single SaaS / agency
A single SaaS is fragile because it sells software without proof. A single agency is fragile because it sells effort without compounding assets. Dealix is built as a **compound holding** so that every project a Business Unit ships simultaneously:

1. Generates **cash** (services, retainers, pilots).
2. Generates **compound assets** (Core OS upgrades, playbooks, proof, capital ledger entries, evals).
3. Earns **governance and trust** (PDPL alignment, audit log, evidence tables).

The holding shape is the structural enforcement of this rule: no Business Unit is allowed to spin up parallel infrastructure, and no Growth Engine is allowed to invent a metric outside the Standard Metrics catalog.

## The four-layer holding shape

```
Dealix Group / Holding
├─ Layer 1 — Dealix Core OS
│   LLM Gateway · Governance Runtime · Data OS · Proof Ledger
│   Capital Ledger · AI Control Tower · Client Workspace
│
├─ Layer 2 — Business Units (productized service P&Ls)
│   Dealix Revenue · Dealix Operations · Dealix Brain
│   Dealix Support · Dealix Governance · Dealix Data
│
├─ Layer 3 — Growth Engines (compounding distribution)
│   Academy · Partners · Labs · Ventures
│
└─ Layer 4 — Shared Services (group-wide)
    Sales · Delivery · Product · QA
    Finance · Legal / Compliance · Brand / Content
```

### Layer 1 — Dealix Core OS
The Core OS is **the single platform** the whole group runs on. It is detailed in [`CORE_OS_ARCHITECTURE.md`](./CORE_OS_ARCHITECTURE.md) and grounded in `docs/BEAST_LEVEL_ARCHITECTURE.md`. It exposes the contracts every Business Unit must consume:

| Core OS module | What it provides | BU consumers |
|---|---|---|
| LLM Gateway | Model routing, cost ledger, prompt registry, evals | All BUs |
| Governance Runtime | Policies, approval flow, audit log, PDPL guardrails | All BUs |
| Data OS | Source registry, quality score, PII detection, lineage | All BUs |
| Proof Ledger | Project proof packs, ROI evidence, capital assets | All BUs |
| Capital Ledger | Reusable assets, prompts, datasets, playbooks | All BUs |
| AI Control Tower | Run telemetry, board metrics, drift alerts | All BUs |
| Client Workspace | Tenant UX, RBAC, project workspace | All BUs |

### Layer 2 — Business Units
Each BU is a **productized service P&L** that consumes Core OS, sells a defined service ladder, and contributes to the Proof Ledger and Capital Ledger. The six BUs:

- [`dealix_revenue`](../business_units/dealix_revenue.md) — turn customer data into pipeline.
- [`dealix_operations`](../business_units/dealix_operations.md) — turn manual processes into governed workflows.
- [`dealix_brain`](../business_units/dealix_brain.md) — turn knowledge into source-cited answers.
- [`dealix_support`](../business_units/dealix_support.md) — raise quality and speed of customer service.
- [`dealix_governance`](../business_units/dealix_governance.md) — enable safe AI use.
- [`dealix_data`](../business_units/dealix_data.md) — prepare data for decisions and AI.

### Layer 3 — Growth Engines
Growth Engines do not deliver client projects directly. They **compound demand and distribution**:

- **Academy** — training, certifications, public methodology.
- **Partners** — agencies and integrators reselling the method.
- **Labs** — verticalized R&D (industry-specific playbooks).
- **Ventures** — strategic equity, co-builds, spin-outs.

### Layer 4 — Shared Services
A single Sales org, a single Delivery org, a single QA function, a single Finance/Legal stack — all serving every BU on an internal-billing basis. Shared Services prevents 6× cost duplication and enforces the single-method discipline of `docs/standards/DEALIX_METHOD.md`.

## The non-negotiable rule
> **Every BU consumes Core OS. No BU builds parallel infrastructure.**

If a BU needs a capability the Core OS does not yet offer, the path is:
1. File a Core OS feature candidate event (`feature_candidate_created`).
2. The Product Council prioritizes and adds it to Core OS.
3. All BUs then inherit the capability.

This is the structural mechanism that makes Dealix **a compounding holding** instead of a federation of agencies.

## Endgame statement
```
Wedge:          Revenue Intelligence
Core:           Governed AI Operations OS
Business Model: Productized Services + Retainers
Moat:           Proof + Governance + Saudi Localization + Capital Ledger
Scale:          Cloud + Academy + Partners + Ventures
Endgame:        Saudi / MENA AI Operations Holding Company
```

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Group strategy, market signals | Holding shape decisions | CEO / Group Strategy | Quarterly |
| BU performance, Scorecard signals | Sell / build / stop / raise / hire | Strategic Control Tower | Weekly |
| Core OS feature candidates | Roadmap commits | Product Council | Bi-weekly |
| Shared Services SLAs | Internal billing, capacity allocation | Group COO | Monthly |
| Proof packs, capital assets | Group asset base growth | Proof Ledger owner | Per project |

## Metrics
- **BU count active** — number of BUs with paying customers in the last 30 days.
- **Core OS adoption ratio** — % of BU production flows running on Core OS modules vs. external tooling.
- **Compound contribution rate** — % of projects that produced at least one capital asset and one proof event.
- **Holding gross margin** — blended margin after Shared Services billing.
- **Strategic decision throughput** — number of weekly sell/build/stop decisions resolved at the Control Tower.

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — group-level strategic plan this holding shape executes.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — non-negotiable operating rules across the group.
- `docs/BUSINESS_MODEL.md` — revenue model the BUs implement.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — Core OS architectural foundation.
- `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md` — Arabic master operating model.
- `docs/company/DEALIX_CEO_STRATEGY.md` — CEO-level strategic frame.
- `docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md` — group-level operating blueprint.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
