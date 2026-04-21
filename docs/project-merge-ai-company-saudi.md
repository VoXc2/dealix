# Merge: `ai-company-saudi` → Dealix (canonical)

**Status:** canonical repo is `VoXc2/dealix`. The `VoXc2/ai-company-saudi`
repository is a parallel prototype that was briefly run on the same server as
Dealix. This document records what was imported into Dealix, what was
intentionally left behind, and how to safely migrate and decommission the
duplicate stack.

**Last updated:** 2026-04-21

---

## 1. Why we are merging

The two repositories evolved in parallel and describe the same product
("Dealix — سيادي، محوكم بالسياسات"). Running both on the same server produced
concrete operational problems:

- **Redis port 6379 conflict** between the Dealix host Redis and the
  `ai-company-redis` container.
- **MongoDB bound to `0.0.0.0:27017`** in the companion compose file —
  publicly reachable on the host's network.
- **Two competing app runtimes** on the same box (the `dealix-api.service`
  systemd unit plus the companion Docker Compose stack), both trying to own
  port `8000`.
- **Unverified health:** the duplicate app never had a confirmed `/health`
  green light.
- **Credential exposure:** the companion `.env` had `APP_SECRET` pasted into
  a chat/log transcript and the GitHub PAT used for `git pull` was similarly
  exposed. Both must be rotated (see §6).

The correct end state is **one Dealix**: the existing systemd-managed API
behind Nginx, using host PostgreSQL 16, host Redis, fail2ban, and the
Dealix `docker-compose.yml` only for local dev.

---

## 2. What was imported into Dealix

| Area | Source path (ai-company-saudi) | Target path (Dealix) | Why |
|---|---|---|---|
| Action classifications | `dealix/classifications/` | `backend/app/governance/classifications/` | A0–A3 / R0–R3 / S0–S3 taxonomy + `NEVER_AUTO_EXECUTE` register — genuinely new, no equivalent in Dealix. |
| Trust plane | `dealix/trust/` | `backend/app/governance/trust/` | In-process `PolicyEvaluator`, approval request model, tool verification, audit sink. |
| Decision contracts | `dealix/contracts/` | `backend/app/governance/contracts/` | `DecisionOutput`, `EvidencePack`, `EventEnvelope`, `AuditEntry` Pydantic models + JSON Schemas. |
| Registers | `dealix/registers/*.yaml` | `backend/app/governance/registers/` | `no_overclaim.yaml`, `compliance_saudi.yaml`, `technology_radar.yaml`, `90_day_execution.yaml`. |
| Master specs | `dealix/masters/*.md` | `docs/governance/masters/` | Constitution, trust fabric spec, execution fabric spec, evidence pack spec, release readiness checklist, incident rollback runbook, repo operating pack. |
| Decommission script | — | `scripts/server/decommission_ai_company_saudi.sh` | Safe teardown of the companion stack only. |
| Server doctor | — | `scripts/server/server_doctor.sh` | Detects port conflicts (`5432`/`6379`/`8000`/`8001`/`27017`), stray Docker stacks, public DB exposure, Ollama/Nginx/systemd status. |

### Import rules applied

- All `from dealix.` / `import dealix.` imports were rewritten to
  `from app.governance.` / `import app.governance.` so the module lives
  inside the FastAPI backend namespace.
- The package is **additive** — no existing Dealix module was renamed,
  moved, or altered. The governance layer is available for new work but is
  not wired into any existing endpoint. Wiring is intentionally a
  follow-up PR so reviewers can see the import surface first.
- `python -c "from app.governance.classifications import ApprovalClass; ..."`
  succeeds from `backend/` with the existing `pyproject.toml` — no new
  runtime dependencies were added (Pydantic v2 is already in Dealix).

---

## 3. What was intentionally NOT imported

