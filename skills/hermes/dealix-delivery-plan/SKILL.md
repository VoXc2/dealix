---
name: dealix-delivery-plan
description: Build the internal delivery plan for an accepted pilot: workspace, milestones, acceptance criteria, evidence collection, and profitability checks. No customer-facing send.
---

# Dealix Delivery Plan

## Scope

- Delivery starts only after written acceptance criteria and an approved proposal exist.
- Plan covers: owner, milestones, evidence per milestone, customer validation gate, rollback.
- Profitability: delivery effort and cost are tracked against the quote.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/commercial/generate_client_delivery_control.py" --help 2>/dev/null || true
"$PY" "$REPO/scripts/create_customer_workspace.py" --help 2>/dev/null || true
```

## Output contract

- Milestones with acceptance criteria and evidence source per milestone.
- Status vocabulary: `PLANNED`, `IN_PROGRESS`, `BLOCKED`, `DELIVERED_PENDING_CUSTOMER_VALIDATION`.
- Customer validation is required before any value claim.

## Forbidden

- Marking delivery complete without customer validation, publishing proof, or charging.
