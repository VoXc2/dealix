# Scope — AI Quick Win Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Operations
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [scope_AR.md](./scope_AR.md)

## Context
The contractually binding scope of the **AI Quick Win Sprint**. The Sprint is deliberately small and bounded — its value is in finishing, not in covering everything. This document exists to make finishing inevitable. It references `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` for the strategic place of the entry tier and `docs/product/WORKFLOW_RUNTIME_DESIGN.md` for the runtime guardrails the Sprint must respect.

## Duration
- **7 business days** end-to-end.
- Kickoff within 5 business days of signed SOW + deposit.
- Optional Day 14 retro included at no extra fee.

## In Scope
1. **One workflow** chosen jointly during intake.
2. **Current-state mapping** of that workflow.
3. **AI-assisted design** with a bounded AI step and a human approval gate.
4. **Build** of a minimum viable implementation using approved tools (`docs/AI_STACK_DECISIONS.md`).
5. **One owner-led test cycle** during the Sprint.
6. **Bilingual SOP** (Arabic + English) the team can follow.
7. **Time-saved estimate** with method documented.
8. **Proof report** + **proof pack**.

## Not In Scope
- **Multi-workflow** designs. One workflow only. Adding a second = new Sprint.
- **Heavy system integration** (custom API connectors, middleware, ETL pipelines).
- **Cross-team rollout.** The Sprint hardens one workflow for one team.
- **Auto-send / auto-pay / auto-contract** actions — all such actions require human approval at the gate.
- **Custom model training or fine-tuning.**
- **Long-term operation** beyond Day 7. Operation is the Monthly AI Ops retainer.
- **Public-facing or customer-facing AI.** Internal use only.
- **PII-heavy use cases** unless agreed with explicit lawful-basis acknowledgement.

## Assumptions
1. The client provides **process documentation** for the chosen workflow within 1 business day of kickoff.
2. The client provides **sample inputs and outputs** sufficient for design.
3. The client names a **single workflow owner** with at least 1 hour/day during the Sprint.
4. The client uses tools that fit within `docs/AI_STACK_DECISIONS.md` (Notion, Sheets, Slack, common SaaS).
5. The chosen workflow can be **tested end-to-end without production data risk**.
6. The client agrees to the data handling DPA (`docs/DPA_DEALIX_FULL.md`).

## Dependencies
- Workflow choice locked by end of Day 1.
- Process docs received by end of Day 1.
- Sample inputs/outputs received by Day 2.
- Owner reviews the AI step design by Day 3.

## Change Control
- One workflow swap allowed before Day 3, with no fee.
- After Day 3, swaps trigger a re-scope.
- Out-of-scope additions become a new SOW.

## Geography & Language
- Delivery in Arabic (Saudi/Gulf) and English.
- Other languages on request (+SAR 1,500 each).
- PDPL-aware. Cross-border posture per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## Acceptance
The Sprint is accepted when:
1. SOP is delivered.
2. Time-saved estimate is documented.
3. Workflow owner signs the handoff note.

Auto-acceptance after 5 business days of silence.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + deposit | Kickoff schedule | Dealix Ops + Sponsor | T-5 days |
| Workflow nomination | Locked choice | Sponsor + DL | Day 1 |
| Owner reviews | Approved AI step | Owner + Designer | Day 3 |
| Test feedback | Final SOP | Owner + QA | Day 6 |
| Signed handoff | Proof pack closure | Sponsor + QA | Day 7 |

## Metrics
- **Scope-change request rate** — Target ≤ 15%.
- **On-time delivery** — Target ≥ 95%.
- **One-workflow discipline** — `% sprints staying with the originally chosen workflow`. Target ≥ 90%.

## Related
- `docs/capabilities/operations_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md` — runtime design
- `docs/product/PRODUCTIZATION_LEDGER.md` — productization ledger
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/AI_STACK_DECISIONS.md` — approved stack
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
