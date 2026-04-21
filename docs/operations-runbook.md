# Dealix — Operations Runbook

**Target environment:** single Ubuntu 24.04 VM, 4 vCPU AMD EPYC, 7.6 GiB RAM, 150 GB disk, no GPU.
**Stack:** docker compose (backend, frontend, postgres, redis, nginx) + host-level Ollama + Let's Encrypt.
**Audience:** founder + one on-call engineer.

All commands assume you are `ssh dealix@prod` as the `dealix` user with sudo, working from `/opt/dealix` (the compose root).

---

## 0. One-page cheat sheet

| Want to… | Command |
|---|---|
| See if site is up | `curl -sf https://dealix.example/api/v1/health \|\| echo DOWN` |
| Tail all logs | `docker compose logs -f --tail=200` |
| Restart backend only | `docker compose restart backend` |
| Restart frontend only | `docker compose restart frontend` |
| Deploy latest main | `git pull && docker compose up -d --build backend frontend && docker compose exec backend alembic upgrade head` |
| Rollback to previous tag | `git checkout <prev-tag> && docker compose up -d --build && docker compose exec backend alembic downgrade -1` |
| Dump DB now | `docker compose exec -T db pg_dump -U dealix dealix \| gzip > /var/backups/dealix/manual-$(date +%F-%H%M).sql.gz` |
| See local AI status | `curl -s localhost:8000/api/v1/local-ai/status \| jq` |
| Ollama logs | `journalctl -u ollama -n 200 --no-pager` |
| Disk usage | `df -h / && docker system df` |
| Kill runaway container | `docker compose kill <service> && docker compose up -d <service>` |

Everything below is the longer form of these.

---

## 1. Deploy

### 1.1 Standard deploy (main → prod)

```bash
cd /opt/dealix
git fetch --all
git checkout main
git pull --ff-only
docker compose pull
docker compose up -d --build backend frontend
docker compose exec backend alembic upgrade head
bash scripts/qa/smoke_test.sh   # expect all green
```

If smoke test reports failures, **do not walk away**. Either roll forward with a fix PR or roll back (see §2).

### 1.2 Deploy a specific commit

```bash
git checkout <sha>
docker compose up -d --build backend frontend
docker compose exec backend alembic upgrade head
```

### 1.3 Deploying changes that include migrations

1. Snapshot DB first (§5.1).
2. `alembic upgrade head`.
3. If it fails: `alembic downgrade -1`, then investigate before retry.

---

## 2. Rollback

### 2.1 Code-only rollback (no schema change)

```bash
cd /opt/dealix
git log --oneline -10              # find previous good commit/tag
git checkout <prev-sha>
docker compose up -d --build backend frontend
bash scripts/qa/smoke_test.sh
```

### 2.2 Rollback that crosses a migration

1. `git checkout <prev-sha>`
2. Read the migration file(s) added by the version being rolled back.
3. `docker compose exec backend alembic downgrade <target_revision>`
4. If downgrade lacks a working `downgrade()` function: **restore from last pre-deploy DB dump** (§5.2). Do not run schema-dropping SQL by hand.

### 2.3 Total service failure

```bash
docker compose down
docker compose up -d
bash scripts/qa/smoke_test.sh
```

If that is not enough: restore yesterday's DB dump (§5.2), then pull previous image tag.

---

## 3. Logs

### 3.1 Where logs live

| Source | Location |
|---|---|
| Backend (FastAPI) | `docker compose logs backend` → also `/var/log/dealix/backend.log` if volume mount enabled |
| Frontend (Next.js) | `docker compose logs frontend` |
| Postgres | `docker compose logs db` |
| Redis | `docker compose logs redis` |
| Nginx | `/var/log/nginx/access.log`, `/var/log/nginx/error.log` |
| Ollama (host) | `journalctl -u ollama` |
| System | `journalctl -xe`, `dmesg -T` |

### 3.2 Common greps

```bash
# Errors in the last hour
docker compose logs --since 1h backend | grep -E 'ERROR|CRITICAL|Traceback'

# Trace a request by id
docker compose logs backend | grep '<trace-id>'

# 5xx from nginx
grep ' 5[0-9][0-9] ' /var/log/nginx/access.log | tail -50
```

### 3.3 Log rotation

`/etc/logrotate.d/dealix` should rotate `/var/log/dealix/*.log` and `/var/log/nginx/*.log` daily, 14 days retained. Verify:

```bash
sudo logrotate -d /etc/logrotate.d/dealix
```

---

## 4. Service management

### 4.1 docker compose services

```bash
docker compose ps                    # status
docker compose restart backend       # graceful restart
docker compose stop backend          # stop
docker compose up -d --build backend # rebuild + start
docker compose exec backend bash     # shell inside backend
```

### 4.2 Host-level services

| Service | Manage with |
|---|---|
| Ollama | `sudo systemctl {status,restart,stop,start} ollama` |
| Nginx  | `sudo systemctl {status,restart,reload} nginx` |
| Certbot renewal | `sudo systemctl list-timers \| grep certbot` |

