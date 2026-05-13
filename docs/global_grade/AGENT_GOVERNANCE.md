# Agent Governance (Enterprise Edition)

The endgame layer defines the **Agent Card** doctrine (`docs/endgame/AGENT_CONTROL_DOCTRINE.md`). This document specifies the **enterprise constraints** under which Dealix is willing to operate agents.

## 1. Agent Card (canonical schema)

```json
{
  "agent_id": "AGT-REVENUE-001",
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

## 2. Autonomy levels

| Level | Meaning |
| --- | --- |
| 0 | Read |
| 1 | Analyze |
| 2 | Draft / recommend |
| 3 | Queue for approval |
| 4 | Execute internal after approval |
| 5 | External action restricted |
| 6 | Autonomous external action — **forbidden** |

## 3. MVP rule for the enterprise tier

- **Allowed in standard engagements:** levels 0–3.
- **Restricted (requires explicit contract clause):** level 4.
- **Enterprise-only:** level 5, with approval engine + audit + risk index in place.
- **Forbidden:** level 6.

This prevents agent sprawl and unsafe automation regardless of buyer demand.

## 4. Runtime requirements

- Every agent invocation passes through `llm_gateway` and references its `agent_id`.
- The runtime conformance engine compares observed behavior to the card.
- The risk index updates per action; threshold breaches trigger containment.
- Drift detection alerts when the action distribution shifts.

## 5. Lifecycle

- **Registration** — required before first invocation.
- **Revision** — autonomy increases require an approver outside the agent's BU.
- **Pause** — any operator with appropriate role can pause an agent.
- **Retirement** — preserved for audit.

## 6. Failure modes

- Cards exist but are not enforced at call time.
- Cards list forbidden actions the gateway does not actually block.
- Autonomy drifts upward through informal exceptions.
- Containment is wired but not paged.
- Multiple agents share an `agent_id` — audit becomes ambiguous.

## 7. Why enterprises require this

- CISOs need to attribute every AI action to a named identity.
- Risk officers need the ability to halt an agent mid-run.
- Auditors need a record that the policy was actually applied to the action.
- The board needs a control plane it can describe in one slide.
