# Capital Allocation Score — Intelligence · Operating Brain

**Layer:** Intelligence · Operating Brain
**Owner:** CEO + CFO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPITAL_ALLOCATION_SCORE_AR.md](./CAPITAL_ALLOCATION_SCORE_AR.md)

## Context
The Capital Allocation Score is how Dealix decides where to invest finite
time and money across opportunities — service lines, internal builds,
partner programs, experiments. It produces a single number per opportunity
that maps to a decision band, plus a fixed allocation of total capital
across five buckets. This is how Dealix says no to attractive distractions
and yes to compounding bets. See
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`,
`docs/UNIT_ECONOMICS_AND_MARGIN.md`, and
`docs/OFFER_LADDER_AND_PRICING.md` for the upstream economics this score
governs.

## Priority Score formula
```
Priority Score =
  revenue_score * 0.25
+ repeatability_score * 0.20
+ proof_score * 0.20
+ productization_score * 0.15
+ strategic_moat_score * 0.10
+ risk_adjusted_score * 0.10
```

Each sub-score is on a 0-100 scale.

### Sub-score definitions
- **revenue_score** — projected 12-month gross margin contribution,
  normalised against the top current line.
- **repeatability_score** — share of the workflow that is templated or
  productized (drawn from Capital Ledger + Productization Ledger).
- **proof_score** — count and diversity of proof events per project
  (drawn from Proof Ledger).
- **productization_score** — module reuse rate plus internal tool usage
  (drawn from Productization Ledger).
- **strategic_moat_score** — defensibility — data, regulatory access,
  distribution, brand category position.
- **risk_adjusted_score** — `100 - delivery_risk - regulatory_risk -
  concentration_risk`, each on 0-30.

## Decision bands
| Score | Band | Default action |
|---|---|---|
| 85-100 | Invest / Scale | Capital allocated, owner named, scaled offer |
| 70-84 | Build carefully | Productize, pilot with 2-3 clients |
| 55-69 | Pilot only | Single paid pilot, no roadmap commitment |
| 40-54 | Hold | Maintain, do not invest new capital |
| <40 | Kill | Sunset, write lessons into Strategic Memory |

## Worked example A — Revenue Intelligence (Scale)
Inputs (0-100):
- revenue_score = 90 (proven 12-month pipeline, healthy margin)
- repeatability_score = 80 (workflow templated, account-scoring module)
- proof_score = 90 (multiple Revenue Value proofs per client)
- productization_score = 75 (Revenue OS module used by 4 projects)
- strategic_moat_score = 70 (data + B2B playbook, MENA category)
- risk_adjusted_score = 80 (low delivery & regulatory risk)

Calculation:
```
Priority Score =
   90 * 0.25  = 22.5
 + 80 * 0.20  = 16.0
 + 90 * 0.20  = 18.0
 + 75 * 0.15  = 11.25
 + 70 * 0.10  =  7.0
 + 80 * 0.10  =  8.0
 -----------------
            = 82.75 → round 83
```
Verdict: **Build carefully (top of band, on the edge of Scale)** — promote
to Scale once the next two retainers close (lifting revenue_score +
moat).

## Worked example B — Custom chatbot for one client (Kill)
Inputs:
- revenue_score = 30 (one-off, low margin)
- repeatability_score = 10 (bespoke flows)
- proof_score = 15 (no measurable client value beyond ticket deflection)
- productization_score = 5 (no reusable module)
- strategic_moat_score = 20 (no defensibility)
- risk_adjusted_score = 50 (delivery risk + concentration risk)

Calculation:
```
Priority Score =
   30 * 0.25  =  7.5
 + 10 * 0.20  =  2.0
 + 15 * 0.20  =  3.0
 +  5 * 0.15  =  0.75
 + 20 * 0.10  =  2.0
 + 50 * 0.10  =  5.0
 -----------------
            = 20.25 → round 20
```
Verdict: **Kill** — write lessons into `STRATEGIC_MEMORY.md` and refuse
similar future requests per `ANTI_AGENCY_RULES.md`.

## Capital buckets
Total capital — founder + team time + cash — is fixed-shared across five
buckets. The share is re-weighted monthly in the Capital Allocation
Review.

| Bucket | Target share | Purpose |
|---|---|---|
| Cash Engine | 40% | Today's revenue lines, paid pilots, retainers |
| Core OS | 25% | Platform, agents, ledgers, governance |
| Proof + Capital Assets | 15% | Proof packs, case studies, reusable assets |
| Growth + Partners | 10% | Marketing, partner program, BD |
| Labs + Experiments | 10% | New service lines under pilot or below 70 score |

Reallocation rules:
- Cash Engine never drops below 30%.
- Labs + Experiments never exceeds 15%.
- A new Scale-band opportunity may temporarily shift up to 5% from Labs
  into Cash Engine for one cycle.

## Scoring cadence
- Per opportunity at intake.
- Re-scored monthly for every opportunity in the active register.
- Re-scored within 7 days of a material event (proof event, retainer win,
  loss, governance incident).

## Governance
- Scoring is owned by the Chief of Staff with sign-off from CEO + CFO.
- All scores are stored in the Venture Signal Ledger with weights, inputs,
  and rationale.
- Disagreements escalate to the Executive Decision Pack
  (`docs/EXECUTIVE_DECISION_PACK.md`).

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Proof, Capital, Unit Performance ledgers | Per-opportunity Priority Score | Chief of Staff | Monthly + on event |
| Priority Scores | Decision band + action | CEO + CFO | Monthly |
| Decision band | Capital bucket reallocation | CEO + CFO | Monthly |
| Capital bucket plan | Hiring, spend, time commitments | Heads | Monthly |

## Metrics
- **Score Coverage** — share of active opportunities with a current
  Priority Score (target: 100%).
- **Score Stability** — share of scores moving >15 points within 30 days
  (target: <20%).
- **Kill Discipline** — share of <40 scored opportunities sunset within 30
  days (target: 100%).
- **Bucket Drift** — variance vs target share by month (target: <=3pp per
  bucket).

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan this score serves
- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — economics behind revenue_score
- `docs/OFFER_LADDER_AND_PRICING.md` — packaging that feeds repeatability_score
- `docs/EXECUTIVE_DECISION_PACK.md` — surface for monthly capital reviews
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
