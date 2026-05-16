# Memory & Knowledge Layer — architecture

- Layer ID: `memory`
- Owner: `Knowledge + Data`
- Purpose: Operate this layer as an enterprise-safe building block, not a feature silo.
- Core responsibilities:
  - Cited answer path exists for knowledge responses.
  - Knowledge evaluation logic exists.
  - Data/source policy bridges are enforced.
  - Event store isolation exists for safer memory operations.
  - Source passport and lineage docs exist.

- Mapped implementation paths:
  - `auto_client_acquisition/revenue_memory/event_store.py`
  - `auto_client_acquisition/revenue_memory/isolated_pg_event_store.py`
  - `auto_client_acquisition/knowledge_os/answer_with_citations.py`
  - `auto_client_acquisition/knowledge_os/knowledge_eval.py`
  - `docs/architecture/SOURCE_PASSPORT.md`

