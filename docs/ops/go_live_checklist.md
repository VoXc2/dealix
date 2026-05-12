# Go-live checklist — 30 items from clean machine to first invoice

> The fastest path from "I just cloned the repo" to "the first paying
> customer's invoice is in their inbox." Each item references the
> existing artefact that makes it real.

## Day 0 — Bootstrap (2 hours)

- [ ] **1.** Clone the repo + `make hooks` + `bash scripts/dev/install_dev.sh`.
- [ ] **2.** `cp .env.example /opt/dealix/.env` — fill week-1 keys
  from `docs/ops/vendor_cost_sheet.md` (`MOYASAR_SECRET_KEY`,
  `ANTHROPIC_API_KEY`, `RESEND_API_KEY`, `JWT_SECRET_KEY`,
  `DATABASE_URL`, `REDIS_URL`, `APP_URL`).
- [ ] **3.** `alembic upgrade head` against the prod DATABASE_URL.
- [ ] **4.** `pytest -q tests/unit/test_invoice_pdf.py tests/unit/test_gcc_currency.py` — baseline green.
- [ ] **5.** `python scripts/dev/check_vertical_truth.py` — pre-deploy gate green.

## Day 0 — Deploy (1 hour)

- [ ] **6.** Pick your path:
  - **A. Single host:** `docker compose -f deploy/docker-compose.prod.yml up -d`.
  - **B. Railway:** `terraform -chdir=infra/terraform/live/prod apply`.
  - **C. K8s:** `helm install dealix deploy/helm/dealix -n dealix-prod -f deploy/helm/dealix/values.prod.yaml`.
- [ ] **7.** Verify the deep health: `curl /api/v1/health/deep` returns
  the configured-vendor matrix you expect.
- [ ] **8.** DNS: point `api.dealix.me` + `app.dealix.me` at the
  ingress. TLS via Cloudflare or cert-manager.
- [ ] **9.** Hit `https://api.dealix.me/healthz` from outside the
  cluster — expect `{"status":"ok"}`.

## Day 1 — Smoke commerce (1 hour)

- [ ] **10.** Trial signup: `curl -X POST https://api.dealix.me/api/v1/trial/start -d '{"email":"founder+test@…sa","company":"Test"}'`. Confirm tenant_id + api_key returned.
- [ ] **11.** Skill execution: `curl -X POST .../api/v1/skills/sales_qualifier/run -H 'X-API-Key: <key>' -d '{"inputs":{"lead_snapshot":{"budget":"y","authority":"y","need":"y","timeline":"y"},"compliance_signals":{"has_pdpl_consent":true}}}'`. Expect score 1.0.
- [ ] **12.** Invoice-intent: `curl -X POST .../api/v1/payment-ops/invoice-intent -d '{"customer_handle":"founder@…sa","amount_sar":499,"method":"moyasar_test","service_session_id":"sprint_499"}'`. With MOYASAR_SECRET_KEY set, response carries `checkout_url`.
- [ ] **13.** Open the `checkout_url` in a browser. Complete a test payment.
- [ ] **14.** Confirm webhook fires: `tail -f` the API logs, watch for
  `moyasar_webhook_processed` → `receipt_email_sent`.
- [ ] **15.** Open the receipt email. Click the signed invoice URL.
  Verify the bilingual ZATCA-shaped invoice renders.

## Day 1 — Trust gates (1 hour)

- [ ] **16.** Status page: configure `BETTERSTACK_HEARTBEAT_URL`
  (or skip — `/api/v1/status` works as a fallback).
- [ ] **17.** Error tracking: paste `SENTRY_DSN` into env; restart.
- [ ] **18.** Cookie consent: verify `landing/components/CookieConsent.js`
  fires on every public landing page.
- [ ] **19.** Procurement landing: visit `https://dealix.me/procurement/` —
  every link works.
- [ ] **20.** `.well-known/security.txt` resolves.

## Day 2 — Outbound (4 hours)

- [ ] **21.** Pick 1 vertical to focus on (`real-estate`, `hospitality`,
  `legal`, `healthcare`, `construction`, `education`, `food-and-beverage`,
  or `financial-services`).
- [ ] **22.** Hit the brochure URL:
  `https://api.dealix.me/api/v1/marketing/brochure/<vertical>.pdf?locale=ar`.
  Verify it renders bilingually.
- [ ] **23.** Source 20 prospects via Wathq lookups (`/api/v1/saudi-gov/maroof/{cr}`
  if configured, manual otherwise).
- [ ] **24.** Send Touch 1 (email) per `docs/sales/cold_outreach_ar.md`.
- [ ] **25.** Day 3: Send Touch 2 (WhatsApp).
- [ ] **26.** Day 7: Send Touch 3 (trial-link nudge).

## Week 2 — First conversions

- [ ] **27.** Day 7 of each trial: hand the prospect their Proof Pack
  (custom-built — pull data from `/api/v1/customer-success/tenant-health/{id}`).
- [ ] **28.** Day 14 of each trial: trigger Stripe / Moyasar upgrade
  via `/[locale]/trial-expired` flow.
- [ ] **29.** Convert first paying customer → manually mark via
  `POST /api/v1/payment-ops/{id}/confirm` after evidence upload.
  The constitution `no_fake_revenue` gate requires this.
- [ ] **30.** Send the founder's Slack a celebratory message + log
  the case in `docs/marketing/case_studies/<name>.md`.

## Done

When all 30 boxes are checked, you have:
- A working production deployment.
- At least one paying customer with a real ZATCA-shaped invoice.
- A measurable repeatable outbound funnel.
- Sub-processor + procurement docs ready for the next prospect.

Total time from clean clone to invoice: ~7 days at a relaxed pace,
~3 days if you're full-time on launch.

## Rollback

If anything in steps 6–9 fails, see
`docs/ops/runbook_zero_to_prod.md` → "Rollback" section.
