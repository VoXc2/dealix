---
title: SLO Framework — SLIs, per-tier SLOs, error budgets, multi-window burn-rate alerts, incident severity matrix
doc_id: W4.T23.slo-framework
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T21.adr-0004, W4.T22.event-store-async-migration, W4.T24.model-cost-governance, W4.T25.data-quality-gates]
kpi: { metric: slo_compliance_rolling_28d_pct, target: 100, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.85, effort: 5pw, score: engineering }
---

# SLO Framework

## 1. Purpose and Scope

Define the Service Level Indicators (SLIs), Service Level Objectives (SLOs) per pricing tier, error-budget policy, alerting strategy (multi-window burn-rate), and the incident severity matrix used by on-call. This document is the authority that downstream alerting rules, dashboards, contracts, and incident response refer back to.

Scope:

- Customer-facing API surface (`api/v1/*`).
- Revenue OS workflows (`auto_client_acquisition/revenue_os/*`).
- Event store (`auto_client_acquisition/revenue_memory/pg_event_store.py`).
- Decision passport pipeline (`api/routers/decision_passport.py`, `dealix/trust/policy.py`).
- Billing API (Moyasar integration).

Out of scope: internal admin UI, batch analytics jobs, marketing site.

## 2. SLI Catalogue

Four SLI families, each with an explicit measurement contract.

### 2.1 Availability

- **Definition**: `(1 - errors / valid_requests)` per service over the SLO window.
- **errors** = HTTP 5xx and timeouts (no response within 30 s).
- **valid_requests** = all non-4xx requests (4xx are caller errors; excluded).
- **Measurement source**: OpenTelemetry HTTP server metrics, aggregated in Prometheus.
- **Granularity**: 1-minute buckets, rolled up to 28-day window.

### 2.2 Latency (p50, p95, p99)

- **Definition**: HTTP server response time, end-to-end, from request received to response flushed.
- **Per endpoint** (the seven critical paths):
  - `POST /api/v1/revenue-os/lead/enrich` — primary enrichment.
  - `POST /api/v1/revenue-os/lead/qualify` — qualification.
  - `POST /api/v1/decision-passport` — emit passport.
  - `GET  /api/v1/decision-passport/{id}` — retrieve passport.
  - `POST /api/v1/revenue-os/action/dispatch` — outbound action.
  - `GET  /api/v1/revenue-os/signals` — signal feed.
  - `POST /api/v1/billing/checkout` — Moyasar checkout.
- **Measurement source**: histogram metric `http_server_duration_ms_bucket` with `route` and `method` labels.

### 2.3 Freshness (data SLI)

- **Definition**: time between event occurrence (source timestamp) and event availability in the read path.
- **Three sub-SLIs**:
  - `freshness_passport` — passport readable via API after emission.
  - `freshness_signal` — external signal visible in `/signals` after source registry ingest.
  - `freshness_event_store` — event readable via `read_stream` after `append`.
- **Measurement**: synthetic probe emitted every 30 s, measured at consumer.

### 2.4 Correctness / Trust

- **Definition**: `(passports_with_complete_evidence / passports_emitted)` over the SLO window.
- **Complete evidence** = all required policy rules evaluated and recorded; evidence level meets the threshold for the action type (see `docs/policy/revenue_os_policy_rules.md`).
- **Measurement source**: domain metric `passport_emitted_total{evidence_completeness}`.

## 3. SLOs per Pricing Tier

| SLI | Starter (1,490 SAR/mo) | Growth (4,900 SAR/mo) | Sovereign (24,000+ SAR/mo) | Internal (Free / Trial) |
|---|---|---|---|---|
| Availability | **99.5%** | **99.7%** | **99.95%** | 99.0% best-effort |
| Latency p50 | ≤ 180 ms | ≤ 140 ms | ≤ 120 ms | n/a |
| Latency p95 | ≤ 400 ms | ≤ 300 ms | ≤ 250 ms | n/a |
| Latency p99 | ≤ 1,200 ms | ≤ 900 ms | ≤ 800 ms | n/a |
| Freshness (passport) | ≤ 5 s p95 | ≤ 3 s p95 | ≤ 2 s p95 | n/a |
| Freshness (signal) | ≤ 60 s p95 | ≤ 30 s p95 | ≤ 15 s p95 | n/a |
| Correctness | ≥ 99.0% | ≥ 99.5% | ≥ 99.9% | n/a |

Window: 28 days rolling for all SLOs.

Sovereign 99.95% = 21.6 minutes/month error budget.
Growth 99.7%   = 129.6 minutes/month error budget.
Starter 99.5%  = 216 minutes/month error budget.

## 4. Error Budgets and Policy

For each tier, the **error budget** is `(1 - SLO) × window_minutes`.

Burn-rate definition: `error_budget_consumed_in_period / period_length × SLO_window_length`. A burn rate of 1 consumes the budget exactly within the SLO window.

