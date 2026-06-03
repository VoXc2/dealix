# Manual Payment Fallback — 499 SAR Pilot

The Pilot is **never auto-charged**. The CLI defaults to test mode and
refuses live keys without `--allow-live`. This doc explains the two
sanctioned payment paths.

## Canonical amount

```
amount_sar      = 499
amount_halalah  = 49,900     (Moyasar uses smallest unit)
mode            = test|manual    (live forbidden by default)
payment_method  = moyasar_test | bank_transfer | other_manual
refund_note     = required_if_delivery_fails_spec
```

## Path 1 — Moyasar test-mode invoice (preferred for Saudi customers)

```bash
python scripts/dealix_invoice.py \
  --email customer@example.sa \
  --amount-sar 499 \
  --description "Dealix Pilot — 7 days (Customer-Slot-A)"
```

What this does:
- Creates a Moyasar **test-mode** hosted-payment URL
- Refuses to run if `MOYASAR_SECRET_KEY` starts with `sk_live_` and
  `--allow-live` is NOT passed
- Prints `INVOICE_ID`, `PAYMENT_URL`, `AMOUNT`, `MODE`,
  `MANUAL_FALLBACK_STEPS`, `REFUND_NOTE_REQUIRED` to stdout
- **Does NOT** charge the customer's card; the customer must visit
  the URL and complete the test transaction (or pay manually)

## Path 2 — Bank transfer (manual, no Moyasar)

When the customer prefers bank transfer:

1. Send IBAN + bank name + reference (`DEALIX-PILOT-<slot>`) via
   WhatsApp or email — manually
2. Wait for confirmation of transfer (screenshot or bank
   confirmation)
3. Do NOT mark `pilot=paid_or_committed` until the founder personally
   confirms the funds landed
4. Issue a manual receipt (Markdown email is fine)

## Refund policy

- 7-day refund window from delivery date
- Refund issued if Dealix delivery did NOT match the
  `growth_starter` spec in `docs/registry/SERVICE_READINESS_MATRIX.yaml`
- Refund processed manually by the founder (Moyasar refund or bank
  reverse-transfer)
- Refund decision is the founder's; no auto-refund

## Hard rules — re-asserted

- ❌ `MOYASAR_SECRET_KEY` starting `sk_live_` is REJECTED unless
  `--allow-live` flag is passed (and even then, the founder must type
  it manually each time)
- ❌ NO `MOYASAR_ALLOW_LIVE_CHARGE` env var; the existing CLI guard
  is enough
- ❌ NEVER claim a customer "paid" before the founder confirms the
  funds landed
- ❌ NEVER claim "revenue live" or "X SAR earned" publicly without
  ≥ 1 archived proof event AND signed permission to publish
- ✅ Test-mode is the default; live charge requires deliberate
  founder action every time

## When in doubt

If the founder is uncertain whether to use test mode or bank
transfer for a specific customer, default to **bank transfer**.
It's the most auditable option and avoids any Moyasar live-charge
risk.
