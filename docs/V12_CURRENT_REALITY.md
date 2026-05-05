# V12 — Current Reality (truth check baseline, 2026-05-05)

## Snapshot at V12 start

| Field | Value |
|---|---|
| Local HEAD | `e279f34` (V11 closure) on `claude/service-activation-console-IA2JK` |
| Production `git_sha` | `8099b00` (pre-V11-redeploy) |
| Production smoke | 27/28 (founder/dashboard timeout pre-cache) |
| V11 verifier | PASS |
| V11 PR | not yet opened (V12 ships in same branch) |
| Test bundle baseline | 1539 passed / 8 skipped / 4 xfailed / 0 failed |

## What V11 left ready (re-used by V12)

- Founder dashboard cache (`auto_client_acquisition/founder_v10/{cache,dashboard_builder}.py`) — V12 extends with 5 OS queues
- Status alias pattern (`api/routers/v10_status.py`, `api/routers/v11_status.py`) — V12 adds 7 OS-level status routes
- Phase E execution kit (`docs/phase-e/`) — V12 references for support knowledge
- Truth labels (`docs/phase-e/00_GO_NO_GO.md`) — V12 must NOT flip
- Hard gates: all blocked

## What V12 adds

- 3 truly new modules: **Support OS, Partnership OS, Compliance OS v12 action_policy**
- 6 thin wrappers exposing existing v5/v6/v7/v10 modules as `/api/v1/<os>-os/` endpoints
- Unified `WorkItem` layer (translator, not replacement)
- 7 bilingual knowledge-base markdown files
- 1 umbrella `daily-command-center` endpoint
- 1 V12 verifier + 1 evidence table

## What V12 explicitly does NOT add (per plan)

- Observability v10 4-file refactor (cosmetic, deferred to V13)
- Full ticket state machine + assignment + CSAT in inbox
- Cross-system consent reconciliation (compliance_os ↔ customer_data_plane)
- Self-modifying code in Self-Improvement OS
- LLM fallback in Support classifier (rule-based only)
- Partner referral revenue-share automation

## Blocks revenue today (still)

NONE for diagnostic-only Phase E. Founder can pick 3 warm intros now;
V12 makes the operational view richer + adds Support OS handling for
when first inbound questions arrive.

## Founder action

After V12 PR ships:
1. Open PR (V11 + V12 in same branch) → merge → Railway redeploy
2. Run `python scripts/dealix_phase_e_today.py` daily
3. After first inbound message: `POST /api/v1/support-os/classify` + draft response
4. Daily: `GET /api/v1/full-ops/daily-command-center` (single call replaces 9 separate dashboards)

## Hard rules

- ❌ NO live WhatsApp / Gmail / LinkedIn / Moyasar live charge
- ❌ NO scraping / cold WhatsApp / fake customers / fake proof
- ❌ NO weakening of existing tests
- ❌ NO new heavy dependency
- ❌ NO renaming / replacing existing modules
- ✅ Arabic primary, English secondary
- ✅ Every external action: `suggest_only` / `draft_only` / `approval_required` / `approved_manual` / `blocked`
