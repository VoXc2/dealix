# QA Checklist — AI Quick Win Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer (independent)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [qa_checklist_AR.md](./qa_checklist_AR.md)

## Context
The QA Sprint gates that must clear before delivery on Day 7. The reviewer must not have produced the deliverables. The protocol enforces `docs/quality/QUALITY_STANDARD_V1.md` and protects the runtime guardrails in `docs/product/WORKFLOW_RUNTIME_DESIGN.md`. It plugs into the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## How To Use
1. Open the sprint Notion record.
2. Walk every gate: Pass / Fail / N/A + evidence pointer.
3. Failures → same-day fix ticket.
4. Round is "passed" when all gates are Pass or N/A.

## Gate 1 — Workflow Owner Identified
- [ ] Workflow owner has a name, role, corporate email.
- [ ] Owner is NOT the sponsor (unless sponsor runs the cycle).
- [ ] Owner has logged ≥ 1h availability on at least 5 of 7 days.

## Gate 2 — Manual Baseline Measured
- [ ] At least one full cycle of the current process was timed.
- [ ] Baseline hours/cycle is documented with the method used.
- [ ] Baseline is the comparator for time-saved claims.

## Gate 3 — AI Step Defined
- [ ] AI step boundary is explicit (where it starts, where it stops).
- [ ] Tool selection from approved list (`docs/AI_STACK_DECISIONS.md`).
- [ ] Inputs and expected outputs of the AI step are documented.
- [ ] No prompt depends on data the client did not provide.

## Gate 4 — Human Review Present
- [ ] At least one explicit human approval gate.
- [ ] Gate is BEFORE any irreversible action (sending, paying, signing).
- [ ] Owner has accepted responsibility for the gate.
- [ ] Override path documented (what to do when the AI step fails).

## Gate 5 — Time Saved Estimated
- [ ] Estimate is computed from baseline minus new-cycle time.
- [ ] Method is documented in the proof report.
- [ ] At least one real cycle of the new flow was measured.
- [ ] Estimate is honest about variability and sample size.

## Gate 6 — SOP Delivered
- [ ] SOP exists in Arabic + English.
- [ ] SOP describes daily run, exception handling, escalation path.
- [ ] SOP names the owner and the approver explicitly.
- [ ] SOP version-tagged and linked from the proof pack.

## Gate 7 — No High-Risk Actions Automated
- [ ] No automated money transfer.
- [ ] No automated contract signing.
- [ ] No automated outbound contact to clients without approval.
- [ ] No automated PII publication.
- [ ] No automated decisions affecting customer rights without human review.

## Gate 8 — Proof Pack Complete
- [ ] All required events present: `intake_completed`, `sprint_initialized`, `workflow_mapped`, `baseline_measured`, `ai_step_designed`, `draft_built`, `owner_reviewed`, `test_cycle_complete`, `sprint_delivered`.
- [ ] Each event has timestamp, actor role, value where applicable.
- [ ] Proof pack is signed by DL + QA + WO.

## Gate 9 — Lawful Basis & DPA
- [ ] Signed data handling acknowledgement on file.
- [ ] Cross-border posture matches `CROSS_BORDER_TRANSFER_ADDENDUM`.
- [ ] Retention policy matches `DATA_RETENTION_POLICY`.

## Gate 10 — Handoff & Upsell
- [ ] Handoff note signed by sponsor.
- [ ] Upsell recommendation drafted (per `upsell.md`).
- [ ] Day-14 retro scheduled (if requested).

## Escalation
- 3+ gate failures → escalate to capability owner.
- Gate 7 failure → engagement paused; safety re-design required.
- Gate 9 failure → engagement paused; legal review.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Day 6 deliverables | Round 1 result | QA | Day 6 |
| Day 7 deliverables | Final signoff | QA | Day 7 |
| Fix tickets | Resolutions | DL + DS | Same day |

## Metrics
- **First-time pass rate** — Target ≥ 75%.
- **Gate failures per Sprint** — Target ≤ 2.
- **PII incidents** — Target = 0.

## Related
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/capabilities/operations_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md` — runtime design
- `docs/product/PRODUCTIZATION_LEDGER.md` — productization ledger
- `docs/AI_STACK_DECISIONS.md` — approved stack
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
