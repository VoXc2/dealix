# Dealix — Service Delivery / تسليم الخدمات

> **Authoritative.** SLA + delivery expectations for Diagnostic +
> Pilot. Support OS service-delivery questions route here.

## Mini Diagnostic delivery

| Item | Value |
|---|---|
| Cost | Free / مجاني |
| Turnaround | 30 minutes (read) |
| Format | Bilingual Markdown |
| Contains | 3 opportunities + 1 Arabic draft + safe channel + 1 risk |
| Action mode | `approval_required` |
| Audience | Internal until customer reviews |

## Pilot delivery (7 days)

| Day | Deliverable | Action mode |
|---|---|---|
| 0 | Diagnostic + intake confirmation | `approval_required` |
| 1 | 10 ranked opportunities | `draft_only` |
| 2 | Drafts (1 per chosen opp) | `draft_only` |
| 3 | Customer-approved sends (manual) | `approved_manual` |
| 4 | 7-day follow-up calendar | `draft_only` |
| 5 | Risk note (≤ 3 items) | `draft_only` |
| 6 | Initial Proof Pack (Draft / Internal) | `approval_required` |
| 7 | Customer review call + upsell decision | manual |

## Arabic — العربيّة

كل تسليم يمرّ بمراجعة المؤسس. لا إرسال آلي. لا اقتباس بدون
توقيع. كل خروج خارجي ينتظر `approval_required` أو
`approved_manual`.

## English

Every deliverable passes through founder review. No automatic
sends. No customer quote without signed permission. Every external
output waits for `approval_required` or `approved_manual`.

## Quality bars

- Every draft passes `tests/test_landing_forbidden_claims.py`
  forbidden-token list.
- Every draft is ≤ 200 words for WhatsApp / ≤ 400 for email.
- Every draft includes a clear ask.
- NO draft references a metric the customer didn't supply.
- NO draft references a specific named competitor without a public
  source.
- NO draft uses customer PII in clear (use placeholders).

## What "delivered" means

A Pilot is **delivered** when:
1. All 6 deliverables (day 1 through day 6) are sent to the customer.
2. The Day-7 review call has happened.
3. The Proof Pack is recorded as `decision: review_required`,
   `audience: internal_only` until the customer signs publish
   permission.

## Refund window

7 days from delivery date. Per `payment_policy_ar_en.md`.
