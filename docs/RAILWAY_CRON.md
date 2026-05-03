# Railway Cron — Daily Ops Schedule

This doc explains how to run the 4 daily-ops windows on Railway as scheduled
jobs. Each window is one CLI invocation; failure is isolated per window so a
broken `morning` doesn't cascade into `midday`.

## What runs

Four windows, defined in `auto_client_acquisition/revenue_company_os/daily_ops_orchestrator.py:WINDOWS`:

| Window     | KSA time | UTC cron       | Roles touched                                        |
|------------|----------|----------------|------------------------------------------------------|
| morning    | 08:30    | `30 5 * * *`   | ceo, sales_manager, growth_manager, customer_success, compliance |
| midday     | 12:30    | `30 9 * * *`   | sales_manager, growth_manager                        |
| closing    | 16:30    | `30 13 * * *`  | sales_manager, finance · also runs **self-growth loop** |
| scorecard  | 18:00    | `0 15 * * *`   | ceo, revops, compliance                              |

The `closing` window additionally calls `self_growth_mode.loop_once()` to
auto-record one experiment per day (idempotent — skips if today's experiment
exists).

## How to enable on Railway

Railway's cron jobs are configured per service via the Railway dashboard
(Settings → Cron Jobs) or via `railway.json`. The schedule lives in
`railway.json` under `cron` so deploys carry it forward.

### railway.json (already wired)

```json
{
  "cron": [
    { "name": "morning",   "schedule": "30 5 * * *",  "command": "python scripts/cron_daily_ops.py --window morning   --quiet" },
    { "name": "midday",    "schedule": "30 9 * * *",  "command": "python scripts/cron_daily_ops.py --window midday    --quiet" },
    { "name": "closing",   "schedule": "30 13 * * *", "command": "python scripts/cron_daily_ops.py --window closing   --quiet" },
    { "name": "scorecard", "schedule": "0 15 * * *",  "command": "python scripts/cron_daily_ops.py --window scorecard --quiet" }
  ]
}
```

After commit + push, Railway picks up the cron config on the next deploy.

### Manual invocation (CLI)

```bash
# Locally (uses .env)
python scripts/cron_daily_ops.py --window morning

# Dry-run — prints plan, no DB writes
python scripts/cron_daily_ops.py --window scorecard --dry-run

# Against staging URL (the CLI runs server-side; from your laptop, use SSH)
railway run --service web -- python scripts/cron_daily_ops.py --window morning
```

## How to disable a single window

Railway dashboard → Settings → Cron Jobs → toggle the row off. Or
remove the entry from `railway.json` and redeploy. The other three
keep running.

## How to monitor

Each successful run inserts one row into `daily_ops_runs` with:
- `run_window` — which window
- `started_at` / `finished_at`
- `decisions_total` — sum across roles
- `risks_blocked_total` — from compliance role
- `error` — non-null only on failure

Quick check from CLI:

```bash
python scripts/dealix_cli.py today    # shows recent_daily_ops + per-window deltas
```

Or via API:

```bash
curl -s https://api.dealix.me/api/v1/daily-ops/history?limit=10 | jq .
```

## Failure handling

- Each role inside a window is wrapped in try/except — a single failed
  brief does NOT abort the rest of the window.
- The CLI exits 1 if the orchestrator returned an `error` field, else 0.
- Railway treats non-zero exits as job failures and surfaces them in the
  logs UI.
- The structured log line `cron_failed window=...` is grep-friendly for
  alerting integrations.

## Why these times

08:30 KSA — ahead of the 09:00 commercial day; founder + sales see the
morning brief in their first coffee.

12:30 KSA — pre-lunch execution check; growth + sales catch issues before
the afternoon push.

16:30 KSA — closing window; sales + finance reconcile the day, self-growth
plans tomorrow's experiment.

18:00 KSA — scorecard window; CEO + RevOps + Compliance see a single
end-of-day snapshot to take home.
