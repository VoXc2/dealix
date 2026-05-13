# Executive Report Template — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Customer Capability Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [report_template_AR.md](./report_template_AR.md)

## Context
Executive deliverable closing every AI Support Desk Sprint. Documents message classification, suggested-reply coverage, escalation accuracy, and time-to-respond improvements. Pairs with `docs/templates/PROOF_PACK_TEMPLATE.md` and `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`.

## Structure

### 1. Executive Summary
One paragraph: messages analyzed, categories created, suggested replies built, escalation rules established.

### 2. Message Classification Coverage
Total messages reviewed, by channel (WhatsApp, email, web). Category coverage percentage (target ≥ 90%).

### 3. Suggested Reply Library
Categories, sample replies, all flagged `draft_only`. No auto-send in MVP.

### 4. FAQ Builder
Top recurring questions, knowledge gaps identified for Company Brain follow-up.

### 5. Escalation Rules
Sensitive topics auto-routed to humans. Sample escalation decisions logged.

### 6. SLA Tracker
Baseline response time vs new estimate with suggested replies + reviewers.

### 7. Governance & Quality
Approvals captured, no PII in logs, Arabic tone passed, no autonomous sending performed.

### 8. Business Value
Time Value (response time reduction) + Quality Value (reply consistency).

### 9. Risks & Limitations
Sensitive cases requiring human-only handling. Channel-specific limitations.

### 10. Recommended Next Step
Continue (Monthly Support AI) / Expand (Feedback Intelligence) / Pause.

## Output rules
- Bilingual summary.
- All sample replies anonymized.
- No claim of automated resolution; all replies are draft-only in MVP.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Anonymized message samples, classifier output, escalation log | Executive Report + Suggested Reply Library | Customer Capability Lead | End of sprint |

## Metrics
- Category coverage (%)
- Suggested replies built
- Escalation accuracy
- Estimated response-time reduction

## Related
- `docs/services/ai_support_desk_sprint/proof_pack_template.md`
- `docs/services/ai_support_desk_sprint/qa_checklist.md`
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/playbooks/clinics_playbook.md`
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md`

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
