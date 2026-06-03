# Moyasar — KYC & Live-Payment Activation Checklist

> Companion to `docs/ops/MANUAL_PAYMENT_SOP.md` (which is for the pre-KYC window). Once this checklist is closed, the SOP can be retired.

## Owner: Founder (CEO). Window: 1–3 business days after submission.

---

## Phase 1 — KYC submission (T-21 to T-14)

- [ ] **1.1** Saudi commercial registration (CR / Sijill Tijari) — scan PDF, certified copy.
- [ ] **1.2** National address (Wasel) — printed certificate.
- [ ] **1.3** Founder national ID — both sides, color scan.
- [ ] **1.4** Authorised signatory letter on company letterhead.
- [ ] **1.5** Saudi bank account (corporate, in CR name). IBAN + bank confirmation letter.
- [ ] **1.6** VAT registration certificate (ZATCA — if turnover ≥ 375,000 SAR; required for B2B invoicing regardless).
- [ ] **1.7** Brief business description: what Dealix sells, average ticket, expected monthly volume, refund policy URL.
- [ ] **1.8** Submit via https://dashboard.moyasar.com → Settings → Verification.
- [ ] **1.9** Record ticket number in `docs/ops/manual_payment_log.md` under "Moyasar verification".

## Phase 2 — Account approval (T-14 → T-10)

- [ ] **2.1** Moyasar responds with approval (or requested clarifications). SLA: 1–3 business days.
- [ ] **2.2** On approval, retrieve `sk_live_xxxxx` from dashboard → API Keys.
- [ ] **2.3** Generate webhook secret locally:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- [ ] **2.4** **Store both in 1Password** (`Dealix Production` vault, items: `Moyasar SECRET_KEY` and `Moyasar WEBHOOK_SECRET`).
- [ ] **2.5** Push to Railway env vars:
  - `MOYASAR_SECRET_KEY=sk_live_xxxxx`
  - `MOYASAR_WEBHOOK_SECRET=<64-hex from step 2.3>`
  - `MOYASAR_MODE=production`

## Phase 3 — Webhook registration (T-10 → T-7)

- [ ] **3.1** In Moyasar dashboard → Webhooks → Add Webhook.
- [ ] **3.2** URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
- [ ] **3.3** Events: `payment_paid`, `payment_failed`, `payment_refunded`, `payment_authorized`, `payment_captured`.
- [ ] **3.4** Secret: **paste the exact same value** as Railway `MOYASAR_WEBHOOK_SECRET`. Any mismatch → 401s and SEV-1 paging.
- [ ] **3.5** Save. Moyasar sends a test ping → expect HTTP 200.
- [ ] **3.6** Verify in Railway logs: `webhook_received source=moyasar signature_valid=true`.

## Phase 4 — End-to-end live test (T-7 → T-5)

Use the `pilot_1sar` plan (1 SAR test charge):

- [ ] **4.1** Run `bash scripts/moyasar_live_test.sh` (existing). Verify:
  - `payment_url` returned
  - Open URL, complete payment with CEO's real card
  - Moyasar dashboard shows status `paid`
  - DB row in `payments` table updated to `paid`
  - PostHog event `checkout_success { plan=pilot_1sar }` fires
  - Sentry shows zero new errors
- [ ] **4.2** Trigger a refund via Moyasar dashboard. Verify:
  - DB row updates to `refunded`
  - PostHog event `checkout_refunded` fires
- [ ] **4.3** Reconciliation drill:
  ```bash
  python scripts/reconcile_moyasar.py --since 1h
  # Expect: discrepancies: [], exit 0
  ```

## Phase 5 — Production cutover (GA day)

- [ ] **5.1** Confirm `MOYASAR_MODE=production` and `sk_live_` is in Railway.
- [ ] **5.2** Remove any test/staging webhook endpoints from Moyasar dashboard.
- [ ] **5.3** Schedule nightly reconciliation cron at 02:00 AST:
  ```cron
  0 2 * * *  python /app/scripts/reconcile_moyasar.py --since 48h >> /var/log/dealix-reconcile.log 2>&1
  ```
- [ ] **5.4** Set Sentry alert: any `webhook_received signature_valid=false source=moyasar` → SEV-1 page.
- [ ] **5.5** Update `docs/ops/MANUAL_PAYMENT_SOP.md` with `STATUS: deprecated as of <date>` (keep for reference, do not delete).

## Phase 6 — Ongoing operations

- [ ] **6.1** Weekly: founder reviews Moyasar dashboard → reconciliation → DB.
- [ ] **6.2** Monthly: VAT tax filing reflects Moyasar receipts.
- [ ] **6.3** Quarterly: rotate `MOYASAR_WEBHOOK_SECRET` (see `docs/security/KEY_ROTATION.md`).
- [ ] **6.4** Annually: confirm KYC documents still current with Moyasar (CR renewal, etc).

## Failure modes — what to do

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Webhook returns 401 | Signature mismatch | Confirm Railway `MOYASAR_WEBHOOK_SECRET` == dashboard secret |
| Webhook returns 500 | Code exception | Sentry trace; rollback if regression |
| Payment paid in Moyasar but DB shows `pending` | Webhook dropped | Replay from DLQ: `python -m dealix.reliability.dlq replay --queue webhooks --filter source=moyasar` |
| Reconciliation finds `missing_in_db` | Webhook never received | Check Moyasar webhook logs in dashboard; replay if recent |
| Reconciliation finds `amount_mismatch` | DB drift / bug | SEV-1 — possible accounting integrity issue |

---

## Sign-off — required before retiring manual SOP

| Item | Signed by | Date |
|------|-----------|------|
| KYC approved | _founder_ | — |
| Live test passed (Phase 4) | _founder_ | — |
| Reconciliation drill passed | _founder_ | — |
| Sentry alert wired | _CTO_ | — |
| `MANUAL_PAYMENT_SOP.md` marked deprecated | _founder_ | — |
