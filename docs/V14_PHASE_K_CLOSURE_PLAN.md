# Phase K — Service Readiness Closure Plan

**Date:** 2026-05-06
**Goal:** Take the 8 "under development" services in
`docs/registry/SERVICE_READINESS_MATRIX.yaml` from `pilot` / `partial`
to **`live`** — starting with WhatsApp.

> **Founder ask (literal):** _"سو خطه لاقفال كلشي و تدشين كلشي و من
> جد الخدمات المهمه الي تقول عنها تحت التطوير انجزها و اولها الواتس
> و اي شي تبيني اسويه انا بسويه بس انجز كلشي بشكل كامل."_

## Current registry state

```
TOTAL = 32 services
LIVE     = 0
PILOT    = 1
PARTIAL  = 7   ← homepage trust-bar shows "8 قيد التطوير"
TARGET   = 24  (deferred — many require third-party setup or PMF proof)
BLOCKED  = 0
BACKLOG  = 0
```

## The 8 services in scope

### Group A — Saudi-killer features (founder priority)

| # | Service | Status | Founder needed | Code work |
|---|---|---|---|---|
| K1 | `lead_intake_whatsapp` | partial | Meta WhatsApp Business credentials | OpenTelemetry traces on webhook entry + abuse-boundary test for opt-out flagged numbers |
| K2 | `qualification` | pilot | none | Failure-path coverage + score-stability test |

### Group B — Trust + governance (pure code)

| # | Service | Status | Founder needed | Code work |
|---|---|---|---|---|
| K3 | `audit_trail` | partial | none | Unify `correlation_id` across all paths + full-coverage test |
| K4 | `consent_required_send` | partial | none | Upgrade consent table schema + default-deny test (when consent absent) |
| K5 | `outreach_drafts` | partial | none | Quiet-hours enforcement (KSA timezone) + reject-outside-active-window test |
| K6 | `routing` | partial | none | Wire consent table + quiet-hours test on KSA timezone |

### Group C — Provider-dependent

| # | Service | Status | Founder needed | Code work |
|---|---|---|---|---|
| K7 | `enrichment` | partial | Real provider API keys (Apollo / Hunter / Clearbit) | Unified confidence-score test (works against any provider) |
| K8 | `release_gate` | partial | OIDC issuer config + cosign keys (or skip in favour of GitHub-native attestations) | Wire OIDC + attestations + run readiness validator in CI on every PR |

## Hard rules (non-negotiable)

- ❌ NO V13 / V14 — every action below either completes an existing
  TODO or finishes a partial implementation. No new architecture.
- ❌ NO live charge / live send / scraping / cold WhatsApp
- ❌ NO "guaranteed" / "نضمن" copy
- ❌ NO new heavy dependency unless absolutely required (and then call
  it out explicitly; founder approves)
- ✅ Every newly-`live` service must satisfy all 8 gates from
  `docs/SERVICE_ACTIVATION_CONSOLE.md`
- ✅ Every status transition writes to the registry YAML and re-runs
  `scripts/verify_service_readiness_matrix.py`
- ✅ Arabic primary, English secondary
- ✅ One PR per group (max 3 PRs total)

## Founder credentials checklist (one-time setup, ~30 min total)

These unlock K1 (WhatsApp) + K7 (enrichment) + Moyasar live + future
TARGET services. Send to me as env-var key=value in a private channel
(e.g. WhatsApp to me directly, NOT in this repo or PR comments):

1. **WhatsApp Business API** (K1):
   - `WHATSAPP_BUSINESS_ID` (from Meta Business Manager)
   - `WHATSAPP_PHONE_NUMBER_ID`
   - `WHATSAPP_ACCESS_TOKEN` (long-lived, NOT a test token)
   - `WHATSAPP_APP_SECRET` (for webhook signature verification)
   - `WHATSAPP_VERIFY_TOKEN` (any random string we agree on)
   - **Founder action:** approve a WhatsApp template message in Meta
     for the daily-decisions outbound (the one that pings you to
     approve pending items). Template name: `dealix_daily_decisions`.

2. **Enrichment provider** (K7) — pick ONE:
   - Apollo: `APOLLO_API_KEY`
   - Hunter: `HUNTER_API_KEY`
   - Clearbit: `CLEARBIT_API_KEY`
   - **Recommendation:** Hunter ($49/mo, low entry, good for KSA emails)

