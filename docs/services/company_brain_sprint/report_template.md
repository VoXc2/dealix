# Executive Report Template — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Knowledge Capability Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [report_template_AR.md](./report_template_AR.md)

## Context
Executive deliverable for Company Brain Sprint. Documents docs indexed, citation coverage, knowledge gaps, governance posture. Companion to `docs/templates/PROOF_PACK_TEMPLATE.md` and `docs/governance/AI_INFORMATION_GOVERNANCE.md`.

## Structure

### 1. Executive Summary
One paragraph: documents inventoried, source registry built, RAG assistant launched, citation coverage achieved.

### 2. Document Inventory
Total docs indexed, by source type, by sensitivity, by owner. Skipped/blocked docs and why.

### 3. Source Registry
Every source has owner, sensitivity, allowed_use, retention, ai_access, external_use. Total sources registered.

### 4. Q&A Quality
Sample 20 questions: correct-with-citation rate, insufficient-evidence rate, false answer rate (target = 0%).

### 5. Citation Coverage
Percentage of answers with valid source citations. Target ≥ 95%.

### 6. Access & Governance
RBAC mapping, sensitive-source gating, audit events written, blocked unauthorized accesses.

### 7. Knowledge Gaps
Top 10 questions the system could not answer with sources. Recommendations to fill.

### 8. Business Value
Knowledge Value (search time reduction estimate, answer consistency).

### 9. Risks & Limitations
What docs are stale, what sensitivity gates need review, what queries triggered escalation.

### 10. Recommended Next Step
Continue (Monthly Brain Management) / Expand (Sales Knowledge Assistant / Policy Assistant) / Pause.

## Output rules
- Bilingual summary.
- No answer presented without citation in the appendix.
- "Insufficient evidence" mode explicitly demonstrated for ungrounded queries.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Indexed docs, source registry, RAG eval results, audit events | Executive Report + Q&A sample | Knowledge Capability Lead | End of sprint |

## Metrics
- Documents indexed
- Citation coverage (%)
- Insufficient-evidence accuracy
- Knowledge gaps logged

## Related
- `docs/services/company_brain_sprint/proof_pack_template.md`
- `docs/services/company_brain_sprint/qa_checklist.md`
- `docs/governance/AI_INFORMATION_GOVERNANCE.md`
- `docs/ledgers/SOURCE_REGISTRY.md`
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md`

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
