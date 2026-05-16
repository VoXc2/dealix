# Knowledge Retrieval Contract

## Goal

Deliver tenant-safe, citation-backed retrieval for high-impact decisions.

## Retrieval Pipeline

1. Query normalization.
2. Permission filter (`tenant_id`, role scope, data class).
3. Candidate retrieval.
4. Re-ranking for relevance and trust.
5. Citation packaging with source lineage.

## Mandatory Retrieval Gates

| Gate ID | Requirement | Test ID |
|---|---|---|
| G-KNW-001 | tenant and role filters applied before retrieval | T-KNW-001 |
| G-KNW-002 | cross-tenant retrieval blocked | T-KNW-002 |
| G-KNW-003 | top results include source lineage | T-KNW-003 |
| G-KNW-004 | retrieval quality threshold met | T-KNW-004 |
| G-KNW-005 | risky/low-confidence responses escalate | T-KNW-005 |

## Retrieval Quality Metrics

- `precision_at_k`
- `recall_at_k`
- `citation_coverage_rate`
- `permission_violation_rate` (target: 0)
- `hallucination_rate` (target: below policy threshold)

## Evidence

- Retrieval eval report against golden dataset.
- Access control logs proving permission checks.
- Sample response payload with citations and lineage metadata.
