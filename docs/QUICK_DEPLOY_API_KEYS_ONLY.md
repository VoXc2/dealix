# Dealix — Quick Deploy with API Keys Only (~30 min)

A single recipe to bring Dealix from `git clone` to a running
production instance with **only API keys** as input. Honors all
hard rules: live-action gates default OFF, no scraping/cold WhatsApp
paths reachable, manual Moyasar invoice path only.

> **Audience:** founder or any operator with shell access + a
> Railway / Supabase / Upstash / Groq / Anthropic / Moyasar
> dashboard login.
>
> **Time:** 25–35 minutes including DNS propagation if a custom
> domain is wired.

## 0. Pre-flight (5 min)

You will need accounts for:

| Service | Why | Free tier? |
|---|---|---|
| Railway | App host (reads Dockerfile) | yes (limited) |
| Supabase OR Railway Postgres | Postgres database | yes |
| Upstash OR Railway Redis | Redis (used by ApprovalGate) | yes |
| Groq | LLM provider (cheapest fallback) | yes |
| Anthropic | LLM provider (quality drafts) | pay-as-you-go |
| Moyasar | KSA payments — **test mode only at this stage** | yes (test) |
| Meta Developer (optional) | WhatsApp Business webhook | yes |

You do NOT need (yet): SendGrid, Clearbit, Unipile, Tempo/Jaeger.
Each is referenced as "target" in the YAML matrix and is
intentionally not required to boot.

## 1. Clone + provision (10 min)

```sh
git clone https://github.com/voxc2/dealix.git
cd dealix
```

Provision the three data services:

- **Postgres** — Supabase project OR Railway "Add Postgres"
- **Redis** — Upstash database (REST URL; either format works) OR
  Railway "Add Redis"
- **LLM provider** — generate at least a Groq key; Anthropic too if
  you have one

You don't need to run anything locally if you're deploying to
Railway. If you DO want to run locally:

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then edit with the values from §2
```

## 2. Environment variables (8 min)

Set these on Railway (Project → Variables). All are required *for
boot*. Anything not on this list is optional.

```ini
# App
APP_ENV=production
APP_DEBUG=false
APP_DEFAULT_LOCALE=ar
APP_DEFAULT_CURRENCY=SAR
APP_TIMEZONE=Asia/Riyadh

# Data
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DB
REDIS_URL=rediss://default:PASSWORD@HOST:6379

# LLM (need at least ONE)
GROQ_API_KEY=gsk_...
ANTHROPIC_API_KEY=sk-ant-...

# Payments — TEST MODE only at this stage
MOYASAR_SECRET_KEY=sk_test_...
# DO NOT set MOYASAR_ALLOW_LIVE_CHARGE — there is no such flag and
# none should be added until live-charge tests + audit pipeline land.