| Area | Reason |
|---|---|
| `api/`, `core/`, `dashboard/` | Dealix already has richer, production-grade equivalents (`backend/app/api/`, `backend/app/ai/`, the Next.js dashboard under `frontend/`). Re-importing would create two competing FastAPI apps in one repo. |
| `core/llm/` (router, anthropic/gemini/glm/openai_compat clients) | Dealix has its own multi-provider layer under `backend/app/ai/providers/` plus the new Ollama local-AI integration (PR #16). The ai-company-saudi router is older and less integrated with Dealix's observability. |
| `integrations/` (HubSpot, LinkedIn, n8n, calendar, whatsapp, email, saudi_market) | Dealix already ships Salla, Zid, Moyasar, Unifonic, WhatsApp, email and ALLaM-provider integrations (PR #14) — and those are the versions hooked into `dealix-api.service`. |
| `auto_client_acquisition/`, `autonomous_growth/` agents | Functionally overlap with `backend/app/agents/{discovery,engagement,qualification,revenue}/`. Keeping two agent trees would fragment the roadmap. The classification/trust layer we *did* import is what gives those Dealix agents the governance layer they were missing. |
| `docker-compose.yml` (ai-company-saudi) | Binds Mongo and Postgres to `0.0.0.0`, and uses hard-coded ports that collide with Dealix's host services. Dealix's existing `docker-compose.yml` is the canonical dev stack. See §4. |
| `Dockerfile` (ai-company-saudi) | Dealix already publishes `backend/Dockerfile` tuned for its layout. |
| `db/`, MongoDB dependency | Dealix is Postgres+Redis. Adding Mongo would mean a third storage engine for no new capability. |
| `scripts/github_setup.sh`, `scripts/seed_data.py`, `scripts/run_demo.py` | Demo-quality; Dealix already has `backend/seed_database.py` and a richer `scripts/` tree. |
| `tests/` | Targets the companion app's module tree; cannot be run as-is against Dealix. New tests for the ported governance layer should live under `backend/tests/governance/` (follow-up). |

---

## 4. Migrating from `/root/ai-company-saudi` to Dealix

Run these commands on the server. **Read §6 on secrets first.**

```bash
# 1. Confirm which Dealix is actually serving traffic
sudo systemctl status dealix-api.service
curl -fsS http://127.0.0.1:8000/health || echo "Dealix API not healthy on :8000"

# 2. Inventory the companion stack WITHOUT stopping anything yet
cd /root/ai-company-saudi
docker compose ps
docker compose config --services

# 3. Run the server doctor from the canonical Dealix checkout
cd /root/dealix  # or wherever Dealix is checked out
bash scripts/server/server_doctor.sh

# 4. Once Dealix is confirmed healthy, decommission the companion stack
bash scripts/server/decommission_ai_company_saudi.sh
```

The decommission script:
- stops only containers whose names start with `ai-company-` (app,
  postgres, redis, mongo),
- removes the compose project,
- **prints — does not run** the `docker volume rm` / `docker network rm`
  commands for `postgres_data`, `redis_data`, `mongo_data` unless invoked
  with `--purge-volumes`,
- copies `/root/ai-company-saudi/.env` to
  `/root/ai-company-saudi.env.bak.<timestamp>` with `chmod 600` before
  teardown.

Nothing in the script touches `dealix-*` containers, host Postgres, host
Redis, or the `dealix-api.service` unit.

---

## 5. Decommissioning checklist (one-time)

- [ ] Dealix API health endpoint returns 200 on `127.0.0.1:8000`.
- [ ] `systemctl is-active dealix-api.service` → `active`.
- [ ] `ss -ltn '( sport = :6379 )'` shows exactly one listener (host Redis).
- [ ] `ss -ltn '( sport = :27017 )'` shows no listener — Mongo is gone.
- [ ] `ss -ltn '( sport = :5432 )'` listener is bound to `127.0.0.1` only.
- [ ] `docker ps --format '{{.Names}}' | grep -c '^ai-company-'` → `0`.
- [ ] Backups: `/root/ai-company-saudi.env.bak.*` and (optionally)
      `docker run --rm -v <vol>:/src -v /root/backups:/dst alpine tar czf ...`
      archive of each companion volume before purge.
- [ ] `fail2ban-client status` shows expected jails active.
- [ ] Nginx reload clean: `sudo nginx -t && sudo systemctl reload nginx`.
- [ ] Reboot the box once after decommission (Ubuntu 24.04 may have kernel
      updates pending from prior apt operations).

---

## 6. Secret rotation (required)

During earlier triage, `APP_SECRET` from the companion `.env` and the
GitHub PAT used by `git pull` were visible in a transcript. Treat both as
compromised and rotate **before** redeploying anything:

1. **Dealix `JWT_SECRET` / `DEALIX_INTERNAL_API_TOKEN`** — generate new
   values (`openssl rand -hex 32`), update the systemd drop-in or
   `/etc/dealix/env`, restart `dealix-api.service`.
2. **GitHub access** — revoke the old PAT under
   GitHub → Settings → Developer settings → Personal access tokens; switch
   to a short-lived fine-grained PAT or, preferably, deploy-key SSH for
   the Dealix checkout.
3. **Companion `APP_SECRET`** — if the same secret is reused anywhere
   (SSO, webhook signing), rotate there too. Do **not** keep the
   companion stack running after rotation — it is being retired.
4. **Provider keys** — if any LLM provider key (Anthropic / OpenAI /
   Groq / Gemini) was copied into the companion `.env`, rotate it in the
   provider console and update the Dealix env file.
5. Run `gitleaks detect --source . --log-level warn` on both repos to
   confirm no credentials are committed.
6. Document the rotation in `docs/operations-runbook.md` and close the
   incident ticket.

This document never prints the old secret values.

---

## 7. Single-runtime rule

Going forward, **only `dealix-api.service` serves production traffic.**
Docker Compose on the server is for one-shot local testing only. If you
need to run the full stack in a container, do it on a workstation or in a
staging VM — never alongside the systemd service.

- `BACKEND_PORT` in `docker-compose.yml` defaults to `8000` and will
  collide with `dealix-api.service`. Set `BACKEND_PORT=8001` in `.env`
  before `docker compose up` if you must run both on the same host.
- `REDIS_PORT` and `POSTGRES_PORT` are also overridable via `.env` for
  the same reason.
- Do **not** bind MongoDB on the server. Dealix does not need it.

---

## 8. Can `ai-company-saudi` be archived?

Yes — after steps §4–§6 are complete and the decommission checklist
(§5) is green, the `VoXc2/ai-company-saudi` GitHub repository can be
archived (Settings → Archive this repository). This document + the
governance layer under `backend/app/governance/` + the master specs
under `docs/governance/masters/` preserve every non-duplicative artifact.

Do not delete the upstream repo — keep it archived so historical links
in issues/PRs continue to resolve.