### 4.3 Redis

```bash
docker compose exec redis redis-cli ping              # expect PONG
docker compose exec redis redis-cli info memory
docker compose exec redis redis-cli flushdb           # DANGER — dev only
```

### 4.4 Postgres

```bash
docker compose exec db psql -U dealix -d dealix
\dt                     # list tables
\l                      # list dbs
SELECT now();           # sanity
```

### 4.5 Ollama health

```bash
curl -s localhost:11434/api/tags | jq '.models[].name'
curl -s localhost:8000/api/v1/local-ai/status | jq
curl -s localhost:8000/api/v1/local-ai/health-check | jq
```

If models are missing:

```bash
ollama pull qwen2.5:0.5b
ollama pull qwen2.5:3b-instruct
```

Disk fill from models: `du -sh ~/.ollama/models/`. Budget 10 GB for this tier.

---

## 5. Backups

### 5.1 Nightly (cron)

`/etc/cron.d/dealix-backup`:

```
15 2 * * * dealix /opt/dealix/scripts/ops/backup_db.sh >> /var/log/dealix/backup.log 2>&1
```

The script should `pg_dump`, gzip, upload to object storage, keep 14 local copies, delete older.

### 5.2 Restore

```bash
# Stop traffic first
docker compose stop backend

# Drop + restore (DANGEROUS — confirm which DB file you are using)
BACKUP=/var/backups/dealix/dealix-YYYY-MM-DD.sql.gz
gunzip -c "$BACKUP" | docker compose exec -T db psql -U dealix -d dealix

docker compose start backend
bash scripts/qa/smoke_test.sh
```

Practice restore into a scratch DB at least monthly (`docker compose exec db createdb -U dealix dealix_restore_test`).

### 5.3 Object storage

Backups go to an off-VM bucket (S3-compatible). Credentials live in `/etc/dealix/env`, not in git.

---

## 6. Monitoring

### 6.1 External

- UptimeRobot / Healthchecks.io pings `GET /api/v1/health` every 60 s. Alert on 2 consecutive fails.
- Certificate expiry alert at 14 days.

### 6.2 Internal

- `docker stats` snapshot every 5 min written to `/var/log/dealix/docker-stats.log`.
- `df -h` + `free -h` snapshot every 15 min.

### 6.3 Dashboards

- Nginx access log → daily summary mailed to founder (home-grown awk script, fine for launch scale).
- Postgres slow query log (> 500 ms) reviewed weekly.

---

## 7. Common failure playbooks

### 7.1 "Site is down"

1. From laptop: `curl -v https://dealix.example/api/v1/health`.
2. If DNS fails → check Cloudflare / registrar.
3. If TLS fails → `sudo certbot renew`. Then `sudo systemctl reload nginx`.
4. If 502: `docker compose ps`. Restart backend.
5. If 500: `docker compose logs --tail=200 backend`. Grep for `Traceback`.
6. If 504: DB may be slow. `docker compose exec db psql -U dealix -c "SELECT pid, state, query FROM pg_stat_activity WHERE state != 'idle';"` and kill runaway queries.

### 7.2 "Ollama not responding"

1. `sudo systemctl status ollama`
2. `journalctl -u ollama -n 100`
3. Disk full? `df -h`. Delete old models: `ollama rm <model>`.
4. OOM killed? `dmesg -T | grep -i oom`. Reduce tier to `nano` (only `qwen2.5:0.5b`).
5. Restart: `sudo systemctl restart ollama`. Wait 10 s. `curl -s localhost:11434/api/tags`.
6. If still bad: set `LOCAL_LLM_ENABLED=0`, restart backend → fallback to Groq. Fix Ollama offline.

### 7.3 "Postgres refuses connections"

1. `docker compose ps db` — running?
2. `docker compose logs db | tail -100` — look for `FATAL` or disk-full.
3. Disk: `df -h`. Postgres will stop on a full disk. Free space (prune images: `docker image prune -a`), then `docker compose restart db`.
4. Connection limit: `SELECT count(*) FROM pg_stat_activity;`. If saturated, restart backend to drop idle connections.

### 7.4 "Redis eviction storm"

1. `docker compose exec redis redis-cli info stats | grep evicted`.
2. Bump `maxmemory-policy` to `allkeys-lru` in compose override if not already.
3. Rolling restart backend to clear stale session data.

### 7.5 "High memory / swapping badly"

Specs are tight (7.6 GiB). If swap is > 50% used:

1. `docker stats --no-stream`. Who is hogging?
2. If Ollama: confirm tier is `small` not `balanced`. `LOCAL_LLM_FORCE_TIER=small`.
3. If backend: look for a celery worker leak; restart backend.
4. Ensure 4 GiB swap file exists (see Launch Plan §2.5).

### 7.6 "Deploy broke on migrate"

1. `alembic downgrade -1`.
2. If downgrade also fails: restore from §5.2.
3. Open incident in `docs/reality_reviews/`.

---

## 8. Emergency

### 8.1 Data leak suspected

