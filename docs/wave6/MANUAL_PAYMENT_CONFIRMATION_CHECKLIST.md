# Manual Payment Confirmation Checklist (Wave 6 Phase 5)

**Hard rule (Article 8 — NO_FAKE_REVENUE):**

- `invoice_intent_created` = ❌ NOT revenue
- `payment_link_sent` = ❌ NOT revenue
- `screenshot/bank_transfer_note_received` = 🟡 EVIDENCE, not final
- `payment_confirmed` (founder explicitly flips state) = ✅ REVENUE
- `written_commitment_received` (signed contract) = ✅ COMMITMENT (proceed with delivery)

Delivery kickoff is allowed ONLY when one of these is true:
1. `payment_confirmed` flag set, OR
2. `written_commitment_received` flag set (signed Service Agreement)

If neither is set → Wave 6 Phase 6 delivery kickoff returns `BLOCKED_WAITING_PAYMENT`.

---

## State machine

```
invoice_intent_created
        ↓
[founder sends bank-transfer details to customer]
        ↓
payment_pending
        ↓
[customer wires money + sends screenshot/reference]
        ↓
evidence_received  (note logged with evidence_note >= 5 chars)
        ↓
[founder verifies bank statement OR receives signed contract]
        ↓
payment_confirmed   OR   written_commitment_received
        ↓
delivery_kickoff_ready  →  Wave 6 Phase 6 unlocks
```

## Required fields per state

| State | Requires |
|---|---|
| `invoice_intent_created` | `amount_sar`, `customer_handle`, `service_type` |
| `payment_pending` | `invoice_intent_created` previously |
| `evidence_received` | `evidence_note` (≥ 5 chars), `evidence_kind` (bank_screenshot/transfer_ref/email_receipt) |
| `payment_confirmed` | `evidence_received` previously, `confirmed_by` (founder name) |
| `written_commitment_received` | `commitment_kind` (signed_service_agreement/email_commitment), `signed_at` |
| `delivery_kickoff_ready` | one of `payment_confirmed` OR `written_commitment_received` |

## Refund rule (for the 14-day window)

- 100% refund within 14 days of Sprint start, no questions
- Bank transfer takes 3-5 business days to clear
- After refund, state goes to `refunded` (terminal); no delivery
- `refund_note` must be added before scaling to next pilot

## Hard NO

- ❌ NEVER mark `payment_confirmed` without `evidence_note` ≥ 5 chars
- ❌ NEVER claim revenue from `invoice_intent_created` or `payment_pending` alone
- ❌ NEVER use Moyasar live charge (NO_LIVE_CHARGE constitutional gate)
- ❌ NEVER auto-confirm — founder always flips the state manually

## Workflow

1. Founder runs `dealix_payment_confirmation_stub.py --action invoice-intent --customer <h> --amount-sar 499`
2. Customer wires money + sends screenshot
3. Founder runs `dealix_payment_confirmation_stub.py --action upload-evidence --customer <h> --evidence-note "BANK-TXN-12345 received 2026-05-08"`
4. Founder verifies in bank statement
5. Founder runs `dealix_payment_confirmation_stub.py --action confirm --customer <h> --confirmed-by "Sami Al-Foulan"`
6. State now = `payment_confirmed` → delivery kickoff unlocked
7. Phase 6 (delivery_kickoff.py) reads this file and proceeds
