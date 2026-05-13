# Delivery Checklist — AI Quick Win Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Operations
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [delivery_checklist_AR.md](./delivery_checklist_AR.md)

## Context
Day-by-day operational script for the 7-day AI Quick Win Sprint. Every Sprint must be reproducible and auditable per `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and `docs/quality/QUALITY_STANDARD_V1.md`. Each checkbox maps to a proof pack event consumed by `docs/templates/PROOF_PACK_TEMPLATE.md`.

## Roles
- **Delivery Lead (DL)** — single accountable.
- **Designer (DS)** — workflow design + build.
- **Workflow Owner (WO)** — client-side single point of contact, daily 1h availability.
- **QA Reviewer (QA)** — independent reviewer.
- **Sponsor (SP)** — final acceptance.

## Day-by-Day Plan

### T-2 to T-1 — Pre-kickoff
- [ ] Welcome email sent with shared folder, intake summary, Day 1 agenda. (DL)
- [ ] Internal Sprint board created in Notion. (DL)
- [ ] Premium re-validated against intake. (DL + Margin Controller)
- [ ] Proof pack initialized with event `sprint_initialized`. (DL)

### Day 1 — Map Current State
- [ ] Kickoff call (30 min) with SP and WO. (DL)
- [ ] Workflow choice locked. (DL + SP)
- [ ] WO walks DS through the current process. (WO + DS)
- [ ] DS produces workflow_map.md draft. (DS)
- [ ] Proof event: `workflow_mapped`. (DS)

### Day 2 — Finalize Map
- [ ] WO reviews and corrects the workflow map. (WO)
- [ ] Manual baseline measurement starts (1 cycle of current process timed). (WO + DS)
- [ ] Baseline hours/cycle locked. (WO + DS)
- [ ] Proof event: `baseline_measured`. (DS)

### Day 3 — AI Step Design
- [ ] DS designs the AI step boundary. (DS)
- [ ] Approval gate location specified. (DS)
- [ ] Tool selection from `docs/AI_STACK_DECISIONS.md`. (DS)
- [ ] Risk check: no auto-send / auto-pay / auto-contract. (QA + DS)
- [ ] WO + SP sign off on design. (WO + SP)
- [ ] Proof event: `ai_step_designed`. (DS)

### Day 4 — Build Draft
- [ ] DS builds minimum viable implementation. (DS)
- [ ] DL reviews intermediate output mid-day. (DL)
- [ ] Test inputs prepared from client samples. (DS)
- [ ] Proof event: `draft_built`. (DS)

### Day 5 — Owner Review
- [ ] WO walks through the draft live with DS. (WO + DS)
- [ ] WO produces a revision list. (WO)
- [ ] DS applies revisions same day. (DS)
- [ ] Proof event: `owner_reviewed`. (WO)

### Day 6 — Test Cycle
- [ ] WO runs one full cycle through the new flow. (WO)
- [ ] Time measured per step. (WO + DS)
- [ ] Time-saved estimate computed. (DS)
- [ ] QA runs the QA checklist. (QA)
- [ ] Any failed gate → fix same day. (DL)
- [ ] Proof event: `test_cycle_complete`, `manual_steps_reduced = N`. (WO + DS)

### Day 7 — SOP + Proof
- [ ] SOP drafted in Arabic + English. (DS)
- [ ] Proof pack finalized. (DL + QA)
- [ ] Executive output drafted. (DL)
- [ ] Final QA pass. (QA)
- [ ] Handoff call (45 min) with SP and WO. (DL)
- [ ] SP signs handoff note. (SP)
- [ ] Proof event: `sprint_delivered`, `hours_saved = X`. (DL)
- [ ] Upsell motion triggered (per `upsell.md`). (DL + CSM)

## Cross-Cutting Controls
- WO availability monitored daily; 2+ day absence triggers a pause.
- All deliverable changes tracked in the Sprint board.
- No deliverable ships without QA sign-off.
- Proof pack updated continuously.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + intake | Sprint board | DL | T-2 |
| Daily standup | Sprint board updates | DL | Daily 10:00 |
| QA result | Fix tickets or signoff | QA + DL | Day 6, Day 7 |
| Final SOP + proof | Handoff | DL + SP | Day 7 |

## Metrics
- **On-time delivery** — Target ≥ 95%.
- **QA pass first time** — Target ≥ 75%.
- **Checklist adherence** — Target = 100%.
- **Owner availability** — `% days where WO was available ≥ 1h`. Target ≥ 90%.

## Related
- `docs/capabilities/operations_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md` — runtime design
- `docs/product/PRODUCTIZATION_LEDGER.md` — productization ledger
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/AI_STACK_DECISIONS.md` — approved stack
- `docs/V14_FOUNDER_DAILY_OPS.md` — operating loop
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
