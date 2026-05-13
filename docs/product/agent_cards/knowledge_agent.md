# Knowledge Agent — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [knowledge_agent_AR.md](./knowledge_agent_AR.md)

## Context
The Knowledge Agent is the retrieval brain behind the Company Brain
service. It answers from approved sources only and refuses to answer when
evidence is insufficient. This stance is mandated by
`docs/DEALIX_OPERATING_CONSTITUTION.md` and the public commitments at
`docs/growth/trust_page/how_we_use_ai.md`.

## Agent Card

- **Role:** Retrieves and answers from approved knowledge sources with
  citations.
- **Allowed Inputs:** indexed approved documents, user query, allowed-users
  scope.
- **Allowed Outputs:** cited answer or "insufficient evidence."
- **Forbidden:** answering without source; using unapproved documents;
  cross-tenant retrieval; leaking sensitive content beyond permission
  scope.
- **Required Checks:**
  - retrieved chunks come from the approved index;
  - citations resolve to live, allowed documents;
  - answer respects sensitivity labels;
  - if evidence < threshold, return "insufficient evidence."
- **Output Schema:** `KnowledgeAnswer { query, answer, citations[],
  confidence, evidence_state }`.
- **Approval:** for external use, source check required.

## Citation rules

- Every claim must point to a source span.
- Citations include doc id, section, and last-updated date.
- Stale documents (beyond freshness window) are flagged.
- Conflicting sources are surfaced; the agent does not silently pick.

## Anti-patterns

- Composite answers without citation per claim.
- Answering from training data when no source matches.
- Bypassing tenant or permission scope.
- Truncating "insufficient evidence" into a guess.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Indexed corpus + query | KnowledgeAnswer | Knowledge Agent | Per query |
| Sensitivity labels | Filtered retrieval | Knowledge Agent | Per query |
| Citation set | Reviewer trace | Reviewer | Per external answer |

## Metrics
- Citation Coverage — % of claims with a resolved citation.
- Refusal Rate — % of queries returning "insufficient evidence."
- Freshness Compliance — % of answers built on in-window sources.
- Cross-Tenant Leakage — must be zero.

## Related
- `docs/AI_STACK_DECISIONS.md` — model and retrieval choices
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval suite
- `docs/EVALS_RUNBOOK.md` — eval execution
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — governance rules
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
