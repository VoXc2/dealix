---
name: dealix-security-audit
description: Run the Dealix agent/security gates (agent security gate, agent team audit, supply-chain scans) read-only and report findings. Fails closed. Never rotates secrets or mutates anything.
---

# Dealix Security Audit

## Scope

- Read-only audits only. Never print secret values; report `PRESENT`, `MISSING` or `ROTATION_REQUIRED` instead.
- Fail closed: any gate failure is reported as `FAIL`, never hidden.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/agent_security_gate.py"
"$PY" "$REPO/scripts/audit_agent_team.py"

rg -n --hidden -g '!*.pyc' -g '!.git' 'MOYASAR_LIVE_MODE|auto_top_up|AUTO_TOPUP' "$REPO/scripts" "$REPO/dealix" 2>/dev/null | head -10 || true
rg -n --hidden -g '!*.pyc' -g '!.git' 'sk-[A-Za-z0-9]{20,}' "$REPO" 2>/dev/null | head -5 || true
```

Supply-chain timers (read-only):

```bash
systemctl list-timers 'dealix-*' --all --no-pager | head -20
```

## Output contract

- `DEALIX_AGENT_TEAM_AUDIT=PASS|FAIL` and the agent security gate verdict verbatim.
- Findings list with file references and severity; no secret values ever.

## Forbidden

- Rotating secrets, editing `.env`, live mode flags, payments, auto top-up, or any production mutation.
