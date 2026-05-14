# Customer Readiness Gate

A simple recommendation a founder can attach to any proposal:

| Recommendation        | Meaning for the buyer                                      |
|----------------------|-------------------------------------------------------------|
| `PROCEED`            | Source Passport present, governance active, scope signed.  |
| `HOLD_FOR_SCOPE`     | Governance OK; we need a signed scope before invoice.      |
| `HOLD_FOR_GOVERNANCE`| Source Passport missing or Governance OS not yet exercising the account. |

## Endpoints

```
GET /api/v1/customer/{handle}/readiness          (admin-gated; full breakdown)
GET /api/v1/customer/{handle}/readiness/public   (public; recommendation only)
```

## What the Public Endpoint Returns

```json
{
  "handle": "acme",
  "recommendation": "PROCEED",
  "as_of": "2026-05-14T00:00:00+00:00",
  "doctrine": "PROCEED is awarded only when Source Passport is present, Governance Runtime is exercising the account, and a signed scope exists. See /api/v1/dealix-promise."
}
```

The public projection deliberately omits counts, rationale, and
internal flags. Safety is locked by
`tests/test_customer_readiness_public_endpoint_is_safe.py`.

## What the Admin Endpoint Returns

The same recommendation plus the full breakdown:

- `source_passport_status` — `present | missing | unknown`
- `governance_decisions_7d` — Governance OS decision count, last 7 days
- `proof_pack_count`
- `capital_asset_count`
- `has_signed_scope`
- `rationale` — list of codes explaining the recommendation

The thresholds are explicit so an auditor can read them:

| Field                          | Required for PROCEED   |
|--------------------------------|------------------------|
| `source_passport_status`       | `present`              |
| `governance_decisions_7d`      | `>= 5`                 |
| `has_signed_scope`             | `True`                 |
| `proof_pack_count`             | `>= 1` (informational) |

## How to Use in a Sale

1. Prospect agrees to a Diagnostic.
2. After 7 days of governance activity, hit
   `/api/v1/customer/{handle}/readiness` privately to read the
   breakdown.
3. If `PROCEED`: attach the **public** payload to the proposal so the
   buyer can independently verify Dealix's recommendation.
4. If `HOLD_FOR_*`: tell the buyer exactly what gate to close before
   they invoice. This is the opposite of a stalling tactic — it is
   the buyer's path to a `PROCEED`.

## Doctrine Anchors

- This endpoint is part of the eleventh non-negotiable
  ("verifiable, not merely trusted").
- The public projection cannot be tricked into leaking operating
  detail — by design and by test.
