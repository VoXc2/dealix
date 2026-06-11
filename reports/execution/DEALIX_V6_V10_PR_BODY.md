# Dealix V6-V10 Scale Enterprise OS

## Summary
Turns the repo from "launch-ready" into a launchable, operable, measurable, commercially-ready live revenue OS. Adds production data + auth + reliability, safe connectors, AI router with safety + evals, growth engine + SEO + industry pages + campaigns, and enterprise readiness + observability + data room + final PR.

- 250+ files changed
- 8,000+ insertions
- 5 distinct run scripts (V6, V8, V9, V10 + master)
- All verifiers pass in demo mode (no external API keys)

## What changed

### V6 — Production data, auth, admin, reliability
- 8 JSON schemas in `business/_schemas/`
- `scripts/lib/`: data_adapter (mode auto-detect), json_adapter (auto-backup), db_adapter stub, repository, audit_log, backup, errors
- `apps/web/middleware.ts`: gates 13 internal routes; demo mode shows banner, production requires DEALIX_ADMIN_TOKEN
- `/login` + `/api/auth/{check,logout}` route handlers
- Scripts: check_required_env, generate_env_report, restore_business_data
- 5 docs in `docs/data/`, 4 docs in `docs/auth/`
- `scripts/dealix_v6_run_all.py` (9/9 OK)

### V7 — Connectors + lead intelligence + CRM sync
- 7 connectors in `connectors/`: CSV, manual research, website signal (functional) + HubSpot, Google Places, WhatsApp, Email (stubs)
- Shared base + registry + normalizer + source_audit
- `business/sources/`: registry, risk matrix, terms checklist, operating rules
- `business/lead-intelligence/`: quality engine, signal library, weakness hypothesis guide, account research checklist
- `scripts/audit_lead_sources.py` and `export_crm_csv.py`
- 3 docs in `docs/integrations/`

### V8 — AI router + prompt registry + evals
- `scripts/lib/ai_router.py`: provider-agnostic, deterministic fallback, supports MiniMax, Kimi, DeepSeek, OpenRouter, OpenAI
- `scripts/lib/ai_safety.py`: forbidden claims + flags check
- 6 versioned prompts in `business/ai/prompts/`
- 4 eval case files in `business/ai/evals/`
- `scripts/run_ai_evals.py` (5/5 passed in demo)
- 4 docs in `docs/ai/`
- `tests/test_ai_router_fallback.py`

### V9 — Growth + SEO + content + industry pages + campaigns
- 7 industry landing pages (`/industries/[id]`) with `generateStaticParams`
- `/book` (Workflow Review CTA) + `/resources` (8 lead magnets)
- 8 lead-magnet templates (AR + EN) in `business/lead-magnets/`
- `scripts/generate_content_calendar.py` (30 days)
- `scripts/generate_campaign_pack.py` (3 campaigns × AR + EN)
- 4 docs in `docs/growth/`
- `scripts/dealix_v9_run_all.py` (9/9 OK)

### V10 — Enterprise release + observability + data room + final PR
- 9 enterprise docs in `business/enterprise/`
- `/enterprise-readiness` page
- 3 new data-room docs (GTM, risk, roadmap)
- 2 demo scripts in `business/demo/`
- 4 new generators (release notes, health snapshot, incident, demo pack)
- 5 new ops docs (V10 observability, error budget, incident response, backup schedule, release process)
- `scripts/dealix_v10_run_all.py` (12/12 OK)
- `docs/ops/V10_ENTERPRISE_RELEASE_GUIDE.md`

## Safety / governance
- AI-assisted · Human-reviewed · Proof-driven · Built for Saudi operations
- No auto-send (enforced by `tests/test_no_auto_send.py`)
- No scraping (connector plans + stubs respect ToS)
- No fake ROI / fake testimonials
- No PII without consent (`docs/data/DATA_RETENTION_POLICY.md`)
- All demo records clearly marked `demo=true`
- Outreach requires `review_status=approved` before any send
- Audit log on every mutation (`reports/audit/audit-YYYY-MM.jsonl`)

## How to test
```bash
python3 scripts/check_no_secrets.py
python3 scripts/check_required_env.py --mode demo
python3 scripts/verify_dealix_ultimate_os.py
python3 scripts/dealix_daily_operator.py --mode demo
python3 scripts/run_ai_evals.py --mode demo
python3 scripts/generate_content_calendar.py --days 30
python3 scripts/generate_campaign_pack.py --campaign revenue-os --lang both
python3 scripts/generate_demo_pack.py --lang both
python3 scripts/generate_health_snapshot.py
python3 scripts/production_readiness_check.py
python3 scripts/pre_push_guard.py
python3 scripts/dealix_v10_run_all.py
```

## Final verification
- ✅ No secrets
- ✅ Master verification
- ✅ Daily operator 7/7
- ✅ AI evals 5/5
- ✅ Production readiness 5/5
- ✅ Pre-push guard green
- ✅ V6 run-all 9/9
- ✅ V8 run-all 5/5
- ✅ V9 run-all 9/9
- ✅ V10 run-all 12/12
- ✅ Tests: no auto-send + AI router fallback
- ✅ Backup + data integrity + source audit + health snapshot

## Known limitations
- Official connectors (HubSpot, Google Places, WhatsApp Business, Email) are stub-only — need API keys + ToS review
- WhatsApp/email sending is NOT automated — drafts only
- Demo data is not traction — `demo=true` clearly marked
- Database mode (Postgres) requires Alembic migrations (planned V11)
- No 2FA / SSO yet (planned V11+)

## Review checklist
- [x] No auto-send added
- [x] No scraping added
- [x] No fake ROI / fake testimonials
- [x] No PII without consent
- [x] Demo records marked `demo=true`
- [x] All verifiers pass in demo mode
- [x] Daily operator runs end-to-end
- [x] Production readiness check passes
- [x] No secrets committed
- [x] Branch pushed to GitHub
- [x] 5 stage checkpoints committed
- [x] Final commit + push done
