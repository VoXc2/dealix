# Service Runtime Table

> The single mapping from "what Dealix sells" to "what runs under the hood".
> Each service ties to its workflows, agents, governance checks, proof
> events, and dashboard tile. If a row is incomplete, the service does not
> ship.

## How to read this table

- **Service** — what the customer buys (per `docs/COMPANY_SERVICE_LADDER.md`).
- **Workflows** — the 8-step runtime workflows that deliver it (see
  `WORKFLOW_RUNTIME_DESIGN.md` + `WORKFLOW_REGISTRY.md`).
- **Agents** — named entries in `AI_AGENT_INVENTORY.md`.
- **Governance checks** — the runtime checks from
  `docs/governance/RUNTIME_GOVERNANCE.md` that gate this service.
- **Proof events** — events written to the event store
  (`auto_client_acquisition/revenue_memory/event_store.py`).
- **Dashboard** — the Control Tower tile that surfaces this service.

## Lead Intelligence Sprint

| Field | Value |
|-------|-------|
| Workflows | Lead Import Preview, Account Scoring, Outreach Drafting |
| Agents | DataQualityAgent, RevenueAgent, OutreachAgent, ComplianceGuardAgent, ReportingAgent |
| Governance checks | Data source, PII, Forbidden-claim, Approval (per draft), Audit log, Proof event |
| Proof events | `lead.import_preview_ready`, `lead.scoring_complete`, `outreach.drafts_approved`, `delivery.proof_pack_created` |
| Dashboard | Lead Intel tile (runs / cost / QA / blocks) in AI Control Tower |

## Company Brain Sprint

| Field | Value |
|-------|-------|
| Workflows | Knowledge Answering, Source Onboarding (Phase 2), Freshness Sweep |
| Agents | KnowledgeAgent, ComplianceGuardAgent, ReportingAgent |
| Governance checks | Permission Mirroring, Data source (no-source-no-answer), PII, Audit log |
| Proof events | `brain.answer_delivered`, `brain.source_added`, `brain.freshness_flagged` |
| Dashboard | Company Brain tile (citation rate / freshness / blocks) |

## AI Quick Win Diagnostic

| Field | Value |
|-------|-------|
| Workflows | Diagnostic Findings, Quick Win Selection, Pilot Conversion |
| Agents | StrategyAgent, ReportingAgent, ComplianceGuardAgent |
| Governance checks | Forbidden-claim (no guaranteed ROI), Audit log, Proof event |
| Proof events | `qw.diagnostic_delivered`, `qw.pilot_proposed` |
| Dashboard | Quick Win tile (diagnostics delivered / conversion to pilot) |

## AI Support Desk Sprint (Designed / Beta)

| Field | Value |
|-------|-------|
| Workflows | Support Triage, Knowledge-Grounded Reply Draft, Escalation Decision |
| Agents | SupportAgent, KnowledgeAgent, ComplianceGuardAgent, ReportingAgent |
| Governance checks | Permission Mirroring, PII, Arabic-tone review, Approval (replies sent), Audit log |
| Proof events | `support.triaged`, `support.draft_approved`, `support.escalated` |
| Dashboard | Support Desk tile (triage volume / Arabic tone / approval latency) |

## AI Governance Program

| Field | Value |
|-------|-------|
| Workflows | Source Registration, Agent Promotion Gate, Monthly Audit, Incident Response |
| Agents | ComplianceGuardAgent (runtime), no autonomous Governance Agent |
| Governance checks | All eight runtime checks active; Approval Matrix; Audit log; Proof event |
| Proof events | `governance.source_registered`, `governance.agent_promoted`, `governance.audit_completed`, `governance.incident_logged` |
| Dashboard | Governance tile (blocks / overdue approvals / open incidents) |

## Hard rules

- Every paid service has a row here. No row, no sale.
- The Workflows column must list at least one entry from
  `WORKFLOW_REGISTRY.md` with status `MVP` or `Production`.
- The Proof events column drives `PRODUCT_TELEMETRY.md` Value metrics —
  if a service writes no proof events, customer-facing value is unverified.
- Adding a new service requires updating: `AI_AGENT_INVENTORY.md`,
  `WORKFLOW_REGISTRY.md`, `PROMPT_REGISTRY.md`, `EVALUATION_REGISTRY.md`,
  and this table, in one PR.

## Cross-links

- `/home/user/dealix/docs/product/WORKFLOW_RUNTIME_DESIGN.md`
- `/home/user/dealix/docs/product/WORKFLOW_REGISTRY.md`
- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/product/AGENT_LIFECYCLE_MANAGEMENT.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/COMPANY_SERVICE_LADDER.md`
- `/home/user/dealix/dealix/reporting/proof_pack.py`
- `/home/user/dealix/auto_client_acquisition/revenue_memory/event_store.py`
