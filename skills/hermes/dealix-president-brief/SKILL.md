---
name: dealix-president-brief
description: Produce the short daily president brief from canonical evidence: health, money-now, approvals, blockers, and exactly one next autonomous action. Deterministic inputs, no invented KPIs.
---

# Dealix President Brief

## Scope

- Short by design: status, verified economic truth, top 3 money-now, L5 approvals, blockers, one next action.
- Never manufacture traction: verified revenue stays 0 until a verified payment exists.
- Founder income lanes are labeled separately from Dealix company revenue.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/run_dealix_daily_ops.py" --skip-api 2>&1 | tail -10
"$PY" "$REPO/scripts/dealix_founder_command_brief.py" --help 2>/dev/null || true
sed -n '1,10p' /opt/dealix/company-os/founder-os/queues/ACTION_QUEUE.tsv
```

## Output contract

- Sections: HEALTH, ECONOMIC TRUTH, MONEY NOW 1-3, APPROVALS NEEDED, BLOCKERS, NEXT AUTONOMOUS ACTION.
- Every number has a source path; `UNKNOWN` stays unknown.
- L5 items are listed, never executed.

## Forbidden

- Long-form essays, invented metrics, or external actions.
