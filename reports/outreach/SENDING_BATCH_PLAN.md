# Sending Batch Plan — Dealix (Phase 8)

Report template for a sending batch PLAN. A batch is a plan by default: `dry_run=true`, `send_enabled=false`. The verdict gate forces **0 sends** if verdict < `LIMITED_SEND_READY`. Real send requires verdict >= `LIMITED_SEND_READY` AND founder approval.

Schema: `schemas/sending_batch.schema.json`. Data: `data/outreach/sending_batches.jsonl`.

---

## 1. Plan Fields

| Field | Value |
|-------|-------|
| batch_id | `____` |
| date | `____` |
| sector_focus | `____` (e.g. `marketing_agencies`) |
| planned_count | `____` |
| deliverability_verdict | `____` |
| status | `plan_only` (default) |
| approved_by | `null` until founder signs |
| dry_run | **true** |
| send_enabled | **false** |

---

## 2. Verdict Gate → Permitted Sends

| Verdict | Permitted sends |
|---------|-----------------|
| NOT_READY | 0 |
| DRY_RUN_ONLY (default) | 0 (plan/draft only) |
| LIMITED_SEND_READY | up to current ramp step cap, after approval |
| RAMP_READY | up to ramp step cap |
| PAUSE_REQUIRED | 0 |

> If verdict < `LIMITED_SEND_READY`: **permitted sends = 0**, this artifact is a plan only.

---

## 3. Pre-Send Gate Check

| Check | Status |
|-------|--------|
| Verdict ≥ LIMITED_SEND_READY | ☐ |
| Suppression list applied | ☐ |
| Within daily cap for ramp step | ☐ |
| No purchased lists | ☐ |
| Founder approval recorded | ☐ |

Suppression source: `data/outreach/suppression_list.jsonl`. Ramp caps: `docs/outreach/SENDING_RAMP_PLAN_AR.md`.

---

## 4. Decision

| Field | Value |
|-------|-------|
| Permitted sends | `____` (0 if verdict < LIMITED_SEND_READY) |
| Status | `____` (plan_only / approved / sent / paused) |
| Approved by | `____` (null until founder signs) |

> Example default state (from `data/outreach/sending_batches.jsonl`): verdict `DRY_RUN_ONLY` → `planned_count` may be set but permitted sends = 0, `status=plan_only`, `dry_run=true`, `send_enabled=false`.

---

*Dealix · Sending Batch Plan · verdict gate → 0 sends if < LIMITED_SEND_READY · dry_run=true, send_enabled=false · Ref: SDAIA PDPL*
