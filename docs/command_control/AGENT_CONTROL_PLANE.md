# Agent Control Plane

Every Dealix agent runs inside a control plane that registers, monitors, contains, and audits it.

## 1. Per-agent attributes

- `agent_id`
- Owner
- Purpose
- Allowed inputs
- Allowed tools
- Forbidden actions
- Autonomy level
- Approval requirements
- Audit requirements
- Decommission rule

## 2. Autonomy levels

| Level | Meaning |
| --- | --- |
| 0 | Read |
| 1 | Analyze |
| 2 | Draft / recommend |
| 3 | Queue for approval |
| 4 | Execute internal after approval |
| 5 | External action — restricted |
| 6 | Autonomous external action — **forbidden** |

## 3. MVP rule

- **Allowed in standard engagements:** 0–3.
- **Restricted, requires explicit contract clause:** 4.
- **Enterprise-only:** 5.
- **Forbidden:** 6.

## 4. Why a plane, not a list

A list of agents is metadata. A plane is **alive**: it can pause an agent, revoke a tool, downgrade autonomy, and log every action.

## 5. Plane components

- **Agent Registry** — the canonical list of cards.
- **AI Run Ledger** — every run, every action, every decision.
- **Policy Engine** — pre-action evaluation.
- **Approval Engine** — human-in-the-loop orchestration.
- **Audit Trail** — append-only, exportable.
- **Runtime Monitor** — risk index, drift detection, conformance.

## 6. Real-time controls

- Agency Risk Index per agent.
- Telemetry of every action and tool call.
- Continuous Authorization Monitoring — revoke mid-run.
- Conformance — observed vs. card.
- Drift detection — alert on action-distribution shifts.
- Containment — pause an agent or downgrade autonomy via a circuit breaker.

## 7. Operating rules

- An agent without a registered card cannot be invoked by `llm_gateway`.
- A card change for an agent at autonomy ≥ 4 requires an approver outside that agent’s BU.
- Retired agents are kept queryable forever for audit.
- Multiple agents cannot share an `agent_id`.

## 8. Failure modes

- Cards exist but not enforced at call time.
- Containment exists but is not paged.
- Autonomy drifts upward via informal exceptions.
- The control plane is bypassed for “quick demos.”
