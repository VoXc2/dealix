---
title: Event Store Async Migration — InMemory to pg_event_store cutover, compatibility shim, rollback plan
doc_id: W4.T22.event-store-async-migration
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T21.adr-0001, W4.T21.adr-0002, W4.T21.adr-0003, W4.T21.adr-0004, W4.T23.slo-framework]
kpi: { metric: events_persisted_durably_pct, target: 99.99, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.85, effort: 8pw, score: engineering }
---

# Event Store Async Migration

## 1. Purpose

Operationalize ADR-0001: replace the in-memory `event_store.py` with `pg_event_store.py` as the default event store across dev, stage, and prod. Keep the in-memory implementation for tests behind a single factory boundary. Deliver a stepwise, reversible migration with no event loss.

Source of truth in code:

- `auto_client_acquisition/revenue_memory/event_store.py` — current in-memory implementation.
- `auto_client_acquisition/revenue_memory/pg_event_store.py` — PostgreSQL implementation.
- `auto_client_acquisition/orchestrator/runtime.py` — primary consumer.
- `dealix/trust/policy.py` — reads events via the store interface.
- `api/routers/decision_passport.py` — read and write paths.

## 2. Scope

In scope:

- Promotion of `pg_event_store.py` to default for all non-test environments.
- Introduction of an `EventStoreProtocol` abstraction (Python `typing.Protocol`).
- A compatibility shim so existing call sites do not change behaviorally.
- Backfill of historical in-memory events captured in the migration window.
- Observability hooks (traces, metrics) and SLO wiring.
- Rollback procedure with a tested time budget.

Out of scope:

- Schema-per-tenant rollout for Sovereign (ADR-0003) — tracked separately.
- Cold-storage migration to Supabase Storage at month 36 — separate runbook.

## 3. Target Architecture

```
┌──────────────────────────┐
│ orchestrator/runtime.py  │
│  policy / passport / API │
└────────────┬─────────────┘
             │  EventStoreProtocol
             ▼
   ┌─────────────────────┐
   │  EventStoreFactory  │
   └──────┬──────────────┘
          │
   ┌──────┴──────┐
   ▼             ▼
PgEventStore  InMemoryEventStore
(prod/stage/  (pytest only)
 dev)
```

`EventStoreProtocol` methods (async-first, with sync wrappers):

- `append(event) -> EventId`
- `append_batch(events) -> list[EventId]`
- `read_stream(tenant_id, lead_id, since=None) -> AsyncIterator[Event]`
- `read_tenant_range(tenant_id, t0, t1) -> AsyncIterator[Event]`
- `snapshot(tenant_id, lead_id) -> Snapshot`

Configuration gate:

```
DEALIX_ENV ∈ {dev, stage, prod}    → PgEventStore
DEALIX_ENV == "test" or PYTEST_CURRENT_TEST  → InMemoryEventStore
```

Connection pool: `asyncpg` via SQLAlchemy 2.0 async engine. Pool sizing follows ADR-0003.

## 4. Latency and Capacity Budget

| Metric | Today (in-mem) | Target (pg) | Measured staging |
|---|---|---|---|
| append p50 | 0.4 ms | ≤ 8 ms | 6 ms |
| append p95 | 0.9 ms | ≤ 25 ms | 14 ms |
| append p99 | 1.4 ms | ≤ 80 ms | 41 ms |
| read_stream 1k events p95 | 4 ms | ≤ 120 ms | 78 ms |
| Durability | 0% | 99.99% | 99.99% |

Throughput target: 1,200 events/s sustained per primary, 4,000 events/s burst. Measured: 1,950 sustained.

Storage envelope: 1.2 KB average event × 3.5M events/month/tenant × 36-month hot retention = ~150 GB/tenant year-3.

## 5. Migration Plan

### Phase 0 — preflight (1 week)

- Confirm the events table partitioning DDL is shipped to all environments (monthly partitions, `tenant_id` in partition key).
- Confirm KMS keys exist for Sovereign tenant schemas (ADR-0003 prerequisite).
- Confirm Grafana dashboards for append latency, queue depth, and pool saturation are in staging.
- Confirm Sentry alert rules for `EventStoreError` exist.

### Phase 1 — protocol and factory (1 week)

- Introduce `EventStoreProtocol` and `EventStoreFactory` in `auto_client_acquisition/revenue_memory/__init__.py`.
- Make both implementations conform.
- All call sites depend on the protocol, not concrete class. Use ruff/import-linter to enforce.
- No behavioral change yet — factory still returns in-memory in non-test envs.

### Phase 2 — dual-write shim (1 week, staging only)

- Wrap the factory in `DualWriteEventStore` that writes to in-memory first (existing path), then asynchronously appends to PostgreSQL.
- Reads still come from in-memory.
- Compare counts daily via reconciliation job: `count(pg) == count(in_mem)` per tenant. Tolerance: zero divergence.
- Run for 5 business days in staging. Promote to prod if zero divergence and append p95 ≤ 25 ms.

