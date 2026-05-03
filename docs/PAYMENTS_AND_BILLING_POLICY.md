# Dealix Payments & Billing Policy

> Source: `dealix/payments/moyasar.py`, `api/routers/full_os.py`,
> `api/routers/pricing.py`, `api/routers/webhooks.py`.

## Pricing — Pilot 499 SAR

The Pilot is denominated in **Saudi Riyal**. If the Moyasar invoices API
is used, amounts must be passed as integer **halalah**:

```
1 SAR  = 100 halalah
499 SAR = 49,900 halalah
```

This is enforced by `MoyasarClient.create_invoice` (passes `amount` directly).

## Default mode — manual fallback

When `MOYASAR_SECRET_KEY` is NOT set, `POST /api/v1/payments/manual-request`
returns:

```
{
  "deal_id": "...",
  "status": "payment_requested",
  "method": "bank_transfer",
  "follow_up_task_id": "task_...",
  "instruction": "Send invoice to customer via WhatsApp/email with bank
                  IBAN or STC Pay number. Use template in
                  docs/ops/MANUAL_PAYMENT_SOP.md."
}
```

This is the **default flow for first customers**. No live charge. No
direct card capture. Customer pays voluntarily by bank transfer or STC
Pay; founder confirms via `POST /api/v1/payments/mark-paid`.

## Optional — Moyasar hosted invoice

When `MOYASAR_SECRET_KEY` is set (sandbox or live), the same
`payments/manual-request` route can be wired to call
`MoyasarClient.create_invoice(amount_halalas=49900, currency="SAR", …)`
which returns a hosted `url` for the customer to pay.

> **Important:** even with Moyasar configured, the customer still pays
> *voluntarily* on a hosted page. Dealix never captures card details.
> The hard rule "no Moyasar live charge" refers to direct card-capture
> flows that are not implemented and must not be added.

## Webhook verification

`POST /api/v1/webhooks/moyasar` verifies a shared `secret_token`
against `MOYASAR_WEBHOOK_SECRET` in constant time. Unsigned or
mis-signed payloads return **401 bad_signature**. Verified live on
prod 2026-05-03.

## What is forbidden

1. Direct credit-card capture by Dealix.
2. Auto-charging customers from saved tokens without explicit per-charge approval.
3. Any "subscribe-and-charge" pattern that does not require a fresh customer click on a hosted Moyasar page.
4. Storing card numbers anywhere in the codebase or logs.
5. Listing live secret keys in `.env.example`, `Dockerfile`, or any committed file.

## Audit trail

Every payment event should be reflected in:

- `DealRecord.stage` transition (`pilot_offered` → `paid` → `won`)
- `CustomerRecord` creation
- `TaskRecord` (`onboarding_task_id`)
- (BACKLOG) `proof_ledger.events.payment_confirmed`

## Paid Beta gate

`PAID_BETA_READY` requires:

1. ≥ 1 real Saudi customer agreed in writing to a Pilot.
2. Real bank-transfer payment confirmed (or Moyasar invoice paid).
3. Proof Pack delivered with at least:
   - opportunities created
   - drafts created with manual-approval evidence
   - risks blocked (compliance/check-outreach record)
   - revenue impact estimate (clearly labelled as estimate)
4. Customer signs off on the Proof Pack in writing.
5. Paid-beta policy doc exists: who can buy, how refunds work, SLA.

Until all 5, verdict cannot exceed `FIRST_CUSTOMER_READY_REALISTIC`.
