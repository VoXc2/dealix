---
title: ADR-0002 Async Boundaries — FastAPI async routers, SQLAlchemy async sessions, sync fallback rules
doc_id: W4.T21.adr-0002-async-boundaries
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T21.adr-0001, W4.T21.adr-0003, W4.T21.adr-0004, W4.T22.event-store-async-migration]
kpi: { metric: p95_latency_ms_revenue_os, target: 250, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.85, effort: 8pw, score: engineering }
---

# ADR-0002: Async Boundaries

> **Decision: All HTTP routers under `api/v1/` are `async def`; all database access uses SQLAlchemy 2.0 async sessions; synchronous code is permitted only for CPU-bound work, third-party libraries without async support, and Alembic migrations.**

## Context

Dealix concurrency model is a mixture of:

- Inbound HTTP from the SPA (~120 RPS sustained, 600 RPS peak).
- Outbound calls to enrichment APIs (Apollo, Clearbit-equivalent, Saudi business registries) with 200–1,500 ms latency each.
- LLM calls (Anthropic, OpenAI) with 600–4,000 ms latency.
- PostgreSQL reads/writes (< 50 ms p95).

Current state in `api/routers/decision_passport.py` and `api/v1/revenue-os/*`: mixed sync and async handlers. Sync handlers block the event loop, causing tail-latency spikes (p99 observed at 2.1 s during enrichment storms in March 2026). A single sync DB call inside an `async def` route silently blocks the loop and degrades all concurrent requests.

Latency budget end-to-end for `/api/v1/revenue-os/lead/enrich`:

- p50 target: 120 ms
- p95 target: 250 ms
- p99 target: 800 ms

To hit p95 ≤ 250 ms while making 1–3 outbound calls, we cannot afford loop-blocking on any handler.

## Decision

1. **Routers**: Every handler in `api/v1/**` is `async def`. Lint rule (`ruff` custom check `DLX001`) fails CI on sync handlers under `api/v1/`.
2. **Database**: `SQLAlchemy 2.0` async engine + `AsyncSession`. Single `get_async_session()` dependency. The synchronous engine is retained only for Alembic migrations and offline scripts under `scripts/`.
3. **Event store**: `pg_event_store.py` exposes both async (`append_async`, `read_stream_async`) and sync wrappers. Production code paths call async; sync wrappers exist only for migrations and test utilities.
4. **HTTP clients**: `httpx.AsyncClient` for all outbound calls. Connection pool size: 100 per worker, keepalive 30 s. Timeout default: 8 s; override per integration in `source_registry.py`.
5. **CPU-bound work** (PDF render, embedding hashing, regex-heavy parsing > 50 ms): offload to `asyncio.to_thread` with a bounded executor (max workers = CPU count × 2).
6. **Sync fallback allowed** only when:
   - The library has no async equivalent (e.g. `pdfplumber`, certain ZATCA SDKs).
   - The call is wrapped in `asyncio.to_thread` so the loop is never blocked.
   - The duration p95 is ≤ 30 ms (otherwise must be moved to a worker queue).
7. **Background jobs**: `arq` (Redis-backed) for queued work; jobs are `async def`. Long-running batch (> 30 s) goes to a dedicated worker pool, not the API process.
8. **Orchestrator** (`auto_client_acquisition/orchestrator/runtime.py`): exposes async entrypoints. Existing sync entrypoint is deprecated as of this ADR; removal in v1.4.

## Status

`Proposed` — under review. Target acceptance: 2026-05-22. Effective: 2026-06-01 with 60-day grace period for sync handler removal.

## Consequences

### Positive

- Eliminates loop-blocking class of incidents (4 in Q1 2026, ~12 hours triage each).
- Restores p99 < 800 ms target; modeled p99 after migration: 540 ms.
- Outbound concurrency: a single worker handles ~80 in-flight enrichment calls vs. ~6 in sync mode.
- Halves worker count needed at peak (cost saving ≈ 320 USD/month at current scale).
- Aligns with `pg_event_store` async-first API (ADR-0001).

### Negative

- Async correctness is harder to debug; requires upskilling. Estimated training cost: 1 person-week per engineer × 4 engineers = 4 person-weeks.
- Mixing sync and async via `to_thread` adds context-switch cost (~50 µs); only material for hot paths.
- Async stack traces in Sentry are noisier; needs custom grouping rules (see ADR-0004).
- Testing requires `pytest-asyncio` discipline; ~3 person-weeks to migrate existing test suite.

### Neutral / Follow-ups

- Add `ruff` custom rule `DLX001` (no sync handlers in `api/v1/`).
- Add `pytest` fixture `async_session` and deprecate `sync_session` outside of migration tests.
- Document the `to_thread` budget (CPU-bound budget < 50 ms p95) in `docs/engineering/event_store_async_migration.md`.
- Decision passport tracer (ADR-0004) must propagate `contextvars` across `to_thread` boundaries.

## Alternatives Considered

| Alternative | Reason rejected |
|---|---|
| **A. All-sync with thread pool sized to peak (200 threads)** | Memory cost ≈ 8 MB/thread × 200 = 1.6 GB per worker; ~3× the cost; tail-latency under load still 4× async due to GIL contention on the JSON serialization path. |
| **B. Mixed sync/async, no enforcement** | Status quo; produced 4 incidents in 90 days; not maintainable. |
| **C. Move to a non-Python runtime (Go/Rust) for the API** | Rewrite cost > 30 person-weeks; deferred until v2.0; not warranted at current scale. |
| **D. Sync API + async workers only** | Doesn't solve the inbound burst problem; SPA pre-fetch causes 600 RPS peaks that overload sync workers. |

## References

- Code: `api/routers/decision_passport.py`, `api/v1/revenue-os/*`, `auto_client_acquisition/orchestrator/runtime.py`.
- SQLAlchemy 2.0 async docs.
- httpx async client.
- Related ADRs: ADR-0001 (event store), ADR-0004 (observability).

## Review Cadence

Quarterly. Re-evaluate if sustained RPS exceeds 1,500 or if a hot CPU-bound path emerges that cannot fit the 50 ms `to_thread` budget.
