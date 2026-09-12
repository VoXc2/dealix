# OP2 CROSS-LANE FINDINGS — full-company frontier (2026-09-12)

Source: live evidence in `/opt/dealix/worktrees/op2-20260912T052940`.
No OP0/OP1-owned files were modified. No L5 executed. No external sends.
All OP2 artifacts are research-only / draft-only / unsent.

## Lane ownership as observed

- OP0 owns release/acceptance/production/deploy/TLS/DNS/rollback.
  Frozen release = `8bb0a6c382c49ca288f7b579cae07676f006e229` (`FROZEN_RELEASE.json`, PR #1705).
- OP1 owns (live branch `work/post-release-autonomy-20260912T042947`, tip `049e34c85`):
  `scripts/ops/audit_dealix_schedulers.py`, `scripts/ops/go_resource_broker.py`,
  `scripts/ops/opencode_model_broker.py`, `scripts/commercial/render_money_now_negotiation_packet.py`
  + their tests (8 files, +824 lines). PR #1707 (DRAFT).
- OP2 (this lane) owns the complementary company frontier, operating *additively*
  (new files only) inside `data/commercial/`, `scripts/commercial/`, `scripts/ops/`,
  and `tests/`.

## FINDING OP2-XL-1 — runtime SESSION_OWNERSHIP.json over-assigns OP1

`/opt/dealix/control/state/parallel/SESSION_OWNERSHIP.json` lists OP1 as owning
Saudi market, B2G, website/SEO/content, diagnostic enhancement, delivery factory,
relationship intelligence, Money Now, and negotiation packets. OP1's actual
committed work (8 files) does **not** cover most of that surface.

OP2 therefore executed the declared frontier **without modifying any OP1 file**,
choosing new, additive paths only. No conflict occurred. Action: none required;
the ownership document is stale and should be reconciled to actual lane commits
by the owning control plane (out of OP2 write scope).

## FINDING OP2-XL-2 — CI-cron plane was unmapped

OP1's scheduler audit covers systemd timers + Hermes cron only. The GitHub
Actions cron plane (37 workflows with `schedule.cron`, 31 distinct slots) had no
inventory or collision detection. OP2 added a read-only map:
`scripts/ops/op2_ci_cron_ownership_map.py` →
`data/commercial/op2_ci_cron_ownership_map_v1.json`.

Deferrable collisions surfaced for PM review (not changed by OP2):
- `0 4 * * *` → `company-brain-daily.yml`, `daily-revenue-machine.yml`, `daily_digest.yml`
- `0 6 * * 0` → `commercial-expand-weekly.yml`, `distribution_weekly_review.yml`,
  `founder_complete_autonomous_weekly.yml`, `founder_weekly_verify.yml`,
  `weekly-founder-content.yml`

## FINDING OP2-XL-3 — duplicate/unowned market-intelligence rankers

Two divergent rankings exist and are not reconciled:
- Canonical: `scripts/ops/sector_economic_ranking.py` (PR #1705), reads the radar
  brief `data/founder_briefs/universal_market_radar_latest.json` (gitignored →
  absent in fresh checkouts) and writes OUTSIDE the repo.
- Unverified legacy: `dealix/commercial/market_intelligence.py` exposes
  `/api/v1/market-intelligence/*` with hardcoded adoption/market-size figures and
  no evidence refs.

OP2 did NOT edit either. OP2 added a committed ranking artifact
(`data/commercial/op2_sector_economy_ranking_v1.json`) that reproduces
deterministically from a committed wave, so the ranking is reproducible in CI.
Recommendation (owner: dealix-engineer): reconcile the legacy API ranker or
clearly deprecate it.

## FINDING OP2-XL-4 — OP1 Money Now packet is not on this base

`scripts/commercial/render_money_now_negotiation_packet.py` exists only on OP1's
branch, not on `8bb0a6c38`. OP2 added a complementary reconciliation reader at
`scripts/commercial/op2_money_now_reconciliation.py` (different purpose: stage
reconciliation + truthful snapshot) with no overlap.

## FINDING OP2-XL-5 — content publish path remains L5

`dealix/marketing_factory/schemas.py` defaults `cta_path` to the legacy
`/dealix-diagnostic` route, while canonical web is `apps/web` `/book`. OP2 did
not modify this shared file; OP2 drafts point at `/book` directly. Owner:
dealix-content/dealix-engineer.

## OP2 L5 items prepared (NOT executed)

- `ACTION_HASH=937837e8d392943d` — iMini/Jannie `EMAIL_SEND` INBOUND_REPLY packet
  (`data/commercial/op2_l5_imini_packet_v1.json`), deny-by-default verified
  `provider_execution_allowed=false`.
- Pre-existing pending items remain OP0/OP1: MERGE `fd7a926a9ef9f266`,
  DEPLOY `9915507edd7e2c53`, FIX_TLS `072b164fc432bd43`, iMini `824a9d8b3caae92d`.

## Truth statement

Research != relationship. Public contact != consent. Draft != sent.
Tender != submission. Verified revenue = 0. No OP2 artifact counts as pipeline,
revenue, relationship, consent, or proof.
