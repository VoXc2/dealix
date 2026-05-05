# Dealix v5 — Release Notes

**Release date:** 2026-05-04
**Branch:** `claude/service-activation-console-IA2JK`
**Status:** Code-shipped + tested (Production redeploy depends on Railway pickup)

---

## TL;DR

Dealix v5 is the "Revenue Operating Company OS" — 12 control planes
that turn the existing service catalog into a real, founder-operable
business OS. Everything is **read-only** in production until the
founder explicitly enables it. Hard rules are enforced by tests
and runtime guards, not by trust.

---

## What's new — 12 v5 layers

| # | Layer | What it does |
|---|---|---|
| 1 | **Customer Loop** | 12-state journey machine (lead intake → upsell) with allowed-transitions, bilingual checklists per state |
| 2 | **Role Command OS** | 7 daily role briefs (CEO / Sales / Growth / Partnership / CS / Finance / Compliance) composed from existing signals |
| 3 | **Service Quality** | Per-service QA gate + SLA registry |
| 4 | **Agent Governance** | 6 autonomy levels + 12 tool categories + 12-agent registry, with 5 platform-FORBIDDEN tools that no level can unlock |
| 5 | **Reliability OS** | 9-subsystem health probe matrix |
| 6 | **Vertical Playbooks** | 5 sector catalogs (agency / b2b services / saas / training & consulting / local services) |
| 7 | **Customer Data Plane** | In-memory consent registry + contactability check + PII redactor (Saudi/Gulf phone, email, national ID) |
| 8 | **Finance OS** | Pricing catalog (5 tiers) + invoice draft DTO + live-charge guard (no env combination unlocks money) |
| 9 | **Delivery Factory** | Per-service delivery plan from YAML — bilingual workflow + intake checklist + QA checklist |
| 10 | **Proof Ledger** | File-backed JSONL with PII redaction on write; export_redacted strips customer_handle without consent |
| 11 | **GTM OS** | Content calendar + message experiment, every item approval-required |
| 12 | **Security & Privacy** | Secret scan + log redaction + data-minimization contracts |

---

## What's new — operational polish

### Founder tooling

- `python scripts/dealix_status.py` — bilingual local dashboard
- `python scripts/dealix_smoke_test.py [--base-url ...]` — cross-platform Python smoke test
- `python scripts/dealix_snapshot.py` — JSON audit trail to `docs/snapshots/<date>.json`
- `python scripts/dealix_diagnostic.py --company X --sector Y --region Z --pipeline-state W` — bilingual Diagnostic brief generator
- `python scripts/dealix_invoice.py --email A --amount-sar 499 --description "..."` — manual Moyasar invoice (refuses sk_live_)
- `python scripts/dealix_morning_digest.py [--print]` — daily founder digest (cron 7AM KSA)
- `bash scripts/post_redeploy_verify.sh` — 22-point bash verifier
- `make v5-status` / `v5-smoke` / `v5-snapshot` / `v5-diagnostic` / `v5-verify` / `v5-digest` — all of the above as Make targets

### API endpoints

| Layer | Status endpoint |
|---|---|
| Customer Loop | `/api/v1/customer-loop/{status,states,journey/advance}` |
| Role Command OS | `/api/v1/role-command/{status,<role>}` |
| Service Quality | `/api/v1/service-quality/{status,sla}` |
| Agent Governance | `/api/v1/agent-governance/{status,agents,evaluate}` |
| Reliability OS | `/api/v1/reliability/{status,health-matrix}` |
| Vertical Playbooks | `/api/v1/vertical-playbooks/{status,list,<vertical>,recommend}` |
| Customer Data Plane | `/api/v1/customer-data/{status,consent/grant,consent/withdraw,contactability/check,redact}` |
| Finance OS | `/api/v1/finance/{status,pricing,pricing/<tier>,invoice/draft}` |
| Delivery Factory | `/api/v1/delivery-factory/{status,services,plan/<service>}` |
| Proof Ledger | `/api/v1/proof-ledger/{status,events,units,export/redacted,export/audit}` |
| GTM OS | `/api/v1/gtm/{status,content-calendar,experiment/draft}` |
| Security & Privacy | `/api/v1/security-privacy/{status,scan-text,redact-log,data-minimization}` |
| Diagnostic Engine | `/api/v1/diagnostic/{status,sectors,generate}` |
| Founder aggregate | `/api/v1/founder/{status,dashboard}` |
| CompanyBrain | `/api/v1/company-brain/{status,/}` |

