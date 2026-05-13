# Sales Pipeline v1 — Dealix Growth Layer

**Layer:** L6 · Growth Machine
**Owner:** Head of Growth / Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SALES_PIPELINE_V1_AR.md](./SALES_PIPELINE_V1_AR.md)

## Context
The Dealix sales pipeline must be opinionated, manual, and auditable
in v1. It removes the constraint of "random outreach with no recorded
state" by defining a fixed set of stages, required fields, and movement
rules. It anchors directly to the Growth Machine loop in
`docs/growth/GROWTH_MACHINE.md`, the offer ladder in
`docs/OFFER_LADDER_AND_PRICING.md`, and the strategic priorities in
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Stages

| # | Stage | Definition |
|---|---|---|
| 1 | Targeted | Account selected from ICP; matches B2B services profile. |
| 2 | Researched | Pain hypothesis written; public sources logged. |
| 3 | Contact Drafted | Manual outreach draft prepared, claim-checked. |
| 4 | Contacted Manually | First message sent by a human via authorized channel. |
| 5 | Discovery Booked | Call scheduled. |
| 6 | Diagnostic Proposed | Paid diagnostic offer sent. |
| 7 | Diagnostic Paid | Invoice paid; data intake started. |
| 8 | Sprint Proposed | Lead Intelligence / AI Quick Win Sprint scope sent. |
| 9 | Sprint Paid | Sprint kickoff confirmed. |
| 10 | Pilot Proposed | 30-day managed pilot proposal sent. |
| 11 | Retainer Won | Monthly retainer signed. |
| 12 | Lost / Nurture | Closed lost with reason or moved to nurture queue. |

## Required Fields per Lead

| Field | Description |
|---|---|
| `company_name` | Legal or trading name. |
| `sector` | B2B services / logistics / clinic / other. |
| `city` | Riyadh / Jeddah / Eastern Province / other. |
| `pain_hypothesis` | One-sentence pain we believe they have. |
| `offer_fit` | Which Dealix sprint fits best. |
| `source` | Where this lead came from. Required. |
| `relationship_status` | Cold / warm intro / referral / inbound. |
| `next_action` | Specific next step. Required. |
| `owner` | Single human owner. |
| `last_touch` | Date of last contact. |
| `compliance_status` | Lawful basis confirmed / pending / blocked. |

## Movement Rules

1. **No source = not ready.** Any lead missing `source` is parked.
2. **No `next_action` = not ready.** A lead without a next action is
   either lost or moved to Nurture, never left silent.
3. **Compliance gate.** A lead cannot move past Stage 4 (Contacted)
   unless `compliance_status = confirmed`.
4. **Manual + authorized + reviewed.** Any external outreach is
   manually drafted, sent by a human, and reviewed against the claim
   rules in `docs/sales/OBJECTION_HANDLER.md`.
5. **Two-week silence rule.** Any lead untouched for 14 days auto-flags
   to Lost or Nurture.

## First Sales Campaign — "B2B Revenue Cleanup"

**Message.** "We help B2B service companies turn scattered customer /
opportunity data into a ranked opportunity list, ready outreach drafts,
and a clear pipeline in 10 days — without spam or unsafe automation."

**Offer.** Lead Intelligence Sprint — SAR 9,500–18,000 — 10 days.

**Deliverables.** Data cleanup, duplicate/missing detection, top 50
opportunities ranked, top 10 immediate actions, outreach draft pack,
mini CRM board, proof report.

**Target list = 40 accounts only**:
- 20 B2B service companies
- 10 logistics / operations companies
- 10 clinics as secondary test

### Sales Week Plan

| Day | Action |
|---|---|
| 1 | Build target list (40 accounts). |
| 2 | Research pains; write hypotheses. |
| 3 | Prepare manual outreach drafts. |
| 4 | Contact manually (authorized channels). |
| 5 | Discovery calls. |
| 6 | Send diagnostic / sprint proposal. |
| 7 | Close first paid diagnostic or sprint. |

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| ICP target list | Stage-tagged leads | Growth | Weekly refresh |
| Discovery notes | Diagnostic / Sprint proposals | Founder / Growth | Per call |
| Sprint deliveries | Proof Packs feeding stage 10 | Delivery + CSM | Per delivery |
| Compliance reviews | Compliance status updates | Compliance Owner | Pre-Stage-4 |

## Metrics

- **Targeted → Discovery Booked** conversion %.
- **Discovery → Diagnostic Paid** conversion %.
- **Sprint → Pilot Proposed** conversion %.
- **Pilot → Retainer Won** conversion %.
- **Average days in stage** per stage.
- **Compliance hold rate** — % of leads blocked at compliance gate.

## Related

- `docs/sales/BATTLECARDS.md` — competitive positioning for stages 4–8.
- `docs/sales/DEMO_SCRIPT.md` — demo flow during Discovery.
- `docs/sales/OBJECTION_HANDLER.md` — objections used by reps in stages 5–10.
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — strategic revenue framing.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
