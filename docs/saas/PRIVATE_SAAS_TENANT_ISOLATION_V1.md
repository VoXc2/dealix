# Dealix Private SaaS — Tenant Isolation V1

## Mission

Prepare Dealix for **private / invite-only multi-tenant SaaS** without turning architectural readiness into a production claim.

This lane does not activate PostgreSQL RLS, mutate a production database, open public self-serve signup, change billing authority, or create a second Company OS.

## Current truth on `main@1fc9cce4417a98cbd2f767dd4d7234ac1381d06e`

The repository already has meaningful tenant foundations:

- server-side tenant authority in `api/security/tenant_scope.py`;
- transaction-local PostgreSQL tenant binding in `db/tenant_session.py`;
- defensive object/list isolation helpers;
- RBAC, SAML, SCIM, audit, usage, jobs and billing surfaces carrying tenant context;
- RLS policy definitions in `db/rls_policies.py`.

However, RLS is deliberately not a production boundary yet. Request sessions are not universally bound through `tenant_session()`, real PostgreSQL `SET LOCAL` semantics are skipped without an isolated acceptance database, and the current policy map is incomplete/internally inconsistent with the ORM inventory.

## V1 inventory result

Static inspection of explicit SQLAlchemy models currently finds:

- 63 tables with an explicit `tenant_id`;
- 23 of those names covered by current `RLS_POLICIES`;
- 1 explicit exemption (`background_jobs`);
- 39 explicit tenant tables pending RLS classification/review;
- 8 RLS policy names that do not map to an explicit-`tenant_id` ORM model in the same inventory.

`config/saas/tenant_boundary_registry_v1.json` freezes those two review sets. `scripts/ops/verify_tenant_boundary_registry_v1.py` fails closed if the ORM/RLS inventory drifts without updating the registry.

The verifier has two meanings:

1. default mode proves **inventory synchronization**;
2. `--activation-ready` is expected to remain non-zero until every pending/mismatch item is resolved.

A green inventory check is **not** permission to execute `apply_rls()`.

## Required activation sequence

1. Classify every pending table as tenant-RLS or a narrowly justified system/global exception.
2. Resolve stale/mismatched policy names against actual schema ownership.
3. Bind the application request DB lifecycle to transaction-local tenant context.
4. Use an isolated PostgreSQL acceptance database and the same application DB role as production.
5. Prove the DB role is not superuser and does not have `BYPASSRLS` where RLS is relied on.
6. Run a two-tenant denial matrix for ordinary users, explicit mismatch, super-admin explicit override, object-ID horizontal access, missing tenant, and pooled connection reuse.
7. Prove tenant propagation through async jobs, cache keys, idempotency keys, object/file storage, rate limits/quotas, webhooks and audit events.
8. Prove invite-only onboarding, revocation/offboarding, DSAR export, retention/deletion and completion receipts.
9. Prove tenant-aware observability without sensitive payload leakage.
10. Only then enable RLS in Test, re-run the matrix, and prepare an exact production migration packet.

## Commercial posture

Dealix remains discovery/quote-first. The current public `/signup -> /book` behavior must not be removed merely to make a generic SaaS checklist green. The first productized SaaS target is **private/invite-only**, where tenancy, entitlements, lifecycle, evidence and governance are proven before public self-service.

## Entitlement boundary

Feature authorization currently reaches into `BillingService`. Before private SaaS activation, introduce one tenant entitlement authority that owns feature/limit/override decisions and audit provenance. Billing/payment/provider state may feed that authority, but provider outages, invoice states or webhook delays must never silently widen access.

## Truth firewall

- architecture prepared != SaaS production ready;
- tenant_id present != tenant isolation proven;
- RLS policy defined != RLS active/safe;
- HTTP 200 != exact-release parity;
- subscription row != payment evidence;
- synthetic/demo record != customer proof;
- public contact != consent;
- draft != sent.

`PRIVATE_SAAS_ACTIVATION_READY=false` until the activation sequence is proven with exact receipts.
