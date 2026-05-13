# Handoff Process — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [HANDOFF_PROCESS_AR.md](./HANDOFF_PROCESS_AR.md)

## Context
The end-of-sprint handoff is where Dealix converts delivered work into
proof, retainer, capital, and the next conversation. This file defines
the standard handoff package and the meeting structure. It depends on
the Delivery Standard (`docs/delivery/DELIVERY_STANDARD.md`), the
Customer Success Playbook (`docs/CUSTOMER_SUCCESS_PLAYBOOK.md`), and
the Operating Equation (`docs/company/OPERATING_EQUATION.md`). No
project closes without a completed handoff.

## Handoff Package
The handoff package is delivered as a single bundle.

1. **Proof pack** — `executive_report.md` filled with hero metric,
   before/after, top risks, next 3 actions; sources tied to audit
   events.
2. **Retainer recommendation** — a one-page recommendation aligned
   with `docs/templates/renewal_proposal.md` and the
   `docs/COMPANY_SERVICE_LADDER.md` next step.
3. **Capital ledger entry** — reusable assets registered in
   `docs/company/IP_REGISTRY.md` with owner and reuse instructions.
4. **Sign-off** — signed delivery note acknowledging acceptance of
   the scope outcomes.
5. **Next-step CTA** — a single named action with owner and date
   (renewal call, expansion scope, productization candidate).

## Handoff Meeting
- **Duration** — 45-60 minutes.
- **Attendees** — Dealix delivery lead, AI platform lead; client
  sponsor, business owner, technical contact.
- **Agenda**:
  1. Walk the hero metric and the before/after.
  2. Walk the top risks and mitigations.
  3. Walk the next 3 actions and assign owners.
  4. Present the retainer recommendation.
  5. Capture sign-off.

## Sign-Off
- Sign-off is captured as a digital acknowledgment with timestamp.
- The acknowledgment includes the hero metric figure and the source
  `AuditEvent` IDs.
- The sign-off triggers final invoice generation.

## Capital Ledger Entry
Every project must produce at least one reusable asset. Examples:
- Reusable prompt or prompt template.
- Schema or data extractor.
- QA checklist refinement.
- Playbook update.
- Reusable governance rule.

The asset record carries:
- asset ID and title
- owner and reuse instructions
- linked AIRun or AuditEvent IDs
- estimated reuse value

## Next-Step CTA
The CTA must be one of:
- **Renewal** — extend the same service for a defined period.
- **Expansion** — add a new capability (e.g., Brain after Revenue).
- **Productization** — promote a recurring pattern to a productized
  feature.
- **Closure** — explicit closure with reasons; rare and audited.

## Failure Modes
- **No proof tied to audit events** — block handoff; revise proof
  pack.
- **No reusable asset registered** — generate a defect ticket; close
  within 7 days.
- **No CTA** — escalate to founder.
- **Sign-off declined** — open dispute resolution; revise scope or
  proof.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Delivered work | Proof pack | Delivery lead | Per project |
| Audit events | Hero metric trace | Delivery lead | Per project |
| Service ladder | Retainer recommendation | Revenue | Per project |
| Sign-off | Final invoice trigger | Finance | Per project |

## Metrics
- **Handoff completion rate** — share of projects with a full
  handoff package. Target: 100%.
- **Sign-off latency** — days from final delivery to sign-off.
  Target: ≤ 5 days.
- **Renewal CTA conversion** — share of CTAs producing a signed
  renewal within 30 days. Target: ≥ 50%.
- **Capital yield per project** — Target: ≥ 1 reusable asset.

## Related
- `docs/delivery/DELIVERY_STANDARD.md` — sibling delivery standard.
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — customer success motion.
- `docs/V14_FOUNDER_DAILY_OPS.md` — founder daily ops.
- `docs/business/MANAGED_PILOT_OFFER.md` — productized pilot offer.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
