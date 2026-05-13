# Incident Response — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Governance Lead / Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [INCIDENT_RESPONSE_AR.md](./INCIDENT_RESPONSE_AR.md)

## Context
AI systems fail. The difference between a damaged client relationship
and a hardened one is how the failure is handled. This file is the
incident-response definition for AI- and data-related incidents inside
Dealix. It sits next to the operational runbooks in
`docs/ops/INCIDENT_RUNBOOK.md` and
`docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`, and connects to the
PDPL breach pathway in `docs/ops/PDPL_BREACH_RUNBOOK.md`.

## Incident Types
Each incident is classified into one of these types:

- **PII exposure** — personal data shown to or sent to an
  unauthorised party.
- **Wrong AI output delivered** — material factual error in a
  client-facing AI output.
- **Unsupported claim** — claim not grounded in the permitted source
  (forbidden behaviour).
- **Unauthorised access** — an agent or user accessed data outside
  their ACL.
- **Client data mishandling** — sample retained beyond policy, copied
  outside the workspace, or sent in plain text.
- **Automation misfire** — workflow took a Level-4/5 action without
  required approval or against scope.

## Response Workflow
The standard response is a fixed eight-step sequence:

1. **Stop the affected workflow.** Pause the agent, the workflow, or
   the integration immediately.
2. **Preserve evidence.** Snapshot ledger rows, governance events,
   approvals, and prompt versions.
3. **Assess impact.** Identify who was affected, what data, what
   actions; classify severity (Low/Medium/High).
4. **Notify the owner.** Inform the client owner and the Dealix
   on-call within agreed SLAs.
5. **Correct the output or data.** Issue a corrected output, retract
   the message, or restore the data.
6. **Document root cause.** Five Whys or equivalent; written record
   stored against `project_id`.
7. **Update controls.** Add eval cases, prompt guards, ACL rules, or
   workflow gates to prevent recurrence.
8. **Update the playbook.** Push the change into the service playbook
   and into `docs/governance/RUNTIME_GOVERNANCE.md` where applicable.

## Severity and SLAs
- **High.** PII exposure, external mis-send to a real party, regulatory
  surface. Notify in ≤ 1 hour. Resolve in ≤ 24 hours.
- **Medium.** Wrong output delivered, unsupported claim, internal
  unauthorised access. Notify in ≤ 4 hours. Resolve in ≤ 72 hours.
- **Low.** Sample retention issue caught quickly, near-miss with no
  external impact. Notify in ≤ 1 business day. Resolve in ≤ 7 days.

## PDPL Pathway
- Any incident classified as a personal-data breach also follows
  `docs/ops/PDPL_BREACH_RUNBOOK.md`.
- Regulatory notifications and DPO involvement are non-negotiable in
  the PDPL pathway, regardless of severity.
- Cross-border transfers in incident scope are reviewed against
  `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## Communication Templates
- Internal alert template (Slack/Email).
- Client notification template, in Arabic and English.
- Customer-facing apology template, in Arabic and English, used only
  when an external party was affected.

## Anti-patterns
- **Hiding incidents.** Even Low-severity events must be logged.
- **Fixing without root cause.** Patches without root-cause analysis
  invite recurrence.
- **One-person handling.** Every incident requires two named people in
  the loop: an owner and a reviewer.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Runtime governance escalations, support tickets, monitoring alerts | Incident records, client notifications, control updates | Governance Lead, Delivery Lead | Per incident |
| Post-incident review | Updated playbooks, evals, gates | Founder | Per incident |
| Monthly review | Trends, repeat offenders, systemic gaps | Founder | Monthly |

## Metrics
- **Mean Time to Notify** — minutes from detection to client owner
  notification (target: meet SLA by severity).
- **Mean Time to Resolve** — hours from detection to resolution
  (target: meet SLA by severity).
- **Recurrence Rate** — share of incident types recurring within 90
  days (target ≤ 10%).
- **Logged Coverage** — share of detected incidents with a written
  record (target = 100%).

## Related
- `docs/ops/INCIDENT_RUNBOOK.md` — operational runbook for incidents.
- `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` — combined
  observability and incident runbook.
- `docs/ops/PDPL_BREACH_RUNBOOK.md` — regulatory breach pathway.
- `docs/governance/RUNTIME_GOVERNANCE.md` — sibling file feeding
  incident triggers.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
