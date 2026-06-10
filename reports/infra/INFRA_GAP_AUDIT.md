# Agent #12 — Infra Gap Audit

**Date:** 2026-06-03
**Auditor:** Agent #12 (Infra, Reliability, Deployment)
**Repository:** https://github.com/Dealix-sa/dealix

---

## 1. Executive Summary

The Dealix repository is **already in a strong production-shape posture**.
Health endpoints, SLOs, backup tiers, secrets scanning, deploy scripts, and
47 GitHub workflows exist. Agent #12 is therefore not building from zero — it
is **codifying, tightening, and closing documentation gaps** so the
operating team (founder + future SRE hire) can answer:

- Which environment are we in, and what is allowed there?
- Is this deploy safe to roll back, and how?
- What metric just broke, who pages, and where is the runbook?
- What is the env-contract drift, and who owns it?

The biggest gaps are **policy and operating-framework docs**, not
infrastructure code. The 2026 research on Agentic Workflow Injection
(`arXiv:2605.07135`) and Indirect Prompt Injection in Tool-Augmented Agents
(`arXiv:2604.11790`) makes the **tool-call-boundary defense** section
mandatory for any new infra doc.

---

## 2. Existing Deploy Setup

| Item | Status | Location |
| --- | --- | --- |
| Railway.toml | ✅ exists | `railway.toml` (healthcheckPath `/healthz`, restart ON_FAILURE, maxRetries 10) |
| Railway.web.toml | ✅ exists | `railway.web.toml` |
| Railway.company-brain.toml | ✅ exists | `railway.company-brain.toml` |
| railway.json | ✅ exists | `railway.json` |
| Multi-stage Dockerfile | ✅ exists | `Dockerfile` |
| Per-app Dockerfiles | ✅ exists | `Dockerfile.web`, `Dockerfile.worker`, `Dockerfile.watchdog`, `Dockerfile.company-brain` |
| docker-compose (local) | ✅ exists | `docker-compose.yml` (Postgres + PgBouncer + Redis + Mongo) |
| docker-compose.prod | ✅ exists | `docker-compose.prod.yml` |
| Procfile | ✅ exists | `Procfile` |
| Pre-deploy hook | ✅ exists | `scripts/railway_predeploy.sh` (857 bytes) |
| Re-deploy checklist | ✅ exists | `scripts/railway_redeploy_checklist.py` |
| Re-deploy verify | ✅ exists | `scripts/post_redeploy_verify.sh`, `scripts/post_redeploy_verify_dealix.py` |
| Server deploy script | ✅ exists | `scripts/server_deploy.sh` |
| Server healthcheck | ✅ exists | `scripts/server_healthcheck.sh` |
| Production config verify | ✅ exists | `scripts/verify_railway_production_config.py` |
| Env matrix check | ✅ exists | `scripts/railway_launch_env_check.py` |
| Generated-env validator | ✅ exists | `scripts/validate_railway_generated_env.py`, `scripts/sync_railway_generated_env.py` |

**Gap:** no single document explains **which deploy path is canonical for
which service** (web, worker, company-brain, watchdog). Founder has to
read 4 separate `railway.*.toml` files plus AGENTS.md to figure it out.

---

## 3. Existing Environment Variables

| File | Purpose |
| --- | --- |
| `.env.example` | Master template (175 lines, all variables) |
| `.env.prod.example` | Production-only subset |
| `.env.railway.example` | Railway-specific subset |
| `.env.staging.example` | Staging-only subset |
| `.dockerignore`, `.claudeignore` | Ignore lists |

Contract: `scripts/check_env_contract.py` (3196 bytes) — the canonical
contract check, runs in `make env-check`.

**Gap:** no `ENV_CONTRACT_AR.md` documenting the **env tier rules**
([REQUIRED] vs [REVENUE] vs [OPTIONAL], flagged in `.env.example` header
comments but not extracted to a doc). Staging/production parity is implicit
in the four env example files but never stated as a policy.

---

## 4. Existing CI Workflows (47 total)

Categorized:

