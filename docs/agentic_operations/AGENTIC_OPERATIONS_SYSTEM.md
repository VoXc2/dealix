# Dealix Autonomous Governance & Agentic Operations

> Dealix uses agents — but never gives them random permissions or lets them act as black boxes. Every agent is identified, scoped, audited, and stoppable.

Layer 29 consolidated doctrine. Typed surfaces in `auto_client_acquisition/agentic_operations_os/`.

## 1. Doctrine

> No autonomous capability without autonomous governance.

## 2. Operating Levels (0–7)

- L0 No Agent
- L1 Assistant
- L2 Drafting
- L3 Recommendation
- L4 Approval Queue
- L5 Internal Execution
- L6 External Action
- L7 Autonomous External — **forbidden**

MVP allows L1–L4. L5 requires strong internal controls; L6 enterprise-only.

## 3. Agent Identity Layer

Each agent has Identity Card (id, name, business unit, owner, purpose, autonomy level, status, created_at, last_reviewed_at). No identity = no agent.

## 4. Agent Permission Layer

Permission Card: allowed_inputs, allowed_tools, forbidden_tools, requires_approval_for. Rule: **least privilege by default**; permission elevation must be audited.

## 5. Tool Boundary — Six classes

- Class A Read-only
- Class B Analysis
- Class C Draft generation
- Class D Internal write (approval required)
- Class E External action (blocked in MVP)
- Class F High-risk (forbidden)

MVP allows A/B/C; D with approval; E/F blocked.

## 6. Governance runtime per agent action

Inspects: agent identity, autonomy level, tool permission, source passport, PII status, allowed use, channel policy, claim risk, approval requirement. Emits a `GovernanceDecision` with matched rules + allowed next step.

## 7. Auditability Card

audit_scope, action_recoverability, lifecycle_coverage, policy_checkability, responsibility_attribution, evidence_integrity, external_actions_allowed. See `auditability_os.auditability_card.AuditabilityCard`.

## 8. Lifecycle

Proposed → Reviewed → Approved → Registered → Tested → Deployed → Monitored → Reviewed Monthly → Restricted/Expanded → Decommissioned.

## 9. Agent Risk Score (7 dimensions, total 100)

| Dimension | Weight |
| --- | ---: |
| Data sensitivity | 20 |
| Tool risk | 20 |
| Autonomy level | 20 |
| External action exposure | 15 |
| Human oversight | 10 |
| Audit coverage | 10 |
| Business criticality | 5 |

Bands: 0–30 low, 31–60 medium, 61–80 high, 81–100 restricted.

## 10. Agent-to-Proof Loop

Each agent contributes to the Proof Pack: counts scored, draft packs generated, unsafe actions blocked, citations provided, rules matched. Agents become part of evidence, not black boxes.

## 11. Handoff to Humans

Every agent output requires an explicit handoff: handoff_id, agent_id, output_id, handoff_to, reason, required_action, deadline. No ambiguous handoff.

## 12. Client transparency

Brief client-facing summary that names the agent, scope, and explicit "no external outreach executed by Dealix".

## 13. The three first agents

- **Revenue Intelligence Agent** — classification, scoring, draft pack.
- **Company Brain Agent** — citations, insufficient evidence, knowledge gaps.
- **Governance Agent** — source passport check, PII detection, policy match, audit event drafts.

## 14. Saudi rules

No autonomous WhatsApp. No cold WhatsApp automation. No LinkedIn automation. No external outreach without human approval. Arabic claim safety required. Relationship/consent status required.

## 15. The closing sentence

> Dealix wins in the agentic era not by building free agents but by building **governed** ones: every agent has identity, permissions, ledger, owner, boundaries, handoff, and proof — converting agentic AI from risk into a sellable operating capability.
