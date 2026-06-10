# Rollback Runbook

> When something is on fire, this is the playbook. Don't improvise.

## Trigger
Any one of:
- Abort criterion from `RELEASE_DAY_RUNBOOK.md`
- New SEV-1 within 24h of a deploy
- Data integrity discrepancy from reconciliation
- Security event (credential leak / unauthorized access)

Declare rollback in `#dealix-launch` with: `ROLLBACK triggered: <reason>`.

---

## Decision tree

```
Is this a code regression?  ──yes──→  Code rollback (path A)
       │
       no
       ↓
Is this a DB / migration issue?  ──yes──→  DB rollback (path B)
       │
       no
       ↓
Is this an external service breaking?  ──yes──→  Service shield (path C)
       │
       no
       ↓
Is this a security event?  ──yes──→  Security rotation (path D)
       │
       no
       ↓
Open SEV-1 → war room → continue investigation, do not deploy.
```

---

## Path A — Code rollback (Railway)

**Time budget: 5 minutes**

1. Railway dashboard → service `dealix` → **Deployments**
2. Find the most recent **healthy** deployment (before the bad one)
3. Click `⋯` → **Redeploy**
4. Wait for new deployment to become Active (typically 2–3 min)
5. Smoke check:
   ```bash
   curl https://api.dealix.me/healthz                    # → 200
   curl https://api.dealix.me/api/v1/pricing/plans | jq  # → 4 plans
   ```
6. Update status page: "Investigating → Identified → Resolved"
7. Open SEV-1/2 ticket and start the post-mortem doc immediately while context is fresh

**If Railway dashboard is itself unhealthy:**
```bash
railway login --browserless   # uses RAILWAY_TOKEN
railway link <project-id>
railway service dealix
railway redeploy --deployment <prior-deploy-sha>
```

---

## Path B — Database rollback

**Time budget: depends on scope; can be 15min → 4h**

### B1 — Simple Alembic downgrade (schema-only, no data lost)
Use only if the migration was strictly additive and we're certain no rows depend on the new schema:
```bash
alembic downgrade -1
```

### B2 — Migration is destructive / data is corrupted

```bash
# 1. Pause writes
#    Railway → set MAINTENANCE_MODE=1 → save → redeploy
#    API returns 503 on writes; reads still possible

# 2. Identify the right backup
ls -lt /var/backups/dealix/dealix-*.pgdump* | head -10

# 3. Restore to a SCRATCH DB first to verify integrity
RESTORE_DATABASE_URL=postgresql://scratch:scratch@scratch-db.local:5432/scratch \
BACKUP_ENCRYPTION_KEY=<from-1password> \
EXPECTED_MIN_LEADS=100 \
bash scripts/restore_test.sh

# 4. If scratch restore PASS, restore to production:
pg_restore --clean --if-exists --no-owner --no-privileges \
  --dbname="$PROD_DATABASE_URL" \
  /var/backups/dealix/dealix-<TIMESTAMP>.pgdump

# 5. Unset maintenance, redeploy
#    Railway → MAINTENANCE_MODE=0 (or remove) → save → redeploy
```

**Data lost between last backup and incident = RPO ≤ 1h.** Communicate this to affected customers honestly.

---

## Path C — External service shield

Used when an external dependency (Moyasar, Meta, Google, etc.) is the source of failure.

1. **Identify the dependency** (Sentry breadcrumbs + status page of provider)
2. **Activate the relevant feature flag** to bypass:
   ```bash
   # Railway env vars (toggle as needed)
   MOYASAR_DISABLE_AUTO=1       # use manual_payment_sop for new orders
   WHATSAPP_ALLOW_LIVE_SEND=false   # pause outbound
   LLM_FALLBACK_CHAIN=local_only    # disable cloud LLM
   ```
3. **Inform customers** via banner on landing + status page
4. **Wait for provider** to recover; do NOT migrate to a fallback provider in the middle of an outage unless explicitly tested

---

## Path D — Security rotation (emergency)

If credentials are compromised:

1. **Mark compromised in 1Password** (red flag tag)
2. **Rotate immediately** in this order (most-blast-radius first):
   - `ADMIN_API_KEYS` (revokes all admin access)
   - `MOYASAR_WEBHOOK_SECRET` (also update Moyasar dashboard)
   - `MOYASAR_SECRET_KEY` (Moyasar dashboard → revoke + regenerate)
   - `JWT_SECRET_KEY` (invalidates all sessions; users re-login)
   - `APP_SECRET_KEY`
   - `API_KEYS`
   - `RAILWAY_TOKEN`
   - `BACKUP_ENCRYPTION_KEY` only if backup vault may be compromised
3. **Audit access logs** for the last 30 days — any anomalous use of the rotated keys
4. **Open PDPL breach assessment** per `PDPL_BREACH_RUNBOOK.md` if personal data may have been touched
5. **Post-mortem within 48h**

---

## Communication script (for status page / customer email)

> Status: **Investigating** (then **Identified** → **Resolved**)
>
> "Some Dealix users may be experiencing [degradation type] since [time]. We've identified the cause and are rolling back. Next update in 30 minutes."
>
> _Resolved version_:
> "All Dealix services restored as of [time]. We will publish a full post-mortem within 48 hours. We apologise for the disruption."

Never speculate publicly about the cause until the post-mortem is published.

---

## Post-mortem (within 48h)

Use `INCIDENT_RUNBOOK.md:128-134` template. Required sections:
1. Summary (1 paragraph)
2. Impact (who, how many, for how long)
3. Timeline (UTC timestamps)
4. Root cause
5. Resolution
6. What went well
7. What went poorly
8. Action items (owner + due date)

File in `docs/ops/incidents/<date>-<slug>.md`. Link from `docs/ops/incident_index.md`.

---

## Drills

- Tabletop once per quarter: pick a fictional SEV-1, walk through this runbook end-to-end with the team
- Live drill once per year: actually run a rollback on staging end-to-end (announced in advance)

Record drills in `docs/ops/observability_drills.md`.
