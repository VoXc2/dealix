# Client Journey — Eight Steps, One CTA Each

**Layer:** L7 · Execution Engine
**Owner:** Founder / CSM
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CLIENT_JOURNEY_AR.md](./CLIENT_JOURNEY_AR.md)

## Context
This file defines the canonical eight-step Dealix client journey, with
exactly one call to action per stage. It removes the most common
revenue leak in services companies — multiple competing CTAs at the
same stage, which produce indecision. It plugs into the customer
success doctrine in `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` and the sales
materials in `docs/sales/DEMO_SCRIPT.md`. This is L7 execution because
journey discipline runs across every active loop.

## The Eight Steps

```
Awareness ─► Diagnostic ─► Sprint ─► Review ─► Pilot ─► Retainer ─► Expansion ─► Enterprise
```

Each step has a single CTA. The buyer never sees more than one option
in a stage. The job of the founder or CSM is to make that single CTA
obvious and easy to say yes to.

## Stage-by-Stage

### 1. Awareness
The buyer encounters Dealix through content, referral, or outbound.
- **CTA:** Book a Diagnostic.
- **Owner:** Founder.
- **Asset:** One-pager, demo video.

### 2. Diagnostic
A paid clarity engagement (SAR 3.5k - 7.5k). Buyer leaves with a
written diagnosis.
- **CTA:** Start a Sprint.
- **Owner:** Founder.
- **Asset:** Diagnosis report.

### 3. Sprint
A fixed-price 2-4 week first-proof engagement (SAR 7.5k - 25k).
- **CTA:** Start a Pilot.
- **Owner:** Founder.
- **Asset:** Proof pack, working artifact.

### 4. Review
Joint review of the sprint outcome. Not a sale stage — a clarity
checkpoint that decides whether the next CTA is offered.
- **CTA:** (none — readiness gate)
- **Owner:** Founder + buyer sponsor.
- **Asset:** Review summary.

### 5. Pilot
A 4-8 week operational validation inside the buyer's environment
(SAR 22k - 60k).
- **CTA:** Start a Monthly Retainer.
- **Owner:** Founder / CSM.
- **Asset:** Pilot report with operational metrics.

### 6. Retainer
Monthly continuity engagement (SAR 8k - 60k / month).
- **CTA:** Expand Capability.
- **Owner:** CSM.
- **Asset:** Monthly proof pack and value report.

### 7. Expansion
A second capability area opens (e.g., the original buyer was Grow
Revenue; we now propose Build Company Brain).
- **CTA:** Add capability (new sprint or new retainer line).
- **Owner:** CSM + Founder.
- **Asset:** Expansion brief.

### 8. Enterprise
Multi-capability, multi-quarter engagement (SAR 85k - 300k+).
- **CTA:** Renew at enterprise terms.
- **Owner:** Founder.
- **Asset:** Enterprise agreement, governance pack.

## The One-CTA Discipline

If a stage's CTA is rejected, the buyer does not regress to the
previous stage — they pause. The next CTA is the same CTA, offered
later, with new evidence. The buyer never sees a second CTA as a
fallback in the same conversation.

## Journey Asset Map

| Stage | Required artifact | Source |
|---|---|---|
| Awareness | One-pager | `docs/sales/ONE_PAGER.md` |
| Diagnostic | Diagnosis report | Sprint template |
| Sprint | Proof pack | `reporting_os.proof_pack` |
| Review | Review summary | Template |
| Pilot | Pilot report | `delivery_os` |
| Retainer | Monthly proof pack | `reporting_os` |
| Expansion | Expansion brief | Template |
| Enterprise | Governance pack | `governance_os` |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Buyer signal, current stage | Single CTA | Founder / CSM | Per touch |
| Stage outcome | Stage advance or pause | Founder / CSM | Per stage gate |
| Retainer maturity | Expansion brief | CSM | Quarterly |

## Metrics
- Stage conversion rate — % advancing at each gate.
- Time in stage — average days per stage.
- CTA acceptance — % accepting the single CTA on first offer.
- Pause-to-resume rate — % of paused buyers who resume the same CTA.

## Related
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CS playbook that runs in stages 5-8.
- `docs/sales/DEMO_SCRIPT.md` — demo used in Awareness and Diagnostic.
- `docs/business/MANAGED_PILOT_OFFER.md` — pilot stage offer design.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
