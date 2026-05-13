# Capital Ledger — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder / Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPITAL_LEDGER_AR.md](./CAPITAL_LEDGER_AR.md)

## Context
The Capital Ledger is the running book of every asset that any project
creates. It is the operational counterpart to
`docs/company/DEALIX_CAPITAL_MODEL.md`: the model defines the five
capitals; the ledger records each individual deposit. Without this
ledger the capital model is aspirational; with it, capital becomes
audit-grade and the company can prove asset compounding to itself,
partners, and the strategic narrative described in
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Schema

Every row of the ledger has the following columns:

| Column | Description |
|---|---|
| ID | Sequential `C-001`, `C-002`, … |
| Project | Source project (sprint, pilot, retainer) |
| Capital Type | Service / Product / Knowledge / Trust / Market |
| Asset Created | Short name of the artifact |
| Reusable? | Yes / No |
| Owner | Person accountable for keeping the asset alive |
| Next Use | The next planned engagement, deal, or deliverable |

## Seed entries

| ID | Project | Capital Type | Asset Created | Reusable? | Owner | Next Use |
|---|---|---|---|---|---|---|
| C-001 | Lead Sprint A | Trust | Anonymized proof pack | Yes | Sami | Sales deck |
| C-002 | Lead Sprint A | Product | Import preview script | Yes | Sami | All lead sprints |
| C-003 | Clinic Sprint | Knowledge | Clinics playbook update | Yes | Sami | Clinic outreach |

These rows are intentionally seeded so the ledger is never empty on day
one and the column conventions are demonstrated by example.

## Minimum-deposit rule

Every project must produce at minimum:

- **1 Trust Asset**, plus
- **1 Knowledge OR Product Asset**.

A project that closes without these two deposits is logged as
capital-debt and remediated in the next sprint window. The delivery
lead may not mark a project as Done until both deposits are recorded.

## Workflow

1. **At project kickoff** the founder pre-declares the expected capital
   deposits in the intake brief.
2. **During delivery** the delivery lead drafts the asset names in the
   ledger with status `pending`.
3. **At project closure** the entries are flipped to `confirmed`, the
   `Next Use` column is filled, and ownership is assigned.
4. **Quarterly** the founder reviews every `Next Use` value; assets
   that have not been reused within two quarters are flagged for
   graduation review (see
   `docs/assets/ASSET_GRADUATION_SYSTEM.md`).

## Storage and source of truth

The canonical ledger lives in the internal Notion workspace under
`Dealix Operations / Capital Ledger`. This Markdown file is the
public-facing schema and seed. Any tool change is allowed only if it
preserves the column set, the minimum-deposit rule, and the audit
trail required by
`docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Project intake brief | Pre-declared capital deposits | Founder | Per project |
| Delivery closure report | New ledger rows | Delivery lead | End of project |
| Reuse log | Updated `Next Use` values | Delivery lead | Per reuse |
| Quarterly review | Graduation candidates | Founder | Quarterly |

## Metrics
- Deposits-per-project — average rows added per closed project; target ≥ 2.
- Reuse rate — share of ledger rows reused within two quarters; target ≥ 60%.
- Trust-deposit share — share of new rows that are Trust assets; target ≥ 25%.
- Capital-debt closures — number of capital-debt projects remediated per quarter; target ≥ 90% of debt opened.

## Related
- `docs/FINANCE_DASHBOARD.md` — financial counterpart to the asset ledger.
- `docs/revenue/PRICING_AND_PACKAGING.md` — pricing that funds asset deposits.
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — KPI surface where capital metrics appear.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — model the ledger implements.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
