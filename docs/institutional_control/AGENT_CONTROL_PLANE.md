# Agent Control Plane (Institutional Edition)

Every agent inside Dealix is governed like an employee. The institutional edition extends the endgame Agent Card with `allowed_tools` and explicit decommission rules.

## 1. Canonical Agent Card

```json
{
  "agent_id": "AGT-REV-001",
  "name": "RevenueAgent",
  "owner": "Dealix Revenue",
  "purpose": "Score accounts and recommend next actions",
  "allowed_inputs": ["client_uploaded_accounts", "approved_public_data"],
  "allowed_tools": ["score_accounts", "generate_draft", "create_summary"],
  "forbidden_actions": ["send_messages", "scrape_web", "cold_whatsapp", "linkedin_automation"],
  "autonomy_level": 2,
  "approval_required_for": ["external_actions", "personal_data_outputs"],
  "audit_required": true
}
```

## 2. Autonomy levels

| Level | Meaning |
| --- | --- |
| 0 | Read |
| 1 | Analyze |
| 2 | Draft / recommend |
| 3 | Queue for approval |
| 4 | Execute internal after approval |
| 5 | External action restricted |
| 6 | Autonomous external action — forbidden |

## 3. MVP rule

Dealix MVP allows only levels 0–3. Levels 4–5 require explicit contract clauses and enterprise controls. Level 6 is forbidden under any contract.

## 4. Why institutional control matters

Recent industry data indicates that a majority of organizations cannot reliably distinguish AI agent activity from human activity, and most report that agents accumulate more privileges than required. The Agent Control Plane is Dealix's structural answer to this risk.

## 5. Required real-time controls

- Agency Risk Index per agent.
- Telemetry of every action and tool call.
- Continuous Authorization Monitoring — revoke an agent mid-run.
- Conformance — observed behavior vs. the card.
- Drift detection — alert on action-distribution shifts.
- Containment — circuit breakers that pause or downgrade.

## 6. Lifecycle

- **Register** before first invocation.
- **Revise** with cross-BU approval when autonomy ≥ 4.
- **Pause** at any time without ceremony.
- **Retire** with the card kept queryable for audit.

## 7. Failure modes

- Cards that exist but are not enforced at call time.
- Containment in code that does not page.
- Autonomy that drifts upward through informal exceptions.
- Multiple agents sharing an `agent_id`.

## 8. The principle

> Every agent is a registered identity inside Dealix. There are no anonymous actors.
