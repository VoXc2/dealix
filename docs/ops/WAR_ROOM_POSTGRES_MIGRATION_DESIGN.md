# War Room — Postgres migration design (post-JSON stabilization)

**Status:** design only — implement after War Room JSON MVP is stable for 2+ weeks.

## Target tables

| Table | Purpose |
|-------|---------|
| `war_room_targets` | One row per funnel lead / target; mirrors `FunnelLeadRecord` war-room columns |
| `war_room_status_history` | Optional audit of `war_room_status` transitions |

## Event bridge

Append `EvidenceEvent` payloads to `revenue_events` via existing [isolated_pg_event_store.py](../../auto_client_acquisition/revenue_memory/isolated_pg_event_store.py):

- `event_type` = `war_room_*` from [war_room.py](../../dealix/revenue_ops_autopilot/war_room.py) `CRITICAL_OUTREACH_EVENTS`
- `entity_id` = `lead_id`

## Migration steps

1. Alembic revision: `war_room_targets` with FK optional to `commercial_engagements` when wired.
2. Backfill script: read `var/revenue_ops_autopilot.json` → upsert rows.
3. Feature flag `DEALIX_WAR_ROOM_STORE=postgres|json` in [store.py](../../dealix/revenue_ops_autopilot/store.py).
4. Dual-write period; compare counts weekly; cut over when diff = 0.

## Non-goals (v1 DB)

- No automated external send columns.
- No invented CRM revenue fields — KPI still from `kpi_founder_commercial_import.yaml`.
