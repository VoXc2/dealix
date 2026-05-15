# Observability Layer — architecture

- Layer ID: `observability`
- Owner: `Reliability + Platform`
- Purpose: Operate this layer as an enterprise-safe building block, not a feature silo.
- Core responsibilities:
  - Tracing schema and trace emitters exist.
  - Alerting runbook and policies are documented.
  - Incident model exists and is covered.
  - Dashboard artifacts exist for ops visibility.
  - Workflow metrics expose bottleneck signals.

- Mapped implementation paths:
  - `auto_client_acquisition/agent_observability/trace.py`
  - `auto_client_acquisition/observability_v10/trace_schema.py`
  - `auto_client_acquisition/observability_v6/incident.py`
  - `docs/observability/posthog_dashboard.json`
  - `docs/ops/INCIDENT_RUNBOOK.md`

