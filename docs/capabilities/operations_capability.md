# Capability Blueprint — Operations Capability

> One of the 7 capabilities Dealix builds inside customers (per
> `docs/company/CAPABILITY_OPERATING_MODEL.md`). Mirrors the structure of
> `docs/capabilities/revenue_capability.md`. Concerns recurring workflow
> automation, executive reporting cadence, and SOP-driven operations.

## Business purpose
Help the customer automate recurring manual work, reduce errors, and
shrink cycle times — with humans in the loop on every action. Operations
that used to be Excel-and-WhatsApp orchestrated become workflows with
triggers, approvals, audit logs, and a runbook anyone can follow.

> **Hard rule**: automate a good process, never automate chaos — fix the
> process first. If the workflow doesn't exist on paper, we don't put it
> in an AI pipeline. Discovery and SOP-clarification happen before
> automation (`docs/services/ai_quick_win_sprint/intake.md`).

## Typical problems
- Weekly reports rebuilt by hand every Sunday night.
- Lead routing handled in a WhatsApp group — sometimes someone follows up,
  sometimes not.
- Support triage done in head; new requests sit until a senior sees them.
- Proposals re-written from scratch each time.
- Inbox / chat backlogs summarized verbally in standups instead of in
  writing.
- "Process" is in one person's head — bus factor of 1.
- No measurable cycle-time baseline, so improvement is unprovable.

## Required inputs from customer
- One painful, recurring process selected on Day 1 (per
  `docs/services/ai_quick_win_sprint/offer.md` curated list).
- Current process map — even a 5-line description is enough to start.
- Named human approver(s) per workflow step.
- ROI baseline data: how long does it take today, how often, who pays.
- Source systems for triggers (email, CRM, sheet, form, webhook).
- Sign-off authority for going live in the customer's environment.

## AI functions that build this capability
- Trigger detection (form submit, inbox message, sheet update, schedule).
- AI step orchestrated by **WorkflowAgent** with schema-validated I/O.
- Draft generation for outputs (report, proposal section, ticket summary,
  routing decision).
- Approval queue rendered as a human task; approver clicks to dispatch.
- Audit log append on every step (per
  `docs/governance/AUDIT_LOG_POLICY.md`).
- Runbook auto-generated from the workflow definition so the customer's
  team can operate it without Dealix.

## Governance controls (binding)
- AI proposes, human approves for any side-effect (per
  `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`).
- External-action workflows (send email, write to a third-party API)
  require Level-5 approval; autonomous external action is BLOCKED.
- Every workflow run logged with actor, decision, latency, cost.
- ComplianceGuardAgent gate runs before any side-effect (forbidden claims,
  PII, lawful basis).
- "Don't automate chaos" — if intake reveals no documented process,
  Dealix produces an SOP first, then automates.

## KPIs (measured before/after)
- Hours saved per week (the headline Time Value metric).
- Cycle time per workflow run (baseline vs. post-launch median).
- Error rate (missed steps, missed deadlines, rework).
- Workflow run count per week + approval rate.
- Audit completeness — 100% of runs logged.
- Customer-team adoption: how many runs happen without Dealix touching
  the workflow.

## Maturity ladder (per `docs/company/CAPABILITY_OPERATING_MODEL.md`)
- **Level 0** — process exists only verbally; nobody owns it end-to-end.
- **Level 1** — manual, spreadsheet-driven, no consistency.
- **Level 2** — SOP documented, owner named, inputs known.
- **Level 3** — One workflow automated with approval + audit
  (AI Quick Win Sprint).
- **Level 4** — Multiple workflows + monthly cadence + reporting +
  governance pass (Workflow Automation Sprint + Monthly AI Ops).
- **Level 5** — Operations OS: cross-workflow dashboard, SLA tracking,
  optimization cadence, customer team self-serves.

## Dealix services that build / advance this capability
| Service | Lifts capability from → to | Indicative price |
|---------|----------------------------|------------------|
| AI Quick Win Sprint | L0–L1 → L3 | SAR 12,000 · 7 days |
| Workflow Automation Sprint (Phase 2) | L3 → L4 | SAR 15,000–50,000 · 2–4 wks |
| Executive Reporting Automation | L1 → L3 | SAR 12,000–40,000 setup + SAR 5,000–15,000 / mo |
| SOP Automation (Phase 2) | L0–L2 → L3 | scoped |
| Monthly AI Ops (retainer) | L3 → L4–L5 | SAR 15,000–60,000 / mo |

Activation rule: Monthly AI Ops is offered **only after** a Sellable
Sprint has been delivered (per `docs/company/SERVICE_REGISTRY.md`).

## Agents involved (per `docs/product/AI_AGENT_INVENTORY.md`)
- **WorkflowAgent** — moves tasks through the defined workflow; autonomy
  level 2; emits structured events for the audit log.
- **ReportingAgent** — generates the weekly Ops report from workflow
  telemetry.
- **ComplianceGuardAgent** — mandatory gate before any side-effect.
- **DeliveryManagerAgent** — runs the underlying stage machine for the
  Sprint itself (not the customer workflow).

## Proof types produced
- **Time Proof** — hours saved per week, cycle-time reduction.
- **Quality Proof** — error rate before/after; audit completeness 100%.
- **Risk Proof** — approval-flow integrity (every side-effect signed off);
  no autonomous external actions executed.
- **Knowledge Proof** — runbook handed to the customer; bus factor lifted
  from 1 to "anyone can run it".

## Saudi-specific notes
- Reports that touch ZATCA-relevant data (invoices, VAT) keep the
  customer as record owner; Dealix builds the pipeline, never becomes
  the controller (per `docs/governance/PDPL_DATA_RULES.md`).
- Bilingual runbooks and approval UIs (AR/EN) are the default — most
  Saudi ops teams operate in Arabic at the front line.
- Sector regulators (SAMA for BFSI, NCA for cyber) inherit the audit log;
  Dealix's append-only event store is built to be exportable.

## Cross-links
- `docs/services/ai_quick_win_sprint/`
- `docs/services/ai_quick_win_sprint/offer.md`
- `docs/services/ai_quick_win_sprint/scope.md`
- `docs/company/CAPABILITY_OPERATING_MODEL.md`
- `docs/company/AI_CAPABILITY_FACTORY.md`
- `docs/company/CAPABILITY_PACKAGES.md`
- `docs/company/VALUE_REALIZATION_SYSTEM.md`
- `docs/product/AI_AGENT_INVENTORY.md`
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md`
- `docs/governance/RUNTIME_GOVERNANCE.md`
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/governance/AUDIT_LOG_POLICY.md`
