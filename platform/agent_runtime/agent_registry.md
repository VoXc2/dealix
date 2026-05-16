# Agent Registry Schema and Control Policy

## Purpose

Define the canonical registration format for every Dealix agent.

## Canonical Agent Record

```yaml
agent_id: sales_agent_v1
name: Sales Qualification Agent
owner_team: revenue_os
version: 1.0.0
status: draft # draft|staging|production|deprecated
role: sales_agent
tenant_scope: single_tenant
memory_scope:
  organizational_memory: read
  customer_memory: read_write
  policy_memory: read
allowed_tools:
  - knowledge.retrieve
  - workflow.score
  - draft.message
  - crm.update
forbidden_tools:
  - external.send_unapproved
  - cross_tenant.query
risk_profile:
  default_risk: medium
  high_risk_actions:
    - crm.update_stage_closed_won
approval_rules:
  high_risk_requires_human: true
eval_thresholds:
  behavior_min_score: 0.85
  policy_compliance_min_score: 0.95
kpis:
  - lead_qualification_accuracy
  - time_to_draft
rollback:
  strategy: version_pin
  previous_version: sales_agent_v0.9.2
```

## Registry Gates

| Gate ID | Condition | Test ID |
|---|---|---|
| G-AGR-001 | required fields present | T-AGR-001 |
| G-AGR-002 | forbidden tool list enforced | T-AGR-002 |
| G-AGR-003 | risk profile mapped to approval policy | T-AGR-003 |
| G-AGR-004 | eval thresholds configured | T-AGR-004 |
| G-AGR-005 | rollback metadata available | T-AGR-005 |

## Promotion Rules

- `draft -> staging`: schema valid + unit/runtime checks pass.
- `staging -> production`: eval thresholds pass + approval policy checks pass.
- `production -> deprecated`: replacement version registered and rollback path validated.
