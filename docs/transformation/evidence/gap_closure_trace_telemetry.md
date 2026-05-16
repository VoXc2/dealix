# Gap closure evidence — Trace contracts and optional OTel

| Field | Value |
| --- | --- |
| **Matrix gap** | Full trace coverage and telemetry contracts |
| **Owner OS** | Observability + Trust |
| **Artifact** | `docs/transformation/07_observability_contracts.md`, `auto_client_acquisition/observability_v10/contract_trace_hook.py` |
| **KPI impact** | `reliability_posture_score`, `unauthorized_external_action_count` |
| **Risk impact** | PII leakage if span attributes widen without review |
| **Verification** | `python3 scripts/verify_global_ai_transformation.py --check-observability` |

**Closure statement:** Contract validation remains mandatory; optional OpenTelemetry span events export when `OTEL_CONTRACT_TRACE_EXPORT=true` and an active span exists (no contract schema change).

---

## Verification record (reference)

Command:

```bash
python3 scripts/verify_global_ai_transformation.py --check-observability
```

Last captured output (trimmed):

```text
GLOBAL AI TRANSFORMATION: PASS
```

**KPI numeric closure:** update `reliability_posture_score` / `unauthorized_external_action_count` in [dealix/transformation/kpi_baselines.yaml](dealix/transformation/kpi_baselines.yaml) when incident/SIEM summaries exist.
