# Memory & Knowledge Layer — observability

- Required signals:
  - Layer score trend
  - Missing evidence paths
  - Failed cross-layer checks tied to this layer

- Runtime artifacts to monitor:
  - `auto_client_acquisition/revenue_memory/event_store.py`
  - `auto_client_acquisition/revenue_memory/isolated_pg_event_store.py`
  - `auto_client_acquisition/knowledge_os/answer_with_citations.py`

- Reporting:
  - Include this layer status in executive readiness brief.
