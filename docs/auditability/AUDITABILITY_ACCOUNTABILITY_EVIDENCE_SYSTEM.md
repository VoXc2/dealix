# Dealix Auditability, Accountability & Evidence System

> The more Dealix can act, the more it must be able to **prove**, **attribute**, and **reconstruct**.

Layer 27 consolidated doctrine. Typed surfaces in `auto_client_acquisition/auditability_os/`.

## 1. Principle

> If Dealix cannot reconstruct it, Dealix should not automate it.

## 2. Evidence Chain (9 layers)

```
Source Evidence → Input Evidence → Policy Evidence → AI Run Evidence →
Human Review Evidence → Approval Evidence → Output Evidence →
Proof Evidence → Value Evidence
```

## 3. Auditability Card per Agent

Beyond the Agent Card: audit_scope, logs_required, tamper_evident_records, external_actions_allowed, responsibility_owner, reconstruction_required, retention_policy.

Rule: no Agent Card + Auditability Card → no production agent.

## 4. Accountability Matrix

| Action | AI | Human | System |
| --- | --- | --- | --- |
| Data classification | suggests | reviews sensitive cases | logs |
| Scoring | suggests | approves priority | logs |
| Outreach draft | writes draft | reviews + decides | DRAFT_ONLY |
| External action | does not execute in MVP | approves + executes | logs approval |
| Claim | suggests phrasing | verifies proof | links to Proof Pack |
| Governance | suggests decision | escalates critical | persists audit event |

## 5. Evidence Integrity

MVP: append-only, unique IDs, timestamps, actor_id, source_id, project_id, governance_decision_id, approval_id.

Enterprise: tamper-evident logs, hash chains, audit exports, role-based access, retention policies, signed approvals.

## 6. Lifecycle Coverage

Design → Configuration → Execution → Review → Approval → Delivery → Proof → Retention → Decommission. For agents and workflows alike.

## 7. Policy Checkability

Every governance decision exposes `matched_rules` + human-readable `explanation`.

## 8. Responsibility Attribution

Owners: System / Agent / Workflow / Data / Approval / Client Sponsor / Dealix Success.

Rule: no owner = no workflow; no approval owner = no external action; no governance owner = no enterprise rollout.

## 9. Audit-to-Proof Loop

Audit events feed Proof Pack evidence: blocked unsafe actions, removed unsupported claims, approvals completed, QA passes.

## 10. Audit-to-Risk Loop

Every audit anomaly becomes a risk signal that yields a rule, test, checklist, and dashboard metric.

## 11. Agent Audit Levels

- L1 Basic Logging — inputs, outputs, timestamps, agent ID, task.
- L2 Governance Logging — policy checks, matched rules, risk, decision.
- L3 Human Review Logging — reviewer, edits, approval, rejection reason.
- L4 Enterprise Audit — tamper-evident, exports, retention, RBAC.

MVP → L2. Retainers → L3. Enterprise → L4.

## 12. Saudi Audit Advantage

Bilingual audit reports with Arabic executive summary; PDPL-aware language; no external action by Dealix without recorded approval.

## 13. Audit Metrics + Thresholds

% AI runs logged, % agents with Auditability Card, % outputs with policy decision, % approvals linked, % proofs linked to audit events, % sources with passports, % incidents with rule/test update, average reconstruction time.

Thresholds: < 100% passport coverage → no scale; < 100% governance coverage → no client outputs; < 90% AI run logging → no enterprise; no auditability card → no production agent.

## 14. The closing sentence

> Dealix wins when AI is not just "working" but "provable" — every action traceable, every decision explainable, every responsibility owned, every value backed by an evidence chain from source to Proof.
