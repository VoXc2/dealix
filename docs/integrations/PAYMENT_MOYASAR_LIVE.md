# Payment — Moyasar Live + Bank Transfer Setup Guide

**Status:** Manual flow PRODUCTION_READY · Moyasar live NOT_LIVE_YET (founder-blocked)
**Audience:** Sami (founder) · accountant · customers (read-only on flow)
**Companion:** `dealix/payments/moyasar.py` · `auto_client_acquisition/revops/payment_confirmation.py` · `scripts/dealix_payment_confirmation_stub.py` · `docs/REFUND_SOP.md` · `docs/ops/MANUAL_PAYMENT_SOP.md`
**Wave:** 7.5 §24.4

> **Honest disclosure:** Moyasar live merchant account requires KYC + bank-grade verification (founder action). Until live, ALL payments use bank transfer (manual confirmation). Moyasar SDK code exists; only live activation is pending.

---

## Two payment paths (until Moyasar live)

### Path A — Bank Transfer (default for customers 1-3)

**Pros:** zero KYC dependency, works today, no transaction fees, founder fully controls.
**Cons:** customer must initiate transfer, founder must verify.

**Steps for customer:**

1. Sami sends Sprint Brief PDF (via `dealix_pilot_brief.py`)
2. Brief contains bank details:
   ```
   البنك: <bank name>
   اسم الحساب: <Dealix entity / Sami personal>
   IBAN: SA<...>
   المبلغ: 499 SAR
   مرجع التحويل: SPRINT-<customer-handle>-<YYYYMMDD>
   ```
3. Customer initiates transfer from their bank app
4. Customer screenshots transfer confirmation, sends to Sami via WhatsApp/email
5. Sami runs:
   ```bash
   python3 scripts/dealix_payment_confirmation_stub.py \
     --action evidence-received --customer-handle <handle> \
     --evidence-note "bank transfer screenshot received: <bank> ref <id>"
   ```
6. Sami verifies money in his bank account (24-48h after transfer)
7. Sami runs:
   ```bash
   python3 scripts/dealix_payment_confirmation_stub.py \
     --action confirm --customer-handle <handle> \
     --evidence-note "payment landed in bank account on <date>" \
     --confirmed-by sami
   ```
8. State machine moves: `invoice_intent_created` → `evidence_received` → `payment_confirmed`
9. `is_revenue=True` flag set ONLY at this step (Article 8 — only payment_confirmed counts as revenue)
10. Sprint delivery starts (`dealix_delivery_kickoff.py`)

### Path B — Moyasar live (deferred until merchant onboarded)

**Pros:** automated, Visa/Mada/Mada-NCT cards, instant confirmation.
**Cons:** 2.75% transaction fee, KYC takes 1-2 weeks.

**Founder action — Moyasar onboarding (~1 week):**

1. Sami visits `dashboard.moyasar.com/register`
2. Submit Saudi commercial registration (CR) + national ID + bank IBAN
3. Wait for Moyasar KYC review (3-5 business days)
4. Receive merchant account credentials
5. Generate API keys:
   - `sk_live_...` (secret key — Railway env var only)
   - `pk_live_...` (publishable key — frontend safe)

**Configuration (Sami):**

```bash
# Railway env vars
DEALIX_MOYASAR_MODE=live  # was "test"
MOYASAR_SECRET_KEY=sk_live_<...>
MOYASAR_PUBLISHABLE_KEY=pk_live_<...>
```

**Customer flow (Wave 8 when live):**

1. Sami sends payment link: `dealix.me/checkout/<invoice_id>`
2. Customer enters card on Moyasar-hosted page
3. Moyasar webhook → `POST https://api.dealix.me/api/v1/webhooks/moyasar`
4. Webhook handler verifies signature → calls `record_payment_confirmation()`
5. State machine: `invoice_created` → `payment_confirmed` (instant)
6. Sprint delivery kicks off automatically

---

## Endpoints (current state)

```bash
# 1. Create invoice intent (no money moves yet)
POST /api/v1/payment-ops/invoice-intent
{"customer_handle": "acme-real-estate", "amount_sar": 499, "sku": "sprint_499"}

# 2. Upload manual evidence (Sami uploads screenshot/receipt)
POST /api/v1/payment-ops/manual-evidence
{"customer_handle": "...", "evidence_note": "bank ref #12345"}

# 3. Confirm payment (Sami manually after verifying bank)
POST /api/v1/payment-ops/confirm
{"customer_handle": "...", "evidence_note": "...", "confirmed_by": "sami"}

# 4. Query state
GET /api/v1/payment-ops/<session_id>/state
```

---

## Verification

```bash
# After customer pays, check the state machine
python3 -c "
import json, pathlib
state = json.loads(pathlib.Path('docs/wave6/live/payment_state.json').read_text())
for c in state.values():
    print(c['customer_handle'], c.get('state'), c.get('is_revenue'))
"

# /health endpoint should NOT include 'moyasar' in providers until live
curl -s https://api.dealix.me/health | jq '.providers'
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Customer's transfer didn't arrive | International SWIFT / wrong IBAN | Verify IBAN with customer; allow 2-5 days for cross-bank settlement |
| Moyasar webhook fails (Wave 8) | Signing key mismatch | Verify `MOYASAR_WEBHOOK_SIGNING_KEY` matches dashboard |
| `is_revenue` set before transfer arrives | Sami ran `confirm` action prematurely | Run `--action refund` to reverse + re-run when verified |
| Customer disputes payment | Payment dispute (rare) | Per `REFUND_SOP.md` §5 — refund within 14d, no questions |

---

## Hard rules (immutable in code)

- ❌ NO_LIVE_CHARGE: in test env, NO real charges happen (verified by `tests/test_finance_os_no_live_charge_invariant.py`)
- ❌ NO_FAKE_REVENUE: only `payment_confirmed` state sets `is_revenue=True`
- ❌ Invoice intent ≠ revenue (Article 8)
- ✅ Every payment has corresponding evidence (screenshot/Moyasar txn ID)
- ✅ Refunds always reverse `is_revenue` to False
- ✅ Bank account / IBAN / API keys NEVER in repo (env vars only)

---

## ZATCA + VAT (per `FINANCE_DASHBOARD.md` §7)

For every Sprint:
- 499 SAR = 433.91 ex-VAT + 65.09 VAT
- Sami collects 499 SAR total
- Sami sets aside 65.09 SAR for VAT (filed quarterly via ZATCA portal)
- Sami sets aside ~13 SAR (3%) as Zakat reserve

For every Partner monthly invoice:
- 12,000 SAR = 10,434.78 ex-VAT + 1,565.22 VAT/month
- Filed quarterly

E-invoicing (ZATCA Phase 2) deferred — manual invoicing OK until ZATCA notifies (per `INVOICING_ZATCA_READINESS.md`).

---

## What's deferred to Wave 8

- Moyasar live merchant onboarding (founder action — 1-2 weeks)
- `/api/v1/webhooks/moyasar` automated handler
- Customer-facing checkout page at `/checkout/<invoice_id>`
- ZATCA Phase 2 e-invoicing automation
- Multi-currency support (USD/EUR for any non-Saudi customers — not currently in ICP)
