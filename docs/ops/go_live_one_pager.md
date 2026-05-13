# 🚀 Go-live one-pager — the CEO runbook

> **Branch:** `claude/comprehensive-qa-review-ZLsYG` @ `d45d347` (v3.8.1)
> **Status:** every endpoint smoke-verified locally; 101/101 unit tests green.
>
> Read this once. Execute top → bottom. Stop on the first thing that
> doesn't work and grep `docs/ops/troubleshooting.md` for the symptom.

---

## SECTION A — The 12 commands that put you live

From a fresh prod host (Linux, Docker 24+, ≥ 4 GB RAM, ≥ 40 GB disk):

```bash
# 1. Clone + checkout the release branch.
git clone https://github.com/VoXc2/dealix.git /opt/dealix
cd /opt/dealix
git checkout claude/comprehensive-qa-review-ZLsYG

# 2. Provision /opt/dealix/.env per docs/ops/key_paste_order.md.
sudo mkdir -p /opt/dealix && sudo chown -R "$USER" /opt/dealix
cp .env.example /opt/dealix/.env
chmod 600 /opt/dealix/.env
$EDITOR /opt/dealix/.env

# 3. Pull or build images.
docker compose -f deploy/docker-compose.prod.yml --env-file /opt/dealix/.env pull
# Alternative if you build locally: docker compose -f deploy/docker-compose.prod.yml build

# 4. First-boot — only data services so migrations can run.
docker compose -f deploy/docker-compose.prod.yml --env-file /opt/dealix/.env up -d postgres redis cerbos meilisearch
sleep 10

# 5. Apply migrations.
docker compose -f deploy/docker-compose.prod.yml --env-file /opt/dealix/.env run --rm api alembic upgrade head
docker compose -f deploy/docker-compose.prod.yml --env-file /opt/dealix/.env run --rm api alembic heads   # must print ONE revision

# 6. Bring up the full stack.
docker compose -f deploy/docker-compose.prod.yml --env-file /opt/dealix/.env up -d
docker compose -f deploy/docker-compose.prod.yml ps         # services 'healthy' / 'running'
docker compose -f deploy/docker-compose.prod.yml logs api --tail=30

# 7. DNS — point api.<domain> + app.<domain> at this box (Cloudflare).
# TLS — caddy reverse-proxy on :443 OR Cloudflare flexible TLS.

# 8. Public smoke.
curl https://api.<domain>/healthz                             # → {"status":"ok"}
bash scripts/ops/post_deploy_smoke.sh --base-url https://api.<domain>

# 9. Take a live test payment (Moyasar SANDBOX key only at this stage).
#    Open https://<domain>/checkout.html?tier=sprint
#    Submit your own email + moyasar_test → redirected to Moyasar hosted checkout.
#    Use test card  4111 1111 1111 1111  /  any CVV  /  any future expiry.
#    Watch:  docker compose logs api -f | grep -E 'moyasar_webhook|receipt_email'

# 10. Open your inbox → click the bilingual receipt link → confirm the
#     ZATCA-shaped PDF/HTML invoice renders.

# 11. Tag + release.
git tag v3.8.1
git push origin v3.8.1
gh release create v3.8.1 -F docs/release/v3.8.0.md

# 12. You are live. Start docs/sales/first_customer_in_7_days.md.
```

---

## SECTION B — Production `.env` paste order

The full file lives at `docs/ops/key_paste_order.md` — paste each
section, restart the API, run the smoke, then move on. Week-1
minimum spend: **< $100/month** (Moyasar + Anthropic + Resend +
Postgres + Redis).

---

## SECTION C — Post-deploy smoke

```bash
bash scripts/ops/post_deploy_smoke.sh --base-url https://api.<domain>
```

Exits 0 with a green dashboard when every critical endpoint
answers correctly; non-zero with red/green lines otherwise. See
the script header for the full check list.

---

## SECTION D — First paying customer in 7 days

Full playbook: `docs/sales/first_customer_in_7_days.md`.

Summary:

| Day | Action |
| --- | --- |
| 0 | Pick ONE vertical, source 10 named prospects. |
| 1 | Touch 1 — cold email + brochure PDF link. |
| 3 | Touch 2 — WhatsApp (5 lines max, Khaliji tone). |
| 5 | Triage replies, book 3 demo calls. |
| 6 | Run demo calls, send trial links. |
| 7 | First trial → manual Day-7 Proof Pack → close SAR 499. |

Expectation: 10 prospects → 3 calls → 1 paying customer.

---

## SECTION E — Troubleshooting

Full matrix: `docs/ops/troubleshooting.md`.

Top symptoms:

1. `/api/v1/skills` returns count=0 → pre-d45d347 deploy; pull and restart.
2. Moyasar webhook 401 → `MOYASAR_WEBHOOK_SECRET` mismatch.
3. Receipt email missing → check `RESEND_API_KEY` + email metadata.
4. Invoice 401 → `JWT_SECRET_KEY` rotated post-email; preserve.
5. Trial-expired button dead → frontend rebuild with `NEXT_PUBLIC_API_BASE`.
6. PostHog flags wrong → use Project API Key (phc_), not Personal.
7. Cerbos unreachable → restart sidecar; static RBAC fallback already active.
8. Deep health no vendors → install `prometheus-fastapi-instrumentator`.
9. WhatsApp 403 verify → re-do Meta verify-token handshake.
10. ZATCA QR invalid → set `DEALIX_VAT_NUMBER` to 15-digit value starting with `3`.

---

## SECTION F — "You are live" — concrete signals

You are unambiguously live when all 5 fire:

1. ✅ `bash scripts/ops/post_deploy_smoke.sh --base-url https://api.<domain>` → exits 0.
2. ✅ Your test card on `https://<domain>/checkout.html?tier=sprint` completes through Moyasar sandbox AND your inbox shows the bilingual receipt with the working invoice link.
3. ✅ `https://api.<domain>/api/v1/marketing/brochure/real-estate.pdf` opens.
4. ✅ `https://<domain>/procurement/` renders with no broken links to SLA / DPA / sub-processors / SOC 2 / ISO 27001.
5. ✅ Sentry shows zero `error`-level events for the past 24 h.

When 1–4 are green and 5 is clean → send Touch 1 from SECTION D.

---

## SECTION G — The 30 days after go-live

- **Week 1** — first paying customer per SECTION D.
- **Week 2** — second + third customer; document the playbook delta in `docs/marketing/case_studies/`.
- **Week 3** — flip `DEALIX_MOYASAR_MODE=live` after 5 successful sandbox payments. Open the Stripe account for USD prospects.
- **Week 4** — wire Sentry + Knock + Plain. Open SOC 2 Type I auditor conversation. Run the first `bash scripts/infra/dr_restore_drill.sh --dry-run`.

Target by day 30: **3 paying customers, SAR 12k MRR floor, audit
conversations open, first Saudi-region migration scoped**.

That's the entire CEO path from `d45d347` to revenue.
