# Dealix Agent Identity, Access & Kill-Switch Control

> Every AI agent in Dealix is treated as a **non-human worker** — with identity, permissions, owner, boundaries, logs, periodic review, and a kill switch.

Layer 30 consolidated doctrine. Typed surfaces in `auto_client_acquisition/agent_identity_access_os/`.

## 1. Doctrine

```
No identity, no agent.
No owner, no agent.
No kill switch, no production.
```

## 2. Agent Identity Model

Required fields: `agent_id`, `name`, `owner`, `purpose`, `business_unit`, `status`, `risk_tier`, `environment`, `created_at`, `last_reviewed_at`.

Forbidden: agents without owner / purpose; shared between clients; permissions exceeding purpose; production without auditability card.

## 3. Access Classes — A0..A7

- A0 No access
- A1 Read approved metadata
- A2 Read source-passported data
- A3 Analyze / classify
- A4 Generate drafts
- A5 Write internal records
- A6 Queue external action for approval
- A7 Execute external action

**MVP allows A1–A4 only.** A5 needs internal approval; A6 needs Approval Engine; A7 forbidden.

## 4. Tool Permission Classes — T1..T7

- T1 Read-only
- T2 Analysis
- T3 Draft generation
- T4 Internal write (approval required)
- T5 External communication (blocked in MVP)
- T6 Sensitive data export (blocked)
- T7 Scraping / bulk collection (forbidden)

MVP allows T1/T2/T3; T4 restricted; T5/T6/T7 blocked.

## 5. Kill Switch

Triggers: owner removed, policy violation, unexpected tool request, attempted external action, PII exposure risk, repeated low QA score, client boundary violation, prompt injection suspected, unused 90 days.

Actions: disable agent, revoke tools, freeze active runs, notify owner, create incident, preserve logs, require review before reactivation.

## 6. Session Control

Each agent run = session with `session_id`, `agent_id`, `client_id`, `project_id`, `task`, `allowed_tools`, `expires_at`. No long-lived unrestricted sessions; no cross-client reuse; no session without project scope.

## 7. Chain Control

`chain_id` + `root_agent` + `delegated_agents` + `allowed_depth` + `current_depth` + `chain_policy` + `trace_required`.

MVP: no autonomous agent-to-agent delegation; explicit logged bounded only; max depth = 1.

## 8. Message-Action Trace

Each agent step emits a Trace Event with `step`, `agent_id`, `message`, `proposed_action`, `tool_called`, `policy_decision`, `output_id`. Risky steps must carry a Trace Contract with the rule and verdict.

## 9. Permission Review cadence

Low-risk monthly, medium bi-weekly, high weekly. Questions: owner still present? purpose still accurate? excess permissions? incidents? QA? new tool requests? autonomy reduce? kill?

## 10. Risk Tiers — 4

- Tier 1 Low Risk — read-only, no PII, internal summaries.
- Tier 2 Medium Risk — PII may exist, client-facing drafts, human review.
- Tier 3 High Risk — external recommendations, sensitive data, approval required.
- Tier 4 Restricted — external execution, bulk outreach, data export.

MVP allows Tier 1–2.

## 11. Security Testing (per agent)

prompt injection, tool misuse, unauthorized data access, role drift, unsupported claims, external action attempts, PII leakage, cross-client leakage.

## 12. Saudi Agent Identity rules

Blocked: autonomous WhatsApp, cold WhatsApp automation, LinkedIn automation, bulk enrichment, unapproved outreach, guaranteed sales claims.

Safe behavior: classify, rank, suggest, draft, surface risks, hand off — never send, scrape, or guarantee.

## 13. The closing sentence

> Dealix becomes safe in the agentic era when every agent has identity, owner, scoped permissions, traced sessions, periodic review, and an instant kill switch — converting agentic AI from a liability into a governed operating capability.
