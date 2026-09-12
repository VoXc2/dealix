---
name: dealix-company-queue
description: Build and read the canonical Company Work Queue from Founder OS queues and the latest V18 portfolio command, with fingerprint change detection so unchanged state costs nothing. Read-only sources; approvals stay pending.
---

# Dealix Company Work Queue

## Scope

- One queue over canonical evidence: ACTION_QUEUE, APPROVAL_QUEUE, V18 top moves.
- Priority = economic probability x value x urgency x fit / founder minutes / cost / risk / dependencies.
- Nothing counts as revenue or pipeline unless the canonical source already says so.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/ops/company_work_queue.py" --write --force
"$PY" "$REPO/scripts/ops/company_work_queue.py"          # NO_MATERIAL_CHANGE when inputs unchanged
sed -n '1,24p' /opt/dealix/company-os/founder-os/queues/COMPANY_WORK_QUEUE.md
```

## Output contract

- Items: id, area, owner, source, status, autonomy, priority, evidence, next_action.
- L5 rows stay `PENDING_FOUNDER`; never auto-execute them.
- `NO_MATERIAL_CHANGE` is a valid, cheap result — do not force recomputation.

## Forbidden

- Mutating canonical business state, inventing queue items, or treating synthetic activity as pipeline.
