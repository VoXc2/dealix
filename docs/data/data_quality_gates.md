---
title: Data Quality Gates — completeness, validity, freshness, uniqueness, accuracy per pipeline stage; quarantine; SLA
doc_id: W4.T25.data-quality-gates
owner: HoData
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T23.slo-framework, W4.T14.revenue-os-policy-rules, W4.T12.event-taxonomy, W4.T21.adr-0001]
kpi: { metric: data_quality_pass_rate_pct, target: 99.5, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.85, effort: 6pw, score: engineering }
---

# Data Quality Gates

## 1. Purpose

Define the data-quality gates every record must pass to flow through the Revenue OS pipeline. Each gate has an explicit measurement, owner, and failure mode. Records that fail are routed to a quarantine queue with a repair SLA. This is the contract between source ingestion, enrichment, policy, and the decision passport.

## 2. Pipeline Stages

```
[1] Source ingest        →  source_registry.py
[2] Normalization        →  signal_normalizer.py
[3] Enrichment waterfall →  enrichment_waterfall.py
[4] Policy check         →  dealix/trust/policy.py
[5] Passport assembly    →  api/routers/decision_passport.py
[6] Action dispatch      →  Revenue OS action endpoints
[7] Outcome capture      →  Revenue Memory (event store)
```

Gates fire **at the boundary between stages**. A record that fails a gate is rejected from progression and routed to quarantine. Each gate is implemented as a typed validator with structured failure reasons (no free-text errors).

## 3. The Five Dimensions

### 3.1 Completeness

- **Definition**: required fields present and non-null per the schema for that stage.
- **Metric**: `(records_with_all_required_fields / records_evaluated)`.
- **Target**: ≥ 99.0% at stage 1; ≥ 99.5% at stages 2+.
- **Examples of required fields**:
  - Stage 1 lead: `tenant_id`, `source`, `external_id`, `received_at`, at least one of `email | phone | company_domain`.
  - Stage 3 enriched lead: `vertical`, `region`, `intent_score`, `evidence_summary`.
  - Stage 5 passport: `passport_id`, `tenant_id`, `lead_id`, `evidence_level`, `policy_decisions[]`, `action_recommendation`.

### 3.2 Validity

- **Definition**: each field matches its type, format, and value constraints.
- **Metric**: `(records_passing_schema / records_evaluated)`.
- **Target**: ≥ 99.5% at every stage.
- **Examples**:
  - `email` matches RFC 5322 and is not on the disposable-mail blocklist.
  - `phone` is valid E.164 and (for KSA leads) starts with `+9665`.
  - `region` ∈ enumerated KSA regions or ISO 3166-2 codes.
  - `intent_score` ∈ [0, 100].

### 3.3 Freshness

- **Definition**: time between source event timestamp and the gate.
- **Metric**: p50, p95 lag in seconds per stage.
- **Targets** (per SLO framework, mirrored here):
  - Stage 1 → 2: p95 ≤ 5 s.
  - Stage 2 → 3: p95 ≤ 8 s.
  - Stage 3 → 5 (passport ready): p95 ≤ 15 s (Sovereign), 30 s (Growth), 60 s (Starter).
- **Stale-record rule**: records older than 24 h since source timestamp at stage 3 are flagged and require re-enrichment.

### 3.4 Uniqueness

- **Definition**: no duplicate records on the natural-key axis for the stage.
- **Metric**: `(unique_records / records_ingested)` per source per day.
- **Target**: ≥ 99.95%.
- **Natural keys**:
  - Stage 1 lead: `(tenant_id, source, external_id)`.
  - Stage 3 enriched lead: `(tenant_id, canonical_company_id, canonical_person_id)`.
  - Stage 5 passport: `passport_id`.
- **Duplicate handling**: dedupe to canonical record; merge metadata; emit `lead_duplicate_merged` event.

### 3.5 Accuracy

- **Definition**: agreement between Dealix's normalized fact and an independent ground truth.
- **Metric**: `(records_matching_truth / records_sampled)`.
- **Target**: ≥ 97% for high-stakes fields (`company_name`, `revenue_band`, `vertical`); ≥ 90% for inferred fields (`intent_score`, `buying_stage`).
- **Sampling**: weekly stratified sample of 200 records per source per tenant; ground truth from a paid third-party reference set or a manual reviewer.
- **Drift trigger**: 2 consecutive weeks below target → source is downgraded in `source_registry.py` priority.

## 4. Per-Stage Gate Matrix

