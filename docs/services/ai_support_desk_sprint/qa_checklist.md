# QA Checklist — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer (independent)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [qa_checklist_AR.md](./qa_checklist_AR.md)

## Context
QA gates the Sprint must clear by Day 14. Reviewer must not have produced deliverables. The protocol enforces `docs/quality/QUALITY_STANDARD_V1.md` and the human-in-the-loop matrix in `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`. Connects to the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## How To Use
1. Open the sprint Notion record.
2. Walk every gate: Pass / Fail / N/A + evidence pointer.
3. Failures → same-day fix tickets.
4. Round passes when all gates are Pass or N/A.

## Gate 1 — Categories Cover ≥ 90% of Sample
- [ ] Holdout sample classified at ≥ 90% coverage.
- [ ] "Other / unclassified" bucket has actionable next-step rule.
- [ ] Each category has a clear definition + 3 example messages.

## Gate 2 — Every Suggested Reply is `draft_only`
- [ ] Every reply in the library has `draft_only` in metadata.
- [ ] No reply contains "send now" / "auto-respond" instructions.
- [ ] No reply impersonates a human agent ("I'm John from Support").

## Gate 3 — Sensitive Topics Escalated to Human
- [ ] Every sensitive case type routes to a named human.
- [ ] No sensitive case has an auto-reply, EVER.
- [ ] Watermark applied to sensitive responses.
- [ ] Test cases for each sensitive type passed.
- [ ] For clinics clients: medical-relevant cases route to a clinician.

## Gate 4 — No Auto-Send in MVP
- [ ] No code path triggers an outbound message without human approval.
- [ ] Integration with WhatsApp / email is read-only OR draft-only.
- [ ] No background scheduler can send replies.

## Gate 5 — No PII in Logs
- [ ] Logs use IDs, not raw customer values.
- [ ] Sensitive samples never leave the encrypted vault.
- [ ] Anonymized exports for marketing pass the PII sweep.

## Gate 6 — Arabic Tone Passed
- [ ] Saudi/Gulf register applied to AR replies.
- [ ] Tone checked against client samples.
- [ ] No literal English-to-Arabic translation artifacts.
- [ ] Politeness markers appropriate for context (formal vs friendly).

## Gate 7 — Governance Check Logged
- [ ] Sensitivity tagging present per category.
- [ ] Lawful-basis acknowledgement on file.
- [ ] PDPL retention applied.
- [ ] Cross-border posture matches `CROSS_BORDER_TRANSFER_ADDENDUM`.
- [ ] For clinics clients: `clinics_playbook` checklist signed off by GR.

## Gate 8 — SLA Tracker Functional
- [ ] All categories have SLA targets.
- [ ] Tracker captures first-response and resolution times.
- [ ] Test entries flowed through correctly.
- [ ] Dashboard view shows breaches in red.

## Gate 9 — Proof Pack Complete
- [ ] All required events present.
- [ ] Each event has timestamp, actor, value.
- [ ] Proof pack signed by DL + QA + GR + SL.

## Gate 10 — Handoff & Upsell
- [ ] Handoff note signed.
- [ ] Upsell recommendation drafted.
- [ ] Day-30 review scheduled (optional).

## Escalation
- 3+ gate failures → escalate to capability owner.
- Gate 3 or 4 failure → engagement paused; sensitive-case re-design.
- Gate 7 failure → engagement paused; legal review.
- Any clinics gate failure → escalate to clinics_playbook reviewer.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Day 12 deliverables | Round 1 result | QA | Day 12 |
| Day 14 deliverables | Round 2 result | QA | Day 14 |
| Fix tickets | Resolutions | DL + Owner | Same day |

## Metrics
- **First-time pass rate** — Target ≥ 70%.
- **Gate failures per Sprint** — Target ≤ 2.
- **PII incidents** — Target = 0.
- **Auto-send incidents** — Target = 0 (must remain 0 forever).

## Related
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/capabilities/customer_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — HITL rules
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CS playbook
- `docs/playbooks/clinics_playbook.md` — clinics premium
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
