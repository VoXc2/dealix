# Observability Layer — readiness

- Owner: `Reliability + Platform`
- Readiness gate intent: this layer must pass enterprise controls before scale.
- KPIs:
  - `trace_coverage_rate`
  - `incident_detection_mttd_minutes`
  - `incident_recovery_mttr_minutes`
  - `alert_noise_ratio`

- Checklist (machine-validated by `scripts/verify_enterprise_layer_readiness.py`):
  - [ ] `tracing_complete` — Tracing schema and trace emitters exist.
  - [ ] `alerts_configured` — Alerting runbook and policies are documented.
  - [ ] `incidents_tracked` — Incident model exists and is covered.
  - [ ] `dashboards_live` — Dashboard artifacts exist for ops visibility.
  - [ ] `bottlenecks_visible` — Workflow metrics expose bottleneck signals.

