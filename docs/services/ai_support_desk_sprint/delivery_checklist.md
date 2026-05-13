# Delivery Checklist — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Customer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [delivery_checklist_AR.md](./delivery_checklist_AR.md)

## Context
Day-by-day operational script for the 14-day AI Support Desk Sprint. Every Sprint reproducible and auditable per `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, the quality standard in `docs/quality/QUALITY_STANDARD_V1.md`, and the human-in-the-loop matrix in `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`. Every checkbox maps to a proof pack event.

## Roles
- **Delivery Lead (DL)** — single accountable.
- **Analyst (AN)** — message clustering, categorization.
- **Copy Lead (CL)** — suggested-reply library.
- **Governance Reviewer (GR)** — sensitivity, escalation, lawful basis.
- **Support Lead (SL)** — client-side single point of contact.
- **QA Reviewer (QA)** — independent reviewer.
- **Sponsor (SP)** — final acceptance.

## Day-by-Day Plan

### T-3 to T-1 — Pre-kickoff
- [ ] Welcome email sent. (DL)
- [ ] Sprint board created. (DL)
- [ ] Premium re-validated, clinics_playbook applied if relevant. (DL + GR)
- [ ] Proof pack initialized with `sprint_initialized`. (DL)

### Days 1–3 — Classification + Categories
- [ ] Kickoff call (45 min) with SP and SL. (DL)
- [ ] Anonymized samples received and PII-swept. (AN + QA)
- [ ] Message clustering run. (AN)
- [ ] Draft categorization rubric. (AN)
- [ ] SL reviews rubric, refines. (SL + AN)
- [ ] Rubric coverage tested on holdout sample: ≥ 90%. (AN)
- [ ] Proof event: `messages_classified = N`, `category_coverage = X%`. (AN)

### Days 4–7 — Suggested Replies + FAQ
- [ ] CL drafts 1–3 suggested replies per category in AR + EN. (CL)
- [ ] Brand tone calibrated against client samples. (CL)
- [ ] FAQ builder structured from top categories. (CL)
- [ ] All replies labeled `draft_only`. (CL)
- [ ] No medical / financial advice generated; sensitive cases stop at escalation card. (GR + CL)
- [ ] Proof event: `replies_drafted = N`. (CL)

### Days 8–10 — Escalation Rules
- [ ] Sensitive-case policy reviewed with client Sec/Legal. (GR + SL)
- [ ] Escalation routing implemented: case type → named human + watermark. (GR + AN)
- [ ] Test sensitive cases routed correctly in dry run. (GR + QA)
- [ ] No sensitive case auto-replied to in the system. (GR + QA)
- [ ] For clinics clients: clinical escalation tested specifically. (GR)
- [ ] Proof event: `escalations_routed = N`, `sensitive_blocks = N`. (GR)

### Days 11–12 — SLA Tracker
- [ ] SLA tracker (Notion/Sheets) provisioned. (DL)
- [ ] Targets per category loaded. (DL + SL)
- [ ] First-response time and resolution time fields wired. (DL)
- [ ] Test cases logged to validate tracker behavior. (QA)

### Days 13–14 — QA + Handoff
- [ ] QA runs full QA checklist. (QA)
- [ ] Any failure → same-day fix. (DL)
- [ ] Support insights report drafted. (DL)
- [ ] Proof report drafted. (DL)
- [ ] Sensitive-field anonymization verified. (QA + GR)
- [ ] Handoff call (75 min) with SP, SL, and at least 2 agents. (DL)
- [ ] SP signs handoff note. (SP)
- [ ] Proof event: `sprint_delivered`. (DL)
- [ ] Upsell motion triggered. (DL + CSM)

## Cross-Cutting Controls
- No auto-send capability shipped in MVP, ever.
- Proof pack continuously updated.
- Sensitive samples never moved off the encrypted vault.
- Clinics clients require GR sign-off in addition to QA.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + intake | Sprint board | DL | T-3 |
| Daily standup | Sprint board updates | DL | Daily 10:00 |
| QA + GR results | Fix tickets or signoff | QA + GR + DL | End of each phase |
| Final library + report | Handoff | DL + SP | Day 14 |

## Metrics
- **On-time delivery** — Target ≥ 95%.
- **Category coverage** — Target ≥ 90% on holdout.
- **Sensitive escalation accuracy** — Target = 100%.
- **No auto-send shipped** — Target = 100%.

## Related
- `docs/capabilities/customer_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — HITL rules
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CS playbook
- `docs/playbooks/clinics_playbook.md` — clinics premium
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/V14_FOUNDER_DAILY_OPS.md` — operating loop
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