Plus the existing Self-Growth OS at `/api/v1/self-growth/*`.

### Founder pages

- `dealix.me/founder-dashboard.html` — bookmarkable mobile-first bilingual page (noindex, fetches `/api/v1/founder/dashboard`)
- `dealix.me/status.html` — Service Activation Console (existing)

### Documentation

- `docs/V5_FOUNDER_RUNBOOK.md` — daily/weekly/monthly cadence + alert response
- `docs/V5_PHASE_E_CHECKLIST.md` — step-by-step first paying customer playbook
- `docs/V5_SYSTEM_OVERVIEW.md` — one-page module/endpoint/test map
- `docs/V5_COMPLETION_ROADMAP.md` — what's done + what's gated
- `docs/V5_OS_SCOPE.md` — original scope doc with 12/12 closure section
- `docs/V5_MASTER_EVIDENCE_TABLE.md` — row-by-row evidence
- `docs/PRE_COMMIT_SETUP.md` — pre-commit hooks operator guide
- `docs/QUICK_DEPLOY_API_KEYS_ONLY.md` — refreshed with all v5 endpoints

---

## Hard rules — what STILL doesn't work, by design

| ❌ Hard rule | Where it's enforced |
|---|---|
| No live charge under any env combination | `finance_os.is_live_charge_allowed()` + `tests/test_finance_os_no_live_charge_invariant.py` |
| No `MOYASAR_ALLOW_LIVE_CHARGE` env flag | Doesn't exist; CLI requires `--allow-live` AND a sk_test_ key |
| No live WhatsApp send | `whatsapp_allow_live_send=False` default; tested |
| No live email send | No `*_ALLOW_LIVE_*` env exists for email |
| No LinkedIn automation | `agent_governance.FORBIDDEN_TOOLS.LINKEDIN_AUTOMATION` |
| No web scraping | `agent_governance.FORBIDDEN_TOOLS.SCRAPE_WEB` |
| No cold WhatsApp | `compliance_os.assess_contactability` blocks default |
| No PII in proof ledger without redaction | `proof_ledger.FileProofLedger.record` redacts on write |
| No customer name in evidence export without consent | `proof_ledger.export_redacted` anonymizes |
| No service marked `live` without 8 quality gates | YAML validator + `tests/test_service_readiness_matrix.py` |
| No marketing claims `نضمن`/`guaranteed`/`blast` | Regex in `tests/test_landing_forbidden_claims.py` |

Each is wrapped in tests that fail loudly if violated.

---

## Test bundle

```
991 passed, 6 skipped, 3 xfailed
```

Skip count: 6 (down from 8 — `CompanyBrain` skips eliminated).
Xfail count: 3 (free-form Arabic/English safety classifier — deliberate bug tickets).

---

## What's NOT in this release

- ❌ `PROOF_LEDGER_POSTGRES` — file-backed JSONL ships now; Postgres swap deferred until ≥5 ProofEvents land (mechanical swap when ready).
- ❌ `LIVE_GATES_FLIPPED` — every gate stays default-OFF.
- ❌ `ROLE_BRIEF_LLM_ENRICHMENT` — current briefs compose existing signals; LLM enrichment ships only after 90 days of operating data.
- ❌ `SEARCH_RADAR_API` — gated on Decision Pack §B4 (founder picks search-data source).
- ❌ Any service marked `live` in YAML (matrix counts: 0/1/7/24/0).

---

## Upgrading from v4 → v5

Nothing to do. v5 is purely additive — no v4 routes/endpoints removed, no settings renamed, no DB migrations.

The only env additions:

- `DEALIX_FOUNDER_EMAIL` — recipient for daily digest + lead alerts (defaults to `sami.assiri11@gmail.com`)
- `RESEND_API_KEY` — required by daily_digest.yml workflow (already used elsewhere)

Existing `MOYASAR_SECRET_KEY=sk_test_*`, `RAILWAY_GIT_COMMIT_SHA`, `DATABASE_URL`, `REDIS_URL`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY` continue to work unchanged.

---

## Founder's next action

After Railway picks up the latest commit:

```bash
make v5-verify          # 22-point production verifier
make v5-status          # bilingual local dashboard
make v5-diagnostic      # confirm Diagnostic CLI healthy
```

Then begin Phase E (warm intros + first paid pilot) per `docs/V5_PHASE_E_CHECKLIST.md`.

— Release Notes v5.0 · 2026-05-04 · Dealix
