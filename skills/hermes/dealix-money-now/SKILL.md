---
name: dealix-money-now
description: Produce the canonical Dealix Money-Now portfolio command from real Founder OS evidence (relationships, events, approvals) and report the top 3 nearest-to-cash moves. Read-only: prepares internal next steps; external sends stay approvals.
---

# Dealix Money Now

## Scope

- Only evidence-backed records count. Research is not a relationship; a quote is not an invoice; an invoice is not a payment; a payment is not recognized revenue until verified.
- Founder income lane (`FOUNDER_INCOME` scope) is tracked separately and is never Dealix company revenue.
- This skill prepares internal next steps only (L0-L4). External send, payment and contract actions are L5 approvals.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/ops/run_v18_portfolio_command.py"
LATEST="$(ls -t "$REPO"/reports/founder/V18_PORTFOLIO_COMMAND_*.md | head -1)"
sed -n '1,60p' "$LATEST"
```

Canonical evidence inputs (read-only):

```bash
sed -n '1,10p' /opt/dealix/company-os/founder-os/tables/SCOPED_RELATIONSHIPS.tsv
sed -n '1,10p' /opt/dealix/company-os/founder-os/queues/ACTION_QUEUE.tsv
sed -n '1,10p' /opt/dealix/company-os/founder-os/queues/APPROVAL_QUEUE.tsv
```

## Output contract

- Top 3 moves with: entity, evidence type, observable state, next safe action, scope lane.
- Verified revenue stays `0` until a verified payment record exists. Never inflate.
- Every L5 item is listed as an approval candidate, never executed.

## Forbidden

- Sending anything externally, charging, merging, or mutating production or business state.
