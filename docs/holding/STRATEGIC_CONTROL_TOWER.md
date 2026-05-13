# Strategic Control Tower — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [STRATEGIC_CONTROL_TOWER_AR.md](./STRATEGIC_CONTROL_TOWER_AR.md)

## Context
The Strategic Control Tower is the **weekly operating cockpit** of the Dealix Group: one screen, two views (Board View and Per-Unit View), one weekly cadence, and a fixed decision vocabulary (sell / build / stop / raise / hire). It plugs `docs/V14_FOUNDER_DAILY_OPS.md` and `docs/ops/DAILY_OPERATING_LOOP.md` into a single recurring decision surface. It is the place where the [`HOLDING_SCORECARD.md`](./HOLDING_SCORECARD.md) signals turn into actions, and where the [`SUCCESS_ASSURANCE_SYSTEM.md`](./SUCCESS_ASSURANCE_SYSTEM.md) cascade is enforced.

## Two views

### Board View
Designed for CEO + Board. Shows holding-level dimensions only.

| Block | What it shows |
|---|---|
| Scorecard | The 10-row Holding Scorecard with red/green |
| Cash | Cash balance, runway months, burn |
| Pipeline | Group ARR pipeline by stage and source |
| Risk | Top 5 open risks (governance, delivery, key-person) |
| Decisions | Open decisions in flight, with owner and due date |
| Quarter goals | Status of 3–5 quarterly OKRs |

### Per-Unit View
Designed for BU GMs + Head of Services. Shows BU-level health.

| Block | What it shows |
|---|---|
| BU P&L | Revenue, contribution margin, headcount |
| BU pipeline | Stage funnel, win rate, time-to-close |
| Delivery | QA score, on-time delivery, refund rate |
| Proof | Proof packs shipped in last 30 days |
| Productization | New steps productized into Core OS |
| Capital | Capital assets created in last 30 days |
| Retention | Sprint→Retainer % for the BU |

## The fixed decision vocabulary

Every weekly review must end with explicit decisions from this set:

| Verb | When to use | Example |
|---|---|---|
| **Sell** | Demand outstrips capacity, margins strong | "Open Dealix Brain to two new pilots." |
| **Build** | Repeated work justifies productization | "Productize 'PDPL data review' into Governance Workspace." |
| **Stop** | A service / experiment is not earning its keep | "Stop the support pilot in financial services." |
| **Raise** | Capital raise or pricing increase | "Increase Revenue Sprint price 15%." |
| **Hire** | Capacity is the binding constraint | "Hire 2 CSMs for Brain BU." |

Decisions outside this vocabulary are out of scope for the Control Tower — they belong to project-level reviews.

## Weekly agenda (90 minutes)

| Min | Block | Owner |
|---|---|---|
| 0–10 | Scorecard read-out (greens, reds) | CFO |
| 10–25 | Per-BU 90-second updates | BU GMs |
| 25–40 | Open decisions: status | Decision owners |
| 40–60 | New decisions: discuss & resolve | CEO leads |
| 60–75 | Risk review | DPO / GC |
| 75–85 | Quarter goal tracking | CEO |
| 85–90 | Confirm decisions logged, next week's prep | Chief of Staff |

## Decision log
Every decision becomes a row in `docs/EXECUTIVE_DECISION_PACK.md` with: ID, verb, scope, owner, due date, success metric, status. Status moves through `proposed → approved → in-flight → done | reversed`.

## Anti-patterns
- Discussing operational tickets — those belong in BU stand-ups, not the Control Tower.
- Issuing decisions outside the 5-verb vocabulary — forces vagueness.
- No CFO data — every red row must be backed by a number, not a feeling.
- Decisions without owners or due dates — automatic reject by Chief of Staff.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Holding Scorecard | Reds and greens | CFO | Weekly |
| BU dashboards | Per-Unit View | BU GMs | Weekly |
| Risk register | Top 5 risks | DPO / GC | Weekly |
| Pipeline CRM | Group pipeline | Head of Sales | Weekly |
| Decision Pack | Decision log | CEO + Chief of Staff | Weekly |

## Metrics
- **Decisions per week** — count of sell/build/stop/raise/hire decisions issued.
- **Decision cycle time** — proposed → approved median.
- **Decision reversal rate** — % of decisions reversed within 60 days.
- **Red-to-decision lag** — days from scorecard red to first related decision.
- **Quarter goal attainment** — % of quarter OKRs delivered.

## Related
- `docs/V14_FOUNDER_DAILY_OPS.md` — founder daily operating rhythm.
- `docs/ops/DAILY_OPERATING_LOOP.md` — daily operating loop.
- `docs/EXECUTIVE_DECISION_PACK.md` — weekly decision packet.
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — feeder dashboard.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic anchor.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
