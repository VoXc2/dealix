# Client Health Score

A single 0–100 snapshot per active client that drives the next action. Backed by
`schemas/client_health.schema.json` and `client_health.json`, checked in
`tests/test_renewal_and_payment_rules.py`.

---

## Inputs

onboarding complete · access complete · first workflow delivered · weekly report
sent · client engagement · open blockers (inverse) · value proof level (L0–L5) ·
renewal fit.

---

## Statuses → action

| Status | Meaning | Action |
|--------|---------|--------|
| `healthy` | On track, proof building | Continue; prep next proof |
| `watch` | Early friction | Monitor; unblock access |
| `at_risk` | Slipping | Founder review |
| `blocked` | Stuck on a dependency | Escalate |
| `renewal_ready` | Value proven (≥ L3) | Draft renewal |
| `expansion_ready` | Value proven (≥ L3) + new need | Draft expansion |
| `churn_risk` | Disengaging | Recovery plan |

---

## Renewal/expansion gate

`renewal_ready` / `expansion_ready` are only valid when **value proof ≥ L3**
(staging/production signal or customer data). A `watch` client below L3 is never put
into a renewal posture. This is enforced in
`tests/test_renewal_and_payment_rules.py`.

---

## First 30 days

Week 1 intake + workflow map · Week 2 first workflow + drafts · Week 3 reporting +
proof · Week 4 optimization + renewal path.

---

*Version 1.0 | 2026-06-03*
