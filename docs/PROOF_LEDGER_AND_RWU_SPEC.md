# Proof Ledger & Revenue Work Units

> Source: live `GET /api/v1/proof-ledger/units` (deploy branch).

## RWU catalog (live, 10 units)

```
opportunity_created       weight 1.0  base_revenue_impact_sar 500
target_ranked            weight 0.5  base 50
draft_created            weight 0.7  base 100
approval_collected       weight 0.6  base —
followup_created         weight 0.4  base —
risk_blocked             weight 0.6  base —
meeting_booked           weight 1.5  base 1500
proof_pack_generated     weight 1.2  base 800
invoice_created          weight 1.0  base —
payment_confirmed        weight 2.0  base —
```

(Sample weights from prod `/proof-ledger/units` 2026-05-03 — exact list
returned by the deploy branch.)

## Required RWU coverage for first-customer flow

| Stage | RWU(s) emitted | Status |
| --- | --- | --- |
| Prospect added | `opportunity_created` | PROVEN_LIVE on deploy |
| Target ranked | `target_ranked` | CODE_EXISTS_NOT_PROVEN |
| Message draft | `draft_created` | PROVEN_LIVE on deploy |
| Approval collected | `approval_collected` | CODE_EXISTS_NOT_PROVEN |
| Risk blocked | `risk_blocked` (every `compliance/check-outreach` block should emit one) | CODE_EXISTS_NOT_PROVEN |
| Meeting booked | `meeting_booked` | CODE_EXISTS_NOT_PROVEN |
| Invoice created | `invoice_created` (via `payments/manual-request`) | PROVEN_LOCAL |
| Payment confirmed | `payment_confirmed` (via `payments/mark-paid`) | PROVEN_LOCAL |
| Proof Pack generated | `proof_pack_generated` | PROVEN_LIVE on deploy |

## Proof Pack contract (target)

Every proof pack must have:

```
{
  "customer_id": "...",
  "executive_summary_ar": "...",
  "inputs":      {...},
  "what_was_created":  [...],
  "what_was_protected":[...],   # blocked risks summary
  "approvals": [...],
  "revenue_impact_estimate_sar": <float>,   # labelled estimate, never guarantee
  "assumptions": [...],
  "next_7_days_plan": [...],
  "upgrade_recommendation": "...",
  "signature_hmac": "<hex>",                # BACKLOG
  "generated_at": "<iso>",
  "company_id": "..."
}
```

Today's response shape from `/api/v1/customers/{id}/proof-pack`:
- has `case_study_md_template`, `testimonial_request_ar`, `referral_ask_ar`, `next_action`
- **does NOT include** `signature_hmac`, `revenue_impact_estimate_sar`, or `assumptions`
  — these are BACKLOG.

## Estimate vs. guarantee

Every numeric impact MUST be rendered with the label "تقدير" / "estimate".
The classifier's `reason_ar` and `reason_en` fields are sweep-tested to
contain neither "guaranteed" nor "نضمن" (`tests/test_no_guaranteed_claims.py`).

## Audit trail

Each proof pack should reference the underlying RWU events. The deploy
branch's `proof-ledger/events` write endpoint is the binding point. To
make a proof pack tamper-evident, sign the canonical JSON form with a
server-side HMAC key (BACKLOG).
