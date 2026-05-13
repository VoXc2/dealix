# Ten Gates — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [TEN_GATES_AR.md](./TEN_GATES_AR.md)

## Context
Building a holding company in stages is risky if you treat it as one linear ramp. Dealix breaks the path into **ten readiness gates**. Each gate is a discrete capability the holding must own before it can confidently expand to the next. The Ten Gates are the checklist behind `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the staging logic for `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`. They drive the **Strategic readiness** row of the [`HOLDING_SCORECARD`](./HOLDING_SCORECARD.md).

## The ten gates

| # | Gate | Question it answers | Exit criteria |
|---|---|---|---|
| 1 | Clear Category | Can we name our category in one phrase? | Public definition published; 3 customers can repeat it back |
| 2 | Sellable Wedge | Is there a small, fast, sellable first offer? | 3 paying customers for the wedge; ≥ 70% gross margin |
| 3 | Repeatable Delivery | Can we ship the wedge consistently? | 3 sprints delivered at QA ≥ 85 with same SOP |
| 4 | Proof Engine | Can we prove ROI on demand? | Proof Pack standard adopted; 3 packs in Proof Ledger |
| 5 | Retainer Conversion | Do sprints convert to retainers? | Sprint→Retainer ≥ 25% over 8 sprints |
| 6 | Productization | Are repeated steps in Core OS? | ≥ 3 productized features shipped from delivery learnings |
| 7 | Governance Trust | Are we PDPL-aware and audit-clean? | DPA, retention policy, audit log live; 0 critical incidents 90 days |
| 8 | Unit Economics | Do we make money per project + per retainer? | Blended GM 65–75%; CAC payback < 6 months |
| 9 | Partner Channel | Can other companies sell our method? | ≥ 3 active partners with paid deal flow |
| 10 | Platform Pull | Do clients want self-serve access? | ≥ 5 enterprise leads asking for platform access |

## Sequence rules

- Gates 1–3 are **founder-must-do**: cannot be delegated.
- Gates 4–6 are **delivery-team-do** with founder oversight.
- Gates 7–8 are **finance + governance**, gating Series A readiness.
- Gates 9–10 are **growth-engine** and **platform**, gating scale-out.
- A gate cannot be claimed closed unless the exit criteria are evidenced in `docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md`.

## Anti-pattern: scaling past an open gate
Scaling past an open gate is the single most expensive mistake a holding can make. Examples and their cost:

| Skip | Likely failure |
|---|---|
| Skip Gate 4 (Proof) | High churn, no referrals, low retainer conversion |
| Skip Gate 6 (Productize) | Margins capped at agency level; burnout |
| Skip Gate 7 (Governance) | Enterprise loss-of-trust event; PDPL fines |
| Skip Gate 8 (Unit Economics) | Profitable on paper, unprofitable at scale |
| Skip Gate 9 (Partner) | Distribution constrained by founder bandwidth |

The Strategic Control Tower is responsible for **stopping work on the next gate** when an upstream gate regresses to red.

## Current state snapshot template
The Ten Gates dashboard reports each gate as `red | amber | green` with date of last status change and evidence link. Example:

```
1.  Clear Category     ✅ green   2026-04-22  → docs/strategic/DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md
2.  Sellable Wedge     ✅ green   2026-04-29  → docs/PROOF_PACK_V6_STANDARD.md
3.  Repeatable Deliv.  🟡 amber   2026-05-06  → QA logs sprint #6–#8
4.  Proof Engine       ✅ green   2026-05-09  → Proof Ledger entries 001–003
5.  Retainer Conv.     🟡 amber   2026-05-10  → 18% conversion; needs CSM hire
6.  Productization     🔴 red     2026-05-11  → 0 features productized this month
7.  Governance Trust   ✅ green   2026-05-12  → Audit log + DPA live
8.  Unit Economics     🟡 amber   2026-05-12  → GM 62%
9.  Partner Channel    🔴 red     2026-05-12  → 0 active partners
10. Platform Pull      🔴 red     2026-05-12  → 1 inbound enterprise lead
```

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Evidence ledger entries | Gate status updates | Chief of Staff | Weekly |
| Gate regressions | Sell/build/stop/hire decisions | CEO | Weekly |
| Open-gate roadmap | Quarterly plan updates | CEO + BU GMs | Quarterly |
| Closed gates | Public proof / case study material | Brand | Per close |

## Metrics
- **Gates closed** — count of gates in green.
- **Time-in-state** — average days each gate has spent in its current state.
- **Gate regressions** — number of gates returning from green to amber/red.
- **Evidence freshness** — max age of evidence supporting a closed gate.
- **Stage alignment** — % of group hiring & spend aligned to the next open gate.

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic anchor.
- `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` — 90-day execution layer.
- `docs/company/NEXT_90_DAYS_EXECUTION_PLAN.md` — next-90-days plan.
- `docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md` — evidence backing each gate.
- `docs/strategic/DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md` — category gate input.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