1. Rotate all `.env` secrets immediately.
2. Invalidate all JWTs: bump `JWT_SECRET` → restart backend.
3. Revoke any third-party tokens (Moyasar, WhatsApp, Groq, OpenAI).
4. Capture evidence: `docker compose logs --since 48h backend > /var/log/dealix/incident-$(date +%F).log`.
5. Notify pilot customers within 72 h per PDPL.
6. Document in `docs/legal/incident-log.md`.

### 8.2 Accidental prod data delete

1. Stop backend immediately: `docker compose stop backend`.
2. Restore most recent pre-incident backup to a **scratch DB**.
3. Extract missing rows; re-insert into prod.
4. Never restore the whole prod DB on top of live data without a written plan.

### 8.3 Compromised SSH / host

1. Kick all sessions: `sudo pkill -KILL -u <suspected-user>` (skip if you're not sure).
2. `last -i`, `ss -tnp`, `netstat -plant` → unknown connections.
3. Rotate SSH keys. Disable password auth in `/etc/ssh/sshd_config`.
4. Rebuild the VM from scratch is often safer than cleaning it.

---

## 9. On-call notes

- **Pager hours:** founder 24/7 until Phase Gate; engineer business hours only.
- **Escalation:** after 15 min of 5xx rate > 5%, post status on founder's WhatsApp to pilot contacts.
- **Change freeze:** no deploys Thu 18:00–Sat 12:00 Riyadh unless fixing an active incident.

---

## 10. Appendix — expected env vars

Required in `/etc/dealix/env` (loaded by compose):

```
POSTGRES_PASSWORD=<rotate>
JWT_SECRET=<rotate ≥32 chars>
DEALIX_INTERNAL_API_TOKEN=<rotate>
GROQ_API_KEY=<real>
OPENAI_API_KEY=<real, fallback>
MOYASAR_SECRET_KEY=<prod>
WHATSAPP_ACCESS_TOKEN=<prod>
WHATSAPP_PHONE_NUMBER_ID=<prod>
LOCAL_LLM_ENABLED=1
LOCAL_LLM_FORCE_TIER=small
ENVIRONMENT=production
LOG_LEVEL=INFO
```

If any of these are missing, the backend may start but refuse to serve — check `docker compose logs backend` for `config validation error`.

---

## 14. Single-runtime rule & port hygiene

On the production VM there is exactly one Dealix: the `dealix-api.service`
systemd unit behind Nginx, using host PostgreSQL 16 and host Redis. Docker
Compose on the server is a **development-only** convenience. Running both at
once causes the conflicts observed during the `ai-company-saudi` merge:

| Conflict | Symptom | Fix |
|---|---|---|
| Host Redis + container Redis on `:6379` | Second container restarts, or app sees stale data | `docker compose down` the container OR set `REDIS_PORT=6380` in `.env` |
| Host Postgres + container Postgres on `:5432` | Container crashes on bind OR inserts land in the wrong DB | Stop the container OR set `POSTGRES_PORT=5433` |
| `dealix-api.service` + container backend on `:8000` | 502s, intermittent routing | Stop the container OR set `BACKEND_PORT=8001` |
| Mongo exposed on `0.0.0.0:27017` | Publicly reachable NoSQL, no auth | Do **not** run Mongo on the server. Dealix does not need it. |

Run `scripts/server/server_doctor.sh` before any deploy; it enforces the
single-listener rule on each of these ports and flags public DB exposure.

## 15. Git checkout hygiene on the server

- Prefer an SSH deploy key tied to the `dealix` user:
  `ssh-keygen -t ed25519 -f ~/.ssh/dealix_deploy -C dealix-prod` and paste the
  public key into the repo's **Deploy keys** (read-only).
- If a PAT is unavoidable, use a **fine-grained** PAT scoped only to the
  Dealix repo with `Contents:read`, and set an expiry ≤ 90 days. Never paste
  the PAT into chat transcripts or logs.
- If a PAT or `APP_SECRET` has ever been visible outside the server, rotate
  immediately (see §16 and `docs/project-merge-ai-company-saudi.md` §6).

## 16. Secret rotation — emergency path

Use when a secret is suspected to have leaked (for example: `APP_SECRET` or
a GitHub PAT was pasted into a chat, a `.env` was copied to an off-host
machine, or a backup was exported without encryption).

1. Generate the new value (`openssl rand -hex 32`).
2. Update `/etc/dealix/env` (or the systemd drop-in) and restart
   `dealix-api.service`.
3. Verify `/health`.
4. Revoke the old token in the provider console AFTER the new one is live.
5. Scan git history: `gitleaks detect --source . --no-banner`.
6. Record the rotation in `docs/execution_log.md`.

## 17. Decommissioning a parallel stack

If someone (or a prior you) has left a companion Docker stack running, use
`scripts/server/decommission_ai_company_saudi.sh` — it is dry-run by default,
touches only `ai-company-*` resources, and leaves Dealix alone. Pair it with
`scripts/server/server_doctor.sh` to confirm a clean host before and after.

After decommission, reboot the VM once to clear any pending kernel updates
that were deferred during earlier `apt` operations.
