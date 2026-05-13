# AI Ops Diagnostic — Offer — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder / Diagnostic Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [offer_AR.md](./offer_AR.md)

## Context
The AI Ops Diagnostic is Dealix's paid entry point: a short, expert
engagement that tells the client which capability to raise first, with
which service, and at what risk. It exists because most Saudi mid-market
companies cannot tell us whether they need data work, governance, or a
revenue sprint — and a wrong first project burns trust. The diagnostic
plugs into the capability model defined in
`docs/company/CAPABILITY_OPERATING_MODEL.md` and is the qualification
gate referenced by `docs/DEALIX_OPERATING_CONSTITUTION.md` and the
Layer-3 service ladder in `docs/COMPANY_SERVICE_LADDER.md`.

## Promise
Identify the highest-value, lowest-risk AI operating opportunities in
your company. Walk out with a 30-day roadmap, a recommended first
Sprint, and a clear picture of what to do — and what not to do — first.

## Deliverables
- **Capability Assessment** of all seven capabilities (see
  `CAPABILITY_ASSESSMENT.md`).
- **Data Readiness Review** at headline level (full assessment available
  via the Data Readiness Assessment service).
- **Process Readiness Review** — owners, SLAs, exception paths.
- **Governance Risk Map** — PII, approvals, external-action exposure.
- **Top 5 Use Cases** — ranked by Diagnostic Score.
- **Recommended First Sprint** with cost and timeline.
- **30-Day Roadmap** for the next two Sprints after this one.

## Diagnostic Score
Each candidate use case is scored on seven dimensions:

| Dimension | What we measure |
|---|---|
| Business value | Revenue, cost, risk impact in SAR. |
| Data readiness | Are inputs accessible, complete, labelled? |
| Process clarity | Is the workflow documented with an owner? |
| Owner readiness | Is there a human who will adopt the output? |
| Governance risk | PII, claims, external action surface. |
| Implementation complexity | Integrations, edge cases, exceptions. |
| Time-to-value | Weeks until measurable benefit. |

Scores feed a 100-point composite that ranks use cases for the client.

## Decision Rule
- **High value + low risk** → recommended first Sprint.
- **High value + high risk** → readiness work first (Data Readiness
  Assessment or Governance Review) before any Sprint.
- **Low value + high complexity** → do not start; record as a future
  candidate.
- **Tie** → choose the option that raises the capability the client
  sells from (usually Revenue or Customer).

## Engagement Shape
- **Duration:** 5 working days, with a 60-minute kickoff and a 90-minute
  readout.
- **Format:** 3 interviews (sales, ops, IT), 1 data sample review, 1
  process walkthrough.
- **Team:** 1 Diagnostic Lead + 1 analyst.
- **Outputs:** PDF report, capability scorecard, Sprint proposal,
  optional governance memo.

## Pricing & Commercials
Pricing follows `docs/OFFER_LADDER_AND_PRICING.md`. The Diagnostic is
sold as a fixed-fee service. If the client buys the recommended Sprint
within 30 days, the Diagnostic fee is credited against the Sprint.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client interviews, data samples, process docs | Capability Assessment, Diagnostic Score, Sprint proposal | Diagnostic Lead | Per engagement |
| Diagnostic results | Sprint scope, governance memo, readiness recommendation | Founder, Delivery Lead | Per engagement |
| Won Sprints | Diagnostic-to-Sprint conversion data | Founder | Monthly |

## Metrics
- **Diagnostic-to-Sprint Conversion** — share of diagnostics that buy
  the recommended first Sprint within 30 days (target ≥ 60%).
- **Sprint Success Rate from Diagnostic** — share of Sprints sourced
  from a diagnostic that hit their capability uplift (target ≥ 80%).
- **Time-to-Roadmap** — calendar days from kickoff to delivered roadmap
  (target ≤ 7 days).
- **Net Promoter (Diagnostic)** — client NPS of the diagnostic itself
  (target ≥ 50).

## Related
- `docs/OFFER_LADDER_AND_PRICING.md` — where the Diagnostic sits in the
  offer ladder.
- `docs/business/MANAGED_PILOT_OFFER.md` — the larger Pilot the
  Diagnostic often leads into.
- `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` — how Diagnostics feed the
  90-day revenue plan.
- `docs/services/ai_ops_diagnostic/CAPABILITY_ASSESSMENT.md` — sibling
  capability scorecard.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
