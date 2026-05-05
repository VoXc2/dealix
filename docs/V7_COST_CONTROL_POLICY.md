# V7 Cost Control Policy

Owner: founder. Status: enforced in `auto_client_acquisition/ai_workforce/cost_guard.py`.

This policy bounds the AI workforce's API spend. It is a hard rule of the
v7 platform: every WorkforceRun must produce a `cost_estimate_usd` (already
part of the v7 P1 schema) and pass `enforce_run_budget(...)` before any
external model call is made.

## Default budgets

| Budget axis | Default (USD) | Configurable |
| --- | --- | --- |
| Per workforce run | 0.50 | yes — `CostBudget.per_run_budget_usd` |
| Per agent step | 0.10 | yes — `CostBudget.per_agent_budget_usd` |
| Monthly founder budget | 50.00 | yes — `CostBudget.monthly_founder_budget_usd` |

The monthly founder budget is the spend ceiling across all WorkforceRuns
combined for the month. The platform stops automated runs once the ceiling
is hit and surfaces the breach in the founder console.

## Thresholds

* Warning at **70%** of the per-run budget — `action="warn_founder"`.
* Pause-for-approval at **90%** of the per-run budget — `action="pause_for_approval"`.
* Hard stop at **100%** of the per-run budget — `action="hard_stop"`.

The same thresholds compose for the monthly founder budget; the rolling
total is computed from the WorkforceRun ledger, not from this module.

## Model tier policy

Three tiers — pick the cheapest tier that completes the task safely.

| Tier | Use for | Avoid for |
| --- | --- | --- |
| `cheap_for_classification` | Intake, scoring, tagging, contactability filtering, structured extraction. | Free-form Arabic drafting, multi-step planning. |
| `balanced_for_drafts` | Arabic / English follow-up drafts, summaries, rewrites, translations. | Strategy decisions, audits, multi-account planning. |
| `strong_for_strategy` | Weekly executive brief, growth audit, decision memos, multi-step plans. | Anything an extractor or classifier can do — escalating wastes the budget. |

The mapping `task_purpose -> ModelTier` is deterministic
(`pick_model_tier`); unknown purposes default to
`cheap_for_classification` so unknowns never auto-escalate to expensive
models.

## When agents must pause for approval

An agent must call `pause_for_approval` and surface to the founder when:

1. `enforce_run_budget(...)` returns `action in {"warn_founder",
   "pause_for_approval", "hard_stop"}`.
2. `human_review_when_budget_exceeded=True` (default) on any estimate that
   would push the rolling per-agent or monthly budget past the warning
   threshold.
3. The task purpose contains `strategy`, `plan`, `audit`, or `weekly_brief`
   AND the estimate exceeds `per_agent_budget_usd`.

## "No runaway agents" rule

* Every `CostEstimate` carries `max_iterations=3`.
* `stop_when_good_enough=True` — agents must accept the first acceptable
  output rather than spend more tokens chasing marginal quality.
* Any loop that exceeds three internal iterations is a bug, not a
  feature; the run is hard-stopped and the founder is notified.

## Audit trail

* Every WorkforceRun returns a `cost_estimate_usd` field (v7 P1 schema)
  alongside `tier`, `cache_key`, and the `enforce_run_budget` decision.
* Estimates are *planning numbers*, not live billing. They are bounded
  conservatively and intentionally do not call any external pricing API.

## What this policy is NOT

* It is not a billing system. Real spend is tracked separately and
  reconciled monthly.
* It is not a marketing claim. We do not promise a fixed monthly cost to
  any customer; the budget protects Dealix's own runtime spend.
* It does not replace the existing live-charge guards
  (`live_charge`, `send_email_live`) — those remain hard rules.
