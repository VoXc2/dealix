# Workflow Schema Contract

## Canonical Workflow Definition

```yaml
workflow_id: sales_lead_qualification_v1
version: 1.0.0
domain: sales
trigger:
  type: lead_created
  source: [website, whatsapp]
conditions:
  - condition_id: lead_has_contact
    expression: lead.email != null or lead.phone != null
actions:
  - action_id: qualify_lead
    type: agent.run
    agent_id: sales_agent_v1
  - action_id: risk_check
    type: governance.risk_score
approvals:
  - rule_id: high_risk_human_approval
    when: risk.level == "high"
retries:
  max_retries: 3
  backoff_seconds: [30, 120, 300]
compensation:
  - on: crm_update_failure
    action: revert_local_status
metrics:
  - lead_score
  - cycle_time_seconds
audit_logs:
  enabled: true
  include_inputs: false
```

## Required Fields

- `workflow_id`
- `version`
- `trigger`
- `conditions`
- `actions`
- `approvals`
- `retries`
- `compensation`
- `metrics`
- `audit_logs`

## Validation Gates

| Gate ID | Rule | Test ID |
|---|---|---|
| G-WFS-001 | required fields present | T-WFS-001 |
| G-WFS-002 | action ids unique | T-WFS-002 |
| G-WFS-003 | approval rules reference valid risk states | T-WFS-003 |
| G-WFS-004 | compensation exists for external side effects | T-WFS-004 |
| G-WFS-005 | metrics include business and reliability signals | T-WFS-005 |

## Versioning Policy

- Semantic versions (`MAJOR.MINOR.PATCH`).
- Major version bump when behavior or policy semantics change.
- Every version must include migration/rollback notes.
