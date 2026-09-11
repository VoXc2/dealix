---
name: dealix-agent-queues
description: Show the continuous work queues for the five permanent Dealix agents (pm, sales, delivery, engineer, content) from canonical Founder OS queues. Read-only; no fake busywork, no external actions.
---

# Dealix Agent Queues

## Permanent team

- `dealix-pm` - priority, MoneyNow, approvals, president brief
- `dealix-sales` - market, diagnostics, qualification, discovery, proposals
- `dealix-delivery` - delivery plans, acceptance, value, proof
- `dealix-engineer` - repo, website, infrastructure, Hermes, models, reliability
- `dealix-content` - Arabic/English sector content, SEO, education, proof-safe distribution

Hermes bots, profiles and sessions are temporary execution capability, not company agents.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/founder_agent_queue_status.py"

sed -n '1,12p' /opt/dealix/company-os/founder-os/queues/ACTION_QUEUE.tsv
sed -n '1,10p' /opt/dealix/company-os/founder-os/queues/APPROVAL_QUEUE.tsv
ls "$REPO/.claude/agents" | head -20
```

## Output contract

- Report the queue state and the next real task per agent. No synthetic tasks.
- `DEEP_WIP_MAX=3`; do not exceed it.
- Anything external remains an approval item.

## Forbidden

- Inventing work, duplicating schedulers, or performing external actions from this skill.
