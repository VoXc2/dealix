# First 3 Warm Intros Board (placeholders only)

This is the **canonical 3-slot tracker** for Phase E. Real names live
on your phone, never in this repo.

> The script `python scripts/dealix_first3_board.py` regenerates a
> live-but-blank version of this board at
> `docs/phase-e/live/FIRST_3_CUSTOMER_BOARD.md` (which is gitignored).
> This file is the **template** that documents the columns + rules.

## Board

| Slot | Company | Source | Consent | Segment | Problem | Diagnostic | Pilot | Proof | Next | Owner |
|------|---------|--------|---------|---------|---------|------------|-------|-------|------|-------|
| **A** | Slot-A | warm_intro | not_yet_asked | b2b_services | tbd | not_started | not_started | not_started | ask_for_30m | founder |
| **B** | Slot-B | warm_intro | not_yet_asked | b2b_services | tbd | not_started | not_started | not_started | ask_for_30m | founder |
| **C** | Slot-C | warm_intro | not_yet_asked | b2b_services | tbd | not_started | not_started | not_started | ask_for_30m | founder |

## Status vocabulary (canonical)

- **Diagnostic**: `not_started` → `requested` → `drafting` → `delivered` → `accepted` → `declined`
- **Pilot**: `not_started` → `offered` → `payment_pending` → `paid_or_committed` → `in_delivery` → `delivered` → `proof_pack_ready`
- **Proof**: `not_started` → `events_logged` → `pack_drafted` → `customer_reviewed` → `customer_approved` → `published_internal` (NEVER `published_external` without signed permission)

## Rules

- ✅ Use placeholders (`Slot-A` / `Slot-B` / `Slot-C`) in the public
  doc; real names + emails stay on your phone or your private notes.
- ✅ Move a slot to the next status only after a real signal
  (e.g. `requested` only after the customer says yes).
- ❌ NEVER list a customer publicly without signed consent.
- ❌ NEVER flip `proof.published_external` without a signed
  permission email from the customer.

## When to refill a slot

When **slot N's pilot delivers + proof pack is approved by the
customer**, that slot becomes:
- `proof.customer_approved` → archive in `docs/proof-events/<slot-slug>.json`
- Slot is open → pick the next warm intro

Only AFTER you have at least 2 archived proof events should you scale
beyond 3 concurrent slots.
