# Intelligence Layer — Operating Brain

**Layer:** Intelligence · Operating Brain
**Owner:** CEO / Chief of Staff
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [INTELLIGENCE_LAYER_AR.md](./INTELLIGENCE_LAYER_AR.md)

## Context
The Intelligence Layer is the operating brain of Dealix. It sits **above** the
Core OS — it does not serve clients directly. It serves Dealix itself, by
converting raw events from every project, agent, and ledger into the four
strategic questions the company has to answer every week: **what to scale,
what to stop, what to productize, what to convert to retainer, and what to
promote to venture**. This file is the umbrella for the seven-component stack
that produces those answers. Without this layer, Dealix can deliver work but
cannot compound it, and the company silently regresses into a custom-work
agency. See `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and
`docs/DEALIX_OPERATING_CONSTITUTION.md` for the strategic mandate this layer
fulfils, and `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` for the autonomous
revenue posture it governs.

## Position above Core OS
The Core OS is the **execution stack** — agents, workflows, ledgers, runtime
governance, delivery and revenue surfaces that produce client outcomes. The
Intelligence Layer is the **decision stack** — it consumes everything Core OS
emits and produces the strategic decisions that change what Core OS does next.

```
+---------------------------------------------------+
|           Intelligence Layer (this doc)           |
|       Event -> Ledger -> Metric -> Decision       |
|       -> Capital -> Venture -> Memory             |
+----------------------^----------------------------+
                       | events, ledger entries
+----------------------|----------------------------+
|                  Core OS                          |
|  Agents · Workflows · Delivery · Revenue · Govern |
+---------------------------------------------------+
```

Core OS feeds the Intelligence Layer raw events; the Intelligence Layer feeds
Core OS strategic decisions (kill, scale, productize, graduate). They are two
distinct layers, not nested. Treating the Intelligence Layer as a sub-module
of Core OS is the single most common architectural mistake — it collapses
strategy into operations and removes Dealix's ability to think.

## The seven-component stack
```
1. Event Layer        — every meaningful action emits an event.
2. Ledger Layer       — events accumulate in named ledgers.
3. Metric Layer       — ledgers produce indicators.
4. Decision Layer     — indicators become weekly/monthly decisions.
5. Capital Allocation — decisions allocate time/money to buckets.
6. Venture Signal     — units scored for graduation.
7. Strategic Memory   — lessons captured per project.
```

Each component has a dedicated file in this folder. The order matters: you
cannot have decisions without metrics, you cannot have metrics without
ledgers, you cannot have ledgers without a disciplined event vocabulary. Skip
one and the whole stack degrades into dashboards-without-action.

### 1. Event Layer
Every meaningful action inside Dealix emits a structured event. The event
taxonomy is defined in `EVENT_TO_DECISION_SYSTEM.md`. Events are the only
sanctioned input into the Intelligence Layer; anything not represented as an
event is invisible to strategy.

### 2. Ledger Layer
Events accumulate into nine named ledgers (AI Run, Audit, Proof, Capital,
Productization, Client Health, Unit Performance, Partner, Venture Signal).
Schemas and primary consumers are defined in `LEDGER_ARCHITECTURE.md`. Each
ledger has exactly one accountable owner.

### 3. Metric Layer
Ledgers produce indicators — cost per project, proof-to-retainer conversion,
schema failure rate, unit margin, productization ratio. The full catalog is
in `METRICS_ENGINE.md`. Metrics are the lingua franca between layers.

### 4. Decision Layer
Indicators trigger weekly and monthly decisions. The pipeline from event to
decision is in `EVENT_TO_DECISION_SYSTEM.md`. A decision is a binding
instruction to the Core OS — to route to a cheaper model, to promote a
service line, to halt a custom build, to elevate a unit to graduation.

### 5. Capital Allocation
Decisions allocate finite time and money to five buckets (Cash Engine, Core
OS, Proof + Capital Assets, Growth + Partners, Labs + Experiments). The
priority score formula and bands are in `CAPITAL_ALLOCATION_SCORE.md`. Capital
allocation is how Dealix says no.

### 6. Venture Signal
Service lines, modules, and business units are scored continuously for
graduation. The Venture Readiness Score and the four bands (Venture, Business
Unit, Service Line, Keep-Inside) are in `VENTURE_SIGNAL_MODEL.md`. This is
how Dealix produces ventures instead of stalling as a single company.

### 7. Strategic Memory
Every project, win, and loss writes lessons into a structured memory store.
The capture template and files are in `STRATEGIC_MEMORY.md`. Memory is what
turns a single delivery into a compounding asset.

## What the layer outputs
- A weekly **Decision Pack** consumed by the CEO and Heads (see
  `docs/EXECUTIVE_DECISION_PACK.md`).
- A monthly **Capital Allocation Review** that re-weights the five buckets.
- A quarterly **Venture Signal Review** that promotes or demotes units.
- A continuously updated **Strategic Memory** that feeds new pitches,
  pricing, playbooks, and product candidates.

## What the layer refuses to do
- It does not run client workflows. Those belong to Core OS.
- It does not write code or generate deliverables. Those belong to agents.
- It does not negotiate, sell, or invoice. Those belong to Revenue OS.
- It does not approve PDPL or governance actions. Those belong to
  `docs/governance/RUNTIME_GOVERNANCE.md`.

This layer's only job is to **decide**.

## Guardrails
- The Intelligence Layer reads from ledgers; it never writes into Core OS
  state directly. It emits decisions, which Core OS owners then execute.
- Two anti-drift doctrines bound this layer:
  `ANTI_AGENCY_RULES.md` prevents drift into custom-work agency,
  `ANTI_EMPTY_SAAS_RULES.md` prevents premature SaaS.
- Every agent that touches this layer is bound by
  `AGENT_CONTROL_DOCTRINE.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Core OS events (all 21 types) | Weekly Decision Pack | CEO | Weekly |
| Nine ledgers | Capital Allocation Review | CFO + CEO | Monthly |
| Metric Engine outputs | Venture Signal Review | CEO + Unit Owners | Quarterly |
| Project lessons | Strategic Memory updates | Heads of Delivery, Revenue, Product | Per project |
| Anti-drift rules | Kill / Scale / Productize calls | CEO | Weekly |

## Metrics
- **Decision Throughput** — number of binding decisions per week derived from
  the layer (target: >=5/week).
- **Decision Reversal Rate** — share of decisions reversed within 30 days
  (target: <15%).
- **Event Coverage** — share of meaningful Core OS actions emitting a
  registered event (target: >=95%).
- **Ledger Completeness** — share of decisions traceable to at least one
  ledger entry (target: 100%).
- **Strategic Memory Capture Rate** — share of closed projects with a full
  lessons capture (target: 100%).

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic mandate the layer fulfils
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — governing principles for all layers
- `docs/EXECUTIVE_DECISION_PACK.md` — weekly artefact this layer produces
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — KPI surface fed by the Metric Layer
- `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` — autonomous revenue posture this layer governs
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
