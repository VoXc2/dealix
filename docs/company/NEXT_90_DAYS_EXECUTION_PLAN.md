# Next 90 Days Execution Plan — Master · Operating Blueprint

**Layer:** Master · Operating Blueprint
**Owner:** CEO (Sami)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [NEXT_90_DAYS_EXECUTION_PLAN_AR.md](./NEXT_90_DAYS_EXECUTION_PLAN_AR.md)

## Context
This plan turns the Dealix Master Operating Blueprint into a 90-day
operational program. It is the canonical answer to the question
"what are we actually doing this quarter?". It supersedes ad-hoc
planning notes and aligns with `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`,
`docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`, and the founder's daily rhythm
in `docs/V14_FOUNDER_DAILY_OPS.md`. Every milestone in this plan must
map to a Proof Pack (`docs/templates/PROOF_PACK_TEMPLATE.md`) and pass
the Quality Standard (`docs/quality/QUALITY_STANDARD_V1.md`).

## Phase 1 — Sellable Spine (Days 1–14)

### Documents to land
- POSITIONING (one-pager)
- SERVICE_CATALOG (3 sprint offers)
- DELIVERY_STANDARD
- QUALITY_STANDARD_V1
- GOVERNANCE_STANDARD
- PROOF_PACK_TEMPLATE

### Code spine
Verify each module against the existing `auto_client_acquisition/`
tree before adding anything new. This is a documentation reference
only; do not commit code as part of this plan.

- `data_os.import_preview` — accept a CSV/XLSX upload, surface row counts and column types.
- `data_os.data_quality_score` — produce a numeric 0–100 readiness score with reasons.
- `governance_os.policy_check` — block disallowed actions before they execute.
- `revenue_os.account_scoring` — rank accounts using deterministic + LLM signals.
- `reporting_os.proof_pack` — assemble the Proof Pack from logged proof events.

### Phase-1 gate
- All five core spine modules tested on a synthetic dataset.
- No PII in logs (validated by `governance_os.policy_check`).
- QA average ≥ 85 on the synthetic dataset using
  `docs/quality/QUALITY_STANDARD_V1.md` scoring.

## Phase 2 — First Sales (Days 15–30)

- 3 discovery calls per week with qualified Saudi-market accounts.
- 3 paid sprints booked (mix: Lead Intelligence, AI Quick Win, Revenue
  Diagnostic).
- 1 Proof Pack delivered, anonymized per
  `docs/templates/PROOF_PACK_TEMPLATE.md`, and filed.
- 1 vertical playbook drafted — start with B2B services
  (consulting / agencies / professional services).
- Sales motion run from `docs/ops/DAILY_OPERATING_LOOP.md`.

## Phase 3 — Productize (Days 31–60)

- Client Workspace v1 (read-only client portal for deliverables and Proof
  Packs).
- Report Generator (turns raw module output into branded PDF).
- Outreach Template Library (Arabic + English, source-cited).
- QA Scoring engine (machine-graded, human-reviewable).
- Capital Ledger UI (visible to founder; tracks reusable assets).
- Proof Ledger UI (timeline of proof events per client).

## Phase 4 — Retainers (Days 61–90)

- Monthly reports auto-generated from `reporting_os`.
- Client Health Score in the Client Workspace.
- Capability Backlog per client (which capability is shipping next).
- Renewal Recommendations triggered 14 days before retainer end.
- Monthly Operating Cadence template adopted with first retainer.

## Weekly Rhythm

| Day | Focus | Output |
|---|---|---|
| Sunday | CEO Review | Decisions log, kill-list, double-down list |
| Monday | Sales + Market | New pipeline rows, 5 outreach drafts |
| Tuesday | Product Build | 1 shipped capability or prompt update |
| Wednesday | Delivery QA | All in-flight deliveries scored against v1 |
| Thursday | Learning + Assets | New playbook entry or capital ledger row |
| Friday | Buffer / Sales recovery | Close week with all dashboards green |
| Saturday | Rest / Strategic reading | No standing meetings |

### Weekly questions (asked every Sunday)
1. What did we **sell**?
2. What did we **deliver**?
3. What did we **learn**?
4. What did we **productize**?
5. What did we **prove**?
6. What did we **stop**?
7. What did we **double down on**?

## Definition of Done — 90-Day MVP

1. 3 sellable services with full 10-per-service support
   (`docs/company/SERVICE_READINESS_BOARD.md`).
2. Core spine running: `data_os` + `governance_os` + `revenue_os` +
   `reporting_os` + `delivery_os`.
3. Every AI output passes governance — no exceptions.
4. Every project produces a Proof Pack.
5. Every project logs at least one capital asset.
6. Internal revenue / delivery / quality dashboard live and reviewed
   weekly.
7. 3 paying customers (cash received, not just signed).
8. 1 retainer signed.
9. 0 PII incidents.
10. QA average ≥ 85 across all delivered work.
11. Same service delivered twice at the same quality (proof of
    repeatability).

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Service Readiness Board | List of services that can be sold this week | CEO | Weekly |
| Daily Operating Loop | New pipeline rows, follow-ups | CEO + CSM | Daily |
| Quality Standard v1 | Pass/fail per delivery | QA Lead | Per delivery |
| Proof Pack Template | Filed Proof Packs | Delivery Lead | Per delivery |
| `auto_client_acquisition/` code | Module health | Engineering | Continuous |

## Metrics
- **Paid sprints booked** — target: 3 by day 30, 6 by day 60, 9 by day 90.
- **Retainers signed** — target: 1 by day 90.
- **QA average score** — target: ≥ 85 every week from day 14.
- **PII incidents** — target: 0.
- **Time-to-first-value** (signed to first Proof Pack) — target: ≤ 14 days.
- **Repeatability** — same service delivered ≥ 2× by day 90.

## Related
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategy this plan executes.
- `docs/V14_FOUNDER_DAILY_OPS.md` — founder daily mechanics.
- `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` — prior 90-day plan; cross-check before changing scope.
- `docs/ops/DAILY_OPERATING_LOOP.md` — daily execution loop.
- `AGENTS.md` (repo root) — code module reference for the spine.
- `docs/company/SERVICE_READINESS_BOARD.md` — services this plan promises to make Ready.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
