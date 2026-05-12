# Zero-to-prod runbook

> Single document a new SRE follows to deploy Dealix from a clean
> machine to a live production tenant. Each step is idempotent.

## Pre-requisites

You need:

- A Railway / AWS / GCP account (for Terraform target).
- A managed Postgres 16 (RDS / Cloud SQL / Neon / Supabase) with the
  `pgvector` and `pg_partman` extensions enabled.
- A managed Redis 7 endpoint.
- A Cloudflare account with the apex domain pointed at the platform.
- A GitHub Actions environment named `production` with two
  approvers (founder + co-founder).
- 1Password / Bitwarden / Infisical for secrets.

## Step 1 — Bootstrap

```sh
# Clone + verify the checkout.
git clone git@github.com:VoXc2/dealix.git
cd dealix
make hooks            # pre-commit + commit-msg hooks installed.
bash scripts/dev/install_dev.sh   # Python venv + Node deps.
pytest -q tests/unit/             # baseline green.
```

## Step 2 — Provision infra (Terraform)

```sh
cd infra/terraform/live/prod
cp prod.auto.tfvars.example prod.auto.tfvars
# fill in railway_token, railway_project_id, cloudflare_api_token,
# anthropic_api_key, openai_api_key, sentry_dsn.

terraform init
terraform plan
# review the diff. ONLY apply after human approval.
terraform apply
```

What Terraform creates:

- Railway service `dealix-api-prod` building from `main` branch.
- Postgres + Redis add-ons attached.
- Cerbos sidecar service.
- Cloudflare DNS for `api.dealix.me` and `app.dealix.me`.

## Step 3 — Database migrations

```sh
DATABASE_URL=postgres://… alembic upgrade head
```

Confirm `alembic heads` returns a single revision.

## Step 4 — Optional: single-host Docker pilot

For founder-managed pilots, skip step 2/3 and use the compose file:

```sh
# On the pilot host (≥ 4 GB RAM):
git clone …; cd dealix
cp .env.example /opt/dealix/.env  # fill secrets.
docker compose -f deploy/docker-compose.prod.yml up -d
# Verify:
docker compose logs api --tail 50
curl https://api.<your-domain>/healthz
```

## Step 5 — Kubernetes deploy (Helm)

When you outgrow the single-host pilot:

```sh
kubectl create namespace dealix-prod
kubectl create secret generic dealix-secrets -n dealix-prod \
  --from-env-file=/opt/dealix/.env
helm install dealix deploy/helm/dealix -n dealix-prod \
  --values deploy/helm/dealix/values.prod.yaml
kubectl get pods -n dealix-prod -w
```

## Step 6 — Smoke tests

```sh
# 1. Health.
curl https://api.dealix.me/healthz
curl https://api.dealix.me/health/deep | jq '.checks.vendors'

# 2. Skills runtime.
curl -X POST https://api.dealix.me/api/v1/skills/sales_qualifier/run \
     -H 'X-API-Key: <tenant-key>' \
     -d '{"inputs":{"lead_snapshot":{"budget":"y","authority":"y","need":"y","timeline":"y"},
                    "compliance_signals":{"has_pdpl_consent":true}}}'
# expect: {"result":{"score":1.0,"recommended_action":"qualify_and_book_meeting"}, …}

# 3. ZATCA + payments health.
curl https://api.dealix.me/api/v1/billing/health
curl https://api.dealix.me/api/v1/billing/gcc/health
```

## Step 7 — Backup + DR drill

```sh
# Cron the backup (host crontab):
0 2 * * * bash /opt/dealix/scripts/infra/backup_pg.sh

# Schedule the S3-verify cron:
0 3 * * * bash /opt/dealix/scripts/infra/backup_s3_verify.sh

# Run the DR drill once a quarter (dry-run on shared infra, real
# against a scratch DB):
bash scripts/infra/dr_restore_drill.sh --dry-run
```

## Step 8 — Observability

1. Sentry DSN → `SENTRY_DSN` env. Tail:
   `https://sentry.io/organizations/<org>/issues/`.
2. PostHog project key → `POSTHOG_API_KEY`. Tail:
   `https://app.posthog.com/`.
3. BetterStack heartbeat URL → `BETTERSTACK_HEARTBEAT_URL`. Status
   page renders at `status.dealix.me` automatically.
4. Optional: Grafana dashboards in `infra/grafana/dashboards/` —
   import each JSON via Grafana UI or provision via
   `infra/grafana/provisioning.yaml`.

## Step 9 — Cut over DNS

Update the apex `dealix.me` and `app.dealix.me` A/AAAA records to
point at the Cloudflare-fronted ingress.

## Step 10 — Post-launch checklist

- [ ] First five tenants onboarded via `/api/v1/onboarding/*`.
- [ ] ZATCA Phase 2 certificate uploaded.
- [ ] WorkOS organisation linked for the first enterprise tenant.
- [ ] Stripe + Moyasar webhook URLs registered.
- [ ] Loops list ingested with the trial sequence.
- [ ] `/.well-known/security.txt` returns 200.
- [ ] Public sub-processor page (`landing/trust/sub-processors.html`)
      renders the current list.
- [ ] `docs/sla.md` matches the actual environment.
- [ ] Founder-on-call + secondary in `OPS_ROTATION.md`.

## Rollback

```sh
# Helm:
helm rollback dealix <previous-revision> -n dealix-prod

# Compose:
docker compose -f deploy/docker-compose.prod.yml pull && \
docker compose -f deploy/docker-compose.prod.yml up -d --force-recreate

# Terraform: revert the bad commit + `terraform apply` again.
```

## Incident response

See `docs/ops/incident_response.md` for SEV-1/2/3 escalation.
The PagerDuty key sits in `PAGERDUTY_INTEGRATION_KEY`; without it the
fallback is Knock → founder email.