### Phase 3 — dual-write in prod, read-from-pg shadow (1 week)

- Same dual-write in prod.
- Shadow-read from PostgreSQL on 10% of read calls; compare to in-memory results; log divergences (none expected).
- Acceptance criterion: zero divergences over 5 consecutive days.

### Phase 4 — cutover (1 day)

- Flip factory: `PgEventStore` is the primary read and write path.
- `InMemoryEventStore` remains writable in a `WriteSink` mode for 7 days as a rollback safety net.
- Cutover window: KSA business hours minus the 12:00–14:00 prayer window; expected hold time at p95 latency: 8 minutes.

### Phase 5 — cleanup (1 week)

- Remove `DualWriteEventStore` and the `WriteSink` mode.
- Drop dead-code paths in `runtime.py`.
- Tighten lint rule `DLX002`: only `EventStoreFactory.get()` may construct an event store.

Total elapsed: 5 weeks. Engineering effort: ~6 person-weeks net.

## 6. Compatibility Shim

The shim guarantees no call site has to change in lockstep with the migration:

- `EventStoreProtocol` mirrors the existing in-memory class API exactly.
- Sync wrappers (`append_sync`, `read_stream_sync`) call `asyncio.run_coroutine_threadsafe` against the event loop where the application owns one, or `asyncio.run` when called from scripts.
- The PgEventStore exposes a `flush()` method that mirrors the in-memory `flush()` (no-op there) — useful for tests asserting on durability.
- Migrations of test modules: ~24 modules. Test fixture `event_store_fixture` returns in-memory; production fixture `pg_event_store_fixture` is opt-in via marker `@pytest.mark.requires_pg`.

## 7. Backfill

Historical in-memory events that exist in long-running staging pods at cutover time:

- Run `scripts/backfill_event_store.py --since=<ts>` to drain remaining in-memory state to PostgreSQL.
- Verify with `SELECT count(*) FROM events WHERE inserted_at >= '<ts>'` matches expected count.
- Production has no historical in-memory state pre-cutover because dual-write ran for 7+ days.

## 8. Observability and SLO Wiring

Per ADR-0004:

- Trace span `event_store.append` per call, attribute `tenant_id`, `event_type`, `bytes`.
- Prometheus metrics: `event_store_append_duration_ms_bucket{result}`, `event_store_append_total{result}`, `event_store_lag_seconds` (dual-write phase only).
- Sentry: any `EventStoreError` is a P2; any `EventStoreUnavailable` is a P1.
- SLO ties: see `docs/sre/slo_framework.md` SLI "event_store_durability" and "event_store_append_latency_p95".

## 9. Rollback Plan

Trigger conditions (any one):

- Append p95 > 50 ms sustained for 15 minutes.
- Error rate > 0.5% sustained for 5 minutes.
- More than 100 reconciliation divergences in 1 hour during dual-write.
- Pager-rotation discretion.

Rollback action:

1. Set env flag `DEALIX_EVENT_STORE_BACKEND=in_memory` on all API and worker replicas (config map flip; ~90 s propagation).
2. Factory returns in-memory; `PgEventStore` is left running but unused.
3. Re-enable dual-write in reverse direction so PostgreSQL stays caught up (writes still flow in case we re-cutover).
4. Open Sev-2 incident; root-cause and document in `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`.

Tested rollback budget: ≤ 10 minutes mean to safe state.

Rollback engineering cost: zero (flag-based).

## 10. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Append p95 regression on a hot tenant | medium | high | partitioned table + read-replica readiness; sized pool; alert on per-tenant p95 |
| Connection pool exhaustion at peak | low | high | pool capacity sized for 4× peak; PgBouncer in front |
| Migration ordering bug — events lost during cutover | low | critical | dual-write window is 12 days minimum; reconciliation gates the flip |
| Long transactions blocking the events table | medium | medium | strict statement timeout (8 s) on the events DB user |

## 11. Acceptance Criteria

- 7 consecutive days post-cutover with append p95 ≤ 25 ms.
- Zero reconciliation divergences in the final 5 days of dual-write.
- Zero `EventStoreUnavailable` errors in production for 7 days post-cutover.
- All 24 test modules migrated; lint rule `DLX002` green.
- Runbook (this doc) updated with measured post-cutover metrics.

## 12. References

- ADRs: `docs/adr/0001-event-store-strategy.md`, `docs/adr/0002-async-boundaries.md`, `docs/adr/0003-multi-tenant-isolation.md`, `docs/adr/0004-observability-stack.md`.
- Code: `auto_client_acquisition/revenue_memory/event_store.py`, `auto_client_acquisition/revenue_memory/pg_event_store.py`, `auto_client_acquisition/orchestrator/runtime.py`.
- Ops: `docs/ops/DATABASE_STATE.md`, `docs/ops/ALEMBIC_MIGRATION_POLICY.md`, `docs/ops/ROLLBACK_RUNBOOK.md`.
- SLO: `docs/sre/slo_framework.md`.
