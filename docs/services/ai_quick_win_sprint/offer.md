# Offer — AI Quick Win Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Operations Capability Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [offer_AR.md](./offer_AR.md)

## Context
This file defines the public-facing promise of the **AI Quick Win Sprint**. It is the second entry-tier service on the Dealix ladder, designed to convert "where do we even start with AI" interest into a single, named workflow win in 7 days. It plugs into the strategic monetization plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the productization ledger in `docs/product/PRODUCTIZATION_LEDGER.md`. Every promise here is checked against the quality regime in `docs/quality/QUALITY_STANDARD_V1.md`.

## Promise
> Pick **one** weekly workflow, save your team **hours**, and prove it in **7 business days** — with a documented SOP and a signed proof pack.

The Sprint replaces the "we tried ChatGPT" lurch with a focused, owner-led, human-reviewed automation that the team can actually use the day after delivery.

## The Problem We Solve
- Teams know AI should save them time but cannot point at one process AI fixed for them.
- "AI projects" balloon into multi-month initiatives that don't ship.
- No one owns the workflow after the experiment.
- There's no proof to show the executive sponsor.

The Sprint compresses this to one workflow, one owner, seven days, one proof pack.

## Deliverables
1. **Workflow map** — current state of the chosen workflow with steps, owners, and time per step.
2. **AI-assisted process design** — the new flow with the AI step clearly bounded.
3. **Human approval point** — the gate where a named person reviews before the action completes.
4. **Standard Operating Procedure (SOP)** — bilingual instructions the team can follow on Day 8.
5. **Time-saved estimate** — measured against baseline, with assumptions stated.
6. **Proof report** — executive-ready narrative + numbers, signed off by the workflow owner.
7. **Proof pack** — events log, screenshots, anonymization rules.

All deliverables are produced under `QUALITY_STANDARD_V1` and shipped with a `PROOF_PACK_TEMPLATE` instance.

## What's NOT Included
- **Full system integration** with ERPs, CRMs, or accounting systems unless explicitly scoped.
- **Cross-team rollout.** This sprint hardens ONE workflow for ONE team. Multi-team work is the Workflow Automation Sprint or Pilot.
- **High-risk automations** — anything that auto-sends money, signs contracts, or contacts clients without human approval is excluded by policy.
- **Replacement of staff.** The Sprint augments humans; it does not eliminate them.
- **Custom model training.** The Sprint uses Dealix's approved stack (`docs/AI_STACK_DECISIONS.md`).
- **Ongoing operation after Day 7.** Continuation is the Monthly AI Ops retainer.
- **Public chatbot or external-facing AI.** Internal workflows only.

## Buyer Profile
- B2B operations lead, founder, or department head in KSA/GCC.
- A named workflow that runs at least weekly and currently consumes ≥ 1 hour per cycle.
- A named owner willing to spend 1 hour/day during the sprint.
- Tolerance for human-in-the-loop AI (not full automation).

## Why It Sells
- **7 days.** Shorter than the time most teams spend planning an AI project.
- **One owner.** Avoids the "no one's on the hook" failure mode.
- **Proof-backed.** Time saved is measured, not asserted.
- **Bridge to retainer.** Every Sprint cleanly upsells into Monthly AI Ops or Workflow Automation Sprint.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Workflow nomination | Workflow choice signed off | Sponsor + Dealix DL | Day 1 |
| Current process docs | Workflow map | Workflow Owner + Analyst | Day 2 |
| Sample inputs/outputs | AI step design | Dealix Designer | Day 3 |
| Owner feedback | Built draft | Dealix Designer + Owner | Days 4–5 |
| Test results | SOP + proof | Owner + QA | Days 6–7 |

## Metrics
- **Sprint completion rate** — `% sprints delivered on or before Day 7`. Target ≥ 95%.
- **Owner adoption** — `% sprints where owner uses the SOP within 7 days of delivery`. Target ≥ 80%.
- **Hours saved per cycle** — `mean hours saved per workflow cycle`. Target ≥ 1.5h.
- **Upsell rate** — `% sprints converted to a paid follow-on within 60 days`. Target ≥ 35%.
- **Proof pack completeness** — `% sprints with signed proof pack`. Target = 100%.

## Related
- `docs/capabilities/operations_capability.md` — capability blueprint behind this service
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map placement
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md` — runtime design used by the Sprint
- `docs/product/PRODUCTIZATION_LEDGER.md` — productization tracking
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/AI_STACK_DECISIONS.md` — approved AI stack
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
