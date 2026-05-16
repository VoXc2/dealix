# Enterprise Readiness Model

## Gate sequence
1. Stability (compile/import/lint)
2. Tenant Isolation (`tenant_id` on operational objects)
3. Governance Proof (approval-first rollback/policy edit/contracts)
4. Runtime Safety + Value Evidence
5. End-to-End Revenue Control Plane
6. UI Surfaces + Persistence + CI

## Readiness levels
- **Client Pilot Ready:** all gates pass once with deterministic evidence.
- **Enterprise Ready:** all gates pass across 3 tenants with Postgres + UI + CI.
- **Mission Critical Ready:** failure drills, rollback drills, and observability coverage are automated.