### 4.1 Error budget policy

- **If burn rate over 7 days > 1.0**: shipping new features for the affected surface is **paused**; engineering shifts to reliability work until 7-day burn rate < 0.5.
- **If error budget for the rolling 28-day window is exhausted**: a written reliability plan with named owner and target date is required before resuming feature work.
- **Bug fixes and security patches** are never blocked by budget exhaustion.
- **Sovereign-affecting incidents** of any size trigger a CEO notification within 60 minutes.

## 5. Multi-Window Burn-Rate Alerts

Two alert classes per SLO, following Google SRE multi-window pattern.

### 5.1 Fast burn (page on-call)

Triggers if **both** windows breach simultaneously (reduces false positives):

- 5-minute window: burn rate > 14.4 (would exhaust 2% of budget in 5 min).
- 1-hour window: burn rate > 14.4.

Severity: P1 (page).

### 5.2 Slow burn (ticket to on-call)

- 30-minute window: burn rate > 6.
- 6-hour window: burn rate > 6.

Severity: P2 (Slack notify + ticket).

### 5.3 Per-tier alert routing

- Sovereign alerts → primary pager, CEO at P1.
- Growth alerts → primary pager.
- Starter alerts → primary pager during business hours; secondary off-hours.

Alert config lives in code under `infra/alerts/` (to be added). Source of truth: this document.

## 6. Incident Severity Matrix

| Severity | Definition | Examples | Page? | Comms |
|---|---|---|---|---|
| **P1 (Critical)** | Sovereign customer-impacting outage; or any breach of compliance/PDPL; or revenue-flow (billing) down. | Sovereign /enrich returns 5xx for ≥ 5 min; data leak across tenants; Moyasar callbacks failing. | Yes, 24/7 | Status page yellow→red within 10 min; CEO Slack DM at P1. |
| **P2 (High)** | Growth-tier impact, or partial Starter outage, or persistent latency breach. | Growth p95 latency > 600 ms for 30 min; passport correctness drops to 99.2%. | Yes, business hours | Status page yellow; #incidents Slack thread. |
| **P3 (Medium)** | Internal degradation, no customer impact yet. | Background enrichment lag 5 min; non-critical worker queue backlog. | No, ticket | #incidents Slack message; daily standup. |
| **P4 (Low)** | Observability gap, flaky test, doc inconsistency. | Trace sampling misconfigured for one service. | No | Backlog ticket. |

Time-to-acknowledge targets: P1 ≤ 5 min, P2 ≤ 15 min, P3 ≤ 24 h.

Time-to-resolve targets (mean): P1 ≤ 30 min, P2 ≤ 4 h, P3 ≤ 1 business day.

## 7. Reporting Cadence

- **Daily**: SLO compliance email to engineering, auto-generated. One number per SLI per tier.
- **Weekly**: error-budget burn review in eng standup; reliability backlog re-prioritized.
- **Monthly**: SLO report to CEO; incidents summary; budget consumption per tier; root-cause categories.
- **Quarterly**: SLO targets reviewed; tier-by-tier renegotiation; correlation with churn.

## 8. SLI Implementation Notes

- **Histograms** must use exponential buckets (factor 2, 8 buckets from 1 ms to 32 s) to compute p99 reliably.
- **Cardinality cap**: per-tenant labels capped at top 50 + "other" bucket; per-route labels enumerated.
- **Synthetic probes** run from inside the KSA region for Sovereign and from a representative second region for non-Sovereign.
- **Probe failures** count against availability only if they reproduce the failure for real traffic in the same window — avoids probe-only false positives.

## 9. Data Sources

| SLI | Source | Owner |
|---|---|---|
| Availability | Prometheus, OTel HTTP metrics | SRE |
| Latency | Prometheus, OTel HTTP histograms | SRE |
| Freshness | Synthetic probe (Pinger service) | SRE |
| Correctness | Domain metric from `dealix/trust/policy.py` | Head of Data |
| Event store durability | `event_store_append_total{result}` | CTO |

## 10. Change Management

Any change to:

- SLO targets — requires CTO + CEO approval (contract impact).
- SLI definitions — requires CTO approval; backwards compatibility check.
- Alert thresholds — requires SRE lead approval.
- Severity matrix — requires CTO approval.

All changes go through PR review with the doc owner; status flipped to `draft → accepted` on merge.

## 11. References

- ADR-0004 Observability Stack: `docs/adr/0004-observability-stack.md`.
- Event store: `docs/engineering/event_store_async_migration.md`.
- Existing SLO sketch: `docs/SLO.md` (deprecated by this doc once accepted).
- Incident runbook: `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`.
- Pricing tiers: `docs/PRICING_AND_PACKAGING_V6.md`.
- Multi-window burn-rate: Google SRE Workbook chapter 5.