| Category | Workflows |
| --- | --- |
| Core CI | `ci.yml`, `codeql.yml`, `security.yml`, `repository-hardening.yml`, `agentic-security-gate.yml` |
| Deploy | `deploy.yml`, `railway_deploy.yml`, `railway_deploy_frontend.yml`, `docker-build.yml`, `deploy-pages.yml`, `release.yml`, `release-please.yml` |
| Smoke | `production-smoke.yml`, `staging-smoke.yml`, `scheduled_healthcheck.yml`, `production_api_trust_smoke.yml`, `production-watchdog.yml`, `playwright_smoke.yml`, `soft_launch_api_smoke.py` |
| Daily / weekly ops | `daily-revenue-machine.yml`, `daily_digest.yml`, `daily_snapshot.yml`, `business_now_snapshot.yml`, `commercial-expand-weekly.yml`, `governed-full-ops-daily.yml`, `founder_commercial_daily.yml`, `founder_complete_autonomous_weekly.yml`, `founder_weekly_scorecard.yml`, `founder_weekly_verify.yml`, `founder_content_weekly.yml`, `founder_evening_evidence.yml`, `founder_autonomous_ops_weekly.yml`, `weekly_self_improvement.yml`, `weekly-founder-content.yml`, `ctO_weekly_anchor.yml` (typo in actual filename: `cto_weekly_anchor.yml`) |
| Brain / control | `brain-control-command.yml`, `company-brain-daily.yml`, `enterprise-control-plane.yml` |
| Verify / launch | `official-launch-verify.yml`, `verify-full-autonomous-ops.yml`, `local_stack_verify.yml`, `enterprise-readiness.yml`, `reliability_drills_scorecard.yml` |
| Lighthouse / UX | `lighthouse_ci.yml`, `design-system.yml`, `scorecard.yml` |
| Hermes / growth | `hermes-revenue-growth-os.yml` |
| Drift / DLQ | `dlq_check.yml`, `watchdog_drift.yml` |
| Misc | `labeler.yml`, `generate-web-lockfile.yml`, `founder_strongest_ops_daily.yml`, `global-ai-transformation.yml` |

**Gap:** no document distinguishes **read-only workflows** (smoke, verify,
drift) from **action workflows** (deploy, re-deploy, sync). For Agentic
Workflow Injection defense, this distinction is the single most important
hygiene rule and is currently implicit in workflow names.

---

## 5. Existing Docker / Railway Setup

Already covered in §2. **Gap:** no per-image dependency pinning policy.
Dockerfiles exist but pinning rule (digest vs `latest`, Renovate cadence)
is undocumented.

---

## 6. Existing Health Checks

**Strong coverage:**

| Endpoint | Module | Notes |
| --- | --- | --- |
| `/health` | `api/routers/health.py` (line 14) | Standard health response model |
| `/healthz` | `api/routers/platform_meta.py` (line 31) and `health.py` (line 145) | Standard liveness; `?deep=1` for deep probe |
| `/health/deep` | `api/routers/health.py` (line 40) | DB-aware deep check |
| `/health/live` | `api/security/api_key.py` (line 38) | Public, liveness |
| `/health/ready` | `api/security/api_key.py` (line 39) | Public, readiness |
| Per-router `/health` | simulation_os, self_evolving_os, sandbox_os, runtime_safety_os, org_graph_os, human_ai_os, platform_foundation, public, value_engine_os | Module-level health |
| `/api/v1/reliability/health-matrix` | `api/routers/reliability_os.py` (line 29) | Aggregated matrix |
| `/api/v1/revenue-metrics/health-check` | `revenue_metrics.py` (line 299) | Revenue health |
| `/api/v1/founder/launch-status` | `founder_launch_status.py` (line 231) | Single-pane readiness JSON |
| `/api/v1/kpi/health-score` | `kpi_dashboard.py` (line 306) | AI-calculated health score |

Railway healthcheck is wired to `/healthz`. UptimeRobot polls documented in
`docs/SLO.md` Tier 1.

**Gap:** the **liveness vs readiness split** is implemented in code
(`/health/live`, `/health/ready`) but is not documented in a single
`HEALTH_CHECKS_AR.md` or `READINESS_LIVENESS_POLICY_AR.md`. New services
(company-brain, worker, watchdog) lack explicit liveness/readiness probes
in their Dockerfiles.

---

## 7. Existing Observability / Logging

| Surface | Status |
| --- | --- |
| PostHog | ✅ `POSTHOG_API_KEY`, `POSTHOG_HOST` in env; `docs/observability/posthog_dashboard.json` |
| Sentry | ✅ `SENTRY_DSN` in env; `docs/observability/sentry_alerts.yaml` |
| Metrics middleware | ✅ `api/middleware/metrics.py` |
| Privileged audit middleware | ✅ `api/middleware/privileged_audit.py` |
| IP allowlist middleware | ✅ `api/middleware/ip_allowlist.py` |
| Log level | `LOG_LEVEL=INFO` in env, set to INFO by default |

**Gap:** no single document defines **what must be in every log line**
(trace_id, request_id, actor_id, action_type, approval_state, risk_level)
nor a **PII redaction rule** at the log layer. The `no_pii_in_logs` test
exists but the operational log format is not pinned.

---

## 8. Existing Backup / Restore

**Excellent coverage** (see `docs/ops/BACKUP_RESTORE.md`):

- 5 tiers (Hourly → Daily → Weekly → Monthly → Yearly)
- S3 encryption (AES-256-CBC + PBKDF2)
- 1Password vault for encryption key
- `scripts/hourly_backup.sh`, `scripts/server_backup.sh`, `scripts/setup_aws_backup.sh`
- `scripts/restore_test.sh` and `scripts/verify_backup.py`
- Quarterly restore drill documented

**Gap:** disaster recovery (RTO/RPO targets, regional failover,
multi-region) is mentioned but not formalized. `DISASTER_RECOVERY_AR.md`
is missing.

---

