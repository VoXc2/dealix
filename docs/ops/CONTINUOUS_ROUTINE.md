# Continuous Routine

The Dealix operating loop is **continuous, automated, and read-only**.
No script in this loop edits commercial state. The verifier is the
judge; these scripts are only its scheduling and rendering layer.

---

## Cadence

| Cadence    | Trigger                                          | Script                       | Outputs                                                    |
|-----------:|--------------------------------------------------|------------------------------|-------------------------------------------------------------|
| **Daily**  | GitHub Actions cron `0 3 * * *` (06:00 KSA)      | `scripts/daily_routine.py`   | `data/_state/daily_brief_*.md`, `*.json`, history JSONL    |
| **Weekly** | GitHub Actions cron `0 3 * * SUN` (Sunday 06:00 KSA) | `scripts/weekly_ceo_review.py` | `data/_state/weekly_review_*.md`, `*.json`                 |
| **Per push / PR** | CI gate                                   | `scripts/render_verifier_report.py` | `landing/assets/data/verifier-report.json` (drift gate)    |

All three scripts compose the master verifier (`scripts/verify_all_dealix.py --json`).
None of them mutate marker files.

---

## What Each Script Surfaces

### `daily_routine.py`

- **Today's CEO bottleneck** (one sentence, from the lowest-scoring
  failing top-8 system).
- Verifier state: overall, CEO-complete, pass count.
- Day-over-day score deltas vs the prior history row.
- Market-motion counts (read-only): `outreach_sent_count`,
  `invoice_sent_count`.
- A list of every failing system with its missing items.
- A snapshot from `dealix_founder_daily_brief.py` if present.

Outputs:

```
data/_state/daily_routine_<YYYY-MM-DD>.json   # full machine-readable payload
data/_state/daily_brief_<YYYY-MM-DD>.md       # human brief
data/_state/verifier_history.jsonl            # appended; one row per run
```

### `weekly_ceo_review.py`

- End-of-week verifier state.
- Week-over-week score changes (first vs last run in the ISO week).
- Market activity in the week (entries added to partner /  invoice /
  capital-asset logs whose `sent_at` / `created_at` falls in window).
- **Top 3 actions for next week**, auto-derived from failing top-8
  systems and the CEO-complete gate.

Outputs:

```
data/_state/weekly_review_<YYYY-Www>.md
data/_state/weekly_review_<YYYY-Www>.json
```

### `render_verifier_report.py`

- Renders the verifier JSON to `landing/assets/data/verifier-report.json`.
- Output is byte-stable across runs (sorted keys, no timestamps), so
  `git diff --exit-code` is a true drift gate, not a noise alarm.
- Consumed by the static dashboard at
  `landing/founder-command-center.html`.

---

## Honest-Marker Discipline

These three scripts **never** edit:

- `data/partner_outreach_log.json`
- `data/first_invoice_log.json`
- `data/capital_asset_index.json` (introduced in PR3)
- `data/anchor_partner_pipeline.json`
- `data/founder_command_center_status.json`

The only path to bumping `outreach_sent_count` or `invoice_sent_count`
is the marker-honesty CLI tools delivered in PR3:

```
scripts/log_partner_outreach.py   --really-i-sent-this   # bumps outreach
scripts/log_invoice_event.py      --capital-asset-id <ID> # bumps invoice
scripts/register_capital_asset.py                          # registers an asset
```

The CLI tools record `git_author` + `entry_id` on every entry so each
bump is traceable. PR4 adds a CI test
(`test_no_inflated_marker_counts.py`) that fails the build if the
counter and `len(entries)` disagree.

---

## How GitHub Actions Apply Updates

Both daily and weekly workflows use `peter-evans/create-pull-request`
to open a state-update PR labeled `state-update`. The founder reviews
and merges. The PR scope is restricted to:

- `data/_state/**`
- `landing/assets/data/verifier-report.json`

This means automated routines can **never** modify code, doctrine,
markers, or any commercial state — only the read-only snapshot
artifacts. A reviewer can approve these PRs safely.

---

## Manual Operation

If GitHub Actions is paused:

```bash
python scripts/daily_routine.py            # ~5 seconds, no external deps
python scripts/weekly_ceo_review.py
python scripts/render_verifier_report.py
```

Re-running is idempotent for the same day / week.

---

## Files Referenced

| Purpose                  | Path                                           |
|--------------------------|------------------------------------------------|
| Master verifier (judge)  | `scripts/verify_all_dealix.py`                 |
| Daily routine            | `scripts/daily_routine.py`                     |
| Weekly review            | `scripts/weekly_ceo_review.py`                 |
| Dashboard renderer       | `scripts/render_verifier_report.py`            |
| Daily cron               | `.github/workflows/daily_routine.yml`          |
| Weekly cron              | `.github/workflows/weekly_ceo_review.yml`      |
| Operating state          | `data/_state/`                                 |
| History (append-only)    | `data/_state/verifier_history.jsonl`           |
| Public dashboard         | `landing/founder-command-center.html`          |

---

_Owner: Founder._
_The verifier is the judge; this routine is only its lens._
