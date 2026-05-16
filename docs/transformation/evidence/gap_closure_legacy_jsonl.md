# Gap closure evidence — JSONL catalog and tiered migration

| Field | Value |
| --- | --- |
| **Matrix gap** | Legacy JSONL outside critical control paths |
| **Owner OS** | Platform + Value + Delivery |
| **Artifact** | `dealix/transformation/jsonl_migration_catalog.yaml`, `value_ledger_events` + `operational_event_streams` (Alembic `012`) |
| **KPI impact** | `measured_customer_value_sar`, operational audit completeness |
| **Risk impact** | Orphan files on disk if mirror disabled; dual-write drift if misconfigured |
| **Verification** | `python3 scripts/verify_global_ai_transformation.py --check-jsonl` |

**Closure statement:** JSONL usage is catalogued with tiers, Postgres targets, and optional `DEALIX_OPERATIONAL_STREAM_BACKEND` mirroring for tier-2 append paths; tier-1 value ledger supports `postgres`/`dual`.

---

## Verification record (reference)

Command:

```bash
python3 scripts/verify_global_ai_transformation.py --check-jsonl
```

Last captured output (trimmed):

```text
GLOBAL AI TRANSFORMATION: PASS
```

**KPI numeric closure:** tie `measured_customer_value_sar` and operational completeness metrics in [dealix/transformation/kpi_baselines.yaml](dealix/transformation/kpi_baselines.yaml) once finance exports exist.
