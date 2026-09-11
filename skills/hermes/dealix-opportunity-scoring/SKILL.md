---
name: dealix-opportunity-scoring
description: Rank evidence-backed opportunities with the canonical portfolio command and economic-cell score. Research, estimates and synthetic records must never be promoted to real pipeline.
---

# Dealix Opportunity Scoring

## Scope

- Only records with direct evidence count: real interaction, inbound signal, verified relationship.
- Score = probability of verified economic movement x expected value / founder minutes / cost / risk.
- Estimates stay `ESTIMATED`; unknown stays `UNKNOWN`.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/ops/run_v18_portfolio_command.py"
LATEST="$(ls -t "$REPO"/reports/founder/V18_PORTFOLIO_COMMAND_*.md | head -1)"
sed -n '1,50p' "$LATEST"
```

## Output contract

- Top moves with entity, evidence type, observable state, next safe action, scope lane.
- Promotion rules: `DRAFT != SENT`, `QUOTE != INVOICE`, `INVOICE != PAYMENT`, `PAYMENT != RECOGNIZED_REVENUE`.
- Synthetic activity never carries economic weight.

## Forbidden

- External send, spend, contract commitment, or inflating probabilities above evidence.
