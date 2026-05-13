# Agent Risk Board

Per-agent row that the board can read in one minute.

## 1. Columns

```
agent_id
owner
purpose
autonomy_level
allowed_inputs
allowed_tools
forbidden_actions
last_audit
risk_level
incident_count
decommission_status
```

## 2. Rules

- Autonomy 0–2 → allowed in MVP.
- Autonomy 3 → allowed with approval queue.
- Autonomy 4 → limited internal post-audit.
- Autonomy 5 → enterprise-only.
- Autonomy 6 → forbidden.

## 3. Risk Bands

`mvp_allowed` / `contract_required` / `enterprise_only` / `containment_required` / `retired`. Typed in `board_ready_os.agent_risk_board.agent_risk_band()`.

## 4. The principle

> The board reads agent risk like it reads cash: one screen, one decision per agent.