3. **Optional for K8 release gate:** GitHub OIDC works out of the
   box. Cosign / sigstore is optional; we can defer until first paid
   pilot. **Skip for now unless you want it.**

---

## Execution order (3 PRs, ~3-day plan)

### PR #166 — WhatsApp + Audit Trail + Qualification (~6h, K1 + K2 + K3)

**Why first:** K1 is the founder's explicit #1 ask. K3 (audit trail)
is a prerequisite for K1 quality gate. K2 (qualification) is
already pilot → just needs one test to flip to live.

#### K1 · WhatsApp lead_intake — full implementation

**Existing:**
- `/api/v1/webhooks/whatsapp` GET (verify) + POST (incoming) — wired
- `/api/v1/prospect/inbound/whatsapp` — inbound prospect handling
- `integrations/whatsapp` — WhatsAppClient with signature verification

**Missing → add:**
1. **Outbound message-send endpoint** (gated by approval-center):
   `POST /api/v1/whatsapp/send-approved` — accepts `approval_id`,
   verifies the approval is in `approved` state, sends via WBA,
   records the message_id in audit trail. Hard-gated: refuses to
   send unless `WHATSAPP_LIVE_SEND_ENABLED=true` env var is set
   AND the approval has `action_type=whatsapp_outbound` AND status
   is `approved`.
2. **Quiet-hours guard** for KSA timezone (Asia/Riyadh): no outbound
   send between 22:00–08:00 unless explicitly flagged
   `customer_consent_outside_quiet_hours=true`.
3. **OpenTelemetry traces** on every webhook entry (already partial;
   complete it).
4. **Abuse-boundary test** (`tests/test_whatsapp_opt_out_v14.py`):
   verify that an opt-out flagged number cannot receive any further
   outbound, even if approved. Default-deny.
5. **Daily-decisions-via-WhatsApp:** the existing `decisions.html`
   page already lists pending approvals. We add: a "Send today's
   pending decisions to my WhatsApp" button → calls a new endpoint
   `POST /api/v1/founder/decisions/send-via-whatsapp` that fires the
   approved `dealix_daily_decisions` template to the founder's
   number. Tied to founder-tier auth only.
6. **Update registry:** `lead_intake_whatsapp` status `partial` → `live`.

**Files:**
- `api/routers/whatsapp_send.py` (NEW, ~120 lines)
- `api/routers/founder_decisions.py` (NEW, ~80 lines — extends founder router)
- `auto_client_acquisition/whatsapp_quiet_hours.py` (NEW, ~50 lines)
- `auto_client_acquisition/whatsapp_opt_out.py` (NEW, ~60 lines)
- `tests/test_whatsapp_opt_out_v14.py` (NEW, ~60 lines)
- `tests/test_whatsapp_quiet_hours_v14.py` (NEW, ~50 lines)
- `tests/test_whatsapp_send_approval_gated_v14.py` (NEW, ~80 lines)
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` (status update)
- `landing/decisions.html` (add "Send to WhatsApp" button)

#### K2 · Qualification (pilot → live)

**Existing:**
- `auto_client_acquisition/qualification/` (BANT / MEDDPICC)
- `tests/test_qualification_*.py` — happy-path covered

**Missing → add:**
- **Failure-path coverage test** — what happens when scoring inputs
  are missing/malformed? Score should default to "insufficient_data"
  not crash.
- **Score-stability test** — same inputs in 100 trials → same score
  (deterministic).

**Files:**
- `tests/test_qualification_failure_paths_v14.py` (NEW, ~80 lines)
- `tests/test_qualification_score_stability_v14.py` (NEW, ~40 lines)
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` (status update)

#### K3 · Audit Trail (partial → live)

**Existing:**
- `auto_client_acquisition/agent_governance/audit.py` (audit log)
- Many routers log events with their own IDs

**Missing → add:**
- **Unified `correlation_id`** — every request gets a UUID that
  threads through all log/audit events. Implement via FastAPI
  middleware that injects a `correlation_id` into request state +
  log context, then audit module reads it.
- **Full-coverage test** (`tests/test_audit_correlation_id_v14.py`):
  hits 10 distinct endpoints, asserts each request's audit events
  share the same correlation_id and don't bleed across requests.

**Files:**
- `api/middleware/correlation_id.py` (NEW, ~40 lines)
- `auto_client_acquisition/agent_governance/audit.py` (modify to
  read correlation_id from contextvar)
