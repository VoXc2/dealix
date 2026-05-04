# Manual Payment Fallback — 499 SAR Pilot

> Default payment path. Live Moyasar charge stays OFF. No card details
> are collected. Customer pays voluntarily by bank transfer or STC Pay.

## Why manual

| Constraint | Why |
| --- | --- |
| `MOYASAR_ALLOW_LIVE_CHARGE=false` | Hard gate — flipping requires a written refund/charge policy first |
| No card capture by Dealix | We never store card numbers; nothing to leak |
| Customer pays voluntarily | They confirm WHEN to pay, on a hosted page or by transfer |

## Allowed payment methods

| Method | When | Tracking |
| --- | --- | --- |
| Saudi bank transfer | default | record IBAN reference |
| STC Pay | when customer prefers | record STC Pay transaction reference |
| Moyasar hosted invoice | only if `MOYASAR_SECRET_KEY` is set + sandbox mode | record invoice ID + URL |

If Moyasar is configured: amount is **49,900 halalah** (= 499 SAR × 100).

## Founder action when prospect says yes to the pilot

```bash
# 1. Record the lead — capture `id` from the response JSON as <lead_id>
LEAD=$(curl -sX POST https://api.dealix.me/api/v1/leads \
  -H "Content-Type: application/json" \
  -d '{"name":"<contact>","email":"<email>","company":"<co>","phone":"<+966...>","source":"linkedin","sector":"<sector>"}')
LEAD_ID=$(python -c "import json,sys; d=json.loads(sys.argv[1]); print(d.get('lead',{}).get('id') or d.get('id',''))" "$LEAD")
echo "lead_id=$LEAD_ID"

# 2. Create deal at pilot_offered — capture `id` as <deal_id>
DEAL=$(curl -sX POST https://api.dealix.me/api/v1/deals \
  -H "Content-Type: application/json" \
  -d "{\"lead_id\":\"$LEAD_ID\",\"value_sar\":499,\"stage\":\"pilot_offered\"}")
DEAL_ID=$(python -c "import json,sys; d=json.loads(sys.argv[1]); print(d.get('deal',{}).get('id') or d.get('id',''))" "$DEAL")
echo "deal_id=$DEAL_ID"

# 3. Manual invoice — bank-transfer instructions returned
curl -sX POST https://api.dealix.me/api/v1/payments/manual-request \
  -H "Content-Type: application/json" \
  -d "{\"deal_id\":\"$DEAL_ID\",\"amount_sar\":499}"

# 4. Send the customer the bank IBAN / STC Pay number via WhatsApp/email manually.

# 5. When the transfer arrives — capture `customer_id` from the mark-paid response:
PAID=$(curl -sX POST https://api.dealix.me/api/v1/payments/mark-paid \
  -H "Content-Type: application/json" \
  -d "{\"deal_id\":\"$DEAL_ID\",\"reference\":\"<bank-ref>\"}")
CUSTOMER_ID=$(python -c "import json,sys; print(json.loads(sys.argv[1]).get('customer_id',''))" "$PAID")
echo "customer_id=$CUSTOMER_ID"
```

## Payment tracking fields (per pilot)

```
customer:           <name + company>
amount:             499 SAR
method:             bank_transfer | stc_pay | moyasar_invoice
invoice_link:       <url if Moyasar>  OR  manual_ref: <bank IBAN reference>
status:             not_sent | sent | viewed | paid | committed | expired | cancelled
paid_at:            <ISO timestamp once confirmed>
proof_file:         <screenshot/PDF of bank confirmation, stored offline>
notes:              <free text>
```

## Allowed status values

| Status | Meaning | Next action |
| --- | --- | --- |
| `not_sent` | invoice/instructions not yet sent | send |
| `sent` | instructions sent to customer | wait 24h then follow up |
| `viewed` | customer acknowledged receipt | wait |
| `paid` | bank/STC Pay receipt confirmed | mark paid via API + start delivery |
| `committed` | written commitment to pay (e.g. PO from a corporate) | start delivery, expect payment within agreed window |
| `expired` | 7 days since `sent` with no response | move to `nurture` |
| `cancelled` | customer changed mind | thank them, move to `closed_lost` |

## Hard rules

- Never mark `paid` without proof: bank screenshot, STC Pay reference,
  or Moyasar webhook event.
- Never charge a card directly. The live-charge gate stays OFF.
- Never accept partial payment for a 499 SAR pilot — keeps accounting
  clean.
- If a corporate customer needs to pay via PO / invoice + 30/60-day
  terms: mark `committed`, deliver the pilot, send the Proof Pack on
  day 7, and trust the corporate process. Track the payment date
  separately.
- Never share bank credentials in chat or screenshots.

## When to escalate to "live charge enabled"

NOT until ALL of these are true:

1. ≥ 3 paid pilots with manual fallback complete.
2. A written refund/charge policy is published in `docs/PAYMENTS_AND_BILLING_POLICY.md`.
3. ZATCA invoicing flow is documented (per Saudi B2B requirements).
4. Founder explicitly approves the gate flip.

Until then: `MOYASAR_ALLOW_LIVE_CHARGE=false` stays.