# Safety defaults — leave these UNSET (defaults are correct).
# WHATSAPP_ALLOW_LIVE_SEND        # → defaults to False; do NOT flip.
```

For Railway specifically:

- It auto-injects `RAILWAY_GIT_COMMIT_SHA`. The `Settings.git_sha`
  field reads that as a fallback. So `/health` will surface the
  real commit SHA on every deploy.

## 3. Deploy (5 min)

Push to `main`. Railway auto-builds via the Dockerfile (the
`railway_deploy.yml` workflow has `paths:` filters for `api/**`,
`core/**`, `dealix/**`, `auto_client_acquisition/**`,
`autonomous_growth/**`, `integrations/**`).

Watch the Railway build log:

- Stage 1 (builder): pip install — ~2 min
- Stage 2 (runtime): copies venv + app — ~30 s
- Health check on `/healthz` — should pass within 20 s of boot

## 4. Verify (5 min)

Replace `https://api.dealix.me` below with your Railway public URL
if you haven't wired a custom domain.

```sh
# 1. Liveness + git SHA
curl -fsS https://api.dealix.me/health
# Expected:
# {"status":"ok","version":"3.0.0","env":"production",
#  "providers":["groq","anthropic"],
#  "git_sha":"<real commit SHA, NOT 'unknown'>"}

# 2. Self-growth read-only API
curl -fsS https://api.dealix.me/api/v1/self-growth/status
# Expected: {"service_activation_available":true, ...,
#            "guardrails":{"no_live_send":true, "no_scraping":true,
#                          "no_cold_outreach":true,
#                          "approval_required_for_external_actions":true}}

# 3. Service Activation Matrix (32 services)
curl -fsS https://api.dealix.me/api/v1/self-growth/service-activation \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d['counts'])"
# Expected: {'live': 0, 'pilot': 1, 'partial': 7, 'target': 24,
#            'blocked': 0, 'backlog': 0, 'total': 32}

# 4. SEO audit report
curl -fsS https://api.dealix.me/api/v1/self-growth/seo/audit \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d['summary'])"
# Expected: pages_with_required_gap == 0
```

## 5. First customer flow (manual, no automation)

This is intentionally manual until the first 3 paid pilots. See
`docs/STRATEGIC_MASTER_PLAN_2026.md` Part VI for the full 90-day
plan.

```sh
# Use the helper to draft a Diagnostic intake template.
python scripts/diagnostic_intake_form.py --company "ACME Saudi"

# When the prospect agrees to Pilot 499 SAR:
#   1. Create a Moyasar invoice via dashboard OR via:
python -c "
from dealix.payments.moyasar import create_invoice
print(create_invoice(amount_sar=499, description='Dealix Pilot 7 days'))
"
#   2. Send the hosted-checkout URL manually (WhatsApp / email)
#   3. Wait for Moyasar webhook → verify in dashboard
#   4. Begin 7-day Pilot delivery

# Record the first ProofEvent manually (until the ledger ships):
mkdir -p docs/proof-events
cp docs/proof-events/SCHEMA.example.json docs/proof-events/<pilot-slug>.json
# Edit with real customer-approved data, commit (with consent).
```

## 6. What this deploy does NOT enable

By design:

- ❌ No live WhatsApp sending — `whatsapp_allow_live_send=False`
- ❌ No live email sending — no `_allow_live_send` field exists for Gmail
- ❌ No live charging — manual Moyasar invoice URL only
- ❌ No scraping — no scraper ever boots; `crawler.py` is gated
- ❌ No LinkedIn DM automation — `SafeAgentRuntime.restricted_actions`
  blocks it at the runtime level
- ❌ No cold WhatsApp — `assess_contactability()` blocks it statically
- ❌ No fake live revenue — first paid pilot must produce a real
  Moyasar transaction + customer-signed Proof Pack

Each of those is enforced by tests in `tests/test_*safety*.py`,
`tests/test_*policy*.py`, `tests/test_live_gates_default_false.py`.

## 7. Common boot issues

| Symptom | Likely cause | Fix |
|---|---|---|
| `/health` returns 200 but `git_sha=unknown` | Neither `GIT_SHA` (Dockerfile ARG) nor `RAILWAY_GIT_COMMIT_SHA` is set | Railway: confirm "Auto-set Railway environment variables" is on. GHCR builds: confirm `docker-build.yml` passes `build-args: GIT_SHA=...`. |
| `/api/v1/self-growth/service-activation` returns 503 | `landing/assets/data/service-readiness.json` missing from the deploy artifact | Re-run `python scripts/export_service_readiness_json.py` and redeploy; `.gitignore` excludes `data/` but unignores this specific file. |
| LLM calls fail with `provider unavailable` | No working LLM key | Set at least `GROQ_API_KEY`; the multi-provider router in `core/llm/router.py` falls back automatically. |
| `assess_contactability` always returns BLOCKED for WhatsApp | This is correct! Cold WhatsApp is blocked by default. Pass `has_opt_in=True` or `has_prior_relationship=True`. | Working as designed. |

## 8. After your first paid pilot

Read `docs/EXECUTIVE_DECISION_PACK.md` and sign off on the 10
decisions. Then ship the next layer per the strategic plan
(`docs/STRATEGIC_MASTER_PLAN_2026.md` Part V.B):

1. Build the ProofEvent ledger (Postgres table + writer + reader)
2. Wire role-specific brief endpoints
3. Add the content draft engine (uses existing `ApprovalGate`)
4. Implement the search radar (only after a search-data source is chosen)

Each layer ships behind tests; none change pricing; none flip live
gates without a separate audit ticket.
