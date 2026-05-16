# Memory & Knowledge Layer — readiness

- Owner: `Knowledge + Data`
- Readiness gate intent: this layer must pass enterprise controls before scale.
- KPIs:
  - `citation_coverage_rate`
  - `retrieval_relevance_score`
  - `memory_isolation_incidents`
  - `source_lineage_coverage_rate`

- Checklist (machine-validated by `scripts/verify_enterprise_layer_readiness.py`):
  - [ ] `citations_working` — Cited answer path exists for knowledge responses.
  - [ ] `retrieval_evals_present` — Knowledge evaluation logic exists.
  - [ ] `permissions_respected` — Data/source policy bridges are enforced.
  - [ ] `memory_isolated` — Event store isolation exists for safer memory operations.
  - [ ] `lineage_visible` — Source passport and lineage docs exist.

