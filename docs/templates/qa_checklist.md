# QA Checklist — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** QA Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [qa_checklist_AR.md](./qa_checklist_AR.md)

## Context
This is the QA gate checklist used at the Validate stage of the
Delivery Standard (`docs/delivery/DELIVERY_STANDARD.md`). It pairs
with the Quality Standard (`docs/quality/QUALITY_STANDARD_V1.md`), the
forbidden-action register
(`docs/governance/FORBIDDEN_ACTIONS.md`), and the Approval Matrix
(`docs/governance/APPROVAL_MATRIX.md`). Every Draft delivered to a
client must clear this checklist with a score ≥ 85.

## Scoring
Each item is scored 0/3/5. Total possible: 30 items × 5 = 150. Convert
to 100-scale: `score = total * 100 / 150`. Pass threshold: 85.

## Business (6 items)
- [ ] Output addresses the agreed business problem (5)
- [ ] Output respects the agreed scope (5)
- [ ] Output cites the hero metric and target (5)
- [ ] Output reads as native Arabic where Arabic is in scope (5)
- [ ] Output reads as native English where English is in scope (5)
- [ ] Output uses correct entity names, titles, and dates (5)

## Data (6 items)
- [ ] Source dataset has a valid DRS ≥ required threshold (5)
- [ ] No record uses data outside the declared `allowed_use` (5)
- [ ] Schema conformance verified for inputs and outputs (5)
- [ ] Deduplication and freshness checks pass (5)
- [ ] PII redacted where required (5)
- [ ] All source references resolve to a known asset (5)

## AI (6 items)
- [ ] Every AIRun is logged with `ai_run_id` (5)
- [ ] Prompt version is registered and not ad-hoc (5)
- [ ] Output schema validated by Gateway (5)
- [ ] No Gateway bypass detected (5)
- [ ] Risk level attached to every output (5)
- [ ] Eval sample emitted where applicable (5)

## Compliance (6 items)
- [ ] No forbidden-action match on outputs (5)
- [ ] Action class declared and routed correctly (5)
- [ ] Approval recorded with expiry, where required (5)
- [ ] No PII in logs or proof pack (5)
- [ ] Source citations present for knowledge answers (5)
- [ ] No guaranteed-outcome claims (5)

## Reusability (6 items)
- [ ] Reusable asset candidate identified (5)
- [ ] Capital ledger entry drafted (5)
- [ ] Playbook update candidate identified (5)
- [ ] Feature candidate logged if pattern recurred (5)
- [ ] Proof pack uses repeatable structure (5)
- [ ] Handoff package ready (5)

## Total
- Items passed at 5: `<count>` / 30
- Items passed at 3: `<count>` / 30
- Items failed (0): `<count>` / 30
- Raw total: `<total>` / 150
- 100-scale score: `<score>` / 100
- Decision: `<PASS | REWORK>`

## Notes And Defects
Free text: list defects, root causes, and remediation actions.

## Sign-Off
- QA reviewer: `<name, date>`.
- Delivery lead acknowledgment: `<name, date>`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Draft | QA score record | QA reviewer | Per draft |
| QA score | Pass/rework decision | QA reviewer | Per draft |
| Defects list | Rework backlog | Delivery lead | Per draft |
| Pattern recurrence | Feature candidate | AI platform lead | Per pattern |

## Metrics
- **QA first-pass rate** — share of drafts passing on first review.
  Target: ≥ 80%.
- **Rework cycles per project** — Target: ≤ 1.
- **Compliance-section pass rate** — Target: 100% on critical items.

## Related
- `docs/quality/QUALITY_STANDARD_V1.md` — quality bar.
- `docs/governance/FORBIDDEN_ACTIONS.md` — forbidden actions.
- `docs/governance/APPROVAL_MATRIX.md` — approval matrix.
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack sibling.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
