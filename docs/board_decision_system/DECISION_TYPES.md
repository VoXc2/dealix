# Decision Types

## 1. Scale Decision

**When:** sold repeatedly, proof strong, delivery repeatable, retainer path exists, governance risk controlled, margin healthy.

**JSON shape (example)**

```json
{
  "decision": "SCALE",
  "target": "Revenue Intelligence Sprint",
  "evidence": [
    "sold 3+ times",
    "average proof score >85",
    "retainer path exists",
    "delivery checklist stable"
  ],
  "actions": [
    "raise price",
    "publish one-pager",
    "build account_scoring module",
    "create B2B services playbook"
  ]
}
```

## 2. Build Decision

**When:** manual step repeated 3+, takes 2+ h/project, linked to paid offer, reduces risk or improves margin, client pull exists.

## 3. Hold Decision

**When:** signal weak, demand unclear, proof insufficient, governance not ready, high maintenance risk.

Include `next_condition` (measurable re-entry gate).

## 4. Kill Decision

**When:** low margin, scope creep, weak proof, no retainer path, high governance risk, no repeatability.

Always name a **replacement** offer or motion when killing a SKU.

## Composite decisions (CEO Command Center)

See [CEO_COMMAND_CENTER.md](./CEO_COMMAND_CENTER.md) for `OFFER_RETAINER`, `BUILD_MVP`, `RAISE_PRICE`, `REJECT_BAD_REVENUE`, `CREATE_PLAYBOOK`, etc.