- `tests/test_audit_correlation_id_v14.py` (NEW, ~70 lines)
- `api/main.py` (wire middleware)
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` (status update)

**Verification:** all 3 tests pass + readiness validator says
`SERVICES_TOTAL=32 LIVE=3 PILOT=0 PARTIAL=4 TARGET=24 BLOCKED=0`.

---

### PR #167 — Consent system trio (~5h, K4 + K5 + K6)

**Why second:** K4 (consent_required_send), K5 (outreach_drafts), K6
(routing) are all in the same code path — one round of work touches
all three.

**Existing:**
- `auto_client_acquisition/customer_inbox_v10/consent_status.py` —
  consent enum + checker
- `auto_client_acquisition/customer_inbox_v10/routing_policy.py` —
  routing engine
- `auto_client_acquisition/outreach_*` modules

**Missing → add:**
1. **Consent table schema upgrade** — current consent is a flag per
   customer. Upgrade to per-channel + per-purpose consent (e.g.
   `whatsapp_marketing=false, email_transactional=true,
   email_marketing=false`). File-backed JSONL store
   (`var/consent-table.jsonl`, gitignored).
2. **Default-deny test** — any send without explicit consent →
   blocked, even if customer is "active".
3. **KSA quiet-hours test** — 22:00–08:00 Asia/Riyadh blocks
   outbound by default.
4. **Active-conversation-window test** — outreach drafts only valid
   in 72h window after last inbound; drafts older than 72h auto-flag
   as `requires_re_engagement_consent`.

**Files:**
- `auto_client_acquisition/consent_table.py` (NEW, ~120 lines —
  per-channel × per-purpose grid)
- `auto_client_acquisition/customer_inbox_v10/consent_status.py`
  (modify to read from new table)
- `auto_client_acquisition/customer_inbox_v10/routing_policy.py`
  (modify to enforce KSA quiet hours)
- `tests/test_consent_default_deny_v14.py` (NEW)
- `tests/test_routing_quiet_hours_ksa_v14.py` (NEW)
- `tests/test_outreach_active_window_v14.py` (NEW)
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` (3 status updates)

**Verification:** all 3 tests pass + readiness validator says
`LIVE=6 PARTIAL=1` (only `enrichment` + `release_gate` left).

---

### PR #168 — Enrichment + Release Gate (~3h, K7 + K8)

#### K7 · Enrichment

**Existing:**
- `auto_client_acquisition/enrichment_*` modules
- `/api/v1/prospect/enrich-tech` and `/enrich-domain`

**Missing → add:**
- **Provider abstraction** — pick one of: Apollo / Hunter / Clearbit.
  Founder picks based on cost + KSA email coverage.
- **Unified confidence-score test** — works against any provider:
  given a known company, returns score in expected range.

**Founder action:** provide ONE provider API key.

**Files:**
- `auto_client_acquisition/enrichment_provider.py` (NEW, abstract base
  + Hunter implementation as default)
- `tests/test_enrichment_confidence_score_v14.py` (NEW)
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` (status update)

#### K8 · Release Gate

**Existing:**
- `scripts/verify_service_readiness_matrix.py`
- GitHub Actions CI

**Missing → add:**
- **Run readiness validator in CI on every PR** — already exists in
  `.github/workflows/ci.yml`? Verify; add if missing.
- **Sigstore/cosign attestations** — defer (founder explicitly said
  K8 OIDC is optional).
- For now: just ensure the validator runs in CI and the registry
  status update lands automatically.

**Files:**
- `.github/workflows/ci.yml` (verify validator step exists; add if not)
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` (status update)

**Final verification:** `SERVICES_TOTAL=32 LIVE=8 PARTIAL=0`.

---

## Ship-when (per PR)

### PR #166 (WhatsApp + Audit Trail + Qualification)
- Founder provides WhatsApp Business credentials → I set them as
  Railway env vars (or you do, I send the exact list)
- I commit + push + PR + you merge
- Railway redeploys → run smoke against `/api/v1/whatsapp/send-approved`
  with a test message to the founder's number
- If clean → flip `WHATSAPP_LIVE_SEND_ENABLED=true` for production
- Run `bash scripts/verify_service_readiness_matrix.py` → expect
  `LIVE=3`

