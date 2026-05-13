# Governance Capability — AI Capability Factory

**Layer:** L4 · AI Capability Factory
**Owner:** Founder / Compliance
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [governance_capability_AR.md](./governance_capability_AR.md)

## Context

The Governance capability lets a company use AI safely with explicit
approvals and full audit. It is the operational expression of
`docs/DEALIX_OPERATING_CONSTITUTION.md`, the incident discipline of
`docs/ops/INCIDENT_RUNBOOK.md`, and the regulator-facing posture in
`docs/ops/PDPL_BREACH_RUNBOOK.md`. Maturity is scored using
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## Business Purpose

Use AI safely — with approvals, logs, and incident response — so the
company can defend every action to a regulator, an auditor, or a board.

## Typical Problems

- No AI policy.
- No approval flow before external action.
- No audit trail.
- No risk register.

## Required Inputs

- Tools currently in use.
- Data flows and integrations.
- Owners per system and per workflow.

## AI Functions

- Apply rules-as-code to each AI run.
- Monitor for policy violations.
- Redact PII before storage or send.
- Escalate on rule trip.

## Governance Controls

- Rules-as-code in the runtime.
- Evals before promotion.
- Incident response playbook live.
- Quarterly governance review.

## KPIs

- Blocked actions — count and reason breakdown.
- Approvals logged — count of human approvals.
- Incident count — total and by severity.

## Services

- AI Readiness Review — paid assessment.
- AI Usage Policy — written policy + training.
- Governance Program — recurring governance retainer.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Tool / data inventory | Risk register | Delivery | Per assessment |
| Policy draft | Approved policy + training | Client | Per engagement |
| Runtime events | Blocked actions report | Runtime | Real-time |
| Incident | Postmortem + fix | Delivery | Per incident |

## Metrics

- Blocked actions and approvals logged (see KPIs).
- Mean time to detect / respond / resolve.
- Policy coverage — % of AI use covered by written policy.

## Related

- `docs/DEALIX_OPERATING_CONSTITUTION.md` — constitution this capability enforces.
- `docs/ops/INCIDENT_RUNBOOK.md` — incident discipline.
- `docs/ops/PDPL_BREACH_RUNBOOK.md` — regulator-facing breach response.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — maturity anchor (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
