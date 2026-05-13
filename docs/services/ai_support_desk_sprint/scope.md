# Scope — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Customer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [scope_AR.md](./scope_AR.md)

## Context
Contractually binding scope of the AI Support Desk Sprint. The Sprint is bounded to **suggested replies only** in the MVP — auto-sending is explicitly excluded by policy and by `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`. References `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` for strategic placement and `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` for CS continuity.

## Duration
- **10–14 business days** end-to-end.
- Kickoff within 5 business days of signed SOW + deposit.

## In Scope
1. **Message sample analysis** — anonymized export of the last 30 days, up to 5,000 messages.
2. **Categorization rubric** covering ≥ 90% of the sample.
3. **Suggested reply library** in Arabic + English, with brand tone and `draft_only` flag.
4. **FAQ builder** for the top categories.
5. **Escalation rules** for sensitive cases (clinics, healthcare, finance, complaints).
6. **SLA tracker** definition + tooling (Notion or Sheets-based).
7. **Support insights report**.
8. **Proof report** + **proof pack**.

## Not In Scope
- **Auto-sending** of any reply on any channel.
- **Customer-facing chatbot** (no AI talks directly to customers).
- **Inbox provider migration.**
- **Multilingual delivery** beyond AR + EN unless premium agreed.
- **Sentiment analysis for pricing or marketing decisions.**
- **Medical or financial advice generation.**
- **CRM integration** beyond import/export of message samples (deeper integrations = separate scope).
- **Long-term operation.** Operation is **Monthly Support AI**.
- **Custom model training.**

## Assumptions
1. The client provides **anonymized message samples** within 2 business days of kickoff.
2. The client has or can produce a **basic FAQ** in 1–2 pages.
3. The client defines **what counts as a sensitive case** for their industry (this varies sharply between sectors).
4. The client provides **response-time targets** by category.
5. The client agrees to the DPA (`docs/DPA_DEALIX_FULL.md`) and the cross-border posture (`docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`).
6. The client has at least one **named agent reviewer** available 1h/day during the Sprint.

## Dependencies
- Anonymized samples by end of Day 2.
- FAQ doc by end of Day 4.
- Sensitive-case policy by end of Day 8.
- SLA targets by end of Day 10.

## Change Control
- One scope swap allowed before Day 5 with no fee.
- Beyond Day 5, swaps require change order.
- Out-of-scope work = new SOW.

## Geography & Language
- Delivery in Saudi/Gulf Arabic + business English.
- Other languages on request at +SAR 1,500/lang.
- PDPL-aware. Cross-border per `CROSS_BORDER_TRANSFER_ADDENDUM`.
- **Clinics/healthcare** clients incur a +30–50% premium (see `pricing.md`) and additional governance per `docs/playbooks/clinics_playbook.md`.

## Acceptance
The Sprint is accepted when:
1. Categorization rubric is delivered with ≥ 90% coverage on a holdout sample.
2. Suggested reply library, FAQ, escalation rules, SLA tracker are delivered.
3. Sponsor signs handoff note.

Auto-acceptance after 5 business days of silence.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + deposit | Kickoff schedule | Dealix Ops + Sponsor | T-5 days |
| Anonymized samples | Classification rubric | Client Support Lead + Analyst | Days 1–3 |
| Sensitive-case policy | Escalation rules | Client Sec/Legal + DL | Days 8–10 |
| Reviewer feedback | Final deliverables | Client + QA | Days 13–14 |

## Metrics
- **Scope-change request rate** — Target ≤ 15%.
- **On-time delivery** — Target ≥ 95%.
- **Suggested-only discipline** — `% sprints with zero auto-send capability shipped`. Target = 100%.

## Related
- `docs/capabilities/customer_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — human-in-the-loop rules
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CS playbook
- `docs/playbooks/clinics_playbook.md` — clinics premium reference
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
