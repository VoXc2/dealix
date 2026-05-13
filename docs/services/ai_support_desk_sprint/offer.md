# Offer — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Customer Capability Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [offer_AR.md](./offer_AR.md)

## Context
This file defines the public-facing promise of the **AI Support Desk Sprint**. It exists because B2B and consumer-facing teams in KSA/GCC are drowning in WhatsApp threads, email inboxes, and DM volumes that grow faster than headcount. The Sprint plugs into the customer capability blueprint in `docs/capabilities/customer_capability.md`, the customer success playbook in `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`, and the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`. Every promise here is bounded by the human-in-the-loop rules in `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`.

## Promise
> Turn WhatsApp/inbox overload into **categorized, suggested-reply support** in **14 business days** — with explicit escalation rules for sensitive cases and a human in the loop on every outbound message.

The Sprint replaces the "we'll get back to you when we can" tax with a desk that knows what came in, what's urgent, what's been answered before, and what needs a human now.

## The Problem We Solve
- 200–2,000 messages per week land across WhatsApp, email, DMs.
- Categories don't exist; agents triage from scratch every time.
- Same questions get answered 5 different ways by 5 different agents.
- Sensitive cases (complaints, medical, financial) get the same SLA as a price question.
- No SLA tracker; nobody knows the response time.

The Sprint compresses this into a 14-day build of a categorized, suggested-reply, escalation-aware support layer.

## Deliverables
1. **Message categorization** — classification rubric covering ≥ 90% of the volume.
2. **Suggested reply library** — bilingual, brand-tone, version-tagged.
3. **FAQ builder** — top-N answered questions, source-cited where applicable.
4. **Escalation rules** — sensitive cases routed to humans with a watermark.
5. **SLA tracker** — first-response time, resolution time, by category.
6. **Support insights report** — top categories, response-time trends, sensitive-case rate.
7. **Proof report** — executive narrative + numbers.
8. **Proof pack** — events log, governance log, anonymization rules.

All deliverables under `QUALITY_STANDARD_V1` and shipped with a `PROOF_PACK_TEMPLATE` instance.

## What's NOT Included
- **Auto-sending replies.** This Sprint produces SUGGESTED replies; humans send.
- **Replacing humans.** The Sprint augments support agents; it does not eliminate them.
- **Public chatbot.** No customer-facing AI in the MVP.
- **Inbox provider migration** (we work with the client's existing WhatsApp Business / email / CRM).
- **Sentiment-based pricing changes** or any commercial decisions.
- **Health diagnosis or financial advice.** Sensitive cases are always escalated.
- **Long-term operation** beyond the Sprint. Continuation is **Monthly Support AI**.

## Buyer Profile
- B2B or B2C team in KSA/GCC with 200–2,000 inbound messages per week.
- WhatsApp Business + email + 1–2 DM channels.
- Existing agents (1–10) currently handling triage.
- Defined FAQ list, or willingness to define one.
- Tolerance for human-in-the-loop AI.

## Why It Sells
- **14 days visible.** Short enough to fit a board cycle.
- **No auto-send.** Eliminates the "AI sent something wrong to my customer" fear.
- **Bilingual.** Saudi/Gulf tone Arabic + business English.
- **Bridge to retainer.** Every Sprint cleanly upsells to Monthly Support AI or Feedback Intelligence.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Anonymized message sample | Classification rubric | Client Support Lead + Analyst | Days 1–3 |
| Current FAQ doc | Suggested reply library | Client + Dealix Copy Lead | Days 4–7 |
| Sensitive-case policy | Escalation rules | Client Sec/Legal + Dealix | Days 8–10 |
| Response-time targets | SLA tracker | Client Ops + Dealix | Days 11–12 |
| Reviewer feedback | Final deliverables | Client Reviewer + DL | Days 13–14 |

## Metrics
- **Sprint completion rate** — Target ≥ 95%.
- **Category coverage** — `% inbound messages classified into a named category`. Target ≥ 90%.
- **Suggested-reply acceptance** — `% drafts agents use without rewrite`. Target ≥ 70%.
- **Sensitive-case escalation rate** — `% of identified sensitive cases routed to humans within SLA`. Target = 100%.
- **Upsell rate** — `% sprints converted within 60 days`. Target ≥ 40%.

## Related
- `docs/capabilities/customer_capability.md` — capability blueprint behind this service
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map placement
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — human-in-the-loop rules
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CS baseline
- `docs/playbooks/clinics_playbook.md` — clinics premium reference
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
