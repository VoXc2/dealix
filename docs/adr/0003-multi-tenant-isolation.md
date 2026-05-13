---
title: ADR-0003 Multi-Tenant Isolation — tenant_id row-level for Starter/Growth, schema-per-tenant for Sovereign
doc_id: W4.T21.adr-0003-multi-tenant-isolation
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T21.adr-0001, W4.T21.adr-0002, W4.T21.adr-0004, W4.T14.revenue-os-policy-rules, W1.T31.revenue-memory]
kpi: { metric: cross_tenant_data_leak_incidents, target: 0, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.85, effort: 10pw, score: engineering }
---

# ADR-0003: Multi-Tenant Isolation

> **Decision: Starter and Growth tenants share a single PostgreSQL schema with `tenant_id` row-level isolation enforced by RLS policies; Sovereign tenants get a dedicated schema (`tenant_<uuid>`) inside the same database, with separate connection pool and per-schema KMS key.**

## Context

Dealix sells three tiers with materially different isolation requirements:

| Tier | Monthly price (SAR) | Tenant count target Y1 | Data residency clause | SLA |
|---|---|---|---|---|
| Starter | 1,490 | 200 | KSA preferred, not contractual | 99.5% |
| Growth | 4,900 | 80 | KSA contractual | 99.7% |
| Sovereign | 24,000+ | 8 | KSA dedicated, named DPA, regulator-ready audit | 99.95% |

Sovereign customers (typically regulated entities — banks, ministries, family offices) have repeatedly asked for:

1. Cryptographic isolation of their event stream and lead records.
2. The ability to disconnect their schema during incidents elsewhere without affecting their own service.
3. Per-tenant retention overrides (e.g. 84-month retention on a single dataset).
4. Per-tenant audit log export to their own SIEM.

A pure row-level model satisfies (1) only weakly (single misplaced filter leaks data) and fails (2) and (4). A full database-per-tenant model is operationally infeasible at 200+ tenants. Hybrid is the only viable shape.

Code anchors:

- `auto_client_acquisition/revenue_os/source_registry.py` — must scope sources per tenant.
- `auto_client_acquisition/revenue_memory/pg_event_store.py` — must route writes by tenant tier.
- `dealix/trust/policy.py` — must apply tier-specific policy thresholds.

## Decision

**Hybrid isolation model with one PostgreSQL instance per region.**

1. **Shared schema `public`** for Starter and Growth. Every table that holds tenant data has `tenant_id UUID NOT NULL`. PostgreSQL **Row-Level Security** policies enforce `tenant_id = current_setting('dealix.tenant_id')::uuid`. Application sets `SET LOCAL dealix.tenant_id` per request inside the async session middleware.
2. **Dedicated schema `tenant_<uuid>`** for each Sovereign tenant. Same table shapes, no RLS (schema search_path provides the boundary). Migrations are applied to every Sovereign schema by the deploy pipeline.
3. **Connection pools**: shared pool (50 conns) for Starter/Growth; per-Sovereign pool (10 conns each). Total pool budget per API replica: 50 + 10 × N_sovereign.
4. **Encryption at rest**: AES-256 (KMS managed) globally; Sovereign tenants get a per-schema KMS key for column-level encryption of PII fields (lead email, phone).
5. **Audit log routing**: every privileged action goes to `audit_log` in the tenant's home schema; Sovereign exports daily to the tenant's S3 bucket via signed URL.
6. **Index strategy**: every shared table has `(tenant_id, <natural_key>)` as the primary or first composite index. The events table is partitioned monthly with `tenant_id` in the partition key for prune efficiency.

**Out of scope**: separate database instances per tenant, cross-region replication for Sovereign (handled by ADR-0007 when written).

Owner of record: CTO.

## Status

`Proposed` — pending CTO + Compliance sign-off. Target acceptance: 2026-05-25. Effective: 2026-06-15 (with Sovereign migration in two waves).

## Consequences

### Positive

- Cross-tenant data leakage requires bypassing both ORM filter and RLS policy — defense in depth.
- Sovereign tenants get auditable schema isolation without the cost of separate instances (~70% cheaper than instance-per-tenant).
- Per-Sovereign rollback or restore becomes possible (schema-level `pg_dump`).
- Per-schema KMS rotation possible without affecting other tenants.
- Compliance posture: PDPL Article 13 (controlled access) and proposed SAMA cybersecurity controls aligned.

### Negative

- Operational complexity: migrations must run N+1 times (N Sovereign + 1 shared). Estimated migration runtime at 8 Sovereign tenants: ~3 minutes vs. 30 seconds. Mitigation: parallelized in CI.
- RLS adds 3–7 ms per query on shared schema. Within the 50 ms DB budget.
- Connection pool sizing must grow O(Sovereign tenants). At 20 Sovereign tenants the per-replica pool is ~250 conns — manageable up to ~40 Sovereign before re-architecting.
- Test fixtures need a `set_tenant_context()` helper; ~2 person-weeks refactor across ~30 test modules.
- Backup strategy diverges: `pg_basebackup` for shared, plus per-schema logical dumps for Sovereign.

### Neutral / Follow-ups

- Update `docs/ops/DATABASE_STATE.md` with schema inventory and naming convention.
- Add Grafana panel: per-Sovereign connection pool saturation, RLS rule hit rate.
- Document tenant-onboarding runbook: schema creation, KMS key provisioning, search_path setup.
- Define the Sovereign tenant offboarding flow: schema export, key destruction certificate.

## Alternatives Considered

| Alternative | Reason rejected |
|---|---|
| **A. Single shared schema with row-level isolation only** | Fails Sovereign contractual isolation language; cannot per-tenant restore; per-tenant retention overrides require app-level filters that ORM cannot enforce. |
| **B. Database-per-tenant for all tiers** | At 280 tenants Y1, ops cost (backups, migrations, connection pools) exceeds 1.2 SRE FTE. Storage overhead alone ~9× shared. |
| **C. Sharded clusters by region** | Premature — at projected 2026 volume a single primary handles it. Adds Citus or Vitess complexity for no current win. |
| **D. Schema-per-tenant for all** | Migrations time linearly with tenant count; at 200 tenants migration windows exceed 30 minutes — incompatible with continuous deploy. |
| **E. Logical replication to per-tenant slave for Sovereign** | Replication lag (1–3 s) is not acceptable for Sovereign 99.95% SLO; complex failover; deferred until v2. |

## References

- Code: `auto_client_acquisition/revenue_memory/pg_event_store.py`, `dealix/trust/policy.py`, `api/v1/revenue-os/*`.
- PostgreSQL Row-Level Security docs.
- PDPL Articles 13, 19, 23 (controlled access, cross-border, breach).
- Related ADRs: ADR-0001 (event store), ADR-0002 (async boundaries), ADR-0004 (observability).
- Pricing: `docs/PRICING_AND_PACKAGING_V6.md`.

## Review Cadence

Quarterly. Re-evaluate at 40 Sovereign tenants (connection pool inflection) or if a single Sovereign exceeds 100M events/month (consider extracting to its own instance).
