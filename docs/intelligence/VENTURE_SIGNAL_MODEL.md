# Venture Signal Model — Intelligence · Operating Brain

**Layer:** Intelligence · Operating Brain
**Owner:** CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [VENTURE_SIGNAL_MODEL_AR.md](./VENTURE_SIGNAL_MODEL_AR.md)

## Context
The Venture Signal Model scores Dealix's service lines, modules, and
candidate business units for graduation. It answers the question that
defines whether Dealix becomes one stalled company or a holding that
produces ventures: **is this unit ready to stand on its own?** The score
combines paid-client traction, retainer depth, repeatability, product
maturity, playbook maturity, margin, and owner readiness into a single
number, then bands it into four outcomes. See
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` for the holding posture and
`docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` for the revenue OS that hosts
candidate ventures.

## Venture Readiness Score formula
```
Venture Score =
  paid_clients * 0.15
+ retainers * 0.20
+ repeatability * 0.20
+ product_module_usage * 0.15
+ playbook_maturity * 0.10
+ margin * 0.10
+ owner_readiness * 0.10
```

Each input is on a 0-100 scale, normalised as below.

### Input definitions
- **paid_clients** — count of distinct paid clients in the last 12 months,
  scaled: 0 clients = 0, 1 = 30, 3 = 60, 5 = 80, 10+ = 100.
- **retainers** — active monthly-recurring retainers, scaled: 0 = 0,
  1 = 40, 2 = 70, 3 = 85, 5+ = 100.
- **repeatability** — share of the workflow that is templated/productized
  (from Capital Ledger).
- **product_module_usage** — % of projects in the line using a shared
  module (from Productization Ledger).
- **playbook_maturity** — coverage of pitch, intake, delivery, proof,
  pricing, ICP playbooks, each weighted 1/6 (0-100).
- **margin** — unit gross margin %, capped at 100.
- **owner_readiness** — accountable owner exists, has authority, has P&L
  literacy: binary 0 or 100, multiplied by 1.0 / 0.5 / 0.0 for proof
  library state (mature / partial / none).

## Decision bands
| Score | Band | Default action |
|---|---|---|
| 85+ | Venture candidate | Open graduation review; named CEO, P&L, brand |
| 70-84 | Business unit | Run inside Dealix with dedicated owner and budget |
| 55-69 | Service line | Keep in current org, productize aggressively |
| <55 | Keep inside core services | No standalone treatment |

## Worked example A — Dealix Revenue (Venture candidate)
A line with:
- 6 paid clients in 12 months (paid_clients = 85)
- 2 active retainers (retainers = 70)
- repeatability = 80 (Revenue OS workflows templated)
- product_module_usage = 75 (Revenue OS module in 4/5 projects)
- playbook_maturity = 85 (B2B playbook mature across all 6 dimensions)
- margin = 65
- owner_readiness = 90 (owner exists, proof library mature)

Calculation:
```
Venture Score =
   85 * 0.15  = 12.75
 + 70 * 0.20  = 14.0
 + 80 * 0.20  = 16.0
 + 75 * 0.15  = 11.25
 + 85 * 0.10  =  8.5
 + 65 * 0.10  =  6.5
 + 90 * 0.10  =  9.0
 -----------------
            = 78.0
```
Verdict: **Business unit (top end)** — at 78 it is a strong business
unit. Crossing into Venture candidate (85+) requires lifting paid_clients
toward 10, retainers toward 3, and margin past 70. The source note in the
brief stipulates Dealix Revenue qualifies as venture when "5+ clients,
2+ retainers, Revenue OS module used, B2B playbook mature, margin healthy,
owner exists, proof library exists" — those qualifiers, when all green,
push the score above 85.

## Worked example B — Internal Eval Lab (Keep inside)
- 0 paid clients (paid_clients = 0)
- 0 retainers (retainers = 0)
- repeatability = 60 (some eval suites reusable)
- product_module_usage = 40 (used in 2 projects)
- playbook_maturity = 30 (eval playbook only)
- margin = 0 (internal cost centre)
- owner_readiness = 50 (owner exists, no proof library externally)

Calculation:
```
Venture Score =
    0 * 0.15  =  0.0
 +  0 * 0.20  =  0.0
 + 60 * 0.20  = 12.0
 + 40 * 0.15  =  6.0
 + 30 * 0.10  =  3.0
 +  0 * 0.10  =  0.0
 + 50 * 0.10  =  5.0
 -----------------
            = 26.0
```
Verdict: **Keep inside core services** — Eval Lab is infrastructure, not
a venture. It feeds `docs/EVALS_RUNBOOK.md` and the AI Run metrics, but
should never be packaged for spin-out.

## Graduation review (85+)
When a unit sustains a Venture Score of 85+ for 30 days:

1. CEO opens a graduation review.
2. CFO confirms unit margin, capital needs, and runway.
3. Head of Governance confirms PDPL and contractual readiness.
4. Head of Brand confirms naming, identity, and brand isolation.
5. Owner readiness is reconfirmed via a written governance plan.
6. Approval gates per `docs/governance/AUTONOMY_VALIDATION_GATES.md` and
   `AGENT_CONTROL_DOCTRINE.md` are re-evaluated for the new entity.

The output is either a graduation plan (entity, leadership, capital,
brand, governance) or a hold with explicit gaps and a 90-day re-evaluation
date.

## Scoring cadence
- Continuous accumulation via the Venture Signal Ledger.
- Monthly recomputation of all candidate units.
- Quarterly Venture Signal Review with the CEO.

## Anti-gaming rules
- Inputs cannot be self-attested. Each input must trace to ledger entries.
- Owner readiness is binary on owner existence; gaming via "shadow owner"
  is rejected at the graduation review.
- Margin uses fully-loaded unit cost, including allocated platform and
  governance overhead.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Venture Signal Ledger | Venture Readiness Score | Chief of Staff | Monthly |
| Score band | Graduation review or hold | CEO | Quarterly |
| Graduation review | Spin-out plan or 90d hold | CEO + CFO | Per review |
| Anti-gaming audit | Score corrections | Head of Governance | Quarterly |

## Metrics
- **Score Coverage** — share of candidate units with a current Venture
  Score (target: 100%).
- **Graduation Throughput** — number of units graduated per year
  (target: >=1).
- **False Promotion Rate** — share of graduated units returning to parent
  within 12 months (target: 0).
- **Audit Trace Rate** — share of score inputs traced to ledger entries
  (target: 100%).

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — holding posture context
- `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` — host for candidate ventures
- `docs/governance/AUTONOMY_VALIDATION_GATES.md` — gates for new entities
- `docs/EXECUTIVE_DECISION_PACK.md` — quarterly review surface
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
