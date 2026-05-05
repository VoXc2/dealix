# Dealix v5 — Comprehensive Completion Plan

> Roadmap to bring v5 to **12 of 12** layers shipped, production
> verified, master evidence table green. Each phase has owner +
> exit criterion + safe-fallback.

## Snapshot

| Item | State (2026-05-04 21:55 UTC) |
|---|---|
| Branch | `claude/service-activation-console-IA2JK` @ `d2dbc71` |
| main HEAD | `812054d` (PR #137 merged @ 21:35) |
| Branch ahead of main | 3 commits (the d2dbc71 batch) |
| v5 layers shipped | **9 of 12** |
| Tests passing | **321** + 2 skipped + 3 xfailed |
| Production `/health` | 200 OK, `version=3.0.0`, **`git_sha="unknown"`** |
| New endpoints in production | **404** (Railway hasn't picked up the merge yet) |

## Why production isn't showing the merge yet

Two possible reasons:

1. **Railway redeploy used the OLD deployment** (the one before `812054d` merged at 21:35). When you click Redeploy on a specific deployment in Railway, it rebuilds THAT commit, not the latest main. The fix is: trigger a fresh deploy from the latest main commit (Railway → dealix → "Deploy from latest commit" or push a new commit to main).
2. **Railway is still building.** A Docker multi-stage build with 60+ Python packages takes 5–15 min on a healthy node. Their earlier incident may still be slowing their queue.

Either way, the d2dbc71 batch (3 v5 layers from this session) is **not on main yet** — it lives on the feature branch awaiting PR #139.

## Phases

### 🟢 Phase A — Open PR #139 for the latest 3 v5 layers (5 min, Claude)

`d2dbc71` carries customer_data_plane + finance_os + delivery_factory
(the 3 v5 layers shipped in pt3). Opening a PR triggers CI and
gives the founder a review surface to merge.

**Exit:** PR #139 open, CI green.

### 🟢 Phase B — Verify Railway picked up `812054d` (5 min, founder)

While Phase A's CI runs, the founder needs to confirm Railway's
last deploy is from main HEAD (`812054d` or later):

1. Open https://railway.com → dealix → Deployments.
2. Top deployment should reference commit `812054d` or later.
3. If it references an older commit:
   - Click the kebab on the active deployment → **"Redeploy from latest"**
   - OR push an empty commit to main: `git commit --allow-empty -m "chore: trigger redeploy" && git push origin main`

**Exit:** `curl https://api.dealix.me/health` returns `git_sha` matching `812054d` (or newer).

### 🟢 Phase C — Build the 3 remaining v5 layers safely (~3 hrs, Claude)

These are the layers v5 listed but I deferred. With careful scoping,
each can ship REAL without the founder decisions originally cited:

#### C.1 — `proof_ledger/` (file-backed stopgap)

The DB-backed Postgres ledger is deferred until founder approves
schema. **In the interim**, ship a file-backed JSON-Lines ledger:

- `auto_client_acquisition/proof_ledger/file_backend.py` — append-
  only JSONL writer at `docs/proof-events/<date>.jsonl`
- `proof_event.py` schema (typed Pydantic `ProofEvent` +
  `RevenueWorkUnit`)
- `proof_pack_builder.py` — wraps existing `proof_snippet_engine.render_pack`
- `evidence_export.py` — exports a JSONL slice with PII redaction
  (uses the existing `pii_redactor`)
- Endpoint: `POST /api/v1/proof-ledger/events`, `GET /api/v1/proof-ledger/events`
- Tests: 8 cases

When the Postgres ledger ships, the writer/reader interface stays
the same — only the storage backend changes.

#### C.2 — `gtm_os/` enrichments

GTM core lives across self_growth_os already (geo_aio_radar,
partner_distribution_radar, weekly_growth_scorecard, daily_growth_loop).
Add 2 small modules to complete the v5 prompt's surface:

- `content_calendar.py` — generates a **draft-only** weekly content
  calendar for landing pages (anchored to which page from
  `seo_audit_report.json` is lowest-scoring). All entries
  approval_required.
- `message_experiment.py` — typed schema for tracking experiments
  (variant_a, variant_b, success_metric). No execution — just a
  template for the founder to fill in manually.
- Endpoint: `GET /api/v1/gtm/content-calendar`,
  `POST /api/v1/gtm/experiment/draft`
- Tests: 6 cases

#### C.3 — `security_privacy/` (thin code wrapper)

The security policy IS founder-written (PRIVACY_PDPL_READINESS.md,
trust-center.html, etc.). What can ship as **code**:

- `secret_scan_policy.py` — wraps gitleaks-style scanning over
  given paths (uses regex; no real gitleaks call needed).
- `log_redaction.py` — wraps `pii_redactor.redact_dict` for log
  middleware.
- `data_minimization.py` — typed contract: which fields are
  PII-flagged per object type.
- Endpoint: `POST /api/v1/security-privacy/redact`,
  `POST /api/v1/security-privacy/scan-text`
- Tests: 6 cases

### 🟢 Phase D — Master Evidence Table v5 (15 min, Claude)

Author `docs/V5_MASTER_EVIDENCE_TABLE.md` with explicit pass/fail
per row. Run `bash scripts/post_redeploy_verify.sh` against
production after Phase B succeeds — the result populates the table.

**Exit:** Evidence table committed, every row anchored.

### 🟢 Phase E — Final commit + push + PR #139 (10 min, Claude)

Stage everything from Phase A + C + D. Commit message lists the
final 12-of-12 v5 layers. Push to the branch. Update PR #139
description to reflect total shipped state.

**Exit:** PR #139 has all v5 work, CI green, ready for founder merge.

### 🟢 Phase F — Founder action + final verdict (5 min, founder + Claude)

- Founder merges PR #139.
- Railway auto-redeploys.
- Claude runs `post_redeploy_verify.sh` against the new live state.
- Final verdict block printed.

## Hard rules — re-asserted

- ❌ No new `*_ALLOW_LIVE_*` env flag added in any phase.
- ❌ No service marked Live without explicit `gates:` block.
- ❌ No live customer outbound. No live charge.
- ❌ No scraping. No LinkedIn automation. No cold WhatsApp.
- ❌ The 4 REVIEW_PENDING strings remain founder decisions.
- ❌ Proof Ledger file backend NEVER exposes raw PII (redactor
  required on every export).
- ❌ Content calendar drafts are NEVER published — they go to the
  existing `safe_publishing_gate` first, then ApprovalGate.

## Critical files this plan touches

| Phase | New files | Modified files |
|---|---|---|
| C.1 (proof_ledger) | `auto_client_acquisition/proof_ledger/{__init__,schemas,file_backend,proof_event,revenue_work_unit,evidence_export}.py`, `api/routers/proof_ledger.py`, `tests/test_proof_ledger_v5.py` | `api/main.py` |
| C.2 (gtm_os) | `auto_client_acquisition/gtm_os/{__init__,content_calendar,message_experiment}.py`, `api/routers/gtm_os.py`, `tests/test_gtm_os_v5.py` | `api/main.py` |
| C.3 (security_privacy) | `auto_client_acquisition/security_privacy/{__init__,secret_scan_policy,log_redaction,data_minimization}.py`, `api/routers/security_privacy.py`, `tests/test_security_privacy.py` | `api/main.py` |
| D | `docs/V5_MASTER_EVIDENCE_TABLE.md` | — |
| Final | — | `docs/V5_OS_SCOPE.md` |

## End-state target (Phase F success)

```
DEALIX_V5_VERDICT=ALL_LAYERS_SHIPPED_PRODUCTION_VERIFIED
LOCAL_HEAD=<sha of merged d2dbc71 + Phase C/D commits>
PROD_GIT_SHA=<matches LOCAL_HEAD>
PRODUCTION_HEALTH=pass
v5 layers shipped:        12 / 12
Test bundle:              350+ / 350+ pass
Hard rules:               all pass
Customer-serving loop:    customer_loop + role_command_os + delivery_factory live
Safety:                   compliance + pii redactor + agent_governance + safe_publishing_gate live
Self-growth:              all 12 self_growth_os modules live
First-customer ready:     yes_warm_only_manual_payment
```
