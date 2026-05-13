# CEO Command Center

## Principle

الـ Command Center لا يعرض «أرقامًا فقط». يعرض **قرارات**: ما الذي يجب اتخاذه هذا الأسبوع، ولِمَ، وبأي دليل.

## Surfaces (product)

- **Top 5 decisions** — ranked, each with `decision`, `target`, `reason`, `priority`
- Revenue quality (margin mix, bad revenue flags)
- Proof strength (ladder, consent posture)
- Retainer opportunities (adoption × proof × workflow depth)
- Client risks (governance, delivery, sponsor)
- Productization queue (scorecard output)
- Governance risks (gates, policy blocks)
- Bad revenue to reject (unsafe channels / ungoverned automation)
- Business unit maturity (repeatability, playbook coverage)
- Venture signals (margin + repeat + governance + expansion)

## Example Top Decisions (JSON)

```json
[
  {
    "priority": 1,
    "decision": "OFFER_RETAINER",
    "target": "Client A",
    "reason": "Proof Score 87, Adoption Score 78, monthly workflow exists"
  },
  {
    "priority": 2,
    "decision": "BUILD_MVP",
    "target": "Approval Center",
    "reason": "Approval friction repeated across 4 clients"
  },
  {
    "priority": 3,
    "decision": "RAISE_PRICE",
    "target": "Revenue Intelligence Sprint",
    "reason": "High proof score and repeatable delivery"
  },
  {
    "priority": 4,
    "decision": "REJECT_BAD_REVENUE",
    "target": "Cold WhatsApp automation request",
    "reason": "Unsafe channel risk and prohibited automation"
  },
  {
    "priority": 5,
    "decision": "CREATE_PLAYBOOK",
    "target": "B2B Services Revenue Readiness",
    "reason": "Repeated sector pattern"
  }
]
```

## API

`POST /api/v1/board-decision-os/ceo-top-decisions` — deterministic composition from a compact signal payload (see router schema).