## 9. Existing Rollback

- `scripts/post_redeploy_verify.sh` runs **after** deploy
- `scripts/railway_redeploy_checklist.py` for re-deploys
- `railway.toml` has `restartPolicyType = "ON_FAILURE"` and
  `restartPolicyMaxRetries = 10`

**Gap:** explicit **rollback policy** (when to roll back, who can roll
back, time budget, data-loss rules) is not in a single doc.

---

## 10. Secret-Handling Risks

| Existing | Note |
| --- | --- |
| `.gitleaks.toml` + `.secrets.baseline` | Pre-commit secret scanning |
| `pre-commit-config.yaml` | Hook enforcement |
| `scripts/security_smoke.py` | Repo-level smoke check |
| `detect-secrets` baseline | Tracked separately |
| `.env.example`, `.env.prod.example`, `.env.staging.example` | Templates only, real `.env` gitignored |
| `1Password vault` reference in `BACKUP_RESTORE.md` | For `BACKUP_ENCRYPTION_KEY` |

**Risks identified:**

1. Many env vars in `.env.example` are duplicated in
   `.env.prod.example` / `.env.railway.example` — drift risk, no contract
   test pins the three in sync.
2. No documented policy on **who can read production secrets** (founder
   only? future SRE hire? CI bot?).
3. AGENTS.md says "no production secret sprawl" but there is no
   `SECRETS_MANAGEMENT_AR.md` to define what "sprawl" means operationally.
4. The `agentic-security-gate.yml` workflow exists but its allowlist
   policy (which untrusted inputs are allowed into which tools) is not
   documented.

---

## 11. Production Readiness Gaps

| Gap | Severity | Phase |
| --- | --- | --- |
| No `docs/infra/` directory | HIGH | Phase 1 |
| No environment policy document | HIGH | Phase 1 |
| No secrets management policy document | HIGH | Phase 1 |
| No env contract documentation (only script) | MEDIUM | Phase 1 |
| No configuration-drift policy | MEDIUM | Phase 1 |
| No health-checks / readiness-liveness policy doc | MEDIUM | Phase 2 |
| No production-readiness checklist (one-shot) | MEDIUM | Phase 2 |
| No observability operating-system doc | MEDIUM | Phase 3 |
| No logging / metrics / alerting policy doc | MEDIUM | Phase 3 |
| No disaster-recovery doc | MEDIUM | Phase 4 |
| No rollback policy doc | MEDIUM | Phase 4 |
| No data-export policy doc | LOW | Phase 4 |
| No CI/CD policy / approval / release doc | MEDIUM | Phase 5 |
| No `infra-readiness-review.yml` workflow | LOW | Phase 5 |
| No `production-readiness-gate.yml` workflow | LOW | Phase 5 |

---

## 12. Recommended Implementation Order

1. **Phase 1** — Environment Policy, Secrets, Env Contract, Drift Policy.
   *Why first:* these are the prerequisites for every other phase and
   they are the cheapest to write.
2. **Phase 2** — Health Checks, Readiness, Production-Readiness Checklist.
   *Why second:* build on env policy; codify the endpoints that already
   exist.
3. **Phase 3** — Observability, Logging, Metrics, Alerting.
   *Why third:* needs a stable env contract to bind log format to.
4. **Phase 4** — Backup/Restore (already strong), Rollback Policy,
   Disaster Recovery, Data Export.
   *Why fourth:* leverage existing scripts; close the policy gap.
5. **Phase 5** — CI/CD Hardening, Deployment Approval, Release Checklist,
   `infra-readiness-review.yml`, `production-readiness-gate.yml`.
   *Why last:* these gate everything else, so they need stable policies
   to reference.
6. **Phase 6** — Final Report.

---

## 13. Non-Negotiable Cross-Cutting Rules

These rules MUST be embedded in every Phase 1-5 doc:

1. **Tool-call boundary defense** (per `arXiv:2604.11790`):
   no untrusted input (issue body, PR comment, fetched web content, MCP
   response, skill file) may reach a tool call that can mutate state, send
   messages, or move money.
2. **Agentic workflow injection hygiene** (per `arXiv:2605.07135`):
   workflows that ingest `pull_request_target`, `workflow_run`, or any
   untrusted text must declare an allowlist + a manual approval gate for
   production-affecting steps.
3. **No secrets in logs, reports, prompts.**
4. **Staging first, production requires founder approval.**
5. **No destructive migrations, no production deploy, no live external
   sends** from any agent in this run.

---

## 14. Founder Next Actions

1. Approve Phase 1 docs.
2. Decide on **production secret owner roster** (founder-only for now?).
3. Approve **deploy path canonicalization** (which Railway service is the
   primary API, which is the web, which is the brain, which is the worker).
4. Schedule a **first quarterly restore drill** (procedures exist; the
   drill itself has not been run yet, per BACKUP_RESTORE.md).
5. Approve a **UptimeRobot API key** to wire Tier 1 SLI measurement
   (already flagged as a blocker in SLO.md).
