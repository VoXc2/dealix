# Gap closure evidence — Postgres-first critical paths

| Field | Value |
| --- | --- |
| **Matrix gap** | In-memory fallback on critical operational paths |
| **Owner OS** | Platform + Control Plane |
| **Artifact** | `db/migrations/versions/20260515_011_enterprise_control_plane.py`, `dealix/transformation/jsonl_migration_catalog.yaml` |
| **KPI impact** | `governance_integrity_rate`, `tenant_isolation_violation_count` (see `kpi_baselines.yaml`) |
| **Risk impact** | Data loss / split-brain if silent fallback hides persistence failures |
| **Verification** | `python3 scripts/verify_global_ai_transformation.py` |
| **PR / engineering note** | Control-plane tables + explicit backend flags (`VALUE_LEDGER_BACKEND`, `PROOF_LEDGER_BACKEND`, operational stream mirror). |

**Closure statement:** Critical-path persistence is Postgres-capable with explicit env cutover and documented rollback (remain on JSONL/file until `engineering_cutover_policy.yaml` signal).
