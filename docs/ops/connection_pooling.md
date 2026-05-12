# Connection pooling — PgBouncer tuning

Dealix uses PgBouncer in production to multiplex Postgres connections.
This doc explains the knobs and the values we ship with.

## Why PgBouncer

- FastAPI + asyncpg holds a connection per worker. With 2 workers and
  `pool_size=20` per worker, we'd peg Postgres at 40 connections per
  app instance. Even a 100-connection Railway plan saturates fast.
- PgBouncer's **transaction-pooling** mode multiplexes our short-lived
  transactions onto a small upstream pool, so Postgres sees a stable,
  small number of connections regardless of API replica count.

## Current values (docker-compose.yml)

| Param | Value | Why |
| --- | --- | --- |
| `POOL_MODE` | `transaction` | Required for our short SQLAlchemy txns. |
| `MAX_CLIENT_CONN` | 200 | App-side concurrency ceiling. |
| `DEFAULT_POOL_SIZE` | 20 | Active upstream connections per database. |
| `RESERVE_POOL_SIZE` | 5 | Burst headroom. |
| `RESERVE_POOL_TIMEOUT` | 5 | Seconds before tapping the reserve. |
| `MAX_DB_CONNECTIONS` | 25 | Total upstream — fits inside a 100-conn Railway pool with overhead. |
| `SERVER_RESET_QUERY` | `DISCARD ALL` | Clean session between clients. |
| `STATS_PERIOD` | 60 | Refresh metrics for Grafana. |

## What the SQLAlchemy side must do

- Use `NullPool` when behind PgBouncer (we *already* do — `db/session.py`
  picks `NullPool` when `DATABASE_URL` contains `pgbouncer=true`).
- Disable prepared statements: `connect_args={"statement_cache_size": 0}`.
  asyncpg's prepared-statement cache + transaction pooling = data
  corruption. Verified in our session factory.
- Set `pool_pre_ping=False` — PgBouncer already health-checks upstream.

## Diagnosing pool saturation

`Grafana → Dealix Postgres → "Pool saturation %"` (see
`infra/grafana/dashboards/postgres.json`). Alerts fire from
`infra/grafana/alerts/availability.yaml` when saturation crosses 80%.

Quick local check:

```bash
psql "$DATABASE_URL" -c "SELECT count(*) FROM pg_stat_activity WHERE datname='dealix';"
```

If you see numbers approaching `MAX_DB_CONNECTIONS`, either:

1. A long-running query is blocking the pool — kill it.
2. The reserve pool is exhausted — bump `DEFAULT_POOL_SIZE` only after
   you've confirmed Railway will allow more upstream connections.
3. A new background job is leaking connections — check `arq` worker
   logs for unclosed sessions.

## When to switch to a larger plan

- Sustained `>80%` saturation for >2 hours.
- `RESERVE_POOL_TIMEOUT` waits showing up in PgBouncer's `SHOW STATS`
  output.
- `pg_stat_activity` shows >5 idle-in-transaction sessions older than
  10 minutes. (Usually a hung agent.)
