# Command Center

The Command Center is **not a pretty dashboard**. It is a decision surface used by the CEO, BU leads, and the Office of the Standard.

## 1. Twelve required views

1. CEO Decisions
2. Revenue Health
3. Delivery Risk
4. Governance Risk
5. Proof Strength
6. Capital Creation
7. Productization Queue
8. Retainer Opportunities
9. Business Unit Maturity
10. Venture Signals
11. Market Power
12. Enterprise Readiness

Each view shows a small number of decisions, not a wall of metrics.

## 2. Decision shape

Decisions emitted by the Command Center carry the same structured form across every view:

```json
{
  "decision": "PRODUCTIZE",
  "target": "proof_pack_generation",
  "reason": "Repeated 5 times, 3 hours per project, used across all services",
  "expected_impact": "Higher delivery margin and consistent proof quality",
  "priority": "high"
}
```

```json
{
  "decision": "OFFER_RETAINER",
  "target": "Client A",
  "reason": "Proof score 88, client health 76, recurring workflow detected",
  "recommended_offer": "Monthly RevOps OS"
}
```

## 3. Operating rules

- Decisions accumulate in the **Decision Log** with their inputs.
- Reversals are allowed and recorded; secret pivots are not.
- A decision without an accountable owner is rejected.
- A decision without a target is rejected.
- A decision without a reason is rejected.

## 4. Cadence

- **Daily** — delivery risk, governance risk.
- **Weekly** — revenue health, retainer opportunities.
- **Monthly** — capital creation, productization queue.
- **Quarterly** — BU maturity, venture signals, market power, enterprise readiness.

## 5. Why this is not just a BI dashboard

A BI dashboard answers “what happened.” The Command Center answers “what do we decide now.” The structural difference is that every view is paired with an action vocabulary and an owner.

## 6. Failure modes

- Becoming a BI tool. The Command Center must end every view with a decision option.
- Becoming a status meeting prop. Decisions belong in the log, not on a slide.
- Letting view design drift across BUs. The vocabulary stays uniform.
- Hiding red signals. Red signals are the entire point.
