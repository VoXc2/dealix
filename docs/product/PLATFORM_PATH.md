# Platform Path — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PLATFORM_PATH_AR.md](./PLATFORM_PATH_AR.md)

## Context
The Platform Path is the long-arc plan to convert delivery code into
client-facing software. It is intentionally slow. Too many services
firms attempt a SaaS pivot too early and burn the company. This file
declares the five stages, the gating conditions, and the architectural
constraints that govern progress. It inherits engineering ambition
from `docs/BEAST_LEVEL_ARCHITECTURE.md`, reliability discipline from
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`, and AI-stack decisions
from `docs/AI_STACK_DECISIONS.md`.

## The five platform stages

| Stage | Definition |
|---|---|
| 1 | Internal tools — used by Dealix only to deliver sprints. |
| 2 | Client-visible reports — outputs exposed to the client, not interactive. |
| 3 | Client workspace — clients interact with data, reports, approvals. |
| 4 | Self-serve modules — modules clients run with guardrails. |
| 5 | SaaS subscription workspace — full self-serve with usage-based modules. |

Each stage is a different software product with different
expectations, support models, and risk profiles. They are not
incremental UI tweaks.

## Promotion conditions

Do not advance from one stage to the next until **all** of the
following are true at the current stage:

- **Workflow repeats** — the same operation runs the same way across
  three or more clients.
- **Client understands the value** — clients can describe the value
  without being prompted.
- **Support doesn't kill you** — projected support load fits inside
  the operating capacity defined in
  `docs/company/DELIVERY_CAPACITY_MODEL.md`.
- **Governance is strong** — the controls in
  `docs/DEALIX_OPERATING_CONSTITUTION.md` are demonstrably in place.

The conditions are conjunctive. Missing one means staying at the
current stage.

## Stage-specific notes

- **Stage 1** Code is allowed to be brittle. The point is to learn
  what repeats.
- **Stage 2** Reports are immutable for the client; mutation happens
  internally.
- **Stage 3** A workspace is a deeply contracted product. Treat
  every screen as a commitment.
- **Stage 4** Guardrails are explicit: rate limits, approval gates,
  abuse handling, observability.
- **Stage 5** Pricing model becomes usage-aware; legal, billing, and
  trust posture move to full SaaS standards.

## What the platform is not

- It is not the way to "scale faster" out of a services bottleneck.
  Capacity is solved in
  `docs/company/DELIVERY_CAPACITY_MODEL.md`, not in code.
- It is not a marketing differentiator. Platform exists when usage
  justifies it, not because the deck looks better.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Delivery scripts | Internal tooling backlog | Founder | Per service |
| Reuse stats | Stage promotion candidates | Founder | Quarterly |
| Engineering capacity | Stage roadmap | Founder | Quarterly |
| Governance audit | Stage 4 / 5 readiness | Founder | Quarterly |

## Metrics
- Workflow-repeat rate — share of delivery workflows running the same way across ≥ 3 clients; target ≥ 50% before any Stage-3 push.
- Support-load forecast — projected hours of platform support; capped at 20% of founder capacity pre-launch.
- Governance coverage — controls in place at the target stage; target 100%.
- Stage advancement events — promotions per year; target ≤ 1 per year while founder-led.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — engineering ambition the path serves.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability discipline required for Stage 3+.
- `docs/AI_STACK_DECISIONS.md` — AI stack the platform composes against.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital model the platform compounds.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
