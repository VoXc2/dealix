---
title: ADR-0001 Event Store Strategy — pg_event_store canonical, in-memory for tests
doc_id: W4.T21.adr-0001-event-store-strategy
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T22.event-store-async-migration, W4.T21.adr-0002, W4.T21.adr-0003, W1.T31.revenue-memory]
kpi: { metric: event_persistence_durability_pct, target: 99.99, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.9, effort: 6pw, score: engineering }
---

# ADR-0001: Event Store Strategy

> **Decision: We will use `pg_event_store.py` (PostgreSQL-backed) as the canonical event store in dev, stage, and prod for every tenant, and restrict `event_store.py` (in-memory) to unit tests and ephemeral local smoke runs.**

## Context

Dealix Revenue OS is event-sourced. Every lead enrichment, policy check, decision passport emission, and outbound action is captured as an immutable event. Today the repo contains two implementations:

- `auto_client_acquisition/revenue_memory/event_store.py` — in-memory list, no persistence, sub-millisecond append, used since v5.
- `auto_client_acquisition/revenue_memory/pg_event_store.py` — PostgreSQL append-only table with composite index on `(tenant_id, lead_id, occurred_at)`.

Observed pain points (Q1 2026):

- **Data loss on restart**: 4 incidents in last 90 days where in-memory store lost between 200 and 1,800 events on container recycle. Mean recovery cost: 3.5 engineering-hours per incident.
- **Inconsistent decision passports**: passports referencing events that no longer existed after a deploy. Trust impact: 2 customer escalations.
- **Multi-tenant blast radius**: a single OOM kill wipes events for all tenants. Sovereign tier contractually requires per-tenant durability (99.99%).
- **Audit gap**: PDPL Article 13 requires retention of evidence-of-processing for a minimum 24 months; in-memory cannot satisfy this.

Latency budget for write path: p95 < 25 ms append, p99 < 80 ms. Measured `pg_event_store` p95 on staging: 14 ms; p99: 41 ms. Within budget.

Storage envelope: 1.2 KB average event size × 3.5M events/month per tenant × 36-month retention = ~150 GB/tenant at year-3. PostgreSQL with partitioning handles this without sharding until ~50 tenants.

## Decision

**`pg_event_store.py` is the default and only persistence path in shipped environments.** Concretely:

1. `EventStore` factory in `auto_client_acquisition/revenue_memory/__init__.py` returns `PgEventStore` when `DEALIX_ENV in {dev, stage, prod}`.
2. Returns `InMemoryEventStore` only when `PYTEST_CURRENT_TEST` is set or `DEALIX_ENV == "test"`.
3. Both implementations share the abstract `EventStoreProtocol` (append, read_stream, read_tenant_range, snapshot).
4. Sovereign tier uses a dedicated PostgreSQL schema per tenant (see ADR-0003).
5. Retention: 36 months hot in primary, then move to cold object storage (Supabase Storage) with metadata pointer; total 84 months retention.

Migration follows the plan in `docs/engineering/event_store_async_migration.md` (W4.T22).

## Status

`Proposed` — pending CTO + Head of Data sign-off. Target acceptance: 2026-05-20. Effective: 2026-06-01.

## Consequences

### Positive

- Durability moves from 0% (in-memory) to 99.99% (Postgres + WAL + daily logical backup).
- Eliminates the 4-per-quarter event loss incident class — estimated 14 engineering-hours/quarter saved.
- Decision passports become legally defensible: events referenced are guaranteed to exist for ≥36 months.
- Unlocks Sovereign tier (99.95% availability SLO requires durable storage).
- Enables async read replicas for analytics without affecting write path.

### Negative

- Write-path latency increases from sub-millisecond to 14 ms p95 (+13.5 ms). Acceptable within the 25 ms budget but consumes ~5% of the end-to-end 250 ms p95 envelope.
- Adds PostgreSQL operational burden: connection pooling, vacuum, partition management, replica monitoring. Estimated +0.4 SRE FTE.
- Storage cost: ~150 GB/tenant year-3 at ~0.10 USD/GB-month = 15 USD/tenant/month. Recovered via Sovereign price uplift.
- Test suite must wire `InMemoryEventStore` explicitly; one-time refactor of ~24 test modules, ~3 person-weeks.

### Neutral / Follow-ups

- Update `docs/ops/DATABASE_STATE.md` with new table inventory.
- Add Grafana dashboard panel: events-per-second per tenant, append p95/p99.
- Define schema migration SOP for the events table (see ADR-0002 async boundaries for connection handling).

## Alternatives Considered

| Alternative | Reason rejected |
|---|---|
| **A. Keep in-memory + periodic snapshot to S3** | Snapshot interval (15 min) means up to 15 min of events lost on crash; fails PDPL durability and Sovereign SLA. |
| **B. Kafka / Redpanda as canonical log** | Operational complexity for a 3-engineer team; estimated +0.8 SRE FTE; vendor cost ~1,800 USD/month; overkill at current 3.5M events/month/tenant. |
| **C. DynamoDB / managed NoSQL** | Cross-region data residency for KSA is unresolved with AWS at time of decision; PDPL transfer review adds 8 weeks; PostgreSQL already in stack. |
| **D. EventStoreDB (specialized)** | Single-vendor lock-in; team has zero ops experience; no clear win over PostgreSQL at current volume. |

## References

- Code: `auto_client_acquisition/revenue_memory/event_store.py`, `auto_client_acquisition/revenue_memory/pg_event_store.py`, `auto_client_acquisition/orchestrator/runtime.py`.
- Migration plan: `docs/engineering/event_store_async_migration.md`.
- Related ADRs: ADR-0002 (async boundaries), ADR-0003 (multi-tenant isolation), ADR-0004 (observability).
- Compliance: `docs/PRIVACY_PDPL_READINESS.md`, `docs/ops/PDPL_RETENTION_POLICY.md`.

## Review Cadence

Quarterly. Re-evaluate when sustained event rate exceeds 50M/month/tenant or when the tenant count passes 40 (sharding inflection point).
