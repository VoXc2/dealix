---
title: ADR-0004 Observability Stack — OpenTelemetry traces, structured JSON logs, Sentry, Dealix decision-passport tracer
doc_id: W4.T21.adr-0004-observability-stack
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T21.adr-0001, W4.T21.adr-0002, W4.T23.slo-framework, W4.T12.event-taxonomy]
kpi: { metric: mean_time_to_detect_minutes, target: 5, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.85, effort: 6pw, score: engineering }
---

# ADR-0004: Observability Stack

> **Decision: We adopt OpenTelemetry (OTLP) for traces and metrics, structured JSON logs to stdout collected by the platform, Sentry for application errors, and a custom in-process `DecisionPassportTracer` that emits domain spans for every passport lifecycle event.**

## Context

Current observability is fragmented:

- Application logs go to stdout in plain text — unparseable in aggregate.
- Sentry is wired only for API exceptions; orchestrator and workers are dark.
- No distributed tracing — an enrichment that crosses `source_registry → enrichment_waterfall → signal_normalizer → policy → passport` is unobservable end-to-end.
- Latency histograms exist only at the load balancer; per-operation latency requires log-scraping.

Operational pain (Q1 2026):

- Mean Time To Detect (MTTD) for production incidents: 23 minutes (target ≤ 5).
- Mean Time To Resolve (MTTR): 1 h 48 min (target ≤ 30 min for P1).
- Two customer-visible incidents in 90 days where the root cause was a slow enrichment provider; no provider-level latency telemetry existed.
- Auditors asked for "show me the trace of decision passport PP-2026-04-1284" — currently un-answerable.

Cost envelope: ≤ 1,400 USD/month for observability tooling.

## Decision

**Four-layer stack.**

1. **Traces (OpenTelemetry, OTLP)**
   - Auto-instrument FastAPI, SQLAlchemy async, httpx, redis, arq.
   - Manual spans around every step in `auto_client_acquisition/orchestrator/runtime.py` and every source in `source_registry.py`.
   - Sampling: 100% of error traces, 100% of traces > 1 s, 10% of healthy traces. Tail-based sampler at the collector.
   - Backend: Grafana Tempo (self-hosted in KSA region for Sovereign compliance) for Sovereign tenant traces; managed (Grafana Cloud) for Starter/Growth aggregate.

2. **Metrics (OpenTelemetry → Prometheus)**
   - RED metrics (Rate, Errors, Duration) per endpoint, per orchestrator step, per outbound source.
   - Domain metrics: `passport_emitted_total`, `policy_blocked_total{rule}`, `enrichment_source_latency_ms{source}`.
   - 14-day retention high-resolution (15 s); 13-month rollup (5 min).

3. **Logs (structured JSON, stdout)**
   - All logs are JSON with required fields: `ts`, `level`, `service`, `tenant_id`, `trace_id`, `span_id`, `event`, plus optional domain fields.
   - Collected by the platform (Railway/Fly logs → Loki).
   - PII redaction at emit-time via a `redact()` helper; redact list defined in `dealix/trust/policy.py`.
   - Retention: 30 days hot, 12 months cold.

4. **Errors (Sentry)**
   - All services. DSN per environment. Release tag = git SHA.
   - PII scrubbing enabled. `tenant_id` tag attached automatically via middleware.
   - Alert rules: any new issue in prod, any spike > 3× baseline in 5 min.

5. **`DecisionPassportTracer` (custom)**
   - Lives in `dealix/trust/passport_tracer.py` (to be created).
   - Emits a typed span for each passport lifecycle event: `intent_created`, `evidence_collected`, `policy_checked`, `action_dispatched`, `outcome_recorded`.
   - Every span carries `passport_id`, `tenant_id`, `evidence_level`, `policy_rules_evaluated[]`, `decision`.
   - Spans are also persisted as events (ADR-0001) so the audit trail survives independently of trace retention.

## Status

`Proposed` — pending CTO sign-off. Target acceptance: 2026-05-24. Effective: 2026-06-10.

## Consequences

### Positive

- MTTD modeled to 4 minutes (multi-window burn-rate alerts; see SLO framework).
- End-to-end traces let SRE answer "where did the 1.8 s come from?" in < 60 seconds.
- Audit answer for "show me trace of passport X" becomes a one-click drill-down.
- Cost projection: Grafana Cloud Pro plan + Tempo KSA pod = ~1,150 USD/month; under budget.
- Provides the SLI data that the SLO framework requires (W4.T23).

### Negative

- Engineering cost: ~6 person-weeks instrumentation + ~1 person-week dashboards.
- Cardinality risk: `tenant_id` as a high-cardinality label; mitigated by capping at metrics layer to the top 50 tenants + an "other" bucket.
- Trace storage: ~80 GB/month at projected volume; included in plan.
- Sentry quota: estimated 400k events/month at v1.0 stable rate; well within team plan.

### Neutral / Follow-ups

- Add per-source latency dashboard for `source_registry.py`.
- Define alert rules in `docs/sre/slo_framework.md`.
- Document the redaction helper and PII denylist.
- Add `trace_id` to every API response header (`x-dealix-trace-id`) so customer support can correlate.

## Alternatives Considered

| Alternative | Reason rejected |
|---|---|
| **A. Datadog full-stack** | Cost at projected volume ≈ 3,800 USD/month, 2.7× budget. Sovereign data-residency story unclear (no KSA region). |
| **B. Honeycomb + Sentry** | Honeycomb has no KSA presence; pricing per event would exceed budget at projected 5M events/month. |
| **C. Self-host full Grafana stack (Loki+Tempo+Prometheus+Mimir) from day one** | Ops cost ~0.6 SRE FTE; defer until 2027 when scale justifies. Hybrid (managed for non-Sovereign, self-host for Sovereign traces) chosen instead. |
| **D. Only Sentry + plain logs** | No distributed tracing; cannot meet MTTD target; cannot answer audit queries. |

## References

- Code: `api/routers/decision_passport.py`, `auto_client_acquisition/orchestrator/runtime.py`, `dealix/trust/policy.py`.
- OpenTelemetry FastAPI auto-instrumentation docs.
- `docs/OBSERVABILITY_ENV.md`, `docs/AI_OBSERVABILITY_AND_EVALS.md`.
- Related ADRs: ADR-0001 (event store), ADR-0002 (async boundaries), ADR-0003 (multi-tenant).
- SLO framework: `docs/sre/slo_framework.md`.

## Review Cadence

Quarterly. Re-evaluate cost when monthly observability bill exceeds 2,000 USD or when trace volume exceeds 12M/month.