| Stage | Completeness | Validity | Freshness (p95) | Uniqueness | Accuracy |
|---|---|---|---|---|---|
| 1 Source ingest | ≥ 99.0% | ≥ 99.5% | ≤ 5 s | ≥ 99.95% | sampled weekly |
| 2 Normalization | ≥ 99.5% | ≥ 99.7% | ≤ 8 s | ≥ 99.99% | sampled weekly |
| 3 Enrichment | ≥ 99.5% | ≥ 99.7% | ≤ 15 s (Sov) / 30 s (Growth) / 60 s (Starter) | ≥ 99.99% | ≥ 97% high-stakes |
| 4 Policy | ≥ 100.0% (all required evidence present) | ≥ 99.9% | ≤ 1 s | n/a | n/a |
| 5 Passport | ≥ 100.0% | ≥ 99.9% | ≤ 2 s | 100% (`passport_id` UUID) | derived from upstream |
| 6 Action dispatch | ≥ 99.9% | ≥ 99.9% | ≤ 30 s | 100% (idempotency key) | post-hoc by outcome |
| 7 Outcome capture | ≥ 99.5% | ≥ 99.5% | ≤ 2 s | ≥ 99.99% | sampled |

Where any gate is below target for 60 minutes, an alert fires per the SLO framework (slow-burn class).

## 5. Quarantine Queue

A single `quarantine` table partitioned by `tenant_id` and `quarantine_reason`. Each quarantined record carries:

- Original payload (encrypted at rest).
- Failed gate name + dimension.
- Failure detail (typed enum, never free text).
- `quarantined_at`, `tenant_id`, `source`, `stage`.
- `repair_attempts` count, `last_repair_at`.

Quarantine routing rules:

- **Auto-repair eligible** (validity fixable by deterministic rules, e.g. phone reformatting): goes to the auto-repair worker; retries within 5 min.
- **Manual-repair required** (accuracy, missing required field that can't be inferred): goes to the data-ops review queue.
- **Discarded** (PII without lawful basis, banned source, duplicate canonical): logged and deleted per PDPL retention rules.

## 6. Repair SLA

| Severity | Definition | Target time to repair |
|---|---|---|
| **Q1** | Sovereign tenant; blocks a passport; revenue-impacting. | ≤ 30 minutes |
| **Q2** | Growth tenant; blocks a passport. | ≤ 4 hours |
| **Q3** | Starter tenant; degrades but does not block. | ≤ 1 business day |
| **Q4** | Internal / no customer impact. | ≤ 1 week |

If repair fails 3 times, record is escalated to data-ops lead.

Quarantine queue depth itself is an SLI: `queue_depth_p95 ≤ 200 records` global, ≤ 10 records per Sovereign tenant.

## 7. Implementation

- Gate implementations live in `auto_client_acquisition/revenue_os/quality_gates.py` (to be added).
- Each gate is a function `(record, context) -> GateResult` with `passed: bool` and `failures: list[GateFailure]`.
- Gates are pure and composable; the orchestrator runs them at stage boundaries.
- Failure types are an exhaustive enum: `MISSING_REQUIRED`, `INVALID_FORMAT`, `STALE`, `DUPLICATE`, `ACCURACY_DRIFT`, `POLICY_VIOLATION`.
- Every quarantine event is an immutable record in the event store (per ADR-0001) so the audit trail survives repair.

## 8. Observability

Per ADR-0004:

- Metric `quality_gate_evaluations_total{stage, dimension, result}`.
- Metric `quarantine_queue_depth{tenant_id, severity}`.
- Trace span `quality_gate.evaluate` per gate, attribute `dimension`, `result`.
- Dashboards: one row per stage, columns per dimension, time series of pass rate.

## 9. Governance and Change Management

- Adding or modifying a gate requires:
  - PR review with Head of Data + CTO.
  - Pre-merge: shadow-run on production data for 24 h with delta report (records newly passing or failing).
  - Backward compatibility: a tightened gate runs in "warn-only" mode for 7 days before "enforce".
- Quarterly review: gates that have not fired in 90 days are reviewed for removal (false-economy gates add latency without value).

## 10. Data Quality SLO Roll-Up

A single roll-up SLI: **DQ-Pass-Rate** = `(records_passing_all_gates / records_evaluated)` per tenant per day.

Targets:

- Starter: ≥ 98%.
- Growth: ≥ 99%.
- Sovereign: ≥ 99.5%.

This number is reported in the executive KPI spec dashboard (W4.T13) and in the monthly customer success review.

## 11. References

- ADRs: ADR-0001 (event store), ADR-0003 (multi-tenant), ADR-0004 (observability).
- Code: `auto_client_acquisition/revenue_os/source_registry.py`, `auto_client_acquisition/revenue_os/signal_normalizer.py`, `auto_client_acquisition/revenue_os/enrichment_waterfall.py`, `dealix/trust/policy.py`.
- Related docs: `docs/DATA_MAP.md`, `docs/policy/revenue_os_policy_rules.md`, `docs/sre/slo_framework.md`, `docs/analytics/event_taxonomy.md`.
- Compliance: `docs/PRIVACY_PDPL_READINESS.md`, `docs/ops/PDPL_RETENTION_POLICY.md`.
