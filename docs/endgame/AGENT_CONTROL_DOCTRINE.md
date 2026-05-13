# Agent Control Doctrine

Every agent running inside or on behalf of Dealix carries a formal **Agent Card**. No card → no execution. Cards are registered in the Agent Registry and referenced by the AI Run Ledger.

## 1. Agent Card schema

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
| 0 | Read only — no transforms |
| 1 | Analyze — internal computation only |
| 2 | Draft / recommend — produces artifacts, never ships them |
| 3 | Queue for approval — items routed to humans |
| 4 | Execute internal action after approval |
| 5 | External action — restricted, must be channel-policy gated |
| 6 | Autonomous external action — **forbidden** in current doctrine |

The default for new agents is level 2.

## 3. Required real-time controls

Inspired by current research on Agentic AI Governance, every agent must support:

- **Agency Risk Index** — composite score across actions taken, blast radius, data sensitivity.
- **Telemetry** — every action and tool call streamed to the AI Run Ledger.
- **Continuous Authorization Monitoring** — the runtime can revoke an agent mid-run.
- **Conformance Engine** — checks that observed behavior matches the card.
- **Drift Detection** — flags when the agent’s action distribution shifts.
- **Containment** — circuit breakers that pause an agent or downgrade its autonomy.

## 4. Agent Registry

```
agent_id (PK)
name
owner
business_unit
purpose
allowed_inputs[]
forbidden_actions[]
autonomy_level
approval_required_for[]
audit_required (bool)
created_at
updated_at
status: active | paused | retired
```

## 5. Operating rules

- An agent without a card cannot be invoked by `llm_gateway`.
- An agent cannot self-modify its card.
- Card changes require an approver outside the agent’s BU when autonomy level ≥ 4.
- Retired agents remain queryable for audit forever.

## 6. Failure modes

- Cards exist but are not enforced at call time.
- Cards reference forbidden actions that the gateway does not actually block.
- Autonomy levels drift upward through informal exceptions instead of explicit reviews.
- Containment exists in code but is never wired to an alert.

Each failure mode has a periodic check owned by Governance.
