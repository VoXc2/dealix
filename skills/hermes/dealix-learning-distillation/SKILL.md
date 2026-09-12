---
name: dealix-learning-distillation
description: Turn recurring executions, failures, and wins into durable learning: updated procedures, tests, and candidate skills. Learning never weakens governance to gain throughput.
---

# Dealix Learning Distillation

## Scope

- Inputs: receipts, failed checks, incidents, delivered work, customer-validated outcomes.
- Outputs: durable procedure updates, new tests, skill improvements, stop-doing list.
- Maturity path: manual -> verified procedure -> skill -> tests -> bounded automation.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/founder_weekly_ceo_retro.py" --help 2>/dev/null || true
"$PY" "$REPO/scripts/dealix_weekly_ceo_packet.py" --help 2>/dev/null || true
ls -t /opt/dealix/company-os/founder-os/current/HERMES_LEARNING_DISTILLATION.md 2>/dev/null | head -1
```

## Output contract

- Lessons with evidence refs, affected procedure/skill, and the exact change proposed.
- Regression candidates become tests before automation.
- Explicitly record what was NOT proven.

## Forbidden

- Weakening approval gates, hiding failures, or rewriting history without evidence.
