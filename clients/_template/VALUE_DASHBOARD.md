# Value Dashboard — <CLIENT_NAME>

**Layer:** Client Template · Operational Kit
**Owner:** CSM Lead — <OWNER_NAME>
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [VALUE_DASHBOARD_AR.md](./VALUE_DASHBOARD_AR.md)

## Context
Dealix sells **measured business value**, not features. The value
dashboard is the per-client instance of
`docs/company/VALUE_REALIZATION_SYSTEM.md` and the row source for
`docs/ledgers/VALUE_LEDGER.md`. It standardizes how value is named,
evidenced, and shown to `<CLIENT_NAME>` every month, so renewals,
expansions, and references all run from the same numbers. Without
it, retainers slip into "feature theater" — exactly what
`docs/DEALIX_OPERATING_CONSTITUTION.md` forbids.

## Header
- **Client:** `<CLIENT_NAME>` · `<SECTOR>` · `<CITY>`
- **Reporting period:** `<YYYY-MM>`
- **CSM:** `<OWNER_NAME>`
- **Linked proof pack:** `<path to proof pack>`
- **Currency / unit:** SAR (anonymized to bands in public repo)

## 1. Revenue Value
| Metric | Baseline | Current | Delta | Evidence |
|---|---|---|---|---|
| Qualified pipeline (count) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Won deals (count) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Avg deal size band | `<band>` | `<band>` | `<+/-%>` | `<link>` |
| Sales cycle (days) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Net new MRR band | `<band>` | `<band>` | `<+/-%>` | `<link>` |

## 2. Time Value
| Metric | Baseline | Current | Delta | Evidence |
|---|---|---|---|---|
| Hours saved / week (team) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Lead-to-first-touch (min) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Ticket resolution (hrs) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Report turnaround (hrs) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Onboarding (days) | `<n>` | `<n>` | `<+/-%>` | `<link>` |

## 3. Quality Value
| Metric | Baseline | Current | Delta | Evidence |
|---|---|---|---|---|
| AI eval pass rate | `<%>` | `<%>` | `<+/-pp>` | `<link>` |
| HITL override rate | `<%>` | `<%>` | `<+/-pp>` | `<link>` |
| CSAT (post-interaction) | `<n/5>` | `<n/5>` | `<+/->` | `<link>` |
| Defect / re-work rate | `<%>` | `<%>` | `<+/-pp>` | `<link>` |
| Data accuracy | `<%>` | `<%>` | `<+/-pp>` | `<link>` |

## 4. Risk Value
| Metric | Baseline | Current | Delta | Evidence |
|---|---|---|---|---|
| Incidents / month | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Mean time to mitigate (min) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| PDPL findings open | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Audit exceptions | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Critical workflow uptime | `<%>` | `<%>` | `<+/-pp>` | `<link>` |

## 5. Knowledge Value
| Metric | Baseline | Current | Delta | Evidence |
|---|---|---|---|---|
| SOPs codified | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Internal questions answered by AI | `<%>` | `<%>` | `<+/-pp>` | `<link>` |
| Time-to-onboard new staff (days) | `<n>` | `<n>` | `<+/-%>` | `<link>` |
| Knowledge coverage of workflows | `<%>` | `<%>` | `<+/-pp>` | `<link>` |
| Re-asked questions rate | `<%>` | `<%>` | `<+/-pp>` | `<link>` |

## Monthly summary
**Top 3 value moves this month:**
1. `<one-line statement + evidence link>`
2. `<one-line statement + evidence link>`
3. `<one-line statement + evidence link>`

**Net value index (CSM-scored, 0–100):** `<n>`
*Composed of weighted % moves across the five sections; see
`docs/company/VALUE_REALIZATION_SYSTEM.md` for the weighting model.*

**Decisions to surface next month:**
- `<decision>`
- `<decision>`

## Evidence rules
- Every row needs a link. No link → row is reported as **claim**, not
  value, and excluded from `VALUE_LEDGER.md`.
- Baseline is locked at engagement start and recorded in the proof pack.
- A delta is only valid if measured for at least 2 consecutive
  reporting periods (single-month spikes are flagged but not booked).
- Anonymize SAR figures into bands for the public repo
  (`< 50K, 50–250K, 250K–1M, 1–5M, > 5M`).

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sprint outputs, evals, ops metrics | Rows in the 5 tables | Delivery Lead | Weekly population |
| CSAT, surveys, audits | Quality + risk rows | CSM Lead | Monthly |
| `docs/ledgers/VALUE_LEDGER.md` | New value-ledger row | CSM Lead | Monthly |
| Monthly retainer review | Decisions surfaced | Account Director | Monthly |

## Metrics
- **Evidence coverage** — % of rows with valid evidence link
  (target ≥ 95%).
- **Value continuity** — % of metrics tracked for ≥ 2 periods.
- **Value index trend** — month-over-month change in net value index.
- **Time to evidence** — days from value claim to evidence linked
  (target ≤ 5).

## How to fill this
1. Lock baselines at engagement start with the client owner.
2. Update the tables weekly during weekly review; freeze monthly
   snapshot on the last working day.
3. Always link the source artefact, not a summary.
4. Roll the snapshot into `VALUE_LEDGER.md` within 48 hours of
   month-end.

## Related
- `docs/company/VALUE_REALIZATION_SYSTEM.md` — wider value system
- `docs/ledgers/VALUE_LEDGER.md` — cross-client ledger
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — KPI dashboard spec
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
