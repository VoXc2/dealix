# Capability Backlog — <CLIENT_NAME>

**Layer:** Client Template · Operational Kit
**Owner:** CSM Lead — <OWNER_NAME>
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPABILITY_BACKLOG_AR.md](./CAPABILITY_BACKLOG_AR.md)

## Context
The backlog is the **prioritized list of capability gaps** for
`<CLIENT_NAME>` that have not yet been addressed by a sprint or
retainer. It is the bridge between the static `CAPABILITY_SCORECARD.md`
and the dynamic `CAPABILITY_ROADMAP.md`. Every item is sized, owned,
and tied to a Dealix offer so that nothing sits in "we should
probably look at that someday" — the failure mode
`docs/company/CAPABILITY_OPERATING_MODEL.md` was written to prevent.

## Header
- **Client:** `<CLIENT_NAME>` · `<SECTOR>` · `<CITY>`
- **Owner (Dealix):** `<OWNER_NAME>`
- **Owner (Client):** `<role>`
- **Last grooming:** `<YYYY-MM-DD>`
- **Next grooming:** end of `<sprint name>` retainer call

## Priority bands
- **P0 — Critical risk** (data, governance, security, customer-facing).
  Must be addressed in current sprint or escalated.
- **P1 — High value** (top three by composite score × value impact).
- **P2 — Standard** (next-six items, planned but not committed).
- **P3 — Watchlist** (parked, revisit at quarterly review).

## Backlog
| # | Priority | Capability | Current level | Target level | Gap description | Next action | Offer / sprint | Owner | Size | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | P0 | `<capability>` | `<0–5>` | `<0–5>` | `<concise 1–2 lines>` | `<task>` | `<offer>` | `<role>` | `<S/M/L>` | `<open / in sprint / done / parked>` |
| 2 | P0 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| 3 | P1 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| 4 | P1 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| 5 | P1 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| 6 | P2 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| 7 | P2 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |
| 8 | P3 | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` | `<>` |

Size = relative effort: S (≤ 1 sprint, ≤ 2 weeks), M (1 sprint, 4–6
weeks), L (multi-sprint).

## Grooming rules
- Backlog is groomed **weekly** during the weekly review; full
  reprioritization happens **monthly** at the retainer call.
- Every item must have:
  - a measurable target level move from `CAPABILITY_SCORECARD.md`,
  - an offer or sprint name from `docs/company/OFFER_ARCHITECTURE.md`,
  - a named owner on the client side.
- Items in P0 carry the same on-call response as a production
  incident under `docs/INCIDENT_RUNBOOK.md`.
- Items parked > 90 days are demoted to P3 and reviewed at the
  next QBR.

## Linking to the roadmap
When an item enters a sprint, mark it `in sprint` and reference the
sprint folder in `docs/services/<sprint>/`. After delivery, mark `done`
and record the level move in `CAPABILITY_SCORECARD.md` (with evidence
in `VALUE_DASHBOARD.md`). Closed items remain in the table for 90 days
for traceability, then move to `_archive/backlog_closed.md` in the
client's private workspace.

## Common item templates
- **"Reduce manual data reconciliation in CRM"** — Data 2 → 3, Quick
  Win Sprint, S.
- **"Stand up evals + observability for first AI workflow"** —
  Governance 1 → 3, AI Governance Program, M.
- **"Codify support SOPs"** — Knowledge 1 → 3, Company Brain Sprint, M.
- **"Reduce ticket response time"** — Customer 2 → 4, AI Support Desk
  Sprint, M.
- **"Lift qualified pipeline"** — Revenue 2 → 3, Lead Intelligence
  Sprint, M.

Use these only as starting points; never copy verbatim.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Scorecard, sprint outputs | New backlog items | CSM + capability owner | Weekly |
| Retainer call decisions | Reprioritization | CSM Lead | Monthly |
| Incident / audit findings | P0 items | Governance + CSM | As they arise |
| QBR | Demotion / archive | Account Director | Quarterly |

## Metrics
- **Backlog age** — median days an open item has been in the backlog.
- **P0 cycle time** — days from raised to closed for P0 items
  (target ≤ 14).
- **Throughput** — items closed per quarter.
- **Coverage** — % of P0+P1 items linked to a named offer.

## How to fill this
1. Seed the backlog from the first `CAPABILITY_SCORECARD.md` —
   every Level 0/1 row becomes at least one backlog item.
2. Keep items ≤ 2 lines in the gap description; longer items split.
3. Never use Severity 0 (incident) language for backlog — keep it
   distinct from `docs/INCIDENT_RUNBOOK.md`.
4. Update visibly on each weekly review; backlog without diffs over a
   month is a red flag.

## Related
- `docs/company/CAPABILITY_OPERATING_MODEL.md` — capability vocabulary
- `docs/company/CAPABILITY_FACTORY_MAP.md` — cross-client patterns
- `docs/company/OFFER_ARCHITECTURE.md` — Dealix offers and bundles
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
