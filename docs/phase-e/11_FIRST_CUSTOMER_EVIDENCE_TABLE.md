# First Customer Evidence Table

For each Phase E slot, record the following evidence as you go. NEVER
make up an entry. NEVER quote a customer without their permission.
NEVER fill in `published_external` without a signed permission email.

## Per-slot evidence table

| Field | Type | Notes |
|---|---|---|
| `slot` | `A` / `B` / `C` | Stays a placeholder in this repo |
| `relationship` | `warm_intro` / `existing_contact` / `referral` | Cold sources are forbidden |
| `consent_status` | `not_asked` / `asked` / `granted` / `revoked` | Default starts `not_asked` |
| `mini_diagnostic_sent_at` | ISO date | Local time, founder records |
| `mini_diagnostic_response` | `accepted` / `declined` / `no_reply` | If `no_reply` after 7 days, archive |
| `pilot_offered_at` | ISO date | Only after `mini_diagnostic_response=accepted` |
| `pilot_payment_method` | `moyasar_test` / `bank_transfer` / `not_paid` | Live charge forbidden |
| `pilot_paid_at` | ISO date | Only after founder confirms funds |
| `pilot_delivered_at` | ISO date | After 7-day delivery |
| `proof_pack_drafted_at` | ISO date | When `proof_pack.py` ran |
| `proof_pack_customer_approved_at` | ISO date | Only after written customer sign-off |
| `proof_event_count` | int | From `docs/proof-events/<slot>.json` |
| `audience` | `internal_only` / `public_allowed` | Default `internal_only` |
| `published_external_at` | ISO date or `null` | Only with signed permission |

## What counts as evidence

| Evidence type | Acceptable source | Storage |
|---|---|---|
| Customer reply | WhatsApp/email screenshot in your private vault | NOT in repo |
| Payment confirmation | Moyasar dashboard / bank statement | NOT in repo |
| Delivered Proof Pack | The Markdown file checked-in (placeholder names) | `docs/proof-events/<slot>.json` |
| Customer approval to publish | Signed email | NOT in repo (founder vault) |

## What does NOT count as evidence

- ❌ AI-generated transcript without customer-approved quotes
- ❌ Verbal "yes" with no written confirmation
- ❌ Inferred metric ("they probably saved X SAR")
- ❌ Aggregated industry stat presented as the customer's own result
- ❌ Screenshot edited / annotated to remove caveats

## Bilingual summary

**Arabic**: كل خطوة موثّقة. لا اقتباس بدون موافقة. لا نشر بدون توقيع.
**English**: Every step documented. No quote without permission. No
publish without signed sign-off.
