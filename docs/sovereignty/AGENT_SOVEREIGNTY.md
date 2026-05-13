# Agent Sovereignty

No agent in Dealix is **free**. Every agent has identity, scope, and accountability.

## 1. Agent Card (canonical)

```json
{
  "agent_id": "AGT-REV-001",
  "name": "RevenueAgent",
  "owner": "Dealix Revenue",
  "purpose": "Score accounts and recommend next actions",
  "allowed_inputs": ["client_uploaded_accounts", "approved_public_data"],
  "forbidden_actions": ["send_messages", "scrape_web", "cold_whatsapp"],
  "autonomy_level": 2,
  "approval_required_for": ["external_actions", "personal_data_outputs"],
  "audit_required": true
}
```

## 2. Required attributes

- Identity
- Owner
- Purpose
- Allowed inputs
- Allowed tools
- Forbidden actions
- Autonomy level
- Approval requirements
- Audit requirements
- Decommission rule

## 3. Autonomy levels

| Level | Meaning |
| --- | --- |
| 0 | Read |
| 1 | Analyze |
| 2 | Draft / recommend |
| 3 | Queue for approval |
| 4 | Execute internal after approval |
| 5 | External action — restricted |
| 6 | Autonomous external action — **forbidden** |

## 4. MVP rule

Dealix MVP allows 0–3 only. Levels 4–5 require explicit contract terms and enterprise controls; level 6 is forbidden under any contract.

## 5. Why agent sovereignty is required

- Agents may collect or expose sensitive data during execution.
- Risks emerge from execution paths, not from designs.
- Permissions must be expressible per agent, per tool, per data flow.
- Without identity and accountability, an agent fleet becomes ungovernable.

## 6. Lifecycle

- **Register** before first invocation.
- **Revise** with cross-BU approval when autonomy ≥ 4.
- **Pause** at any time without ceremony.
- **Retire** with the card kept queryable for audit.

## 7. Operating discipline

- The Agent Registry is the canonical list.
- The AI Run Ledger records every action.
- The risk index per agent updates per action.
- Drift detection alerts when an agent’s action distribution shifts.

## 8. Anti-patterns

- Cards that exist but are not enforced.
- Cards with “catch-all” allowed inputs.
- Autonomy that drifts upward via informal exceptions.
- Containment that exists in code but does not page.

## 9. The principle

> Every agent is a registered identity inside Dealix. There are no anonymous actors.