### PR #167 (Consent trio)
- Pure code work, founder no action needed
- Run `python -m pytest tests/test_consent_*_v14.py
  tests/test_routing_*_v14.py tests/test_outreach_*_v14.py` → green
- Verify registry → `LIVE=6`

### PR #168 (Enrichment + Release Gate)
- Founder provides ONE enrichment provider API key
- I add it to Railway env, run integration smoke
- Verify registry → `LIVE=8 PARTIAL=0`
- Update `landing/index.html` trust-bar: was `0 live · 8 partial` →
  now `8 live · 0 partial`. The homepage tells the truth.

## Test plan summary

| Test file | Asserts |
|---|---|
| `test_whatsapp_opt_out_v14.py` | opt-out flagged number → no outbound, default-deny |
| `test_whatsapp_quiet_hours_v14.py` | KSA 22:00–08:00 → blocked outbound |
| `test_whatsapp_send_approval_gated_v14.py` | unapproved send → 403; approved send → records audit |
| `test_qualification_failure_paths_v14.py` | malformed inputs → `insufficient_data`, never crash |
| `test_qualification_score_stability_v14.py` | 100 trials same input → same score |
| `test_audit_correlation_id_v14.py` | 10 endpoints share correlation_id within request, isolated across requests |
| `test_consent_default_deny_v14.py` | absent consent → blocked even for "active" customer |
| `test_routing_quiet_hours_ksa_v14.py` | KSA 22:00–08:00 → routed to `wait_until_morning` |
| `test_outreach_active_window_v14.py` | drafts older than 72h → flagged `requires_re_engagement_consent` |
| `test_enrichment_confidence_score_v14.py` | known company → score in expected range, deterministic |

## Risks + mitigations

| Risk | Mitigation |
|---|---|
| WhatsApp Business approval delayed | All code is feature-flagged behind `WHATSAPP_LIVE_SEND_ENABLED`; we ship the code in PR #166 and flip the flag once Meta approves |
| Hunter / Apollo API rate-limits during test | Mock provider in unit tests; integration test runs only with real key set |
| Existing tests start failing due to correlation_id middleware | Middleware is no-op when no correlation_id is in context (backward-compat) |
| Consent table migration breaks existing customers | New table is additive; old single-flag check stays as fallback for the first 30 days |

## What this plan deliberately does NOT do

- ❌ NO new OS layer (no V14 module beyond completing existing TODOs)
- ❌ NO scraping integration even with provider keys
- ❌ NO automated cold WhatsApp (only template-approved + opt-in)
- ❌ NO new pricing tier
- ❌ NO change to the 8 immutable hard gates
- ❌ Phase H scale work (deferred until 3 paid pilots — Article 13)
- ❌ TARGET-tier services (24 of them — deferred until each has a
  named customer asking for it; per Article 11 "no features beyond
  what's required")

## Founder decisions blocking this plan

1. **WhatsApp Business credentials** — the single biggest gate.
   Without them, K1 ships as "code-complete-pending-credentials"
   rather than fully live.
2. **Enrichment provider choice** — Apollo vs Hunter vs Clearbit.
   Recommendation: Hunter.
3. **K8 OIDC/Sigstore** — defer y/n? Recommendation: defer.

Send the answers + creds via private WhatsApp / encrypted email.
NEVER in this repo, PR comments, or chat history.

## Final state (after all 3 PRs ship)

- `landing/index.html` trust-bar: **8 خدمة حيّة · 0 قيد التطوير ·
  24 في خارطة الطريق** (was: 0 / 8 / 24)
- `dealix.me/founder-leads.html` shows real persisted leads
- `dealix.me/decisions.html` works on phone via WhatsApp browser
- WhatsApp inbound + outbound (template-approved + opt-in) live
- Audit trail traces every action with a single correlation_id
- Consent enforced default-deny across every send path
- Registry: `LIVE=8 PARTIAL=0`
- Production smoke: 28/28 + 10 new tests passing
- Constitution Article 13 trigger: still locked until 3 paid pilots

## One-line summary

> **Phase K = ship the 8 services already 80% done.** WhatsApp first,
> then audit-trail + qualification, then consent trio, then enrichment
> + release gate. 3 PRs, ~14 hours of code work, founder provides 2
> credential bundles. Result: homepage trust-bar tells the truth (8
> live), no V13/V14, every gate immutable. كل شيء جاهز للبيع.
